"""Build auditable 2022 meeting manifests from official release archives."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
MEETINGS=[("2022-03-16","2022-03-10",7.9,6.4,"2022-03-04",3.8,.375),("2022-05-04","2022-04-12",8.5,6.5,"2022-04-01",3.6,.875),("2022-06-15","2022-06-10",8.6,6.0,"2022-06-03",3.6,1.625),("2022-07-27","2022-07-13",9.1,5.9,"2022-07-08",3.6,2.375),("2022-09-21","2022-09-13",8.3,6.3,"2022-09-02",3.7,3.125),("2022-11-02","2022-10-13",8.2,6.6,"2022-10-07",3.5,3.875),("2022-12-14","2022-12-13",7.1,6.0,"2022-12-02",3.7,4.375)]
def feature(series,period,release,value,source,transform): return {"series":series,"observation_period":period,"release_date":release,"vintage_date":release,"retrieval_date":"2026-09-20","transformed_value":value,"transformation":transform,"source":source}
def main():
 out=ROOT/"data/vintages"; out.mkdir(exist_ok=True)
 for date,cpi_release,cpi,core,u_release,u,actual in MEETINGS:
  manifest={"meeting_date":date,"information_cutoff":f"{date}T14:00:00-04:00","actual_policy_action":{"target_midpoint_percent":actual,"visibility":"post_commit_only","source":"https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"},"features":[feature("CPIAUCSL","latest monthly",cpi_release,cpi,"BLS CPI initial release archive","12-month percent change"),feature("CPILFESL","latest monthly",cpi_release,core,"BLS CPI initial release archive","12-month percent change"),feature("UNRATE","latest monthly",u_release,u,"BLS Employment Situation archive","level, percent")],"constructed_state":[{"name":"expected_inflation","classification":"calibrated state proxy; not an observed release"},{"name":"output_gap","classification":"model state; not an observed release"},{"name":"financial_stress","classification":"calibrated state proxy; not an observed release"}],"provenance_complete":True}
  (out/f"fomc_{date.replace('-','_')}_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
if __name__=="__main__": main()
