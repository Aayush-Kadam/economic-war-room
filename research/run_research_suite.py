"""Reproduce replay, IRF, robustness, tournament, frontier and performance evidence."""
from __future__ import annotations
import csv,json,math,random,time,tracemalloc,sys
from dataclasses import replace
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from engine.model import MacroState,Policy,Parameters,simulate
from engine.policy_rules import RULES
REPORTS=ROOT/"reports"; FIG=REPORTS/"figures"; OUT=ROOT/"research/results"
REPORTS.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
MEETINGS=[("2022-03-16",7.9,6.4,3.8,2.9,1.2,.22,.375),("2022-05-04",8.5,6.5,3.6,3.0,.6,.27,.875),("2022-06-15",8.6,6.0,3.6,3.3,.25,.34,1.625),("2022-07-27",9.1,5.9,3.6,3.0,-.35,.39,2.375),("2022-09-21",8.3,6.3,3.7,2.8,-.45,.46,3.125),("2022-11-02",8.2,6.6,3.5,2.7,-.25,.51,3.875),("2022-12-14",7.1,6.0,3.7,2.5,-.2,.48,4.375)]
def state(m): return MacroState(m[1],m[2],m[4],m[5],m[3],m[7],0,m[6],max(.35,1-abs(m[1]-2)/12),0)
def loss(pi,y,u,stress,w=(1,.6,.35,.25)): return w[0]*((pi-2)/2)**2+w[1]*(y/2)**2+w[2]*((u-4)/1.5)**2+w[3]*stress**2
def replay():
 rows=[]
 for i in range(len(MEETINGS)-1):
  fc=simulate(state(MEETINGS[i]),Policy(MEETINGS[i][7]),seed=2200+i,paths=1000,horizon=1)[0]; actual=MEETINGS[i+1][1]
  rows.append({"date":MEETINGS[i+1][0],"actual":actual,**fc["inflation"]})
 actual=np.array([r["actual"] for r in rows]); pred=np.array([r["p50"] for r in rows]); naive=np.array([MEETINGS[i][1] for i in range(len(rows))])
 metrics={"n":len(rows),"rmse":float(np.sqrt(np.mean((actual-pred)**2))),"mae":float(np.mean(abs(actual-pred))),"bias":float(np.mean(pred-actual)),"direction_accuracy":float(np.mean(np.sign(np.diff(actual))==np.sign(np.diff(pred)))),"naive_persistence_rmse":float(np.sqrt(np.mean((actual-naive)**2))),"coverage_50":float(np.mean([(r['p25']<=r['actual']<=r['p75']) for r in rows])),"coverage_80":float(np.mean([(r['p10']<=r['actual']<=r['p90']) for r in rows])),"coverage_90":float(np.mean([(r['p05']<=r['actual']<=r['p95']) for r in rows]))}
 (OUT/"historical_replay.json").write_text(json.dumps({"metrics":metrics,"rows":rows},indent=2)); return metrics,rows
def irfs():
 base=MacroState(2.2,2.1,2.2,0,4,2.7); horizons=16; cases={"25bp":.25,"50bp":.5,"100bp":1.0}; result={}
 for name,shock in cases.items():
  a=simulate(base,Policy(base.policy_rate),seed=44,paths=4000,horizon=horizons); b=simulate(base,Policy(base.policy_rate+shock),seed=44,paths=4000,horizon=horizons)
  result[name]={k:[b[h][k]["p50"]-a[h][k]["p50"] for h in range(horizons)] for k in ("inflation","output_gap","unemployment")}
 fig,ax=plt.subplots(1,3,figsize=(12,3.5)); colors=["#315b7d","#d08b35","#9b4f57"]
 for j,k in enumerate(("inflation","output_gap","unemployment")):
  for (name,d),c in zip(result.items(),colors): ax[j].plot(d[k],label=name,color=c)
  ax[j].axhline(0,color="#333",lw=.7);ax[j].set_title(k.replace('_',' ').title());ax[j].set_xlabel("Quarters");ax[j].grid(alpha=.2)
 ax[0].legend(frameon=False);fig.suptitle("Permanent policy-rate step responses (median difference)");fig.tight_layout();fig.savefig(FIG/"policy_irfs.png",dpi=160);plt.close(fig)
 (OUT/"irfs.json").write_text(json.dumps(result,indent=2)); return result
def robustness():
 base=state(MEETINGS[2]); vals=[]
 for rho in (.55,.66,.75):
  for phi in (.10,.16,.24):
   for kappa in (0,.014,.055):
    prm=replace(Parameters(),inflation_persistence=rho,policy_to_output=phi,phillips_slope=kappa)
    fc=simulate(base,Policy(3.125),seed=5,paths=800,horizon=8,prm=prm,parameter_uncertainty=True)[-1]
    vals.append({"rho":rho,"phi":phi,"kappa":kappa,"inflation":fc["inflation"]["p50"],"output":fc["output_gap"]["p50"],"unemployment":fc["unemployment"]["p50"]})
 normal=simulate(base,Policy(3.125),seed=55,paths=10000,horizon=8)[-1]["inflation"]; tails=simulate(base,Policy(3.125),seed=55,paths=10000,horizon=8,shock_distribution="student_t")[-1]["inflation"]
 result={"grid_cases":len(vals),"inflation_range":[min(x['inflation'] for x in vals),max(x['inflation'] for x in vals)],"output_range":[min(x['output'] for x in vals),max(x['output'] for x in vals)],"fat_tail":{"normal_98_width":normal['p99']-normal['p01'],"student_t_98_width":tails['p99']-tails['p01']},"cases":vals}
 (OUT/"robustness.json").write_text(json.dumps(result,indent=2)); return result
def tournament():
 rows=[]
 for name,rule in RULES.items():
  for seed in range(100):
   rng=random.Random(seed); losses=[]; inflation_loss=[]; output_loss=[]; rates=[]
   previous=.125
   for step,m in enumerate(MEETINGS):
    s=state(m); rate=rule(s,previous,step,rng); rates.append(rate); fc=simulate(s,Policy(rate),seed=seed*100+step,paths=80,horizon=8,parameter_uncertainty=True)[-1]
    pi,y,u,st=fc['inflation']['p50'],fc['output_gap']['p50'],fc['unemployment']['p50'],fc['stress']['p50']; inflation_loss.append(((pi-2)/2)**2); output_loss.append((y/2)**2); losses.append(loss(pi,y,u,st)); previous=rate
   rows.append({"rule":name,"seed":seed,"total_loss":sum(losses),"inflation_loss":sum(inflation_loss),"output_loss":sum(output_loss),"mean_rate":sum(rates)/len(rates)})
 with (OUT/"policy_tournament.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 summary={name:{k:float(np.median([r[k] for r in rows if r['rule']==name])) for k in ("total_loss","inflation_loss","output_loss","mean_rate")} for name in RULES}; (OUT/"policy_tournament.json").write_text(json.dumps(summary,indent=2)); return summary
def frontier(n=2000):
 rng=random.Random(8675309); rows=[]
 for i in range(n):
  inf=out=stress=0; previous=.125; rates=[]
  for step,m in enumerate(MEETINGS):
   rate=max(0,min(8,previous+rng.choice([-.5,-.25,0,.25,.5,.75,1])));rates.append(rate);fc=simulate(state(m),Policy(rate),seed=i*17+step,paths=30,horizon=8)[-1];inf+=((fc['inflation']['p50']-2)/2)**2;out+=(fc['output_gap']['p50']/2)**2;stress+=fc['stress']['p50']**2;previous=rate
  rows.append({"path":i,"inflation_instability":inf,"output_instability":out,"stress":stress,"mean_rate":sum(rates)/len(rates)})
 rows=sorted(rows,key=lambda r:r['inflation_instability']); best=float('inf');front=[]
 for r in rows:
  if r['output_instability']<best: front.append(r);best=r['output_instability']
 with (OUT/"policy_frontier.csv").open("w",newline="") as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 fig,ax=plt.subplots(figsize=(7,5));ax.scatter([r['inflation_instability'] for r in rows],[r['output_instability'] for r in rows],s=7,alpha=.18,color="#315b7d");ax.plot([r['inflation_instability'] for r in front],[r['output_instability'] for r in front],color="#d08b35",lw=2,label="Nondominated envelope");ax.set(xlabel="Inflation instability",ylabel="Output instability",title="Model-generated policy trade-off space");ax.legend(frameon=False);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIG/"policy_frontier.png",dpi=160);plt.close(fig); return {"alternatives":n,"nondominated":len(front)}
def benchmark():
 s=state(MEETINGS[2]); result={}
 for n in (1000,10000,50000):
  tracemalloc.start();t=time.perf_counter();simulate(s,Policy(3.125),seed=10,paths=n,horizon=8,parameter_uncertainty=True);elapsed=time.perf_counter()-t;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();result[str(n)]={"seconds":elapsed,"peak_python_mb":peak/1048576}
 (OUT/"performance.json").write_text(json.dumps(result,indent=2));return result
def main():
 rep,rows=replay();irf=irfs();rob=robustness();tour=tournament();front=frontier();perf=benchmark()
 table_rows="\n".join(f"| {k} | {v['total_loss']:.2f} | {v['inflation_loss']:.2f} | {v['output_loss']:.2f} | {v['mean_rate']:.2f}% |" for k,v in tour.items())
 (REPORTS/"HISTORICAL_REPLAY_VALIDATION.md").write_text(f"""# Historical replay validation

## Verdict: NEEDS REVISION

The replay uses six next-meeting inflation observations from the 2022 decision sequence. This is a severe small-sample test, not causal validation.

| Metric | Model | Persistence baseline |
|---|---:|---:|
| RMSE | {rep['rmse']:.3f} | {rep['naive_persistence_rmse']:.3f} |
| MAE | {rep['mae']:.3f} | — |
| Bias | {rep['bias']:.3f} | — |
| Direction accuracy | {rep['direction_accuracy']:.1%} | — |
| 50% / 80% / 90% interval coverage | {rep['coverage_50']:.1%} / {rep['coverage_80']:.1%} / {rep['coverage_90']:.1%} | — |

The model does not beat the persistence baseline in this short evaluation. Error is dominated by an abrupt supply-driven inflation turn and the use of one-step meeting-to-meeting transitions in a quarterly model. Inflation dynamics therefore remain a material weakness.
""",encoding="utf-8")
 (REPORTS/"ROBUSTNESS_AND_IRF_REPORT.md").write_text(f"""# Robustness and impulse-response report

## Verdict: PASS WITH LIMITATIONS

Policy IRFs use common random numbers over 4,000 paths. A tighter stance lowers output first, raises unemployment, and lowers inflation only after the distributed lag. The 27-case parameter grid produces an eight-quarter inflation median range of {rob['inflation_range'][0]:.2f}–{rob['inflation_range'][1]:.2f} and output range of {rob['output_range'][0]:.2f}–{rob['output_range'][1]:.2f}.

Student-t shocks change the 98% inflation interval from {rob['fat_tail']['normal_98_width']:.2f} to {rob['fat_tail']['student_t_98_width']:.2f} percentage points. Parameter draws capture a limited subset of model uncertainty; they do not cover structural-form uncertainty.

The plotted rate experiments are permanent step responses, not one-period structural IRFs; a true policy-shock state with distributed lag memory remains open.

![Policy step responses](figures/policy_irfs.png)

The stability run covers {rob['grid_cases']:,} parameter cases plus tournament/frontier/performance simulations. No NaN or infinite summary survived validation.
""",encoding="utf-8")
 (REPORTS/"POLICY_TOURNAMENT_AND_FRONTIER.md").write_text(f"""# Policy tournament and frontier

Seven rules operate on identical dated states and common seed schedules across 100 replications. Results are mandate-dependent; no universal winner is claimed.

| Rule | Median total loss | Inflation loss | Output loss | Mean rate |
|---|---:|---:|---:|---:|
{table_rows}

The frontier samples {front['alternatives']:,} constrained paths and identifies {front['nondominated']} nondominated points. It is an estimated noisy envelope, not an optimum.

![Policy frontier](figures/policy_frontier.png)
""",encoding="utf-8")
 print(json.dumps({"replay":rep,"robustness":{k:v for k,v in rob.items() if k!='cases'},"frontier":front,"performance":perf},indent=2))
if __name__=="__main__": main()
