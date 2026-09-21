# Uncertainty validation status

Economic War Room currently does not claim calibrated probabilistic forecast intervals. Multiple real-time interval methods improved empirical coverage but failed the predeclared joint calibration, sharpness, width, and proper-score requirements.

R11 selected exponentially weighted absolute-residual intervals on an earlier window. On the opened 2023–2025 evaluation, long-horizon coverage improved, but mean interval score worsened by 1.7% rather than improving by the required 10%.

R12 froze a new protocol before evaluation and tested rolling conformal, exponentially weighted conformal, and volatility-scaled conformal families. All improved aggregate coverage error in the blocked 2022 confirmation. None met the joint gate: proper scores deteriorated too much, 90% coverage failed at a major horizon, too few horizons improved WIS, or widths became excessive. Only six genuinely new one-month targets were available in 2026; longer-horizon confirmation was immature.

The public simulator may show simulation dispersion from its seeded stochastic shock process. That spread is conditional model sensitivity, not a calibrated predictive interval, confidence interval, or real-world probability statement.

The frozen protocols, candidate outputs, and negative results remain in `r11/`, `r12/`, `reports/R11_RELEASE_HARDENING.md`, and `reports/R12_FINAL_UNCERTAINTY_AUDIT.md`.
