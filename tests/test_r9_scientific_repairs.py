import json
from pathlib import Path

import numpy as np

from engine.inflation_flow import fit_flow_model, forecast_yoy, monthly_log_change, yoy_from_monthly_log_changes
from engine.model import MacroState
from engine.policy_rules import dual_mandate, inflation_focused, smoothing, taylor
from engine.transmission import calibrated_kernels, convolve_policy_deviation, path_deviation

ROOT = Path(__file__).resolve().parents[1]


def test_monthly_flow_maps_exactly_to_log_yoy():
    prices = 100 * np.exp(np.arange(25) * 0.002)
    changes = monthly_log_change(prices)
    assert np.isclose(yoy_from_monthly_log_changes(changes), 100 * np.log(prices[-1] / prices[-13]))


def test_flow_forecast_preserves_twelve_month_measurement_window():
    changes = np.sin(np.arange(180) / 8) / 10
    model = fit_flow_model(changes)
    forecast, future = forecast_yoy(model, changes, 3)
    assert len(future) == 3
    assert np.isclose(forecast, sum([*changes, *future][-12:]))


def test_flow_fit_rejects_short_history():
    import pytest
    with pytest.raises(ValueError):
        fit_flow_model(np.ones(24))


def test_policy_path_is_separate_from_rate_level():
    assert path_deviation([4, 4, 4], [3, 4, 5]) == [1.0, 0.0, -1.0]


def test_zero_policy_deviation_has_zero_response():
    kernel = calibrated_kernels(24)["inflation"]
    assert convolve_policy_deviation([0] * 12, kernel) == [0] * 35


def test_contractionary_deviation_has_documented_signs():
    kernels = calibrated_kernels(48)
    assert min(convolve_policy_deviation([100], kernels["inflation"])) < 0
    assert min(convolve_policy_deviation([100], kernels["output"])) < 0
    assert max(convolve_policy_deviation([100], kernels["unemployment"])) > 0


def test_repaired_rules_are_inertial_distinct_and_not_rate_bound_saturated():
    state = MacroState(8, 6, 1, 0.3, 3.7, 0.125)
    rates = [r(state, .125, 0) for r in (taylor, inflation_focused, dual_mandate, smoothing)]
    assert len(set(round(x, 6) for x in rates)) == 4
    assert all(.125 < x < 10 for x in rates)
    assert smoothing(state, .125, 0) - .125 <= .5


def test_r9_predeclared_acceptance_passes():
    result = json.loads((ROOT / "r9/results/r9_metrics.json").read_text())
    assert result["summary"]["pass"] is True
    assert result["summary"]["mean_short_relative_rmse"] <= 1
    assert result["summary"]["max_coverage_error"] <= .15
