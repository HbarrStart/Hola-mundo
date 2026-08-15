import json,pytest
from scripts.mos_alpha51_replay_audit import ReplayDecision
from scripts.mos_alpha52_audit_export import export_history

def test_export_is_deterministic():
    h=(ReplayDecision(True,'accepted','v1',100),ReplayDecision(False,'replay','v1',101))
    assert export_history(h)=='[{"accepted":true,"key_id":"v1","reason":"accepted","timestamp":100},{"accepted":false,"key_id":"v1","reason":"replay","timestamp":101}]'

def test_empty_history_exports_empty_array(): assert export_history(())=='[]'
def test_invalid_history_fails_closed():
    with pytest.raises(ValueError,match='invalid_history'): export_history(None)
def test_invalid_decision_fails_closed():
    with pytest.raises(ValueError,match='invalid_decision'): export_history(({'accepted':True},))
