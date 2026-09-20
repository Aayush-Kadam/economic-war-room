from __future__ import annotations
import random
from .model import MacroState
RATE_MIN,RATE_MAX=0.0,10.0
def bounded(x): return max(RATE_MIN,min(RATE_MAX,x))
def _inertial(previous,target,rho=.93,max_move=1.25):
    desired=rho*previous+(1-rho)*target
    return bounded(previous+max(-max_move,min(max_move,desired-previous)))
def historical(s,previous,step,rng=None): return [0.375,.875,1.625,2.375,3.125,3.875,4.375][step]
def taylor(s,previous,step,rng=None): return _inertial(previous,2.5+1.5*(s.inflation-2)+.5*s.output_gap,rho=.93)
def inflation_focused(s,previous,step,rng=None): return _inertial(previous,2.5+1.75*(s.inflation-2)+.15*s.output_gap,rho=.93)
def dual_mandate(s,previous,step,rng=None): return _inertial(previous,2.5+1.0*(s.inflation-2)+.75*s.output_gap,rho=.92)
def smoothing(s,previous,step,rng=None): return _inertial(previous,2.5+1.5*(s.inflation-2)+.5*s.output_gap,rho=.96,max_move=.5)
def hold(s,previous,step,rng=None): return previous
def random_rule(s,previous,step,rng=None): return bounded(previous+(rng or random.Random(0)).choice([-.5,-.25,0,.25,.5,.75]))
RULES={"historical":historical,"taylor":taylor,"inflation_focused":inflation_focused,"dual_mandate":dual_mandate,"smoothing":smoothing,"hold":hold,"random":random_rule}
