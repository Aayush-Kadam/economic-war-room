# Project status

Updated: 2026-09-21

Branch: `release/r13-research-preview`

R13 stage: evidence-aligned research-preview release gate passed. The public interface and documentation now describe the shaded distribution only as simulation dispersion, explicitly distinguish observed history from model-generated counterfactuals, and make no calibrated-probability, causal-identification, or optimal-policy claim.

R11 and R12 uncertainty verdicts remain failed and are preserved as negative evidence. No interval method passed the predeclared calibration-and-sharpness gates. The mean model was not recalibrated or changed in R13.

Latest verification: 84 Python tests and 10 browser tests pass; deterministic Python/TypeScript parity passes; a fresh production build passes; a clean clone completes locked installation, official-data reconstruction, estimation, R10/R11/R12 evaluation, all tests, and the production build; the production launcher serves both the application and its client assets; and the complete seven-decision gameplay path reaches the final record with the required scientific labels.

Security and licensing: no committed credential or private absolute path was detected, and no generated raw observation or reconstructed calibration dataset is tracked.

Release decision: `v0.9.0-research-preview` is authorized at the final R13 audit commit. A GitHub release and private backup remain blocked because no remote, GitHub CLI, or authenticated GitHub connector is available. Publication status is `READY FOR PUBLICATION — REMOTE REQUIRED`.

Deployment recommendation: `DEPLOY` the evidence-aligned research preview after the private remote is configured and independently reviewed. This is not authorization for a v1 release.

V1 gate: `CLOSED`. Future work should accumulate genuinely new outcomes and seek independent economist/statistical review rather than tune against the already opened evidence windows.

Finalization phase: started 2026-09-22. Local verification reconfirmed 84 Python tests, 10 browser/TypeScript tests, deterministic parity, and a successful production build. Fast CI, public-release notes, a compact economist review packet, a selective reviewer shortlist, and an unsent outreach draft have been prepared without changing the scientific model or the V0.9 contract. GitHub publication, release publication, visibility, and R13 deployment remain pending external platform completion.
