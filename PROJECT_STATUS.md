# Project status

Updated: 2026-09-21

Branch: `research/r12-final-uncertainty`

R12 stage: final audit complete. Private GitHub backup remains blocked because no GitHub CLI, authenticated GitHub connector, or configured remote is available.

R12 protocol commit: `ab817bf`. Experiment commit: `aa0150c`.

R12 uncertainty verdict: `FAIL`. No candidate passed the predeclared blocked-confirmation gate. Rolling conformal, exponentially weighted conformal, and volatility-scaled conformal improved calibration error but all exceeded the allowed WIS deterioration, failed the per-horizon 90% coverage requirement, and improved WIS at fewer than two horizons. No method was selected and the R12 release gate is closed.

Latest verification: 78 Python tests and 10 browser tests pass, deterministic parity passes, production build passes, clean-clone official-data reconstruction passes, secret/private-path scan is clear, and no generated raw dataset is tracked.

Next action: accumulate genuinely new outcomes and seek external economist/statistical review. Do not tune further against the already opened 2022–2025 evidence. No `v0.9.0-research-preview` or `v1.0.0` tag is authorized.

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
