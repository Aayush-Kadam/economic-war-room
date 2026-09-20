# Economic War Room

**Monetary Policy Under Fire** — a historical central-banking decision laboratory created by Aayush Kadam.

The released scenario places the player at seven FOMC decisions in 2022. Information is cut off at the meeting date, the historical action is hidden until commitment, and a seeded semi-structural model produces a distribution of alternative outcomes. Actual history is always labelled as observed; player outcomes are always labelled as model-generated counterfactuals.

## Quick start

```powershell
pnpm install
pnpm dev
python -m pytest
pnpm test
pnpm build
```

The application stores the Governor's Record in browser-local storage. No account or external service is required. ALFRED retrieval requires a personal `FRED_API_KEY`; copy `.env.example` and do not commit the key.

Private release: https://economic-war-room-aayush.aayushonfleek.chatgpt.site

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

This is a calibrated semi-structural counterfactual simulation—not a structural causal estimate and not a forecast service. Some coefficients are estimated on a frozen pre-pandemic sample; weakly identified policy and credibility mechanisms remain literature-informed or designed. The historical replay currently underperforms persistence, so quantitative paths remain illustrative.

See [MODEL_SPECIFICATION.md](MODEL_SPECIFICATION.md), [METHODOLOGY.md](METHODOLOGY.md), [DATA_SOURCES.md](DATA_SOURCES.md), [LIMITATIONS.md](LIMITATIONS.md), and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
