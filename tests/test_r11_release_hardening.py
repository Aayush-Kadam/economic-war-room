import json,math
from pathlib import Path
import pytest
from scripts.fetch_official_data import fetch_vintage

ROOT=Path(__file__).resolve().parents[1]
PACKETS=json.loads((ROOT/"data/scenarios/fed_2022_pce_initialization.json").read_text())["packets"]

def test_all_seven_meetings_have_pce_packets(): assert len(PACKETS)==7

@pytest.mark.parametrize("packet",PACKETS,ids=lambda p:p["meeting_id"])
def test_exact_twelve_flow_identity(packet):
    assert packet["series_id"]=="PCEPI"
    assert len(packet["monthly_price_changes"])==12
    assert sum(packet["monthly_price_changes"])==pytest.approx(packet["pce_yoy_log"],abs=1e-12)
    assert len(set(round(x,10) for x in packet["monthly_price_changes"]))>1

def test_ui_never_passes_cpi_to_pce_engine():
    page=(ROOT/"app/page.tsx").read_text(encoding="utf-8")
    assert "monthlyPriceChanges:pce.monthly_price_changes" in page
    assert "inflation:m.inflation" not in page
    assert 'label="HEADLINE CPI"' in page and 'label="HEADLINE PCE"' in page

def test_historical_runtime_has_no_equal_flow_fallback():
    core=(ROOT/"lib/unified-core.mjs").read_text(encoding="utf-8")
    assert "Array(12).fill" not in core
    assert "require exactly 12 monthly PCE flows" in core

def test_every_manifest_references_exact_initialization():
    for packet in PACKETS:
        p=ROOT/"data/vintages"/f"fomc_{packet['meeting_id'].replace('-','_')}_manifest.json"
        features=json.loads(p.read_text())["features"];pce=[x for x in features if x["series"]=="PCEPI"]
        assert len(pce)==1 and pce[0]["vintage_date"]==packet["meeting_id"]

def test_public_tree_does_not_bundle_generated_raw_data(): assert not (ROOT/"data/generated").is_relative_to(ROOT) or "data/generated/" in (ROOT/".gitignore").read_text().replace("\\","/")

def test_retrieval_script_rejects_invalid_vintage(monkeypatch):
    monkeypatch.setattr("scripts.fetch_official_data.get",lambda *a,**k:b"not a zip")
    with pytest.raises(Exception):fetch_vintage("PCEPI","not-a-date")

def test_uncertainty_gate_is_predeclared_and_no_lookahead():
    source=(ROOT/"r11/run_uncertainty_repair.py").read_text()
    assert 'origin+h months must be <= current origin' in json.loads((ROOT/"r11/results/uncertainty_metrics.json").read_text())["predeclared"]["observable_error_rule"]
    assert "known<=origin" in source

def test_adaptive_intervals_are_reproducible():
    result=json.loads((ROOT/"r11/results/uncertainty_metrics.json").read_text())
    assert result["selected"]=="ew_abs"
    assert result["gate_results"]["pass"] is False

def test_no_private_absolute_paths_in_tracked_release_sources():
    for rel in ("README.md","PROJECT_STATUS.md","docs/CLEAN_CLONE_REPRODUCTION.md"):
        p=ROOT/rel
        if p.exists():assert "C:\\Users\\" not in p.read_text(encoding="utf-8")
