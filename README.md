# Economic War Room

**Historical Monetary-Policy Simulator — Research Preview**

**Monetary Policy Under Fire** — a historical central-banking decision laboratory created by Aayush Kadam.

The functional scenario places the player at seven FOMC decisions in 2022. Information is cut off at the meeting date, the historical action is hidden until commitment, and a seeded monthly model produces a distribution of alternative outcomes. Actual history is always labelled as observed; player outcomes are model-generated counterfactuals. This is not an official Federal Reserve or RBI product, and no optimal historical policy is claimed.

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

## R10 reproducibility

Run `python r10/run_r10_evaluation.py` after retrieving the listed FRED series (`PCEPI`, `DCOILWTICO`, and `MICH`) into `work/`. Run `python -m pytest`, `pnpm test`, and `pnpm build` for the full verification stack. The currently linked deployment predates R10 and still uses the R9-era browser engine; it has not been replaced.

See [MODEL_SPECIFICATION.md](MODEL_SPECIFICATION.md), [METHODOLOGY.md](METHODOLOGY.md), [DATA_SOURCES.md](DATA_SOURCES.md), [LIMITATIONS.md](LIMITATIONS.md), and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
