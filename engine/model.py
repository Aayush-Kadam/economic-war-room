from __future__ import annotations
from dataclasses import dataclass, asdict
import math, random
from statistics import median

@dataclass(frozen=True)
class MacroState:
    inflation: float; core_inflation: float; expected_inflation: float
    output_gap: float; unemployment: float; policy_rate: float
    credit_gap: float = 0.0; financial_stress: float = 0.2
    credibility: float = 0.75; fx_gap: float = 0.0

@dataclass(frozen=True)
class Policy:
    rate: float; guidance: float = 0.0; balance_sheet: float = 0.0

@dataclass(frozen=True)
class Parameters:
    target: float = 2.0; neutral_real_rate: float = 0.5
    inflation_persistence: float = 0.66; expectation_weight: float = 0.34
    phillips_slope: float = 0.10; policy_to_output: float = 0.16
    output_persistence: float = 0.64; okun: float = 0.16
    credit_sensitivity: float = 0.10; stress_threshold: float = 2.0
    sigma_inflation: float = 0.32; sigma_output: float = 0.28

def _step(s: MacroState, p: Policy, prm: Parameters, shock: tuple[float,float], horizon: int) -> MacroState:
    expected = prm.target + (s.expected_inflation-prm.target)*(0.72-0.18*s.credibility) - p.guidance*0.12
    real_stance = p.rate-expected-prm.neutral_real_rate
    lag = min(1.0, horizon/4.0)
    credit = 0.70*s.credit_gap-prm.credit_sensitivity*real_stance
    stress = max(0.0, min(2.0, 0.78*s.financial_stress + 0.04*max(0, real_stance-prm.stress_threshold) + 0.03*max(0,-credit)))
    output = prm.output_persistence*s.output_gap-prm.policy_to_output*lag*real_stance+0.08*credit-0.08*stress+shock[1]
    supply = 0.68**horizon*(s.inflation-s.core_inflation)
    inflation = prm.inflation_persistence*s.inflation+prm.expectation_weight*expected+prm.phillips_slope*output-0.12*max(horizon-2,0)*lag*real_stance+0.12*supply+shock[0]
    unemployment = max(2.5,min(12.0,s.unemployment-prm.okun*output+0.035*lag*real_stance))
    credibility = max(0.2,min(1.0,s.credibility+0.02-0.003*abs(inflation-prm.target)+0.01*max(0,p.guidance)))
    return MacroState(inflation, inflation-0.4*supply, expected, output, unemployment, p.rate, credit, stress, credibility, s.fx_gap)

def simulate(initial: MacroState, policy: Policy, *, seed: int, paths: int=1000, horizon: int=8, prm: Parameters=Parameters()):
    rng=random.Random(seed); trajectories=[]
    for _ in range(paths):
        s=initial; path=[]
        for h in range(horizon):
            s=_step(s,policy,prm,(rng.gauss(0,prm.sigma_inflation),rng.gauss(0,prm.sigma_output)),h); path.append(s)
        trajectories.append(path)
    def q(name,h,p):
        xs=sorted(getattr(path[h],name) for path in trajectories); return xs[min(len(xs)-1,int((len(xs)-1)*p))]
    return [{"horizon":h,"inflation":{"p10":q("inflation",h,.1),"p50":q("inflation",h,.5),"p90":q("inflation",h,.9)},"output_gap":{"p50":q("output_gap",h,.5)},"unemployment":{"p50":q("unemployment",h,.5)},"stress":{"p50":q("financial_stress",h,.5)}} for h in range(horizon)]

def welfare(state: MacroState, weights=(1.0,.6,.35,.25)) -> float:
    return weights[0]*((state.inflation-2)/2)**2+weights[1]*(state.output_gap/2)**2+weights[2]*((state.unemployment-4)/1.5)**2+weights[3]*state.financial_stress**2
