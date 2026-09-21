"""Nested real-time comparison of fixed and adaptive residual intervals."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];R10=ROOT/"r10/results";OUT=ROOT/"r11/results";OUT.mkdir(parents=True,exist_ok=True)
LEVELS=(50,80,90);H=(1,3,6,12)
GATE={"minimum_90_coverage_each_horizon":.70,"minimum_mean_interval_score_improvement":.10,"maximum_mean_width_ratio":2.5}
def score(y,lo,hi,level):
 a=1-level/100;return (hi-lo)+(2/a)*(lo-y if y<lo else y-hi if y>hi else 0)
def weighted_quantile(x,q,w):
 order=np.argsort(x);x=np.asarray(x)[order];w=np.asarray(w)[order];return float(x[np.searchsorted(np.cumsum(w)/sum(w),q,side="left")])
def bounds(errors,level,method):
 a=1-level/100;e=np.asarray(errors,dtype=float)
 if method=="fixed": use=e[:36]
 elif method=="rolling_signed_36":use=e[-36:]
 elif method=="rolling_abs_36":
  q=float(np.quantile(abs(e[-36:]),level/100));return -q,q
 elif method=="ew_abs":
  use=abs(e);w=.95**np.arange(len(use)-1,-1,-1);q=weighted_quantile(use,level/100,w);return -q,q
 else:raise ValueError(method)
 return tuple(map(float,np.quantile(use,[a/2,1-a/2])))
def evaluate(frame,calibration,method,start,end):
 rows=[]
 for h in H:
  base=calibration[calibration.horizon==h].copy();g=frame[(frame.horizon==h)&(frame.origin>=start)&(frame.origin<=end)].copy()
  history=[(pd.Timestamp(r.origin)+pd.DateOffset(months=h),r.actual-r.core) for r in base.itertuples()]
  for r in g.itertuples():
   origin=pd.Timestamp(r.origin);available=[e for known,e in history if known<=origin]
   if len(available)<24:continue
   row={"origin":r.origin,"horizon":h,"actual":r.actual,"prediction":r.core,"method":method}
   for level in LEVELS:
    lo,hi=bounds(available,level,method);row[f"lo{level}"]=r.core+lo;row[f"hi{level}"]=r.core+hi;row[f"cover{level}"]=row[f"lo{level}"]<=r.actual<=row[f"hi{level}"];row[f"score{level}"]=score(r.actual,row[f"lo{level}"],row[f"hi{level}"],level)
   rows.append(row);history.append((origin+pd.DateOffset(months=h),r.actual-r.core))
 return pd.DataFrame(rows)
def summarize(d):
 out={}
 for h,g in d.groupby("horizon"):
  out[str(h)]={}
  for level in LEVELS:out[str(h)][str(level)]={"coverage":float(g[f"cover{level}"].mean()),"mean_width":float((g[f"hi{level}"]-g[f"lo{level}"]).mean()),"interval_score":float(g[f"score{level}"].mean())}
 return out
def aggregate(summary,key):return float(np.mean([summary[str(h)][str(l)][key] for h in H for l in LEVELS]))
def main():
 hist=pd.read_csv(R10/"historical_test.csv",parse_dates=["origin"]);post=pd.read_csv(R10/"post_2019_stress.csv",parse_dates=["origin"])
 methods=("rolling_signed_36","rolling_abs_36","ew_abs");selection={}
 for m in methods:
  s=summarize(evaluate(post,hist,m,pd.Timestamp("2020-01-01"),pd.Timestamp("2022-12-01")));selection[m]={"mean_interval_score":aggregate(s,"interval_score"),"mean_absolute_coverage_error":float(np.mean([abs(s[str(h)][str(l)]["coverage"]-l/100) for h in H for l in LEVELS]))}
 selected=min(methods,key=lambda m:selection[m]["mean_interval_score"]+selection[m]["mean_absolute_coverage_error"])
 final={};frames=[]
 for m in ("fixed",selected):
  d=evaluate(post,hist,m,pd.Timestamp("2023-01-01"),post.origin.max());frames.append(d);final[m]=summarize(d)
 fixed,adaptive=final["fixed"],final[selected];improvement=1-aggregate(adaptive,"interval_score")/aggregate(fixed,"interval_score");width_ratio=aggregate(adaptive,"mean_width")/aggregate(fixed,"mean_width");min90=min(adaptive[str(h)]["90"]["coverage"] for h in H);passed=min90>=GATE["minimum_90_coverage_each_horizon"] and improvement>=GATE["minimum_mean_interval_score_improvement"] and width_ratio<=GATE["maximum_mean_width_ratio"]
 result={"predeclared":{"selection_window":"2020-01 through 2022-12","untouched_final_window":f"2023-01 through {post.origin.max().date()}","observable_error_rule":"origin+h months must be <= current origin","gate":GATE},"selection":selection,"selected":selected,"final":final,"gate_results":{"minimum_90_coverage":min90,"mean_interval_score_improvement":improvement,"mean_width_ratio":width_ratio,"pass":passed}}
 pd.concat(frames).to_csv(OUT/"uncertainty_predictions.csv",index=False);(OUT/"uncertainty_metrics.json").write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=="__main__":main()
