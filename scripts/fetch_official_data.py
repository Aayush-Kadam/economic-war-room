"""Fetch current FRED data and keyless ALFRED as-of vintages from official endpoints."""
from __future__ import annotations
import argparse,io,json,urllib.parse,urllib.request,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; GENERATED=ROOT/"data/generated"
CURRENT=("PCEPI","DCOILWTICO","MICH")
MEETINGS={"2022-03-16":"2022-02-25","2022-05-04":"2022-04-29","2022-06-15":"2022-05-27","2022-07-27":"2022-06-30","2022-09-21":"2022-08-26","2022-11-02":"2022-10-28","2022-12-14":"2022-12-01"}

def get(url,data=None):
    req=urllib.request.Request(url,data=data,headers={"User-Agent":"Economic-War-Room-research-preview/0.9"})
    with urllib.request.urlopen(req,timeout=60) as r:return r.read()

def fetch_current(series): return get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}")

def fetch_vintage(series,vintage,start="2020-01-01"):
    fields={"form[units]":"lin","form[obs_start_date]":start,"form[obs_end_date]":vintage,"form[entered_vintage_dates]":vintage,"form[file_type]":"2","form[file_format]":"csv","form[download_data]":"Download data"}
    body=get(f"https://alfred.stlouisfed.org/series/downloaddata?seid={series}",urllib.parse.urlencode(fields).encode())
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        csv_name=next(n for n in z.namelist() if n.endswith(".csv"));return z.read(csv_name)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path,default=GENERATED);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    for series in CURRENT:(args.output/f"{series}_latest.csv").write_bytes(fetch_current(series))
    vintage_dir=args.output/"alfred";vintage_dir.mkdir(exist_ok=True)
    for meeting in MEETINGS:(vintage_dir/f"PCEPI_{meeting}.csv").write_bytes(fetch_vintage("PCEPI",meeting))
    manifest={"retrieval":"official FRED graph CSV and public ALFRED download form","series":list(CURRENT),"pce_vintages":MEETINGS,"raw_files":"generated locally and gitignored"}
    (args.output/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8");print(args.output)
if __name__=="__main__":main()
