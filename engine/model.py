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
    inflation_persistence: float = 0.66; expectation_weight: float = 0.06
    phillips_slope: float = 0.014; policy_to_output: float = 0.16
    output_persistence: float = 0.85; okun: float = 0.288
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
    anchor=(1-prm.inflation_persistence-prm.expectation_weight)*prm.target
    transmission=0.10*max(horizon-2,0)*math.exp(-max(horizon-2,0)/6)
    inflation = anchor+prm.inflation_persistence*s.inflation+prm.expectation_weight*expected+prm.phillips_slope*output-transmission*real_stance+0.12*supply+shock[0]
    unemployment = max(2.5,min(12.0,4.0+0.85*(s.unemployment-4.0)-prm.okun*output+0.035*lag*real_stance))
    credibility = max(0.2,min(1.0,s.credibility+0.02-0.003*abs(inflation-prm.target)+0.01*max(0,p.guidance)))
    return MacroState(inflation, inflation-0.4*supply, expected, output, unemployment, p.rate, credit, stress, credibility, s.fx_gap)

def simulate(initial: MacroState, policy: Policy, *, seed: int, paths: int=1000, horizon: int=8, prm: Parameters=Parameters(), shock_distribution: str="gaussian", parameter_uncertainty: bool=False):
    rng=random.Random(seed); trajectories=[]
    for _ in range(paths):
        s=initial; path=[]; draw=prm
        if parameter_uncertainty:
            draw=Parameters(**{**asdict(prm),"inflation_persistence":max(.05,min(.7,rng.gauss(prm.inflation_persistence,.095))),"phillips_slope":max(-.05,min(.12,rng.gauss(prm.phillips_slope,.041))),"policy_to_output":max(.05,min(.35,rng.gauss(prm.policy_to_output,.04))),"okun":max(.12,min(.45,rng.gauss(prm.okun,.035)))})
        for h in range(horizon):
            if shock_distribution=="student_t":
                scale=math.sqrt(3/5); shocks=(rng.gauss(0,1)/math.sqrt(rng.gammavariate(2.5,2/5))*scale*draw.sigma_inflation,rng.gauss(0,1)/math.sqrt(rng.gammavariate(2.5,2/5))*scale*draw.sigma_output)
            else: shocks=(rng.gauss(0,draw.sigma_inflation),rng.gauss(0,draw.sigma_output))
            s=_step(s,policy,draw,shocks,h); path.append(s)
        trajectories.append(path)
    def q(name,h,p):
        xs=sorted(getattr(path[h],name) for path in trajectories); return xs[min(len(xs)-1,int((len(xs)-1)*p))]
    return [{"horizon":h,"inflation":{"p01":q("inflation",h,.01),"p05":q("inflation",h,.05),"p10":q("inflation",h,.1),"p25":q("inflation",h,.25),"p50":q("inflation",h,.5),"p75":q("inflation",h,.75),"p90":q("inflation",h,.9),"p95":q("inflation",h,.95),"p99":q("inflation",h,.99)},"output_gap":{"p10":q("output_gap",h,.1),"p50":q("output_gap",h,.5),"p90":q("output_gap",h,.9)},"unemployment":{"p10":q("unemployment",h,.1),"p50":q("unemployment",h,.5),"p90":q("unemployment",h,.9)},"stress":{"p50":q("financial_stress",h,.5)}} for h in range(horizon)]

def welfare(state: MacroState, weights=(1.0,.6,.35,.25)) -> float:
    return weights[0]*((state.inflation-2)/2)**2+weights[1]*(state.output_gap/2)**2+weights[2]*((state.unemployment-4)/1.5)**2+weights[3]*state.financial_stress**2
