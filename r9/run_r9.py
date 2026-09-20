"""R9 monthly-flow pseudo-out-of-sample evaluation and interval calibration."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from engine.inflation_flow import monthly_log_change,fit_flow_model,forecast_yoy
OUT=ROOT/"r9/results";REPORTS=ROOT/"reports";FIG=REPORTS/"figures";OUT.mkdir(parents=True,exist_ok=True);FIG.mkdir(exist_ok=True)
HORIZONS=(1,3,6,12); EVAL_START="2010-01-01"
ACCEPTANCE={"mean_relative_rmse_1_3_6_max":1.0,"any_horizon_relative_rmse_max":1.15,"coverage_absolute_error_max":.15}
def interval_score(y,lo,hi,alpha): return (hi-lo)+(2/alpha)*(lo-y if y<lo else y-hi if y>hi else 0)
def ar_yoy_forecast(y,origin,horizon,lags):
 train=list(y[:origin+1]);
 for _ in range(horizon):
  z=np.asarray(train);X=np.array([[1,*z[t-lags:t][::-1]] for t in range(lags,len(z))]);b=np.linalg.pinv(X.T@X)@X.T@z[lags:];train.append(float(np.dot([1,*train[-lags:][::-1]],b)))
 return train[-1]
def main():
 p=pd.read_csv(ROOT/"calibration/frozen/raw/PCEPI.csv",parse_dates=[0],index_col=0).iloc[:,0].dropna(); changes=monthly_log_change(p); dates=p.index[1:]; yoy=100*np.log(p/p.shift(12)); start=p.index.get_loc(EVAL_START)
 rows=[]; past_errors={h:[] for h in HORIZONS}
 for origin in range(start,len(p)-max(HORIZONS)):
  model=fit_flow_model(changes[:origin]); history=changes[:origin]
  for h in HORIZONS:
   pred,_=forecast_yoy(model,history,h); actual=float(yoy.iloc[origin+h]); persistence=float(yoy.iloc[origin]); ar1=ar_yoy_forecast(yoy.iloc[12:].to_numpy(),origin-12,h,1); ar4=ar_yoy_forecast(yoy.iloc[12:].to_numpy(),origin-12,h,4)
   row={"origin":str(p.index[origin].date()),"horizon_months":h,"actual":actual,"flow":pred,"persistence":persistence,"ar1":ar1,"ar4":ar4}
   errors=past_errors[h]
   if len(errors)>=24:
    for level in (50,80,90):
     alpha=1-level/100; lo,hi=np.quantile(errors,[alpha/2,1-alpha/2]);row[f"lo{level}"]=pred+lo;row[f"hi{level}"]=pred+hi;row[f"cover{level}"]=row[f"lo{level}"]<=actual<=row[f"hi{level}"];row[f"score{level}"]=interval_score(actual,row[f"lo{level}"],row[f"hi{level}"],alpha)
   errors.append(actual-pred); rows.append(row)
 d=pd.DataFrame(rows);d.to_csv(OUT/"rolling_evaluation.csv",index=False)
 metrics={}
 for h,g in d.groupby("horizon_months"):
  m={"n":len(g)}
  for name in ("flow","persistence","ar1","ar4"):
   e=g[name]-g.actual;m[f"{name}_rmse"]=float(np.sqrt(np.mean(e*e)));m[f"{name}_mae"]=float(np.mean(abs(e)));m[f"{name}_bias"]=float(np.mean(e))
  m["direction_accuracy"]=float(np.mean(np.sign(g.flow-g.persistence)==np.sign(g.actual-g.persistence)))
  for level in (50,80,90):
   z=g.dropna(subset=[f"cover{level}"]);m[f"coverage_{level}"]=float(z[f"cover{level}"].astype(bool).astype(float).mean());m[f"mean_width_{level}"]=float((z[f"hi{level}"]-z[f"lo{level}"]).mean());m[f"interval_score_{level}"]=float(z[f"score{level}"].mean())
  m["relative_rmse"]=m["flow_rmse"]/m["persistence_rmse"];metrics[str(h)]=m
 mean_short=float(np.mean([metrics[str(h)]["relative_rmse"] for h in (1,3,6)])); max_rel=max(v["relative_rmse"] for v in metrics.values()); cover_err=max(abs(metrics[str(h)][f"coverage_{l}"]-l/100) for h in HORIZONS for l in (50,80,90));passed=mean_short<=1 and max_rel<=1.15 and cover_err<=.15
 result={"clock":"monthly","state":"monthly log price change; pce_yoy is exact rolling sum of 12 monthly log changes","training_universe":"expanding origins using data available through each month; all dates <= 2019-12-31","evaluation":"2010-01 through 2019-12 within frozen pre-2020 universe","acceptance_predefined":ACCEPTANCE,"summary":{"mean_short_relative_rmse":mean_short,"max_relative_rmse":max_rel,"max_coverage_error":cover_err,"pass":passed},"horizons":metrics};(OUT/"r9_metrics.json").write_text(json.dumps(result,indent=2))
 fig,ax=plt.subplots(figsize=(6,4)); nominal=np.array([.5,.8,.9]);
 for h in HORIZONS: ax.plot(nominal,[metrics[str(h)][f"coverage_{x}"] for x in (50,80,90)],marker="o",label=f"{h}m")
 ax.plot([.45,.95],[.45,.95],color="#333",ls="--",label="ideal");ax.set(xlabel="Nominal coverage",ylabel="Empirical rolling coverage",title="Inflation interval calibration, 2010–2019");ax.legend(frameon=False);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIG/"r9_interval_calibration.png",dpi=160);plt.close(fig)
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
