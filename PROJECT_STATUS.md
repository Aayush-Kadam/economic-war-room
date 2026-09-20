# Project status

Branch: `research/r9-scientific-repair`

Recovery base: `7259d42d26c703cad94a2e7594a36ac63de222ed` (`m8-public-release-candidate` remains unchanged)

Current milestone: R9 — final gate `PASS WITH LIMITATIONS`

Release position: research preview; no v1.0 tag and no deployment change

R9 repairs the inflation measurement clock, adds a 108-origin monthly rolling replay at four horizons, calibrates intervals only from prior residuals, separates unexpected policy-path deviations from rate levels, and replaces hard-bound-saturating policy rules with inertial alternatives.

Predeclared metrics: mean short-horizon relative RMSE 0.775; worst-horizon relative RMSE 1.041; maximum absolute coverage error 0.107. The 12-month forecast still trails persistence and the policy transmission kernels remain literature-calibrated rather than locally identified.

Existing milestones M0–M8 and the `m8-public-release-candidate` tag are preserved. R9 does not support an unqualified production, causal, forecasting, or policy-advice claim.
