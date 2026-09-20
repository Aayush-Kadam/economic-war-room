import pytest
from engine.model import MacroState,Policy
from engine.extensions import FinancialCrisisExtension,IndiaExtension
S=MacroState(6,5,3,0,5,3,0,.5,.7,0)
def test_crisis_stress_nonlinear(): assert FinancialCrisisExtension().adjust(S,Policy(1),{"bank_stress":1}).financial_stress>S.financial_stress
def test_crisis_liquidity_offsets_stress():
 e=FinancialCrisisExtension(); assert e.adjust(S,Policy(1,balance_sheet=2),{"bank_stress":1}).financial_stress<e.adjust(S,Policy(1),{"bank_stress":1}).financial_stress
def test_crisis_lower_bound(): pytest.raises(ValueError,FinancialCrisisExtension().validate_policy,Policy(-.1))
def test_india_oil_pass_through(): assert IndiaExtension().adjust(S,Policy(6.5),{"oil":1}).inflation>S.inflation
def test_india_fx_intervention():
 e=IndiaExtension(); assert e.adjust(S,Policy(6.5),{"inr_depreciation":1,"fx_intervention":1}).fx_gap<e.adjust(S,Policy(6.5),{"inr_depreciation":1}).fx_gap
def test_modules_are_country_specific(): assert FinancialCrisisExtension().id!=IndiaExtension().id
