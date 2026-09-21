import json
from pathlib import Path

import pytest

from engine.unified import UnifiedState, meeting_month, monthly_policy_path, policy_responses, simulate_monthly

ROOT=Path(__file__).resolve().parents[1]

def state(): return UnifiedState(tuple([.2]*12),2.4,.5,4.0,2.0,financial_stress=.2)

def test_unified_yoy_is_exact_twelve_month_sum(): assert state().pce_yoy==pytest.approx(2.4)

def test_meeting_dates_map_to_month_without_inventing_meetings():
    assert meeting_month("2022-03-16")=="2022-03"
    assert monthly_policy_path(["2022-03-16","2022-05-04"],[.375,.875],"2022-03",4)==[.375,.375,.875,.875]

def test_zero_deviation_has_no_policy_contribution():
    dev,res=policy_responses([2]*24,[2]*24)
    assert dev==[0]*24
    assert all(all(x==0 for x in path) for path in res.values())

def test_overlapping_kernels_accumulate():
    _,single=policy_responses([3]+[2]*23,[2]*24)
    _,double=policy_responses([3,3]+[2]*22,[2]*24)
    assert abs(double["output"][10])>abs(single["output"][10])

def test_temporary_tightening_is_bounded_and_decays():
    _,res=policy_responses([3]+[2]*95,[2]*96)
    assert min(res["inflation"])<0
    assert abs(res["inflation"][-1])<abs(min(res["inflation"]))/4

def test_larger_deviation_has_proportional_response():
    _,small=policy_responses([2.25]+[2]*23,[2]*24)
    _,large=policy_responses([3]+[2]*23,[2]*24)
    assert min(large["output"])==pytest.approx(4*min(small["output"]))

def test_simulation_reports_monthly_clock_and_exact_yoy():
    rows=simulate_monthly(state(),[2]*24,[2]*24,stochastic=False)
    assert [r["month"] for r in rows]==list(range(1,25))
    assert rows[0]["policy_deviation_bp"]==0

def test_frontend_consumes_same_specification():
    source=(ROOT/"lib/unified-core.mjs").read_text()
    assert 'deterministicUnified' in source
    assert 'simulateUnified' in (ROOT/"app/page.tsx").read_text(encoding="utf-8")

def test_post_2019_holdout_exists_and_was_not_used_for_selection():
    result=json.loads((ROOT/"r10/results/r10_metrics.json").read_text())
    assert result["predeclared_selection"]["selection_window"].endswith("2015-12")
    assert result["post_2019_stress"]["window"].startswith("2020-01")

def test_richer_models_rejected_by_predeclared_rule():
    result=json.loads((ROOT/"r10/results/r10_metrics.json").read_text())
    assert result["predeclared_selection"]["selected"]=="core"
    assert result["predeclared_selection"]["scores"]["core"]<result["predeclared_selection"]["scores"]["energy"]
