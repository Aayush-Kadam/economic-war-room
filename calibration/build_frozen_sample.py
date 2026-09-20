"""Build the immutable pre-pandemic U.S. estimation sample from official FRED series.

No scenario-period observation enters this file: the hard cutoff is 2019-12-31.
FRED graph downloads are public, official, and intentionally use latest-revised
pre-cutoff history. Real-time meeting packets are handled separately.
"""
from __future__ import annotations
import hashlib, json, platform, subprocess
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"calibration"/"frozen"
START="1990-01-01"; CUTOFF="2019-12-31"
SERIES={
 "PCEPI":("PCE price index","quarterly last; annualized log difference"),
 "PCEPILFE":("Core PCE price index","quarterly last; annualized log difference"),
 "GDPC1":("Real gross domestic product","quarterly; log growth"),
 "GDPPOT":("CBO real potential GDP","quarterly; output gap"),
 "UNRATE":("Civilian unemployment rate","quarterly mean"),
 "FEDFUNDS":("Effective federal funds rate","quarterly mean"),
 "MICH":("University of Michigan expected inflation","quarterly mean"),
 "NFCI":("Chicago Fed National Financial Conditions Index","quarterly mean"),
 "TOTALSL":("Total consumer credit owned and securitized","quarterly last; annualized log growth"),
 "DCOILWTICO":("WTI crude oil price","quarterly mean; annualized log difference")}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def fred(series):
    url=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={START}&coed={CUTOFF}"
    d=pd.read_csv(url); d.columns=["date",series]; d["date"]=pd.to_datetime(d.date); d[series]=pd.to_numeric(d[series],errors="coerce")
    return d.set_index("date")[series],url
def qmean(s): return s.resample("QE").mean()
def qlast(s): return s.resample("QE").last()
def annualized_log(s):
    import numpy as np
    return 400*np.log(s).diff()
def main():
    import numpy as np
    OUT.mkdir(parents=True,exist_ok=True); raw=OUT/"raw"; raw.mkdir(exist_ok=True)
    series={}; sources=[]
    for sid,(name,transform) in SERIES.items():
        s,url=fred(sid); p=raw/f"{sid}.csv"; s.rename(sid).to_csv(p)
        sources.append({"series_id":sid,"name":name,"url":url,"range":[str(s.index.min().date()),str(s.index.max().date())],"raw_rows":int(len(s)),"raw_nulls":int(s.isna().sum()),"transformation":transform,"sha256":sha(p)})
        series[sid]=s
    q=pd.DataFrame(index=pd.date_range("1990-03-31","2019-12-31",freq="QE"))
    q["headline_inflation"]=annualized_log(qlast(series["PCEPI"]))
    q["core_inflation"]=annualized_log(qlast(series["PCEPILFE"]))
    q["gdp_growth"]=annualized_log(qlast(series["GDPC1"]))
    q["output_gap"]=100*(qlast(series["GDPC1"])/qlast(series["GDPPOT"])-1)
    q["unemployment"]=qmean(series["UNRATE"]); q["policy_rate"]=qmean(series["FEDFUNDS"])
    q["expected_inflation"]=qmean(series["MICH"]); q["financial_conditions"]=qmean(series["NFCI"])
    q["credit_growth"]=annualized_log(qlast(series["TOTALSL"])); q["energy_inflation"]=annualized_log(qmean(series["DCOILWTICO"]))
    q["real_policy_rate"]=q.policy_rate-q.expected_inflation
    q.index.name="quarter"; dataset=OUT/"us_macro_1990q1_2019q4.csv"; q.round(8).to_csv(dataset)
    manifest={"title":"Economic War Room frozen U.S. estimation sample","retrieved_at_utc":datetime.now(timezone.utc).isoformat(),"observation_range":[START,CUTOFF],"estimation_sample":["1991Q2","2019Q4"],"cutoff_rationale":"2019Q4 is the last pre-pandemic quarter and precedes the 2021-23 evaluation episode; it was fixed before estimation and not chosen for fit.","frequency":"quarterly","missing_data":"Equation-specific complete-case rows after lag construction; no imputation.","revision_policy":"Latest-revised official history is accepted for coefficient estimation; real-time evaluation packets use meeting-date availability separately.","dataset":{"path":str(dataset.relative_to(ROOT)).replace('\\','/'),"rows":int(len(q)),"columns":list(q.columns),"sha256":sha(dataset)},"sources":sources,"software":{"python":platform.python_version(),"pandas":pd.__version__,"numpy":np.__version__},"code_version":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()}
    (ROOT/"calibration"/"FROZEN_SAMPLE_MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps({"rows":len(q),"complete_rows":int(q.dropna().shape[0]),"sha256":manifest["dataset"]["sha256"]},indent=2))
if __name__=="__main__": main()
