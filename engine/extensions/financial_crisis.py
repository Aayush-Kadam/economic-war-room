from dataclasses import replace
from engine.model import MacroState,Policy
class FinancialCrisisExtension:
    id="fed-gfc-2007-09"
    def validate_policy(self,policy):
        if policy.rate<0: raise ValueError("effective lower bound")
        if not -1<=policy.balance_sheet<=3: raise ValueError("invalid liquidity/QE stance")
    def adjust(self,state,policy,shock):
        self.validate_policy(policy); bank=float(shock.get("bank_stress",0)); liquidity=max(0,policy.balance_sheet)
        stress=max(0,min(2,state.financial_stress+0.55*bank-0.18*liquidity)); credit=state.credit_gap-0.45*bank+0.15*liquidity
        output=state.output_gap-0.30*max(0,stress-.7)+0.08*liquidity
        return replace(state,financial_stress=stress,credit_gap=credit,output_gap=output)
