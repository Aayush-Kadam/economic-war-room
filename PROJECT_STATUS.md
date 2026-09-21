# Project status

Updated: 2026-09-21

Branch: `research/r12-final-uncertainty`

R12 stage: repository verified; private GitHub backup attempted but blocked because no GitHub CLI, authenticated GitHub connector, or configured remote is available. Scientific protocol design is next. The local repository remains authoritative and clean at the R11 base `7e94445d2056da6b589987eeb7901c4b633cef79`.

R11 verdict: `NEEDS REVISION`.

Recovered R11 work was found uncommitted on top of R10 commit `dc91dd198e64d7b758dc04fd2f3133bf2e64e58b`. It has been preserved and verified. The initial recovered suite had one Python failure (missing PCE retrieval metadata) and one browser failure (a stale reference to the replaced TypeScript engine); both recovery defects were repaired without changing the mean model.

Completed R11 work:

- all seven 2022 FOMC scenarios initialize the PCE engine with twelve actual vintage PCE monthly log-price changes;
- CPI remains supplementary and is never passed to the PCE engine;
- deterministic Python/browser parity covers six policy paths and shared external shocks at `1e-12` tolerance;
- official-data retrieval, vintage construction, calibration, and validation no longer depend on a developer-local `work/` path;
- raw downloaded and reconstructed calibration observations are excluded from the public package;
- the R10 mean model and its recorded 2020–2025 RMSE results remain unchanged;
- 74 Python tests and 10 browser tests pass; the production build passes.
- a fresh isolated clone completed locked dependency installation, official retrieval, vintage and calibration reconstruction, estimation, validation, both test suites, and the production build.

Reproduction caveat: live FRED retrieval in September 2026 contains new and revised observations beyond the archived R10 snapshot, so a live refresh is operationally reproducible but does not reproduce archived forecast metrics bit-for-bit. The canonical mean-model code and committed R10 evidence were not changed by R11.

Uncertainty result: exponentially weighted absolute residual intervals were selected on 2020–2022 and evaluated on untouched 2023–2025 origins. They materially repair 12-month 90% coverage (83.9% to 93.5%) with a 14.0% mean width increase, but mean interval score worsens by 1.7%. This fails the predeclared requirement for a 10% score improvement. Gate F therefore fails.

Next action: design and predeclare a new uncertainty experiment using a new validation/final split or independent future data. Do not tune against the opened 2023–2025 final window.

Release decisions: GitHub research-preview tag `NO`; deployment `DO NOT DEPLOY`; v1.0 gate `CLOSED`. No `v0.9.0-research-preview` or `v1.0.0` tag may be created while Gate F fails.
