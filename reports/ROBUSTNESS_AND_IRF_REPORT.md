# Robustness and transmission report

## R9 verdict: PASS WITH LIMITATIONS

The legacy chart below is retained for reproducibility but renamed correctly: it shows permanent policy-rate step responses from the semi-structural simulator, not identified structural IRFs. Common random numbers isolate model response differences.

![Permanent policy-rate step responses](figures/policy_irfs.png)

The 27-case parameter grid yields eight-quarter median inflation of 1.83–2.09 and output gaps of -0.50 to -0.22. Student-t shocks widen the 98% inflation interval from 1.99 to 2.11 percentage points. These exercises cover parameter and shock-distribution sensitivity, not structural-form uncertainty.

R9's new transmission module instead convolves explicitly defined policy-path deviations with documented monthly calibration kernels. See `TRANSMISSION_IDENTIFICATION.md`. Neither artifact is presented as a locally estimated causal IRF.
