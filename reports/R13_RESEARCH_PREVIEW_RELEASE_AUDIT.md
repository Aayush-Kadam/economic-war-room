# R13 evidence-aligned research-preview release audit

## 1. Executive decision

`PASS` for `v0.9.0-research-preview`. The candidate is suitable for an explicitly limited research preview. It is not a calibrated probabilistic forecasting system, causal estimate, optimal-policy engine, or v1 release.

## 2. Candidate identity

- Branch: `release/r13-research-preview`
- Release tag: `v0.9.0-research-preview`, to be attached only after this audit is committed
- Mean-model baseline: unchanged from the R10/R11/R12 evidence chain
- Audit date: 2026-09-21

## 3. Scientific-contract gate

The public contract is recorded in `docs/V0_9_SCIENTIFIC_CONTRACT.md`. Supported claims are limited to the documented historical simulator, frozen-vintage inputs, shared Python/TypeScript implementation, recorded mean-model validation, and seeded stochastic simulation dispersion.

## 4. Claims removed or narrowed

Probability-interval and confidence language was removed from the public interface. The distribution display is labelled `SIMULATION DISPERSION`, accompanied by the statement that it is not calibrated and must not be interpreted as a probability that the economy will lie inside the range. Results distinguish observed FOMC history from the model-generated counterfactual, and loss is presented as model sensitivity rather than proof of policy superiority.

## 5. Preserved negative evidence

R11 remains `NEEDS REVISION` and R12 remains `FAIL`. Their reports, results, protocol, and tests remain tracked. Neither failure was retried, reinterpreted as success, nor hidden.

## 6. Mean-model integrity

R13 changes public claims, documentation, release checks, and production serving. It does not recalibrate coefficients, alter the mean model, or select a new uncertainty method.

## 7. Public-interface audit

The home, briefing, gameplay, methodology, and final-results states were reviewed. Required uncertainty wording is visible; supplemental CPI is distinguished from PCE; historical facts are distinguished from simulations; and seven historical decisions remain playable.

## 8. Documentation audit

README, methodology, model specification, limitations, clean-clone instructions, uncertainty status, and the v0.9 scientific contract agree on the allowed and disallowed claims. The README includes both successful validation results and material failures.

## 9. Python verification

`84 passed, 0 failed`. This includes R13 release-claim checks, the preserved R11/R12 evidence checks, data-pipeline tests, and deterministic parity fixtures.

## 10. Browser verification

`10 passed, 0 failed`. A production-browser walkthrough also completed all seven decisions and reached the Governor's Record. The final screen displayed the required observed-history/model-counterfactual separation and model-loss qualification.

## 11. Production build and launch

The Vinext production build passed and generated standalone output. A release-owned production launcher serves client assets and proxies application requests. In the clean-clone smoke test, `/` returned HTTP 200 and its generated JavaScript asset returned HTTP 200.

## 12. Clean-clone reproduction

A fresh clone completed locked dependency installation, official-data retrieval, vintage reconstruction, frozen-sample construction, parameter estimation, R10 evaluation, R11 uncertainty repair, parity-fixture construction, R12 evaluation, 84 Python tests, 10 browser tests, and a production build. Regenerating the frozen sample changes manifest run metadata as expected; generated raw/calibration data remain untracked.

## 13. Security and licensing

The tracked tree contains no detected credential, private absolute developer path, generated raw observation file, or reconstructed calibration dataset. Repository licensing remains under `LICENSE`; official-source retrieval scripts and provenance records remain part of the reproducible workflow.

## 14. GitHub and publication status

`READY FOR PUBLICATION — REMOTE REQUIRED`. No Git remote is configured, GitHub CLI is unavailable, and no authenticated GitHub connector is present. Therefore no private backup, push, or GitHub Release was attempted.

Required operator commands:

```text
git remote add origin <PRIVATE_REPOSITORY_URL>
git push -u origin --all
git push origin --tags
```

## 15. Deployment and version decisions

- Research-preview tag: `APPROVED`
- GitHub release: `BLOCKED — REMOTE REQUIRED`
- Deployment recommendation: `DEPLOY` only as the evidence-aligned research preview, after private backup and independent review
- `v1.0.0`: `CLOSED`

## 16. Residual risks and next action

The simulator remains structurally simplified; external validity is limited; live official data can be revised; and uncertainty calibration has not passed. The next scientific step is genuinely new outcomes plus independent economist/statistical review. Do not tune against the already opened 2022–2025 evidence in an attempt to rehabilitate R11 or R12.
