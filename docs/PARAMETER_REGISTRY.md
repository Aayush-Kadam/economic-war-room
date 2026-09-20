# Parameter registry

Frozen estimation sample: 1991Q2–2019Q4. Scenario evaluation begins in 2022. Values below distinguish estimates from model design.

| Symbol | Value | Equation | Method and sample | Uncertainty | Classification |
|---|---:|---|---|---|---|
| ρπ | 0.66 | inflation persistence | Retained Y/Y literature-informed calibration; direct Q/Q estimate was 0.271 (SE 0.095) but failed measurement-consistent replay | sensitivity 0.55–0.75 | literature-informed |
| βe | 0.060 | expected inflation | OLS, 1991Q2–2019Q4 | SE 0.158; weakly identified | estimated, weak |
| κ | 0.014 | Phillips slope | OLS, 1991Q2–2019Q4 | SE 0.041; includes zero | estimated, weak |
| ρy | 0.85 | output persistence | OLS estimate 0.947, conservatively bounded for stability | sensitivity 0.75–0.90 | estimated then regularised |
| φ | 0.16 | policy-to-output response | distributed-lag OLS was endogeneity-contaminated and near zero; retained prior | sensitivity 0.10–0.24 | literature-informed |
| γu | 0.288 | Okun response | OLS of Δu on Δoutput gap, 1990Q2–2019Q4 | equation RMSE 0.233 | estimated |
| ρc | 0.70 | credit persistence | model-state persistence; data estimate 0.443 | sensitivity required | design assumption |
| θc | 0.10 | rate-to-credit response | sign not identified in OLS; retained conservative prior | sensitivity required | literature-informed |
| f* | 2.0 | stress threshold | nonlinear guardrail | scenario stress grid | design assumption |
| π* | 2.0% | inflation target | FOMC longer-run goal | fixed | institutional |
| σπ | 0.32 | inflation innovation | interactive dispersion calibration | fat-tail comparison | design assumption |
| σy | 0.28 | output innovation | interactive dispersion calibration | fat-tail comparison | design assumption |

Machine-readable regression output, standard errors, residuals and expanding-window RMSE are stored in `calibration/estimated_parameters.json`. Weak results are retained as evidence rather than promoted into the engine.
