import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mos_safety_gate", ROOT / "scripts" / "mos_safety_gate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE = {
    "id": "MOS-20260814-0001",
    "source_url": "https://example.org/source",
    "published_at": "2026-08-14T10:00:00+00:00",
    "claim_type": "fact",
    "evidence_types": ["document"],
    "priority": "LOW",
    "category": "CONTEXT",
}


def test_unverified_claim_is_held():
    claim = {**BASE, "status": "PENDING_VERIFICATION"}
    result = module.gate(claim)
    assert result["decision"] == "HOLD"


def test_critical_claim_always_requires_human_review():
    claim = {**BASE, "status": "CONFIRMED_FACT", "priority": "CRITICAL", "category": "ROADS"}
    result = module.gate(claim)
    assert result["decision"] == "HOLD"
    assert result["human_review_required"] is True


def test_operational_instruction_always_requires_human_review():
    claim = {**BASE, "status": "CONFIRMED_FACT", "claim_type": "operational_instruction"}
    result = module.gate(claim)
    assert result["decision"] == "HOLD"
    assert result["human_review_required"] is True


def test_verified_low_risk_is_only_eligible_not_published():
    claim = {**BASE, "status": "CORROBORATED_FACT"}
    result = module.gate(claim)
    assert result["decision"] == "ELIGIBLE_FOR_PUBLICATION"
    assert result["human_review_required"] is False


def test_expired_fact_is_held():
    claim = {**BASE, "status": "CORROBORATED_FACT", "ttl_minutes": 1,
             "published_at": "2026-08-14T08:00:00+00:00"}
    now = datetime(2026, 8, 14, 10, 0, tzinfo=timezone.utc)
    result = module.gate(claim, now=now)
    assert result["decision"] == "HOLD"
    assert "claim_expired" in result["reasons"]


def test_event_existence_does_not_expire_by_ttl():
    claim = {**BASE, "status": "CONFIRMED_EVENT", "claim_type": "event_existence", "ttl_minutes": 1,
             "published_at": "2026-08-10T08:00:00+00:00"}
    now = datetime(2026, 8, 14, 10, 0, tzinfo=timezone.utc)
    result = module.gate(claim, now=now)
    assert result["decision"] == "ELIGIBLE_FOR_PUBLICATION"
