# Economist review packet

## 1. Project summary

Economic War Room is a research-preview historical monetary-policy simulator created by Aayush Kadam. Its released scenario places a player at seven 2022 FOMC meetings, restricts each briefing to information available by the meeting date, records a policy and communication choice, and compares the resulting model-generated path with the observed historical policy path. The project is intended as a serious educational and research tool, not an optimal-policy engine, causal estimate, calibrated forecast, or Federal Reserve product.

## 2. Model architecture

The canonical economy advances monthly. Python and TypeScript consume the shared specification in [`../engine/unified_spec.json`](../engine/unified_spec.json). FOMC decisions are dated events, while target rates are held between meetings. Player-minus-historical rate-path deviations drive the policy response rather than absolute rate levels being treated as repeated shocks.

## 3. Price and inflation state

The core state is the monthly log change in the PCE price index. Reported year-over-year inflation is the exact rolling sum of twelve monthly log changes. Every released 2022 meeting is initialized from twelve actual vintage PCE flows rather than CPI substitution or synthetic equal flows.

## 4. Vintage-data rules

Observation periods, public release dates, vintage dates, and meeting cutoffs are recorded separately. Normal play excludes information unavailable by the decision cutoff. Source metadata, checksums, retrieval scripts, and derived scenario fixtures provide the audit trail. See [`../DATA_SOURCES.md`](../DATA_SOURCES.md) and [`../docs/CLEAN_CLONE_REPRODUCTION.md`](../docs/CLEAN_CLONE_REPRODUCTION.md).

## 5. Policy transmission

Externally calibrated distributed-lag kernels peak at approximately 6 months for financial conditions, 18 for output, 22 for unemployment, and 24 for inflation. These are literature-informed calibration targets, not locally identified causal impulse responses. The review should assess whether path-deviation convolution is sufficiently defensible and restrained for this use.

## 6. Mean-model validation

The predeclared 2010–2015 model-selection window retained the parsimonious core over energy and energy-plus-expectations variants. On the separated 2016–2019 test, core RMSE is 0.131/0.263/0.423/0.726 at 1/3/6/12 months. It beats recorded simple baselines through six months but trails persistence and AR(4) at twelve months. On the archived 2020–2025 stress period, core RMSE is 0.198/0.438/0.780/1.748 and beats all recorded baselines at each horizon. The stress comparison is archived evidence, not a universal superiority claim.

## 7. Uncertainty failure

Fixed pre-2020 intervals under-cover badly in the post-2020 stress period. R11 adaptive uncertainty improved some coverage but failed its proper-score requirement. R12 rolling, exponentially weighted, and volatility-scaled conformal candidates all failed the frozen joint calibration, sharpness, and proper-score gate. The UI therefore labels the shaded range only as **simulation dispersion** and explicitly disclaims calibrated predictive probability.

## 8. Welfare function

The displayed welfare loss is a normalized quadratic illustration over inflation, output, and unemployment. It supports comparisons conditional on the simulator and chosen weights; it is not social welfare measurement or proof of policy optimality.

## 9. Policy benchmarks

Recorded rules are evaluated with identical information and random seeds. They are comparison devices within the model, not claims that a rule should govern real policy.

## 10. Counterfactual interpretation

Observed history and model-generated alternatives are visually and textually separated. A lower model loss means only that a path scores better under the documented engine and weights. It does not establish what would have happened in the real economy.

## 11. Major limitations

- Weak twelve-month pre-pandemic mean forecast relative to simple baselines
- Externally calibrated rather than locally identified policy transmission
- Failed predictive-interval calibration gates
- Structural simplification and limited external validity
- Conditional welfare weights and benchmark rules
- Live-data revisions and unresolved generalization beyond the released U.S. scenario
- No completed independent economist review

## 12. Review questions

1. Is the PCE state construction appropriate?
2. Is the monthly mean-model validation credible?
3. Is literature-calibrated policy-path convolution reasonable for an educational/research simulation?
4. Is the counterfactual interpretation sufficiently restrained?
5. Is the welfare function defensible for comparative simulation?
6. Are player-versus-historical comparisons framed appropriately?
7. Are any mechanisms double-counted?
8. Are any displayed quantities scientifically misleading?
9. Is the simulator publishable as a serious educational/research tool?
10. What specifically prevents a stronger V1.0 claim?
11. Which modelling component is weakest?
12. Which one change would most improve scientific credibility?

## 13. Code and evidence map

- Shared specification: [`../engine/unified_spec.json`](../engine/unified_spec.json)
- Browser engine: [`../lib/unified-core.mjs`](../lib/unified-core.mjs)
- Scientific contract: [`../docs/V0_9_SCIENTIFIC_CONTRACT.md`](../docs/V0_9_SCIENTIFIC_CONTRACT.md)
- Methodology and model: [`../METHODOLOGY.md`](../METHODOLOGY.md), [`../MODEL_SPECIFICATION.md`](../MODEL_SPECIFICATION.md)
- Mean-model evidence: [`../r10/results/model_selection.csv`](../r10/results/model_selection.csv), [`../r10/results/post_2019_stress.csv`](../r10/results/post_2019_stress.csv), and [`../reports/R10_SCIENTIFIC_RED_TEAM.md`](../reports/R10_SCIENTIFIC_RED_TEAM.md)
- Release hardening: [`../reports/R11_RELEASE_HARDENING.md`](../reports/R11_RELEASE_HARDENING.md)
- Frozen uncertainty audit: [`../reports/R12_FINAL_UNCERTAINTY_AUDIT.md`](../reports/R12_FINAL_UNCERTAINTY_AUDIT.md)
- R13 release audit: [`../reports/R13_RESEARCH_PREVIEW_RELEASE_AUDIT.md`](../reports/R13_RESEARCH_PREVIEW_RELEASE_AUDIT.md)
- Limitations: [`../LIMITATIONS.md`](../LIMITATIONS.md)
