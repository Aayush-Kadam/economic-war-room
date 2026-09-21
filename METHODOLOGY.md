# Methodology

## Information and measurement

The released Fed 2022 scenario uses meeting-date information cutoffs. Each meeting initializes the engine with twelve monthly log changes constructed from the PCEPI vintage available at that cutoff. Their rolling sum is the engine's year-over-year PCE inflation state. Headline CPI is displayed only as supplementary historical context.

## Mean inflation model

The canonical mean model is a regularized twelve-lag autoregression in monthly PCE log-price changes. Model selection was fixed to 2010–2015. The parsimonious core beat energy and energy-plus-expectations candidates on mean selection RMSE and was retained. The untouched archived tests cover 2016–2019 and the post-2019 stress period.

## Policy transmission

Counterfactual transmission uses the player's monthly policy path minus the dated historical baseline path. Overlapping monthly response kernels are literature-calibrated. Absolute rate levels are not repeatedly treated as new shocks, and the response is not presented as locally identified causal evidence.

## Simulation dispersion

The interactive display generates 1,000 deterministic seeded paths from the documented stochastic shock process. The centre line is the simulation median and the shaded area contains the central 80% of those generated paths.

That shading is not a calibrated predictive interval, confidence interval, or real-world probability statement. R11 and R12 tested fixed, rolling, exponentially weighted, conformal, and volatility-scaled interval procedures. Some improved empirical coverage, but none satisfied the frozen joint calibration, sharpness, width, and proper-score gates. V0.9 therefore makes no calibrated probabilistic forecasting claim.

## Interpretation

Historical releases and the actual FOMC path are observations. Player outcomes are model-generated counterfactuals conditional on the specified engine, baseline, policy path, and shocks. Simulation frequencies describe the model's own generated paths only; they are not estimates of real-world event probabilities.
