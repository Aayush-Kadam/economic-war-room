import csv,json,math
from pathlib import Path
from engine.model import MacroState,Policy,simulate
ROOT=Path(__file__).resolve().parents[1]
def test_all_seven_manifests_exist(): assert len(list((ROOT/"data/vintages").glob("fomc_2022_*_manifest.json")))==7
def test_actual_actions_post_commit_only():
 for p in (ROOT/"data/vintages").glob("fomc_2022_*_manifest.json"): assert json.loads(p.read_text())["actual_policy_action"]["visibility"]=="post_commit_only"
def test_parameter_registry_classifies_every_parameter(): assert all(p["classification"] for p in json.loads((ROOT/"calibration/parameter_registry.json").read_text())["parameters"])
def test_replay_evidence_is_finite():
 m=json.loads((ROOT/"research/results/historical_replay.json").read_text())["metrics"]; assert all(math.isfinite(v) for v in m.values())
def test_frontier_has_two_thousand_paths():
 with (ROOT/"research/results/policy_frontier.csv").open() as f: assert sum(1 for _ in csv.DictReader(f))==2000
def test_tournament_common_replication_count():
 with (ROOT/"research/results/policy_tournament.csv").open() as f: rows=list(csv.DictReader(f)); assert len(rows)==700 and {sum(r["rule"]==name for r in rows) for name in set(r["rule"] for r in rows)}=={100}
def test_parameter_uncertainty_reproducible():
 s=MacroState(4,3,2.5,0,4,2); assert simulate(s,Policy(3),seed=3,paths=20,parameter_uncertainty=True)==simulate(s,Policy(3),seed=3,paths=20,parameter_uncertainty=True)
def test_fat_tail_mode_finite():
 s=MacroState(4,3,2.5,0,4,2); r=simulate(s,Policy(3),seed=4,paths=50,shock_distribution="student_t"); assert all(math.isfinite(x["inflation"]["p50"]) for x in r)
def test_replay_report_admits_failure(): assert "NEEDS REVISION" in (ROOT/"reports/HISTORICAL_REPLAY_VALIDATION.md").read_text()
def test_secondary_scenarios_are_experimental():
 for p in (ROOT/"scenarios/fed_2008/scenario.json",ROOT/"scenarios/rbi_2022/scenario.json"): assert json.loads(p.read_text())["status"]=="experimental"
