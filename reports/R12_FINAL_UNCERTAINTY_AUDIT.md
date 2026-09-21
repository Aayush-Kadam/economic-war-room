# R12 final uncertainty audit

## Decision

`FAIL`. No uncertainty candidate satisfies the protocol frozen at commit `ab817bf`. No research-preview tag, release, publication, fan-chart change, or deployment is authorized.

## Methods and tuning

Blocked tuning folds were 2016–2017, 2018–2019, and 2020–2021. The predeclared within-family choices were rolling conformal window 60, exponentially weighted conformal decay 0.98, and scaled conformal window 60. Confirmation used 2022 origins only. The 2023–2025 results are previously observed diagnostics and do not affect selection.

## Blocked confirmation

| Method | WIS | Mean coverage error | Mean width | Width ratio | Horizons with lower WIS | Pass |
|---|---:|---:|---:|---:|---:|---|
| Fixed signed baseline | 0.397 | 0.157 | 1.225 | 1.000 | — | comparator |
| Rolling conformal 60 | 0.438 | 0.101 | 1.844 | 1.506 | 1 | no |
| EW conformal 0.98 | 0.435 | 0.094 | 1.864 | 1.523 | 1 | no |
| Scaled conformal 60 | 0.476 | 0.061 | 3.297 | 2.693 | 0 | no |

All candidates improved aggregate calibration error. Rolling and EW conformal missed the maximum 5% WIS deterioration, minimum 70% 90-coverage at every horizon, and two-horizon WIS-improvement requirements. Scaled conformal additionally failed width limits.

## Genuine 2026 confirmation

Official PCE data were available through 2026-07. Completed 2026-target samples were six at one month, four at three months, one at six months, and zero at twelve months. Only the one-month sample met the protocol's minimum size. These results cannot rescue a method that already failed historical confirmation.

At one month, WIS was 0.135 fixed, 0.125 rolling, 0.129 EW, and 0.134 scaled. All four methods had 90% coverage of 66.7% in the six-origin sample.

## Regression and publication audit

- Python: 78 passed, 0 failed.
- Browser: 10 passed, 0 failed.
- Production build: passed.
- Clean clone: passed complete install, official retrieval, reconstruction, estimation, R10/R11/R12 evaluation, tests, and build.
- Security: no committed secret or private absolute path detected.
- Licensing: no generated raw observation or reconstructed calibration CSV is tracked.
- Mean model: unchanged.
- GitHub backup: blocked by unavailable GitHub CLI/authentication and absence of a configured remote.
