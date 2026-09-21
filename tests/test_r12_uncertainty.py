from __future__ import annotations

import pandas as pd
import pytest

from r12.run_r12_uncertainty import conformal_quantile, eligible_errors, interval_score


def test_horizon_error_is_unavailable_until_target_realizes():
    frame = pd.DataFrame(
        {
            "origin": pd.to_datetime(["2025-01-01", "2025-02-01"]),
            "target": pd.to_datetime(["2026-01-01", "2026-02-01"]),
            "horizon": [12, 12],
            "actual": [3.0, 4.0],
            "core": [2.0, 2.0],
        }
    )
    assert eligible_errors(frame, pd.Timestamp("2025-12-01"), 12).empty
    assert len(eligible_errors(frame, pd.Timestamp("2026-01-01"), 12)) == 1


def test_conformal_quantile_uses_predeclared_finite_sample_rank():
    assert conformal_quantile([1, 2, 3, 4], 80) == 4


def test_interval_score_penalizes_misses():
    assert interval_score(5, 1, 4, 80) > interval_score(3, 1, 4, 80)


def test_protocol_records_opened_stress_window():
    text = open("r12/R12_UNCERTAINTY_PROTOCOL.md", encoding="utf-8").read()
    assert "2023–2025 window was opened" in text
    assert "diagnostic evidence only" in text
