# Engine reconciliation audit

## Pre-R10 discrepancy

| Variable | R9 validation | Pre-R10 interactive engine | Compatible? | R10 action |
|---|---|---|---|---|
| Headline inflation | Monthly PCE log-price flow; exact rolling 12-month YoY | Quarterly-style direct YoY AR state using CPI packets | No | Shared monthly flow core and exact rolling YoY identity |
| Expectations | Omitted from selected core | Bounded target/recent-inflation blend | No | Retained as displayed context, rejected from the selected inflation equation |
| Output | Not in inflation core | Quarterly output-gap recursion | Partial | Monthly state with 0.97 persistence plus policy-path kernel |
| Unemployment | Not in inflation core | Quarterly Okun recursion | Partial | Monthly state plus calibrated unemployment kernel |
| Policy rate | Forecasting model omitted policy | Absolute rate repeatedly entered real-stance equation | No | Player-minus-baseline monthly path; rate held between real meetings |
| Credit | Omitted | Ad hoc quarterly gap | No | Recorded state; no unsupported direct inflation coefficient |
| Financial stress | Omitted | Bounded quarterly recursion | Partial | Monthly persistence plus calibrated financial-conditions kernel |
| Credibility | Omitted | Designed bounded state | No | Recorded for welfare/context; not inserted into validated inflation core |

## Canonical clock and mapping

R10 adopts a monthly internal economy. Exact FOMC dates remain UI events. A decision applies in its calendar month and its target rate is held until a later listed meeting changes it. Multiple meetings in a quarter are therefore represented separately; no synthetic meetings are inserted.

The core evolves monthly log price changes. Reported `pce_yoy` is always the sum of the latest twelve flows. Quarterly-style presentation points are snapshots at months 3, 6, …, 24 and do not change the underlying clock.

All executable coefficients and transformations live in `engine/unified_spec.json`. Python consumes it through `engine/unified.py`; the browser consumes the same artifact through `lib/unified-engine.ts`. This JSON bridge is the canonical specification.

## Policy and stochastic mechanisms

The baseline and player paths are separate monthly arrays. Their basis-point difference is convolved with the R9 kernels. Absolute rate levels are not treated as new shocks. Overlapping deviations add linearly and decay with the documented kernels.

Monthly price-flow innovations have sigma 0.09 in the interactive Monte Carlo. The validation results use observed forecast errors and prior-origin residual calibration. Bounds apply only to unemployment (2.5–12), stress (0–2), and credibility (0.2–1).

## Initialization

Historical meeting packets initialize displayed YoY inflation, output, unemployment, stress, and policy levels. Until a complete vintage monthly price-history packet is distributed, the browser initializes twelve equal monthly flows summing to the observed YoY rate. This approximation is transparent and remains an accepted limitation.
