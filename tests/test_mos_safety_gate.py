import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mos_safety_gate", ROOT / "scripts" / "mos_safety_gate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_unverified_claim_is_held():
    claim = {"id":"MOS-20260814-0001","status":"PENDING_VERIFICATION","priority":"LOW","category":"OTHER","evidence_types":[]}
    result = module.gate(claim)
    assert result["decision"] == "HOLD"


def test_critical_claim_always_requires_human_review():
    claim = {"id":"MOS-20260814-0002","status":"CONFIRMED","priority":"CRITICAL","category":"ROADS","evidence_types":["official_document"]}
    result = module.gate(claim)
    assert result["decision"] == "HOLD"
    assert result["human_review_required"] is True


def test_verified_low_risk_with_evidence_can_pass():
    claim = {"id":"MOS-20260814-0003","status":"CORROBORATED","priority":"LOW","category":"CONTEXT","evidence_types":["document"]}
    result = module.gate(claim)
    assert result["decision"] == "PUBLISH"
