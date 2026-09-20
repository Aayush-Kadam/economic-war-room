import random
import pytest
from engine.model import MacroState
from engine.policy_rules import RULES
S=MacroState(4,3,2.5,1,4,2)
@pytest.mark.parametrize("name",list(RULES))
def test_rule_bounds(name): assert 0<=RULES[name](S,2,0,random.Random(1))<=10
def test_inflation_rule_more_hawkish(): assert RULES["inflation_focused"](S,2,0)>RULES["dual_mandate"](S,2,0)
def test_smoothing_limits_jump(): assert abs(RULES["smoothing"](S,2,0)-2)<abs(RULES["taylor"](S,2,0)-2)
def test_random_rule_reproducible(): assert RULES["random"](S,2,0,random.Random(7))==RULES["random"](S,2,0,random.Random(7))
