# Methodology

## Calibration

The release combines equation-specific estimates from a frozen 1990Q1–2019Q4 dataset with literature-informed transmission parameters where identification is weak. The estimation window was fixed before fitting and excludes the pandemic and 2021–23 evaluation episode. Monetary-policy coefficients are not presented as causal because the policy rate reacts endogenously to the economy.

| Parameter | Value | Status | Interpretation |
|---|---:|---|---|
| inflation persistence | 0.66 | literature-informed; direct Q/Q estimate failed measurement-consistent replay | Y/Y inertia |
| expectations weight | 0.06 | estimated, weak | anchored component |
| output persistence | 0.85 | estimated then regularised | activity inertia |
| policy-to-output | 0.16 | literature-informed prior | delayed real-rate channel |
| Phillips slope | 0.014 | estimated, weak | output-to-price pressure |
| Okun coefficient | 0.288 | estimated | activity-to-unemployment |
| inflation shock σ | 0.32 | provisional calibration | path dispersion |
| output shock σ | 0.28 | provisional calibration | path dispersion |

## Historical packets

Meeting dates come from the Federal Reserve calendar. Release values in the interface are contemporaneous headline indicators assembled from official release archives. Production retrieval uses ALFRED vintage parameters; the registry distinguishes vintage-required data. A packet is valid only if every release date is on or before the meeting cutoff.

## Interpretation

Model-implied probabilities are Monte Carlo frequencies conditional on the specified model and shocks. The actual FOMC path and macro outcomes are observations. The player's path is not an estimate of what history would certainly have been.
