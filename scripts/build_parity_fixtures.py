"""Create deterministic cross-runtime fixtures from the canonical Python engine."""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from engine.unified import UnifiedState,simulate_monthly
packets=json.loads((ROOT/"data/scenarios/fed_2022_pce_initialization.json").read_text())["packets"]
flows=packets[0]["monthly_price_changes"];months=36;base=[2.0]*months
cases={"A_baseline":base,"B_25bp_temporary":[2.25]+base[1:],"C_repeated_50bp":[2.5]*6+base[6:],"D_return_to_baseline":[3.0]*3+base[3:],"E_extreme_allowed":[10.0]*12+base[12:],"F_overlapping":[2.5,3.0,3.0,2.5]+base[4:]}
shocks=[{"inflation":.01*((i%3)-1),"output":.02*((i%2)*2-1),"unemployment":.005,"financial_conditions":0.0} for i in range(months)]
fixtures=[]
for name,player in cases.items():
    initial=UnifiedState(tuple(flows),2.4,.5,4.0,2.0,financial_stress=.2)
    expected=simulate_monthly(initial,player,base,stochastic=False,shock_sequence=shocks)
    fixtures.append({"name":name,"input":{"monthlyPriceChanges":flows,"output":.5,"unemployment":4.0,"stress":.2,"playerPath":player,"baselinePath":base},"shockSequence":shocks,"expected":expected})
out=ROOT/"tests/fixtures/unified_parity.json";out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({"tolerance":1e-12,"fixtures":fixtures},indent=2));print(out)
