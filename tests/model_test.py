import math
from engine import MacroState,Policy,simulate
from data.providers.alfred import information_set
S=MacroState(8.0,6.2,3.0,1.0,3.6,.5)
def test_seed_reproducibility(): assert simulate(S,Policy(3),seed=7,paths=20)==simulate(S,Policy(3),seed=7,paths=20)
def test_restrictive_policy_direction():
    loose=simulate(S,Policy(1),seed=8,paths=1000)[-1]; tight=simulate(S,Policy(5),seed=8,paths=1000)[-1]
    assert tight["inflation"]["p50"]<loose["inflation"]["p50"]
    assert tight["output_gap"]["p50"]<loose["output_gap"]["p50"]
    assert tight["unemployment"]["p50"]>loose["unemployment"]["p50"]
def test_no_lookahead():
    rows=[{"series_id":"X","observation_date":"2022-04-01","release_date":"2022-05-01","value":1,"source":"official"},{"series_id":"X","observation_date":"2022-05-01","release_date":"2022-06-20","value":2,"source":"official"}]
    packet=information_set(rows,"2022-06-15"); assert len(packet)==1 and packet[0]["value"]==1
def test_numerical_stability():
    result=simulate(S,Policy(10),seed=9,paths=50,horizon=20)
    assert all(math.isfinite(x["inflation"]["p50"]) and 2.5<=x["unemployment"]["p50"]<=12 for x in result)
