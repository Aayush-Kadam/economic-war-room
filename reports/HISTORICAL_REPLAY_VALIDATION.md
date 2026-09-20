# Historical replay validation

## R9 verdict: PASS WITH LIMITATIONS

R9 replaces the mismatched quarterly/meeting inflation exercise as the primary predictive validation. It models monthly log PCE price changes and derives annual inflation exactly as the rolling sum of twelve monthly changes. Every expanding-window origin uses only observations available at that origin. The frozen evaluation window is January 2010 through December 2019.

| Horizon | N | Flow RMSE | Persistence RMSE | Relative RMSE | Direction accuracy |
|---|---:|---:|---:|---:|---:|
| 1 month | 108 | 0.143 | 0.206 | 0.694 | 74.1% |
| 3 months | 108 | 0.329 | 0.421 | 0.781 | 75.0% |
| 6 months | 108 | 0.539 | 0.633 | 0.851 | 71.3% |
| 12 months | 108 | 0.876 | 0.842 | 1.041 | 72.2% |

The mean 1/3/6-month relative RMSE is 0.775, passing the predeclared ceiling of 1.00. The worst relative RMSE is 1.041, passing the 1.15 guardrail, but the 12-month model does not beat persistence and both AR baselines are stronger there. This is a real limitation, not hidden by an aggregate score.

The original six-meeting 2022 replay remains as a legacy stress diagnostic: RMSE 1.856 versus persistence 0.643, bias -1.761, and zero interval coverage. It is not used as evidence of predictive validity because it combines an incompatible quarterly state with irregular meeting steps.

Machine-readable evidence: `r9/results/rolling_evaluation.csv` and `r9/results/r9_metrics.json`.
