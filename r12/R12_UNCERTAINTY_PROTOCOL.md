# R12 uncertainty protocol

Status: predeclared before any R12 candidate result is computed.

Date frozen: 2026-09-21.

The mean forecast model, its predictors, coefficients, and point forecasts are frozen. R12 changes only the mapping from previously realized forecast errors to predictive intervals.

## Information rule

For an interval issued at origin `t` and horizon `h`, an error from origin `s` is eligible only when `s + h <= t`. Candidate parameters and scales may use only eligible errors. This rule is enforced in code and tested for every emitted interval.

The 2023–2025 window was opened during R11. It is diagnostic evidence only and is never used to tune or select an R12 candidate.

## Forecast horizons and interval levels

- horizons: 1, 3, 6, and 12 months;
- central intervals: 50%, 80%, and 90%;
- the frozen core forecast is the interval centre and is not refitted by R12.

## Candidate families

1. `fixed_signed`: baseline signed residual quantiles, frozen from eligible 2010–2015 residuals and not updated afterward.
2. `rolling_conformal`: symmetric absolute-error conformal quantiles using the most recent eligible 24, 36, or 60 horizon-specific errors.
3. `ew_conformal`: symmetric absolute-error conformal quantiles using all eligible horizon-specific errors with exponential decay 0.95 or 0.98 per observation.
4. `scaled_conformal`: rolling 36- or 60-error conformal scores standardized by a trailing 12-error median absolute scale. The current scale and every historical score scale use only errors eligible at the relevant origin and are clipped to 0.5–2.0 times the preceding 60-error median to prevent arbitrary widening.

Finite-sample conformal quantiles use rank `ceil((n + 1) * level)`, capped at `n`. No interpolation is used for absolute-score candidates.

## Track A: blocked historical evaluation

All dates are forecast-origin dates. Each fold is evaluated sequentially and admits an error only after its target has been realized.

Hyperparameter selection folds:

- Fold 1: 2016-01 through 2017-12;
- Fold 2: 2018-01 through 2019-12;
- Fold 3: 2020-01 through 2021-12.

Within each candidate family, choose the hyperparameter with the lowest observation-weighted aggregate weighted interval score across these three folds. If variants are within 2% of the best score, choose the longer rolling window, higher decay, or otherwise simpler/more stable variant.

Blocked confirmation:

- 2022-01 through 2022-12.

This period is not claimed to be pristine: it was available during R11. It is kept separate from tuning and evaluated only after the family variants and cross-family selection rule are fixed.

Cross-family selection chooses the simplest family with confirmation weighted interval score within 2% of the best confirmation score, provided it satisfies every historical acceptance condition below. Complexity order is fixed as `rolling_conformal`, `ew_conformal`, then `scaled_conformal`. The fixed method is the comparator, not a new candidate.

## Track B: genuinely new 2026 confirmation

Only forecasts with both origin and realized target in calendar 2026 are included. The data cutoff is the latest official PCE observation retrieved on the R12 run date. Sample size is reported separately by horizon. A horizon with fewer than six completed origins is descriptive only. No result is imputed for an unavailable horizon.

## Previously opened stress diagnostic

Origins from 2023-01 through 2025-07 are reported for the selected method and `fixed_signed`. They do not affect tuning, selection, or the release verdict.

## Metrics

For every method and horizon:

- empirical coverage and absolute coverage error at 50%, 80%, and 90%;
- mean and median interval width at each level;
- interval score at each level;
- weighted interval score (WIS), using the frozen core forecast as the centre:

`WIS = (0.5 * absolute_error + sum(alpha / 2 * interval_score_alpha)) / 3.5`

where alpha is 0.50, 0.20, or 0.10. CRPS is not used.

## R12 release acceptance gate

The selected candidate passes only if all conditions hold.

Historical blocked confirmation, relative to `fixed_signed` on 2022 origins:

1. aggregate WIS is no more than 5% worse;
2. mean absolute coverage error across all horizons and levels improves by at least 10%;
3. 90% coverage is at least 70% at every horizon;
4. aggregate mean-width ratio is at most 1.75 and no horizon-level width ratio exceeds 2.0;
5. at least two of four horizons have lower WIS than the baseline.

Genuinely new 2026 confirmation:

6. for every horizon with at least six completed origins, WIS is no more than 25% worse than baseline and 90% coverage is at least 60%.

Horizons with fewer than six new origins cannot pass or fail condition 6 and are reported descriptively. If no 2026 horizon has six completed origins, R12 cannot pass the release gate.

The implementation must also pass no-lookahead, deterministic-output, and finite-interval tests. Criteria will not be changed after results are opened.

## Sensitivity

Report every predeclared hyperparameter variant. Selection is not rerun on confirmation, diagnostic, or 2026 results.
