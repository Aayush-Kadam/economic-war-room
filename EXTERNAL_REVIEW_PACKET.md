# External scientific review packet

## Summary

Economic War Room is an educational historical decision laboratory. The production scenario uses dated information packets and a transparent semi-structural state model. Alternative outcomes are model-generated counterfactuals, not estimates of what certainly would have occurred.

## Identification and calibration

The estimation sample is frozen at 2019Q4. Equation-specific OLS estimates inflation persistence, expectations/slack correlations, output persistence, Okun dynamics and credit correlations. Monetary policy is endogenous; the weak distributed-rate regression is not treated as causal. The policy response profile remains literature-informed, consistent with Federal Reserve discussion of long and variable lags and peak activity/inflation effects around one to two years.

Directly promoting quarterly core-inflation persistence into the year-over-year scenario state failed replay validation. The release therefore retains a measurement-consistent persistence calibration and records the failed alternative. Full equations are in `MODEL_SPECIFICATION.md`; numerical provenance is in `docs/PARAMETER_REGISTRY.md` and `calibration/estimated_parameters.json`.

## Frozen sample

- Window: 1990Q1–2019Q4; equation sample begins after lag construction.
- Ten official FRED series; 120 quarterly rows.
- Dataset and every raw series are SHA-256 checksummed.
- Latest-revised history is used for estimation; meeting packets separately enforce real-time release availability.

## Vintage methodology

Seven 2022 manifests record cutoff, series, observation period, release date, vintage date, retrieval date, transformation and source. Actual policy is stored separately with `post_commit_only` visibility. Adversarial tests reject future releases, future vintages, malformed dates, exposed actions and timezone-boundary leakage. Expected inflation, output gap and stress are honestly marked as constructed states rather than observed releases.

## Validation and robustness

Historical replay verdict: **NEEDS REVISION**. Six next-meeting inflation observations yield RMSE 1.856 percentage points versus 0.643 for persistence; 80% coverage is 0%. The model captures direction in 80% of available transitions but mean-reverts too quickly. It is not validated as a superior forecasting model.

IRFs preserve the intended ordering: activity responds before inflation, unemployment rises after contraction, and magnitude increases with the policy shock. A 27-case parameter grid, Gaussian/Student-t comparison, parameter draws, 2,000-path frontier and policy tournament are reproducible. The limited model-uncertainty layer does not capture structural-form uncertainty.

## Scenario generalisation

Fed 2007–09 and RBI 2022–24 have modular, country-specific experimental extensions. The crisis module includes the effective lower bound, bank-stress feedback and liquidity/balance-sheet offsets. The India module includes oil/imported inflation, INR pass-through, Fed spillovers, intervention and liquidity. Neither has complete vintage packets or replay validation, so neither is production-ready.

## Questions for reviewers

1. Are the transmission mechanisms economically defensible?
2. Is the calibration methodology appropriate?
3. Are lag structures plausible?
4. Are counterfactual claims appropriately limited?
5. Is the uncertainty interpretation clear?
6. Is welfare scoring economically reasonable?
7. Does historical replay provide meaningful validation?
8. Are benchmark policy comparisons fair?
9. What would prevent use as an educational research tool?
10. Which model component is currently least defensible?

## Known limitations

Weak Phillips/expectations identification, no external monetary-policy instrument, six-point replay evaluation, incomplete vintage coverage for constructed states, simplified shock structure, no structural-form model averaging, and experimental-only secondary scenarios.
