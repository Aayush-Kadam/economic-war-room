"""Derive exact twelve-flow PCE initialization packets from downloaded ALFRED vintages."""
from __future__ import annotations
import csv,json,math
from datetime import date
from pathlib import Path
from fetch_official_data import GENERATED,MEETINGS
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/scenarios/fed_2022_pce_initialization.json"
def main(source=GENERATED):
    packets=[]
    for meeting,release in MEETINGS.items():
        path=source/"alfred"/f"PCEPI_{meeting}.csv";rows=list(csv.DictReader(path.open()))
        values=[(r["observation_date"],float(next(v for k,v in r.items() if k!="observation_date"))) for r in rows if next(v for k,v in r.items() if k!="observation_date") not in ("",".")]
        tail=values[-13:]
        if len(tail)!=13:raise ValueError(f"{meeting}: need 13 price levels, got {len(tail)}")
        flows=[100*math.log(tail[i][1]/tail[i-1][1]) for i in range(1,13)]
        packets.append({"meeting_id":meeting,"information_cutoff":meeting,"series_id":"PCEPI","source":"U.S. Bureau of Economic Analysis via ALFRED","source_url":"https://alfred.stlouisfed.org/series?seid=PCEPI","release_date":release,"vintage_date":meeting,"observation_period":tail[-1][0],"transformation":"100 * log(P_t / P_t-1); pce_yoy_log=sum(latest 12 flows)","monthly_observation_dates":[d for d,_ in tail[1:]],"monthly_price_changes":flows,"pce_yoy_log":sum(flows)})
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps({"schema_version":1,"packets":packets},indent=2),encoding="utf-8")
    for packet in packets:
        manifest=ROOT/"data/vintages"/f"fomc_{packet['meeting_id'].replace('-','_')}_manifest.json"
        current=json.loads(manifest.read_text(encoding="utf-8"));current["features"]=[f for f in current["features"] if f.get("series")!="PCEPI"]
        current["features"].insert(0,{"series":"PCEPI","observation_period":packet["observation_period"],"release_date":packet["release_date"],"vintage_date":packet["vintage_date"],"retrieval_date":date.today().isoformat(),"transformed_value":packet["pce_yoy_log"],"transformation":"sum of twelve vintage monthly 100*log price changes","source":packet["source"],"initialization_packet":"data/scenarios/fed_2022_pce_initialization.json"})
        manifest.write_text(json.dumps(current,indent=2)+"\n",encoding="utf-8")
    print(OUT)
if __name__=="__main__":main()
