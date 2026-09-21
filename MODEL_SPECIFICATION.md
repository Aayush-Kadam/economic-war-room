# Model specification

## Canonical monthly state

The released engine is defined by `engine/unified_spec.json` and implemented in Python and the browser. Inflation is represented as twelve monthly PCE log-price changes; reported year-over-year inflation is their exact rolling sum. Activity, unemployment, and financial stress evolve on the same monthly clock.

## Inflation flow

`flow(t+1) = intercept + sum(beta_j * flow(t+1-j)) + policy_response(t)/12 + shock(t+1)`

The twelve autoregressive coefficients and intercept are shared across implementations. The policy response is divided across monthly flow state so the rolling-sum identity remains authoritative.

## Policy path response

For each month, the engine computes the basis-point difference between the player's policy rate and the historical baseline. Literature-calibrated response kernels convolve current and earlier differences into inflation, output, unemployment, and financial-condition contributions. Meeting rates remain in effect until a listed later meeting changes them; no meetings are invented.

## External shocks

Observed external inputs, stochastic innovations, and policy-induced effects are separate channels. Shared deterministic fixtures prove Python/browser equality for zero deviation, temporary and repeated tightening, return to baseline, an extreme allowed path, and overlapping deviations and shocks.

## Simulation dispersion

The browser uses a fixed seed to generate reproducible stochastic paths. The displayed central path and spread summarize these model-generated simulations only. They are not calibrated probabilities or confidence intervals. Formal uncertainty-validation failures are preserved in the R11 and R12 reports.

## Model loss

The interface reports a normalized quadratic model loss combining inflation, output, and unemployment gaps. It is a transparent decision aid and sensitivity measure, not an objectively correct social-welfare function or ranking of historical policymakers.
