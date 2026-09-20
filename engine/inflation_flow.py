"""Monthly price-change model with exact rolling derivation of year-over-year inflation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class FlowModel:
    intercept: float
    lag_coefficients: tuple[float,...]
    ridge: float = 0.2

def monthly_log_change(price_index):
    values=np.asarray(price_index,dtype=float)
    return 100*np.diff(np.log(values))

def yoy_from_monthly_log_changes(changes):
    x=np.asarray(changes,dtype=float)
    if len(x)<12: raise ValueError("twelve monthly changes are required")
    return float(np.sum(x[-12:]))

def fit_flow_model(changes,lags=12,ridge=.2):
    y=np.asarray(changes,dtype=float)
    if len(y)<=lags+12: raise ValueError("insufficient monthly history")
    X=np.array([[1,*y[t-lags:t][::-1]] for t in range(lags,len(y))]); z=y[lags:]
    penalty=np.diag([0]+[ridge]*lags); beta=np.linalg.solve(X.T@X+penalty,X.T@z)
    return FlowModel(float(beta[0]),tuple(map(float,beta[1:])),ridge)

def forecast_yoy(model,history,horizon):
    values=list(map(float,history)); lags=len(model.lag_coefficients)
    for _ in range(horizon): values.append(model.intercept+sum(b*values[-j-1] for j,b in enumerate(model.lag_coefficients)))
    return yoy_from_monthly_log_changes(values),values[-horizon:]
