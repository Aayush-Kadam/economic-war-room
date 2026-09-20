# Model specification

## State and timing

Quarterly state `x = [π, πcore, Eπ, y, u, i, c, f, credibility, fx]`: annual inflation rates, output gap, unemployment rate, nominal policy rate, credit gap, financial stress, bounded credibility and exchange-rate gap. A decision sets `i`, guidance and balance-sheet stance; shocks then realize; financial conditions and output move before inflation.

## Equations

The implementation in `engine/model.py` uses:

`Eπ(t+1) = π* + (Eπ(t)-π*)·(0.72-0.18·credibility) - 0.12·guidance`

`c(t+1) = 0.70c(t) - 0.10·real_stance(t)`

`y(t+1) = 0.64y(t) - 0.16·lag(h)·real_stance(t) + 0.08c(t+1) - 0.08f(t) + εy`

`π(t+1) = 0.66π(t) + 0.34Eπ(t+1) + 0.10y(t+1) - 0.12·max(h-2,0)·lag(h)·real_stance(t) + supply + επ`

`u(t+1) = bound[u(t) - 0.16y(t+1) + 0.035·lag(h)·real_stance(t)]`

`lag(h)=min(1,h/4)` prevents instantaneous inflation effects. Stress is persistent and rises only when restrictive stance or impaired credit crosses a threshold. Credibility is bounded `[0.2,1]`, improves slowly and deteriorates with target misses.

## Shocks and uncertainty

Inflation and demand innovations are Gaussian in the interactive baseline, with standard deviations 0.32 and 0.28. A fixed seed and identical inputs reproduce identical paths. The interface reports the median and 10th/90th percentiles from 1,000 paths.

## Welfare

`L = 1.0((π-2)/2)^2 + 0.6(y/2)^2 + 0.35((u-4)/1.5)^2 + 0.25f^2`. Normalization prevents unlike units from being naively added. These weights represent a dual-mandate profile, not an objectively correct social welfare function.

## Economic signs

Higher sustained real stance lowers credit and output, raises unemployment and lowers inflation with a delay. Positive demand shocks raise output and inflation pressure. Supply pressure raises inflation while decaying. Hawkish guidance modestly lowers expected inflation. Directional tests compare common random numbers rather than requiring every stochastic path to obey the median sign.
