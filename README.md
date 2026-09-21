# Economic War Room

## Historical Monetary-Policy Simulator — Research Preview

**Created by Aayush Kadam**

Economic War Room is a vintage-aware historical monetary-policy simulation laboratory. The playable scenario places the user at seven 2022 FOMC meetings, restricts information to what was available at each decision date, records a policy choice, and reveals the historical decision afterward.

The engine evolves monthly PCE price changes, holds meeting rates until the next listed meeting, and compares the user's policy path with the dated historical baseline through documented literature-calibrated response kernels. Alternative outcomes are model-generated counterfactuals, not observations or causal estimates.

## Scientific status

This is experimental research software—not a calibrated probabilistic forecasting system, structurally identified causal model, optimal-policy calculator, or official Federal Reserve product.

- Short- and intermediate-horizon validation of the mean inflation model is encouraging.
- In the archived 2020–2025 stress evaluation, the core mean model beats the recorded persistence, AR(1), and AR(4) baselines at every reported horizon.
- In the 2016–2019 test, the core beats those baselines at one, three, and six months, but not at twelve months.
- Policy transmission is literature-calibrated rather than locally structurally identified.
- Calibrated predictive intervals are **not claimed**. R11 and R12 uncertainty experiments failed their frozen joint calibration, sharpness, and proper-score gates; the complete negative evidence remains in the repository.
- The interface's shaded spread is simulation dispersion from stipulated stochastic shocks. It is not a confidence interval or a probability that the economy will fall inside the band.

The precise V0.9 claims and nonclaims are frozen in `docs/V0_9_SCIENTIFIC_CONTRACT.md`.

## Playable scenario

- seven FOMC decisions from March through December 2022;
- historically reconstructed PCE initialization from twelve actual vintage monthly flows at every meeting;
- headline CPI shown only as a supplementary statistic;
- hidden historical action until the user's decision is locked;
- communication stance and policy memo;
- observed FOMC path separated from the model-generated counterfactual;
- deterministic seeded simulation and reproducible Governor's Record.

## Validation summary

RMSE; the best recorded simple baseline is shown in parentheses.

| Evaluation | 1 month | 3 months | 6 months | 12 months |
|---|---:|---:|---:|---:|
| 2016–2019 core | 0.131 (0.170) | 0.263 (0.346) | 0.423 (0.506) | 0.726 (0.610) |
| 2020–2025 archived stress core | 0.198 (0.274) | 0.438 (0.651) | 0.780 (1.119) | 1.748 (2.016) |

The twelve-month pre-pandemic result is weaker than every recorded simple baseline. The stress-period comparison is archived evidence, not a claim of universal forecasting superiority. Live official-data refreshes can revise or extend observations, so they need not reproduce archived metrics bit-for-bit.

Full evidence is in `reports/R10_MODEL_SELECTION.md`, `reports/R10_STRESS_TEST.md`, `reports/R11_RELEASE_HARDENING.md`, `reports/R12_FINAL_UNCERTAINTY_AUDIT.md`, and `reports/UNCERTAINTY_VALIDATION_STATUS.md`.

## What did not work

- The original six-transition 2022 replay mixed incompatible timing and measurement conventions and failed against persistence.
- CPI-to-PCE initialization and synthetic equal monthly flows were scientifically inconsistent; both were replaced with exact vintage PCE histories.
- Energy augmentation and energy-plus-expectations augmentation lost the predeclared model-selection comparison to the parsimonious core.
- The core's twelve-month pre-pandemic forecast trails simple baselines.
- R11 adaptive intervals improved coverage but worsened the proper score.
- R12 rolling, exponentially weighted, and volatility-scaled conformal candidates all failed the frozen joint release gate.

These results remain part of the public audit trail.

## Reproduce

Requirements: Python 3.11+, Node.js 22.13+, pnpm, and internet access to official FRED/ALFRED endpoints. No API key or developer-local data directory is required.

```powershell
pnpm install --frozen-lockfile
python scripts/fetch_official_data.py
python scripts/build_vintages.py
python calibration/build_frozen_sample.py
python calibration/estimate_parameters.py
python r10/run_r10_evaluation.py
python r11/run_uncertainty_repair.py
python scripts/build_parity_fixtures.py
python r12/run_r12_uncertainty.py
python -m pytest -q
pnpm test
pnpm build
pnpm start
```

Raw official observations and reconstructed calibration data are retrieved locally into ignored paths. The public package contains code, series metadata, provenance, transformations, derived initialization packets, and research outputs—not unresolved raw datasets.

See `docs/CLEAN_CLONE_REPRODUCTION.md`, `docs/DATA_LICENSING.md`, `METHODOLOGY.md`, `MODEL_SPECIFICATION.md`, and `LIMITATIONS.md`.

## License and citation

Software is released under the MIT License. Third-party data remain subject to their source terms. Citation metadata are provided in `CITATION.cff`.
