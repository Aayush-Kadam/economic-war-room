"""Execute the predeclared R12 real-time uncertainty protocol."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from r10.run_r10_evaluation import H, fit_predict, load

OUT = ROOT / "r12" / "results"
LEVELS = (50, 80, 90)
TUNING_FOLDS = (("2016-01-01", "2017-12-01"), ("2018-01-01", "2019-12-01"), ("2020-01-01", "2021-12-01"))
CONFIRMATION = ("2022-01-01", "2022-12-01")
DIAGNOSTIC = ("2023-01-01", "2025-07-01")
VARIANTS = {
    "rolling_conformal": (24, 36, 60),
    "ew_conformal": (0.95, 0.98),
    "scaled_conformal": (36, 60),
}


def forecast_rows(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    first = data.index.get_loc("2010-01-01")
    for origin_index in range(first, len(data)):
        origin = data.index[origin_index]
        for horizon in H:
            if origin_index + horizon >= len(data):
                continue
            rows.append(
                {
                    "origin": origin,
                    "target": data.index[origin_index + horizon],
                    "horizon": horizon,
                    "actual": float(data.yoy.iloc[origin_index + horizon]),
                    "core": fit_predict(data, origin_index, horizon, "core"),
                }
            )
    return pd.DataFrame(rows).dropna().sort_values(["origin", "horizon"]).reset_index(drop=True)


def eligible_errors(frame: pd.DataFrame, origin: pd.Timestamp, horizon: int) -> pd.DataFrame:
    eligible = frame[(frame.horizon == horizon) & (frame.target <= origin) & (frame.origin < origin)].copy()
    eligible["error"] = eligible.actual - eligible.core
    return eligible.sort_values("target")


def conformal_quantile(values, level: int) -> float:
    x = np.sort(np.asarray(values, dtype=float))
    rank = min(len(x), math.ceil((len(x) + 1) * level / 100))
    return float(x[rank - 1])


def weighted_quantile(values, level: int, decay: float) -> float:
    x = np.asarray(values, dtype=float)
    weights = decay ** np.arange(len(x) - 1, -1, -1)
    order = np.argsort(x)
    x, weights = x[order], weights[order]
    return float(x[np.searchsorted(np.cumsum(weights) / weights.sum(), level / 100, side="left")])


def scaled_bound(errors: np.ndarray, level: int, window: int) -> float:
    errors = np.abs(np.asarray(errors, dtype=float))[-window:]
    scores = []
    for index in range(6, len(errors)):
        prior = errors[max(0, index - 12):index]
        long_prior = errors[max(0, index - 60):index]
        long_scale = max(float(np.median(long_prior)), 1e-9)
        scale = float(np.clip(np.median(prior), 0.5 * long_scale, 2.0 * long_scale))
        scores.append(errors[index] / scale)
    long_scale = max(float(np.median(errors[-60:])), 1e-9)
    current = float(np.clip(np.median(errors[-12:]), 0.5 * long_scale, 2.0 * long_scale))
    return conformal_quantile(scores, level) * current


def bounds(history: pd.DataFrame, method: str, parameter, level: int) -> tuple[float, float]:
    errors = history.error.to_numpy(dtype=float)
    if method == "fixed_signed":
        base = history[history.origin <= pd.Timestamp("2015-12-01")].error.to_numpy(dtype=float)
        alpha = 1 - level / 100
        return tuple(map(float, np.quantile(base, [alpha / 2, 1 - alpha / 2])))
    if method == "rolling_conformal":
        q = conformal_quantile(np.abs(errors[-int(parameter):]), level)
    elif method == "ew_conformal":
        q = weighted_quantile(np.abs(errors), level, float(parameter))
    elif method == "scaled_conformal":
        q = scaled_bound(errors, level, int(parameter))
    else:
        raise ValueError(method)
    return -q, q


def interval_score(actual: float, lo: float, hi: float, level: int) -> float:
    alpha = 1 - level / 100
    return (hi - lo) + (2 / alpha) * ((lo - actual) if actual < lo else (actual - hi) if actual > hi else 0)


def evaluate(frame: pd.DataFrame, method: str, parameter, start: str, end: str) -> pd.DataFrame:
    selected = frame[(frame.origin >= start) & (frame.origin <= end)]
    rows = []
    for item in selected.itertuples():
        history = eligible_errors(frame, item.origin, item.horizon)
        if len(history) < 24:
            continue
        row = {
            "origin": item.origin,
            "target": item.target,
            "horizon": item.horizon,
            "actual": item.actual,
            "prediction": item.core,
            "method": method,
            "parameter": parameter,
            "eligible_errors": len(history),
            "latest_eligible_target": history.target.max(),
        }
        scores = []
        for level in LEVELS:
            lower, upper = bounds(history, method, parameter, level)
            lo, hi = item.core + lower, item.core + upper
            score = interval_score(item.actual, lo, hi, level)
            alpha = 1 - level / 100
            row.update({f"lo{level}": lo, f"hi{level}": hi, f"cover{level}": lo <= item.actual <= hi, f"score{level}": score})
            scores.append(alpha / 2 * score)
        row["wis"] = (0.5 * abs(item.actual - item.core) + sum(scores)) / 3.5
        rows.append(row)
    return pd.DataFrame(rows)


def summarize(frame: pd.DataFrame) -> dict:
    result = {}
    for horizon, group in frame.groupby("horizon"):
        h = {"n": int(len(group)), "wis": float(group.wis.mean())}
        for level in LEVELS:
            widths = group[f"hi{level}"] - group[f"lo{level}"]
            coverage = float(group[f"cover{level}"].mean())
            h[str(level)] = {
                "coverage": coverage,
                "coverage_error": abs(coverage - level / 100),
                "mean_width": float(widths.mean()),
                "median_width": float(widths.median()),
                "interval_score": float(group[f"score{level}"].mean()),
            }
        result[str(int(horizon))] = h
    return result


def aggregate(frame: pd.DataFrame) -> dict:
    coverage_errors = [abs(float(frame[f"cover{level}"].mean()) - level / 100) for level in LEVELS]
    return {
        "n": int(len(frame)),
        "wis": float(frame.wis.mean()),
        "mean_coverage_error": float(np.mean(coverage_errors)),
        "mean_width": float(np.mean([(frame[f"hi{level}"] - frame[f"lo{level}"]).mean() for level in LEVELS])),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = load().dropna(subset=["price"])
    frame = forecast_rows(data)

    tuning_rows = []
    tuning = {}
    chosen_parameters = {}
    for family, parameters in VARIANTS.items():
        family_results = {}
        for parameter in parameters:
            pieces = [evaluate(frame, family, parameter, start, end) for start, end in TUNING_FOLDS]
            joined = pd.concat(pieces, ignore_index=True)
            tuning_rows.append(joined)
            family_results[str(parameter)] = aggregate(joined)
        best_score = min(value["wis"] for value in family_results.values())
        eligible = [p for p in parameters if family_results[str(p)]["wis"] <= 1.02 * best_score]
        chosen = max(eligible)
        chosen_parameters[family] = chosen
        tuning[family] = {"variants": family_results, "selected_parameter": chosen}

    baseline_confirmation = evaluate(frame, "fixed_signed", None, *CONFIRMATION)
    confirmations = {"fixed_signed": baseline_confirmation}
    for family, parameter in chosen_parameters.items():
        confirmations[family] = evaluate(frame, family, parameter, *CONFIRMATION)

    baseline_agg = aggregate(baseline_confirmation)
    family_gates = {}
    for family in VARIANTS:
        candidate = confirmations[family]
        candidate_agg = aggregate(candidate)
        summary, baseline_summary = summarize(candidate), summarize(baseline_confirmation)
        horizon_width_ratios = {
            h: float(np.mean([summary[h][str(level)]["mean_width"] / baseline_summary[h][str(level)]["mean_width"] for level in LEVELS]))
            for h in summary
        }
        lower_wis_horizons = sum(summary[h]["wis"] < baseline_summary[h]["wis"] for h in summary)
        checks = {
            "wis_no_more_than_5pct_worse": candidate_agg["wis"] <= 1.05 * baseline_agg["wis"],
            "coverage_error_improves_10pct": candidate_agg["mean_coverage_error"] <= 0.90 * baseline_agg["mean_coverage_error"],
            "minimum_90_coverage_each_horizon": all(summary[h]["90"]["coverage"] >= 0.70 for h in summary),
            "aggregate_width_ratio_at_most_1_75": candidate_agg["mean_width"] / baseline_agg["mean_width"] <= 1.75,
            "horizon_width_ratios_at_most_2": all(value <= 2.0 for value in horizon_width_ratios.values()),
            "lower_wis_at_least_two_horizons": lower_wis_horizons >= 2,
        }
        family_gates[family] = {
            "checks": checks,
            "historical_pass": all(checks.values()),
            "aggregate": candidate_agg,
            "width_ratio": candidate_agg["mean_width"] / baseline_agg["mean_width"],
            "horizon_width_ratios": horizon_width_ratios,
            "lower_wis_horizons": lower_wis_horizons,
        }

    passing = [family for family in VARIANTS if family_gates[family]["historical_pass"]]
    selected_family = None
    if passing:
        best = min(family_gates[family]["aggregate"]["wis"] for family in passing)
        complexity = ("rolling_conformal", "ew_conformal", "scaled_conformal")
        selected_family = next(family for family in complexity if family in passing and family_gates[family]["aggregate"]["wis"] <= 1.02 * best)

    selected_parameter = chosen_parameters.get(selected_family) if selected_family else None
    # Report every pre-tuned family on diagnostic and new-data tracks even when
    # none passes. These tracks never feed selection or alter the gate.
    methods_for_reporting = {"fixed_signed": None, **chosen_parameters}

    diagnostic_frames = {method: evaluate(frame, method, parameter, *DIAGNOSTIC) for method, parameter in methods_for_reporting.items()}
    last_observation = data.index.max()
    new_start = "2026-01-01"
    new_end = str(last_observation.date())
    new_frames = {method: evaluate(frame, method, parameter, new_start, new_end) for method, parameter in methods_for_reporting.items()}
    for method in new_frames:
        new_frames[method] = new_frames[method][new_frames[method].target.dt.year == 2026]

    new_checks = {}
    any_testable = False
    new_pass = selected_family is not None
    if selected_family:
        base_summary = summarize(new_frames["fixed_signed"])
        selected_summary = summarize(new_frames[selected_family])
        for horizon in H:
            key = str(horizon)
            n = selected_summary.get(key, {}).get("n", 0)
            if n >= 6:
                any_testable = True
                check = {
                    "n": n,
                    "wis_no_more_than_25pct_worse": selected_summary[key]["wis"] <= 1.25 * base_summary[key]["wis"],
                    "minimum_90_coverage": selected_summary[key]["90"]["coverage"] >= 0.60,
                }
                check["pass"] = check["wis_no_more_than_25pct_worse"] and check["minimum_90_coverage"]
                new_checks[key] = check
                new_pass = new_pass and check["pass"]
            else:
                new_checks[key] = {"n": n, "descriptive_only": True}
        new_pass = new_pass and any_testable

    release_pass = selected_family is not None and family_gates[selected_family]["historical_pass"] and new_pass
    result = {
        "protocol_commit_required": "ab817bf",
        "data_as_of": str(last_observation.date()),
        "opened_window_statement": "2023-2025 is previously observed stress diagnostic evidence and is not used for tuning or selection.",
        "tuning": tuning,
        "chosen_parameters": chosen_parameters,
        "confirmation": {method: {"aggregate": aggregate(value), "by_horizon": summarize(value)} for method, value in confirmations.items()},
        "family_gates": family_gates,
        "selected_family": selected_family,
        "selected_parameter": selected_parameter,
        "new_2026": {method: summarize(value) for method, value in new_frames.items()},
        "new_2026_checks": new_checks,
        "diagnostic_2023_2025": {method: summarize(value) for method, value in diagnostic_frames.items()},
        "release_gate_pass": release_pass,
    }
    all_predictions = [baseline_confirmation.assign(track="blocked_confirmation")]
    all_predictions.extend(value.assign(track="blocked_confirmation") for key, value in confirmations.items() if key != "fixed_signed")
    all_predictions.extend(value.assign(track="new_2026") for value in new_frames.values())
    all_predictions.extend(value.assign(track="opened_diagnostic") for value in diagnostic_frames.values())
    nonempty = [value for value in all_predictions if not value.empty]
    pd.concat(nonempty, ignore_index=True).to_csv(OUT / "r12_uncertainty_predictions.csv", index=False)
    (OUT / "r12_uncertainty_metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
