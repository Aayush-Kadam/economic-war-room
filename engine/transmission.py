"""Literature-calibrated policy-path-deviation convolution; not a structural IRF."""
from __future__ import annotations
import math
def _gamma_kernel(length,peak):
    raw=[0.0 if h==0 else (h/peak)*math.exp(1-h/peak) for h in range(length)]
    scale=max(raw) or 1; return [x/scale for x in raw]
def calibrated_kernels(months=48):
    # Magnitudes per 100bp unexpected deviation. Peaks follow published external-
    # instrument evidence: financial conditions first, activity around 12-18m,
    # prices later. They are calibration targets, not estimates from this repo.
    return {"output":[-.60*x for x in _gamma_kernel(months,18)],"inflation":[-.30*x for x in _gamma_kernel(months,24)],"unemployment":[.20*x for x in _gamma_kernel(months,22)],"financial_conditions":[.30*x for x in _gamma_kernel(months,6)]}
def path_deviation(player,baseline):
    if len(player)!=len(baseline): raise ValueError("policy paths must share a clock")
    return [float(a-b) for a,b in zip(player,baseline)]
def convolve_policy_deviation(deviation,kernel):
    out=[]
    for t in range(len(deviation)+len(kernel)-1): out.append(sum(deviation[j]/100*kernel[t-j] for j in range(max(0,t-len(kernel)+1),min(len(deviation)-1,t)+1)))
    return out
