#!/usr/bin/env python3
"""MOS normalization layer.

Converts source observations into a strict common shape. It does not infer facts
that are absent from the source and it never upgrades verification status.
"""
from __future__ import annotations

from datetime import datetime

ALLOWED_TYPES = {"official","territorial","community","independent_media","investigator","elected_official","citizen_report","social_signal"}
ALLOWED_EVIDENCE = {"official_document","document","photo","video","geolocation","testimony","dataset","direct_observation","statement"}


def normalize(raw: dict) -> dict:
    required = ["id","title","source_id","source_type","source_url","published_at"]
    missing = [k for k in required if not raw.get(k)]
    if missing:
        raise ValueError(f"missing_required:{','.join(missing)}")
    if raw["source_type"] not in ALLOWED_TYPES:
        raise ValueError("invalid_source_type")
    datetime.fromisoformat(raw["published_at"].replace("Z", "+00:00"))
    evidence = [e for e in raw.get("evidence_types", []) if e in ALLOWED_EVIDENCE]
    return {
        "id": raw["id"], "claim_key": raw.get("claim_key", raw["id"]),
        "title": raw["title"], "summary": raw.get("summary", ""),
        "source_id": raw["source_id"], "source_name": raw.get("source_name", raw["source_id"]),
        "source_type": raw["source_type"], "source_url": raw["source_url"],
        "published_at": raw["published_at"], "updated_at": raw.get("updated_at", raw["published_at"]),
        "department": raw.get("department"), "municipality": raw.get("municipality"),
        "category": raw.get("category", "CONTEXT"), "priority": raw.get("priority", "MEDIUM"),
        "evidence_types": evidence, "human_report": bool(raw.get("human_report", False))
    }
