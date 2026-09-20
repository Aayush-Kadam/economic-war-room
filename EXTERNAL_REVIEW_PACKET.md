# External review packet

## Purpose

Economic War Room is a playable historical monetary-policy simulator and research preview. It compares a player's policy path with the dated historical baseline; it does not estimate an optimal policy or represent the Federal Reserve.

## Core model and data

The canonical economy is monthly. A frozen pre-2020 PCE price-index sample estimates a regularised 12-lag monthly price-flow model. Reported YoY inflation is the exact rolling sum of twelve monthly log changes. Official FRED series, vintage manifests, checksums, and retrieval code provide the audit trail.

## Estimation and model selection

R9 established the monthly core. R10 predeclared 2010–2015 model selection and required a richer model to improve mean 1/3/6/12-month RMSE by at least 1%. Core, energy-augmented, and energy-plus-expectations models scored 0.555, 0.569, and 0.660 respectively; the parsimonious core was retained.

## Unified architecture

`engine/unified_spec.json` is consumed by both Python and the browser. FOMC decisions remain dated events while the economy advances monthly. The target rate is held between meetings. Player-minus-baseline deviations, not absolute rate levels, drive policy transmission.

## Transmission

Literature-calibrated monthly kernels peak at 6 months for financial conditions, 18 for output, 22 for unemployment, and 24 for inflation. These are calibration targets, not locally identified causal estimates.

## Validation

On the separated 2016–2019 test, core RMSE is 0.131/0.263/0.423/0.726 at 1/3/6/12 months. It beats persistence through 6 months but trails persistence (0.658) and AR(4) (0.610) at 12 months.

On the untouched 2020–2025 stress period, core RMSE is 0.198/0.438/0.780/1.748 and beats all recorded baselines at every horizon. Fixed pre-2020 90% coverage falls to 73.1%/70.1%/52.2%/50.7%, showing severe structural-break under-coverage.

## Welfare and policy rules

The displayed loss is a normalized quadratic illustration over inflation, output, and unemployment. Rule comparisons use identical information and seeds but remain conditional on model and welfare weights.

## Limitations

Long-horizon pre-pandemic performance remains weak; post-pandemic intervals are miscalibrated; policy responses are externally calibrated; browser initialization approximates the unobserved monthly flow history; energy and expectations augmentation did not survive selection; bundled-data redistribution terms require confirmation.

## Questions for an external reviewer

1. Is the monthly flow/rolling-YoY representation adequate for this educational counterfactual use?
2. Is the path-deviation convolution defensible without a locally estimated surprise series?
3. Does adding policy kernels to an autoregressive price-flow core risk double counting persistence or transmission?
4. Are the selection and untouched stress windows sufficiently separated?
5. Should structural-break uncertainty be modelled by regimes, or only disclosed?
6. Are the welfare weights and benchmark rules fair enough for public comparison?
7. What claim language should be further weakened before publication?
