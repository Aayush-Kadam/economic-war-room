"""Small, auditable ALFRED adapter. An API key is read from FRED_API_KEY; never stored."""
from __future__ import annotations
import json, os
from urllib.parse import urlencode
from urllib.request import urlopen

BASE="https://api.stlouisfed.org/fred/series/observations"
def observations(series_id:str, vintage_date:str, start:str="1900-01-01"):
    key=os.environ.get("FRED_API_KEY")
    if not key: raise RuntimeError("FRED_API_KEY is required; use .env.example")
    query=urlencode({"series_id":series_id,"api_key":key,"file_type":"json","vintage_dates":vintage_date,"observation_start":start})
    with urlopen(f"{BASE}?{query}",timeout=30) as response: payload=json.load(response)
    return [{"series_id":series_id,"observation_date":x["date"],"value":None if x["value"]=="." else float(x["value"]),"vintage_date":vintage_date,"source":"Federal Reserve Bank of St. Louis ALFRED"} for x in payload["observations"]]

def information_set(records:list[dict], cutoff:str):
    required={"series_id","observation_date","release_date","value","source"}
    for r in records:
        missing=required-r.keys()
        if missing: raise ValueError(f"missing metadata: {sorted(missing)}")
    return [r for r in records if r["release_date"]<=cutoff]
