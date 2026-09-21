# R11 release hardening

## Measurement and initialization

All seven Fed 2022 meetings now initialize the production engine from PCEPI vintages available at the meeting cutoff. Each packet contains twelve actual monthly log price changes derived from thirteen vintage price-index levels. Headline CPI remains visible only as supplementary information and never enters the PCE engine.

## Runtime parity

Six fixtures cover zero deviation, temporary 25bp tightening, repeated 50bp deviations, return to baseline, an allowed extreme path, and overlapping deviations. Python generates the reference trajectories; Node executes the same browser module and canonical JSON specification. The declared tolerance is 1e-12 for flows, YoY inflation, output, unemployment, stress, policy deviations, and policy contributions.

## Uncertainty decision

The mean model is unchanged. Candidate interval methods were selected on 2020–2022; 2023–2025 remained untouched. Exponentially weighted absolute residuals won selection.

On the final window, adaptive 90% coverage is 83.9%/90.3%/93.5%/93.5% at 1/3/6/12 months, versus fixed coverage of 80.6%/87.1%/90.3%/83.9%. Mean width rises 14.0%. Mean interval score worsens 1.7%, failing the predeclared requirement for a 10% improvement. Therefore Gate F fails even though severe long-horizon coverage collapse is removed.

## Verdict

`NEEDS REVISION`. Measurement, lag history, parity, retrieval, and packaging are repaired. The uncertainty method fails its predeclared proper-score gate, so no v0.9 tag is warranted.

## Verification

- Python: 74 passed, 0 failed.
- Browser: 10 passed, 0 failed.
- Production build: passed.
- Clean clone: passed install, official retrieval, vintage construction, calibration, estimation, validation, tests, and build.
- Security scan: no committed secrets or private absolute paths found.
- Packaging scan: no raw file under `data/generated/` or `calibration/frozen/` is tracked.

Live official data are revision-prone. The September 2026 clean-clone refresh extends and revises the archived R10 evaluation inputs, so refreshed metrics are not bitwise equal to the committed R10 snapshot. R11 leaves the canonical mean-model specification and archived R10 evidence unchanged.
