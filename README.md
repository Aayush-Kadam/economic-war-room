# Economic War Room

### Historical Monetary-Policy Simulator — Research Preview

Creator: **Aayush Kadam**

**Monetary Policy Under Fire** — a historical central-banking decision laboratory created by Aayush Kadam.

The playable Fed 2022 scenario uses vintage-aware PCE initialization and one unified monthly economic specification in Python and the browser. Information is cut off at each meeting date, the historical action is hidden until commitment, and a seeded model produces alternative outcomes. Those counterfactuals are not historical facts. Monetary transmission is literature-calibrated; research-grade structural causality is not claimed. This is experimental research software, not an official Federal Reserve or RBI product, and no optimal historical policy is claimed.

## Quick start

```powershell
pnpm install
pnpm dev
python -m pytest
pnpm test
pnpm build
```

The application stores the Governor's Record in browser-local storage. No account or external service is required. ALFRED retrieval requires a personal `FRED_API_KEY`; copy `.env.example` and do not commit the key.

Existing research-preview deployment: https://economic-war-room-aayush.aayushonfleek.chatgpt.site

## What is implemented

- playable Fed inflation-shock scenario from March through December 2022;
- seven locked decisions, communication stance and policy memo;
- 1,000 seeded paths per decision with median and 80% interval;
- delayed rate transmission, adaptive expectations, credibility, credit and nonlinear stress;
- explicit normalized quadratic loss and Governor's Record;
- machine-readable scenario and data registry;
- ALFRED vintage adapter and anti-lookahead filter;
- reproducibility, directional economics and numerical stability tests;
- responsive briefing-room, results and methodology interfaces.
- frozen 1990Q1–2019Q4 estimation dataset with checksums and ten-series provenance;
- equation-level estimates, parameter registry, historical replay and robustness reports;
- Student-t shocks, parameter uncertainty, seven policy benchmarks and a 2,000-path frontier;
- country-specific experimental Fed-crisis and RBI extensions.

## Scientific position

This is a calibrated counterfactual simulation—not a structural causal estimate, forecast service, or policy-advice system. Code, frozen inputs, retrieval utilities, and tests make the analysis reproducible. The monthly core passes the current short-horizon validation gates but remains weaker than simple baselines at 12 months in the pre-pandemic test. Post-pandemic fixed intervals under-cover materially. Policy transmission is literature-calibrated rather than locally identified. Quantitative paths remain illustrative.

## R11 reproducibility

```powershell
pnpm install --frozen-lockfile
python scripts/fetch_official_data.py
python scripts/build_vintages.py
python calibration/build_frozen_sample.py
python calibration/estimate_parameters.py
python r10/run_r10_evaluation.py
python r11/run_uncertainty_repair.py
python -m pytest -q
pnpm test
pnpm build
```

See [clean-clone reproduction](docs/CLEAN_CLONE_REPRODUCTION.md) and [data licensing](docs/DATA_LICENSING.md). The current live demo predates the R11 candidate and has not been replaced: https://economic-war-room-aayush.aayushonfleek.chatgpt.site

## Current validation

| Window | 1 month | 3 months | 6 months | 12 months |
|---|---:|---:|---:|---:|
| 2016–2019 core RMSE | 0.131 | 0.263 | 0.423 | 0.726 |
| 2020–2025 core RMSE | 0.198 | 0.438 | 0.780 | 1.748 |
| 2023–2025 adaptive 90% coverage | 83.9% | 90.3% | 93.5% | 93.5% |

Known limitations: the 12-month pre-pandemic forecast trails simple baselines; the selected adaptive intervals improve coverage but fail the predeclared interval-score gate; policy transmission is calibrated rather than locally identified; and the live deployment does not yet run this candidate.

![Economic War Room interface](public/og.png)

See [MODEL_SPECIFICATION.md](MODEL_SPECIFICATION.md), [METHODOLOGY.md](METHODOLOGY.md), [DATA_SOURCES.md](DATA_SOURCES.md), [LIMITATIONS.md](LIMITATIONS.md), and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
