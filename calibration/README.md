# Calibration pipeline

Run `python calibration/build_frozen_sample.py` and then `python calibration/estimate_parameters.py`. The hard cutoff is 2019 Q4: the final pre-pandemic quarter, selected before estimation so neither the pandemic nor the 2021–23 evaluation episode can influence fitted coefficients.

The calibration dataset uses latest-revised official history. This is appropriate for estimating stable reduced-form relationships but is distinct from the meeting-date real-time warehouse. Estimated coefficients are equation-specific descriptive relationships; the distributed real-rate regression is not presented as a structural monetary-policy identification.
