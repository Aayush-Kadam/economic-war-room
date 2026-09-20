import json
from pathlib import Path
import pytest
from data.vintages.packet import validate_packet
ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture
def packet(): return json.loads((ROOT/"data/vintages/fomc_2022_06_15_manifest.json").read_text())
def test_valid_packet(packet): validate_packet(packet)
@pytest.mark.parametrize("field,value",[("release_date","2022-06-16"),("vintage_date","2022-06-20")])
def test_rejects_future_dates(packet,field,value): packet["features"][0][field]=value; pytest.raises(ValueError,validate_packet,packet)
def test_rejects_malformed_date(packet): packet["features"][0]["release_date"]="tomorrow"; pytest.raises(ValueError,validate_packet,packet)
def test_rejects_exposed_policy(packet): packet["actual_policy_action"]["visibility"]="pre_commit"; pytest.raises(ValueError,validate_packet,packet)
def test_timezone_boundary_rejected(packet): packet["features"][0]["release_date"]="2022-06-16"; pytest.raises(ValueError,validate_packet,packet)
