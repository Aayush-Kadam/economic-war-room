from __future__ import annotations
from typing import Protocol
from engine.model import MacroState,Policy
class ScenarioExtension(Protocol):
    id:str
    def validate_policy(self,policy:Policy)->None: ...
    def adjust(self,state:MacroState,policy:Policy,shock:dict)->MacroState: ...
