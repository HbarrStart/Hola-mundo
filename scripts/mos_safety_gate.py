#!/usr/bin/env python3
"""MOS Safety Gate: fail-closed eligibility decision.

The gate never publishes content. It only marks a claim as eligible for the
next step or holds it. Operational/critical information always requires a
human decision.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.json"
OUT = ROOT / "data" / "publication_queue.json"

CRITICAL_CATEGORIES = {"RESCUE", "MISSING", "HEALTH", "ROADS", "SHELTER", "WATER", "FOOD", "SUPPLIES"}
HIGH_RISK = {"CRITICAL", "HIGH"}
VERIFIED = {"CONFIRMED_EVENT", "CONFIRMED_FACT", "CORROBORATED_FACT"}


def _expired(claim: dict, now: datetime) -> bool:
    if claim.get("claim_type") == "event_existence":
        return False
    published = claim.get("published_at")
    ttl = claim.get("ttl_minutes")
    if not published or ttl is None:
        return False
    try:
        dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        return (now - dt).total_seconds() > int(ttl) * 60
    except (ValueError, TypeError):
        return True


def gate(claim: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    reasons: list[str] = []
    status = claim.get("status")
    priority = claim.get("priority", "MEDIUM")
    category = claim.get("category")
    claim_type = claim.get("claim_type", "fact")

    if status not in VERIFIED:
        reasons.append("claim_not_sufficiently_verified")
    if not claim.get("source_url"):
        reasons.append("missing_source_url")
    if not claim.get("published_at"):
        reasons.append("missing_timestamp")
    if not claim.get("evidence_types"):
        reasons.append("no_evidence_recorded")
    if status == "CONFLICTING_REPORTS":
        reasons.append("conflicting_sources")
    if _expired(claim, now):
        reasons.append("claim_expired")

    human_required = (
        claim_type == "operational_instruction"
        or priority in HIGH_RISK
        or category in CRITICAL_CATEGORIES
    )
    if human_required:
        reasons.append("human_review_required")

    if reasons:
        decision = "HOLD"
    else:
        # This is eligibility, not publication. A separate publishing layer
        # must consume this result and may require a human approval token.
        decision = "ELIGIBLE_FOR_PUBLICATION"

    return {
        "claim_id": claim.get("id"),
        "decision": decision,
        "reasons": reasons,
        "human_review_required": human_required,
    }


def main() -> None:
    payload = json.loads(CLAIMS.read_text(encoding="utf-8")) if CLAIMS.exists() else {"claims": []}
    decisions = [gate(c) for c in payload.get("claims", [])]
    OUT.write_text(json.dumps({"version":"0.2","decisions":decisions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
