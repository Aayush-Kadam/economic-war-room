# Monetary-policy transmission identification

## Claim boundary

R9 implements a **literature-calibrated policy-path-deviation response**, not an estimated structural impulse response. The input is the unexpected player path minus a dated baseline path, in basis points. The level of the policy rate is stored separately and is never relabelled as a shock.

The deterministic monthly kernels peak first for financial conditions (6 months), then output (18), unemployment (22), and inflation (24). A one-time 100-basis-point contractionary deviation has calibrated peak effects of +0.30 on financial conditions, -0.60 percentage point on output, +0.20 point on unemployment, and -0.30 point on inflation. Convolution allows a multi-meeting path to accumulate and unwind transparently.

These magnitudes and timings are external calibration targets informed by narrative and high-frequency/external-instrument evidence, including Romer and Romer (2004), Federal Reserve external-instrument SVAR work, and Federal Reserve comparisons of shock series. R9 does not claim to reproduce any paper's point estimates.

## Rejected identification choices

- Treating the observed policy-rate level as an exogenous shock was rejected because systematic reaction to inflation and activity is endogenous.
- Relabelling permanent rate-step simulations as structural IRFs was rejected.
- Estimating a high-frequency surprise series locally was rejected because the frozen repository does not contain announcement-window futures data.
- Using contemporaneous monthly inflation without addressing aggregation was rejected; the new price-flow clock makes the annual-rate mapping explicit.

The remaining limitation is material: identification is imported through documented calibration, not recovered from this repository's data. Results support disciplined scenario comparison, not causal attribution or policy-effect estimation.
