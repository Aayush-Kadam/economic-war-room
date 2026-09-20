import hashlib,json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_checksum():
 m=json.loads((ROOT/"calibration/FROZEN_SAMPLE_MANIFEST.json").read_text()); p=ROOT/m["dataset"]["path"]; assert hashlib.sha256(p.read_bytes()).hexdigest()==m["dataset"]["sha256"]
def test_cutoff_precedes_scenario():
 d=pd.read_csv(ROOT/"calibration/frozen/us_macro_1990q1_2019q4.csv"); assert d.quarter.max()[:10]<"2021-01-01"
def test_expected_grain_and_rows():
 d=pd.read_csv(ROOT/"calibration/frozen/us_macro_1990q1_2019q4.csv"); assert len(d)==120 and d.quarter.is_unique
def test_required_series_provenance():
 m=json.loads((ROOT/"calibration/FROZEN_SAMPLE_MANIFEST.json").read_text()); assert len(m["sources"])==10 and all(x["sha256"] and x["url"].startswith("https://fred.stlouisfed.org") for x in m["sources"])
