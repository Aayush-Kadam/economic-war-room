from dataclasses import replace
from engine.model import MacroState,Policy
class IndiaExtension:
    id="rbi-inflation-2022-24"
    def validate_policy(self,policy):
        if not 0<=policy.rate<=12: raise ValueError("repo rate outside scenario bounds")
        if not -1<=policy.balance_sheet<=1: raise ValueError("liquidity stance outside bounds")
    def adjust(self,state,policy,shock):
        self.validate_policy(policy); oil=float(shock.get("oil",0)); depreciation=float(shock.get("inr_depreciation",0)); fed=float(shock.get("fed_tightening",0)); intervention=float(shock.get("fx_intervention",0))
        imported=.08*oil+.12*depreciation-.05*intervention; fx=state.fx_gap+depreciation+.15*fed-.2*(policy.rate-6)-.3*intervention
        inflation=state.inflation+imported; stress=max(0,min(2,state.financial_stress+.08*fed+.06*max(0,fx)))
        return replace(state,inflation=inflation,fx_gap=fx,financial_stress=stress,credit_gap=state.credit_gap+.08*policy.balance_sheet)
