# R9 scientific repair: before and after

| Scientific defect | Before R9 | After R9 | Residual limitation |
|---|---|---|---|
| Inflation clock | Quarterly state advanced at irregular meetings | Monthly price-change state; annual inflation is exactly 12 monthly log changes | Twelve-month forecast trails AR and persistence baselines |
| Replay | Six 2022 transitions; RMSE 1.856 vs 0.643 persistence | 108 expanding origins at 1/3/6/12 months; short-horizon relative RMSE 0.775 | Frozen pre-2020 sample only |
| Uncertainty | Simulation bands; 0% coverage in meeting replay | Prior-residual rolling calibration; max coverage error 10.7 points | 12-month bands under-cover |
| Transmission | Rate level/step responses risked shock language | Player-minus-baseline path deviations and documented monthly kernels | External calibration, not local causal identification |
| Policy rules | Extreme formulas rapidly hit the 10% bound | Inertial rules with distinct coefficients and movement limits | Tournament remains model- and loss-dependent |
| Positioning | Public release language despite weak replay | Explicit research preview and validation caveats | Not production, forecast, or policy-advice software |

## Predeclared R9 gate

- Mean 1/3/6-month relative RMSE <= 1.00: **PASS (0.775)**.
- Worst-horizon relative RMSE <= 1.15: **PASS (1.041)**.
- Maximum interval coverage error <= 0.15: **PASS (0.107)**.
- Transmission claim separates path deviations from rate levels: **PASS WITH LIMITATIONS**.
- Policy rules avoid the 0%/10% hard bound in the dated 2022 path and preserve distinct behavior: **PASS**.

## Overall verdict

**PASS WITH LIMITATIONS.** R9 repairs the specific scientific defects well enough for a clearly labelled research preview. It does not establish structural causality, does not rescue the legacy 2022 meeting replay, and does not justify a v1.0 claim.
