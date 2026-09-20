"""Monthly economic core shared by validation and the browser's exact JSON bridge."""
from __future__ import annotations
from dataclasses import dataclass
import json, math, random
from pathlib import Path

SPEC=json.loads((Path(__file__).with_name("unified_spec.json")).read_text())

@dataclass(frozen=True)
class UnifiedState:
    monthly_price_changes: tuple[float,...]
    expected_inflation: float
    output_gap: float
    unemployment: float
    policy_rate: float
    credit_gap: float=0.0
    financial_stress: float=0.2
    credibility: float=0.75

    @property
    def pce_yoy(self): return sum(self.monthly_price_changes[-12:])

def gamma_kernel(length:int,peak:int,magnitude:float):
    raw=[0.0 if h==0 else (h/peak)*math.exp(1-h/peak) for h in range(length)]
    scale=max(raw) or 1.0
    return [magnitude*x/scale for x in raw]

def meeting_month(date:str): return date[:7]

def monthly_policy_path(meetings, rates, start_month, months):
    """Hold each decision rate until a later meeting changes it; never invent meetings."""
    dated=sorted((meeting_month(d),float(r)) for d,r in zip(meetings,rates))
    out=[]; current=dated[0][1]
    sy,sm=map(int,start_month.split("-"))
    for k in range(months):
        y=sy+(sm-1+k)//12; m=(sm-1+k)%12+1; key=f"{y:04d}-{m:02d}"
        for d,r in dated:
            if d<=key: current=r
        out.append(current)
    return out

def policy_responses(player,baseline):
    if len(player)!=len(baseline): raise ValueError("policy paths must share a monthly clock")
    deviation=[100*(p-b) for p,b in zip(player,baseline)]
    cfg=SPEC["transmission"]; result={}
    for name,item in cfg.items():
        if name=="months": continue
        kernel=gamma_kernel(cfg["months"],item["peak_month"],item["magnitude_per_100bp"])
        result[name]=[sum(deviation[j]/100*kernel[t-j] for j in range(max(0,t-len(kernel)+1),t+1)) for t in range(len(deviation))]
    return deviation,result

def simulate_monthly(initial:UnifiedState, player_path, baseline_path, *, seed=0, stochastic=True):
    deviation,response=policy_responses(player_path,baseline_path); rng=random.Random(seed)
    changes=list(initial.monthly_price_changes); output=initial.output_gap; unemployment=initial.unemployment; stress=initial.financial_stress; rows=[]
    inf=SPEC["inflation"]; st=SPEC["state"]
    for t,rate in enumerate(player_path):
        base=inf["intercept"]+sum(b*changes[-j-1] for j,b in enumerate(inf["lag_coefficients"]))
        shock=rng.gauss(0,inf["monthly_shock_sigma"]) if stochastic else 0.0
        # The kernel is a level effect on reported YoY inflation; divide by 12 in
        # the flow state so the exact rolling identity remains authoritative.
        changes.append(base+response["inflation"][t]/12+shock)
        output=st["output_persistence"]*output+response["output"][t]
        unemployment=4+st["unemployment_persistence"]*(unemployment-4)+response["unemployment"][t]
        stress=st["stress_persistence"]*stress+response["financial_conditions"][t]
        rows.append({"month":t+1,"pce_yoy":sum(changes[-12:]),"monthly_price_change":changes[-1],"output_gap":output,"unemployment":max(2.5,min(12,unemployment)),"financial_stress":max(0,min(2,stress)),"policy_rate":rate,"policy_deviation_bp":deviation[t]})
    return rows
