# Historical replay validation

## Verdict: NEEDS REVISION

The replay uses six next-meeting inflation observations from the 2022 decision sequence. This is a severe small-sample test, not causal validation.

| Metric | Model | Persistence baseline |
|---|---:|---:|
| RMSE | 1.856 | 0.643 |
| MAE | 1.761 | — |
| Bias | -1.761 | — |
| Direction accuracy | 80.0% | — |
| 50% / 80% / 90% interval coverage | 0.0% / 0.0% / 0.0% | — |

The model does not beat the persistence baseline in this short evaluation. Error is dominated by an abrupt supply-driven inflation turn and the use of one-step meeting-to-meeting transitions in a quarterly model. Inflation dynamics therefore remain a material weakness.
