from scripts.mos_risk_engine import RiskInput, assess
from scripts.mos_safety_gate_v2 import GateInput, decide


def test_personal_data_is_blocked():
    r = assess(RiskInput('CASUALTY_COUNT','READY_FOR_SAFETY_GATE','HIGH',personal_data=True))
    assert r.action == 'BLOCK'


def test_operational_claim_needs_review():
    r = assess(RiskInput('ACCESS_STATUS','READY_FOR_SAFETY_GATE','HIGH',operational=True))
    assert r.action == 'HUMAN_REVIEW'


def test_gate_holds_missing_hash():
    r = decide(GateInput('READY_FOR_SAFETY_GATE','ALLOW',False,True))
    assert r.decision == 'HOLD'


def test_gate_blocks_unregistered_source():
    r = decide(GateInput('READY_FOR_SAFETY_GATE','ALLOW',True,False))
    assert r.decision == 'BLOCK'


def test_gate_reviews_contradiction():
    r = decide(GateInput('READY_FOR_SAFETY_GATE','ALLOW',True,True,contradiction=True))
    assert r.decision == 'HUMAN_REVIEW'


def test_gate_allows_low_risk_verified_claim():
    r = decide(GateInput('READY_FOR_SAFETY_GATE','ALLOW',True,True))
    assert r.decision == 'ALLOW'
