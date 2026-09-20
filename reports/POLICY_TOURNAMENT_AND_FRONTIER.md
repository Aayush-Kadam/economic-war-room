# Policy tournament and frontier

Seven rules operate on identical dated states and common seed schedules across 100 replications. Results are mandate-dependent; no universal winner is claimed.

| Rule | Median total loss | Inflation loss | Output loss | Mean rate |
|---|---:|---:|---:|---:|
| historical | 4.01 | 1.08 | 2.43 | 2.38% |
| taylor | 93.13 | 21.12 | 57.71 | 10.00% |
| inflation_focused | 93.13 | 21.12 | 57.71 | 10.00% |
| dual_mandate | 93.13 | 21.12 | 57.71 | 10.00% |
| smoothing | 31.39 | 6.60 | 19.77 | 6.33% |
| hold | 9.38 | 3.66 | 5.48 | 0.12% |
| random | 6.66 | 2.57 | 3.72 | 0.61% |

The frontier samples 2,000 constrained paths and identifies 4 nondominated points. It is an estimated noisy envelope, not an optimum.

![Policy frontier](figures/policy_frontier.png)
