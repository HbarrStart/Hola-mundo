#!/usr/bin/env python3
"""MOS Safety Gate: fail-closed publication policy.

This gate is intentionally conservative. It produces a decision but never
publishes anything. Critical/high-risk claims require human approval.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.json"
OUT = ROOT / "data" / "publication_queue.json"

CRITICAL_CATEGORIES = {"RESCUE", "MISSING", "HEALTH", "ROADS", "SHELTER", "WATER", "FOOD", "SUPPLIES"}
HIGH_RISK = {"CRITICAL", "HIGH"}


def gate(claim):
    reasons = []
    status = claim.get("status")
    priority = claim.get("priority", "MEDIUM")
    category = claim.get("category")
    evidence = claim.get("evidence_types", [])

    if status not in {"CONFIRMED", "CORROBORATED"}:
        reasons.append("claim_not_sufficiently_verified")
    if not evidence:
        reasons.append("no_evidence_recorded")
    if priority in HIGH_RISK or category in CRITICAL_CATEGORIES:
        reasons.append("human_review_required")

    # Fail closed: only low/medium-risk corroborated/confirmed claims with
    # recorded evidence can pass automatically. Critical/high-risk claims
    # are always held for explicit human review.
    publishable = not reasons
    return {
        "claim_id": claim.get("id"),
        "decision": "PUBLISH" if publishable else "HOLD",
        "reasons": reasons,
        "human_review_required": bool(priority in HIGH_RISK or category in CRITICAL_CATEGORIES),
    }


def main():
    payload = json.loads(CLAIMS.read_text(encoding="utf-8")) if CLAIMS.exists() else {"claims": []}
    decisions = [gate(c) for c in payload.get("claims", [])]
    OUT.write_text(json.dumps({"version":"0.1","decisions":decisions}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
