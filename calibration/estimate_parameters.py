"""Transparent equation-by-equation OLS with expanding-window validation."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def ols(y,X,names):
    X=np.column_stack([np.ones(len(X)),X]); inv=np.linalg.pinv(X.T@X); b=inv@X.T@y; e=y-X@b; n,k=X.shape; s2=float(e@e/max(1,n-k)); se=np.sqrt(np.diag(inv)*s2); pred=X@b
    return {"n":n,"r2":float(1-(e@e)/((y-y.mean())@(y-y.mean()))),"rmse":float(np.sqrt(np.mean(e**2))),"coefficients":dict(zip(["intercept"]+names,map(float,b))),"std_errors":dict(zip(["intercept"]+names,map(float,se))),"residuals":e.tolist(),"predicted":pred.tolist()}
def fit(df,y,features):
    d=df[[y]+features].dropna(); return ols(d[y].to_numpy(),d[features].to_numpy(),features),d
def rolling_rmse(df,y,features,start=60):
    errors=[]
    for i in range(start,len(df)):
        train=df.iloc[:i][[y]+features].dropna(); row=df.iloc[[i]][[y]+features].dropna()
        if len(train)<30 or row.empty: continue
        m=ols(train[y].to_numpy(),train[features].to_numpy(),features); b=m["coefficients"]; errors.append(float(row[y].iloc[0]-(b["intercept"]+sum(b[f]*row[f].iloc[0] for f in features))))
    return float(np.sqrt(np.mean(np.square(errors)))),len(errors)
def main():
    df=pd.read_csv(ROOT/"calibration/frozen/us_macro_1990q1_2019q4.csv",parse_dates=["quarter"]).set_index("quarter")
    df["core_l1"]=df.core_inflation.shift(1); df["gap_l1"]=df.output_gap.shift(1); df["u_l1"]=df.unemployment.shift(1); df["du"]=df.unemployment.diff(); df["dgap"]=df.output_gap.diff(); df["real_rate_l1"]=df.real_policy_rate.shift(1); df["real_rate_l2"]=df.real_policy_rate.shift(2); df["real_rate_l3"]=df.real_policy_rate.shift(3); df["credit_l1"]=df.credit_growth.shift(1); df["nfci_l1"]=df.financial_conditions.shift(1)
    specs={
      "inflation":{"y":"core_inflation","x":["core_l1","expected_inflation","gap_l1","energy_inflation"]},
      "output":{"y":"output_gap","x":["gap_l1","real_rate_l1","real_rate_l2","real_rate_l3","financial_conditions"]},
      "okun":{"y":"du","x":["u_l1","dgap"]},
      "credit":{"y":"credit_growth","x":["credit_l1","real_rate_l1","nfci_l1"]}}
    out={"sample_cutoff":"2019-12-31","estimator":"OLS with Moore-Penrose inverse; heteroskedasticity is not corrected in v1","equations":{}}
    for name,s in specs.items():
        model,d=fit(df,s["y"],s["x"]); model["oos_rmse"],model["oos_n"]=rolling_rmse(df,s["y"],s["x"]); model["features"]=s["x"]; model["sample"]=[str(d.index.min().date()),str(d.index.max().date())]; out["equations"][name]=model
    p=ROOT/"calibration/estimated_parameters.json"; p.write_text(json.dumps(out,indent=2),encoding="utf-8"); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
