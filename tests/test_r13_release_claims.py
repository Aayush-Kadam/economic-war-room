from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_ui_removes_probability_interval_overclaims():
    page = (ROOT / "app/page.tsx").read_text(encoding="utf-8")
    for forbidden in ("80% SIMULATED INTERVAL", "MODEL DISTRIBUTION", "forecast fan chart", "recession probability"):
        assert forbidden not in page
    assert "SIMULATION DISPERSION" in page
    assert "not a calibrated probability interval" in page


def test_results_separate_observed_and_counterfactual_content():
    page = (ROOT / "app/page.tsx").read_text(encoding="utf-8")
    assert "OBSERVED HISTORY vs MODEL-GENERATED COUNTERFACTUAL" in page
    assert "Observed FOMC history" in page
    assert "Model-generated policy path" in page


def test_scientific_contract_excludes_unsupported_claims():
    contract = (ROOT / "docs/V0_9_SCIENTIFIC_CONTRACT.md").read_text(encoding="utf-8")
    for phrase in ("structural causal identification", "calibrated predictive intervals", "real-world recession", "research-grade"):
        assert phrase in contract


def test_public_package_tracks_no_generated_raw_data():
    tracked = subprocess.check_output(["git", "ls-files", "data/generated", "calibration/frozen"], cwd=ROOT, text=True)
    assert tracked.strip() == ""


def test_negative_uncertainty_evidence_is_preserved():
    required = (
        "r11/results/uncertainty_metrics.json",
        "r12/R12_UNCERTAINTY_PROTOCOL.md",
        "r12/results/r12_uncertainty_metrics.json",
        "reports/R12_FINAL_UNCERTAINTY_AUDIT.md",
        "reports/UNCERTAINTY_VALIDATION_STATUS.md",
    )
    assert all((ROOT / path).is_file() for path in required)
