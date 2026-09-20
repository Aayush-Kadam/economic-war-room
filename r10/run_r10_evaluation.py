"""Predeclared model selection and untouched post-2019 stress evaluation."""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from engine.inflation_flow import monthly_log_change
OUT=ROOT/"r10/results";OUT.mkdir(parents=True,exist_ok=True)
H=(1,3,6,12); RIDGE=.2

def load():
 p=pd.read_csv(ROOT/"work/PCEPI_latest.csv",parse_dates=[0],index_col=0).iloc[:,0].rename("price")
 oil=pd.read_csv(ROOT/"work/DCOILWTICO_latest.csv",parse_dates=[0],index_col=0,na_values=".").iloc[:,0].resample("MS").mean().rename("oil")
 mich=pd.read_csv(ROOT/"work/MICH_latest.csv",parse_dates=[0],index_col=0,na_values=".").iloc[:,0].rename("mich")
 d=pd.concat([p,oil,mich],axis=1);d["flow"]=pd.Series(monthly_log_change(p),index=p.index[1:]);d["oil12"]=100*np.log(d.oil/d.oil.shift(12));d["yoy"]=100*np.log(d.price/d.price.shift(12));return d
def fit_predict(d,origin,h,kind):
 lags=12; train=d.iloc[:origin+1].copy(); cols=[]
 for j in range(1,lags+1): train[f"l{j}"]=train.flow.shift(j);cols.append(f"l{j}")
 if kind=="energy": cols+=["oil12"]
 if kind=="expectations": cols+=["oil12","mich"]
 clean=train.dropna(subset=["flow",*cols]);X=np.c_[np.ones(len(clean)),clean[cols]];y=clean.flow.to_numpy();pen=np.diag([0]+[RIDGE]*(X.shape[1]-1));b=np.linalg.solve(X.T@X+pen,X.T@y)
 hist=list(d.flow.iloc[1:origin+1].astype(float));last=train.iloc[-1]
 for _ in range(h):
  x=[1,*hist[-lags:][::-1]]
  if kind=="energy":x += [float(last.oil12)]
  if kind=="expectations":x += [float(last.oil12),float(last.mich)]
  hist.append(float(np.dot(x,b)))
 return sum(hist[-12:])
def ar(y,origin,h,lags):
 z=list(y[:origin+1]);
 for _ in range(h):
  a=np.asarray(z);X=np.array([[1,*a[t-lags:t][::-1]] for t in range(lags,len(a))]);b=np.linalg.solve(X.T@X+np.diag([0]+[.01]*lags),X.T@a[lags:]);z.append(float(np.dot([1,*z[-lags:][::-1]],b)))
 return z[-1]
def rows_for(d,start,end,models):
 rows=[];y=d.yoy.to_numpy()
 for origin in range(d.index.get_loc(start),d.index.get_loc(end)+1):
  if origin+12>=len(d):break
  for h in H:
   actual=float(d.yoy.iloc[origin+h]);row={"origin":str(d.index[origin].date()),"horizon":h,"actual":actual,"persistence":float(d.yoy.iloc[origin]),"ar1":ar(y[12:],origin-12,h,1),"ar4":ar(y[12:],origin-12,h,4)}
   for m in models:row[m]=fit_predict(d,origin,h,m)
   rows.append(row)
 return pd.DataFrame(rows)
def metrics(frame,names):
 out={}
 for h,g in frame.groupby("horizon"):
  out[str(h)]={}
  for n in names:
   e=g[n]-g.actual;out[str(h)][n]={"rmse":float(np.sqrt(np.mean(e*e))),"mae":float(np.mean(abs(e))),"bias":float(np.mean(e))}
 return out
def main():
 d=load().dropna(subset=["price"]);models=["core","energy","expectations"]
 selection=rows_for(d,"2010-01-01","2015-12-01",models);sm=metrics(selection,[*models,"persistence","ar1","ar4"])
 score={m:float(np.mean([sm[str(h)][m]["rmse"] for h in H])) for m in models};best=min(score,key=score.get)
 # Richer models require >=1% mean-RMSE improvement over the parsimonious core.
 selected=best if best=="core" or score[best]<=.99*score["core"] else "core"
 historical=rows_for(d,"2016-01-01","2018-12-01",models);post=rows_for(d,"2020-01-01",str(d.index[-13].date()),[selected]);normal=post[pd.to_datetime(post.origin)>=pd.Timestamp("2022-01-01")]
 hm=metrics(historical,[selected,"persistence","ar1","ar4"]);pm=metrics(post,[selected,"persistence","ar1","ar4"]);nm=metrics(normal,[selected,"persistence","ar1","ar4"])
 # Fixed pre-2020 residual calibration; post-period outcomes never tune widths.
 for h in H:
  cal=historical[historical.horizon==h];errs=(cal.actual-cal[selected]).to_numpy()
  for target in (50,80,90):
   a=1-target/100;lo,hi=np.quantile(errs,[a/2,1-a/2]);g=post[post.horizon==h];pm[str(h)][selected][f"coverage_{target}"]=float(((g[selected]+lo<=g.actual)&(g.actual<=g[selected]+hi)).mean());pm[str(h)][selected][f"width_{target}"]=float(hi-lo)
 result={"predeclared_selection":{"selection_window":"2010-01 through 2015-12","criterion":"lowest mean 1/3/6/12-month RMSE; added regressors need >=1% improvement","scores":score,"selected":selected},"historical_test":{"window":"2016-01 through 2019-12 (origins end 2018-12 for complete 12m outcomes)","metrics":hm},"post_2019_stress":{"window":f"2020-01 through {post.origin.max()}","metrics":pm},"post_emergency":{"window":f"2022-01 through {normal.origin.max()}","metrics":nm},"data_as_of":str(d.index[-1].date()),"source":"FRED PCEPI, DCOILWTICO, MICH downloaded 2026-09-20"}
 selection.to_csv(OUT/"model_selection.csv",index=False);historical.to_csv(OUT/"historical_test.csv",index=False);post.to_csv(OUT/"post_2019_stress.csv",index=False);(OUT/"r10_metrics.json").write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=="__main__":main()
