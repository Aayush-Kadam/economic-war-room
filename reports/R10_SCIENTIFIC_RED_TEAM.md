# R10 scientific red-team review

| Attack | Classification | Finding / required control |
|---|---|---|
| Policy endogeneity | Mitigated | Absolute rates no longer masquerade as shocks; kernels remain externally calibrated. |
| Inflation measurement mismatch | Resolved | Estimation, simulation, and display share monthly flows and an exact rolling-YoY identity. |
| Lookahead leakage | Mitigated | Selection ends in 2015, historical test is 2016–2019, stress begins in 2020; post outcomes never set interval widths. |
| Aggregation error | Accepted limitation | Meeting-month mapping is exact, but monthly GDP/output is a persistent latent state rather than observed monthly GDP. |
| Post-pandemic instability | Release blocker for research-grade claims | Pre-2020 90% intervals cover only 50.7% at 12 months after 2019. |
| Double-counted transmission | Mitigated | The selected price-flow core excludes policy variables; only path deviations add the policy kernel. Autoregressive persistence can still propagate the adjusted flow. |
| Inflation persistence | Accepted limitation | Strong short-horizon evidence; 12-month 2016–2019 RMSE remains worse than persistence and AR baselines. |
| Expectations treatment | Resolved for selected core | Expectations augmentation failed the predeclared selection rule and was rejected. |
| Energy omission | Accepted limitation | Energy augmentation also failed selection; pandemic supply shocks expose the cost of omission. |
| Welfare weights | Accepted limitation | Designed normative weights are disclosed; tournament rankings are not policy recommendations. |
| Benchmark fairness | Mitigated | Persistence, AR(1), and AR(4) are all reported; the model loses at 12 months pre-pandemic. |
| False precision | Mitigated | Reports distinguish calibrated responses, model-conditioned intervals, and observations. |
| Browser initialization | Release blocker for exact historical replication | Twelve equal flows reproduce initial YoY exactly but not the actual monthly price-change history. A full vintage packet is required for exact trajectory identity. |
| Bundled data rights | Release blocker | Source-agency redistribution terms have not been confirmed series by series. |

## Adversarial verdict

The architecture is materially more coherent, but exact historical browser/validation trajectory equivalence is not yet established because the UI lacks vintage monthly flow histories and external shocks. Public research-preview publication should remain blocked until data licensing and initialization are resolved. Research-grade release is not warranted.
