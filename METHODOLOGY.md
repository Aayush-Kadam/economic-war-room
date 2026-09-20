# Methodology

## Calibration

The release is a transparent literature-informed calibration, not a newly estimated causal model. Persistence, Phillips slope, Okun mapping and distributed policy lag are intentionally conservative and exposed in `Parameters`. Their purpose is plausible signs, timing and uncertainty—not reproduction of the realized 2022 path. This is a limitation and the principal target for the next research release.

| Parameter | Value | Status | Interpretation |
|---|---:|---|---|
| inflation persistence | 0.66 | provisional calibration | quarterly inertia |
| expectations weight | 0.34 | identity complement | forward/anchored component |
| output persistence | 0.64 | provisional calibration | activity inertia |
| policy-to-output | 0.16 | literature-informed prior | delayed real-rate channel |
| Phillips slope | 0.10 | literature-informed prior | output-to-price pressure |
| Okun coefficient | 0.16 | literature-informed prior | activity-to-unemployment |
| inflation shock σ | 0.32 | provisional calibration | path dispersion |
| output shock σ | 0.28 | provisional calibration | path dispersion |

## Historical packets

Meeting dates come from the Federal Reserve calendar. Release values in the interface are contemporaneous headline indicators assembled from official release archives. Production retrieval uses ALFRED vintage parameters; the registry distinguishes vintage-required data. A packet is valid only if every release date is on or before the meeting cutoff.

## Interpretation

Model-implied probabilities are Monte Carlo frequencies conditional on the specified model and shocks. The actual FOMC path and macro outcomes are observations. The player's path is not an estimate of what history would certainly have been.
