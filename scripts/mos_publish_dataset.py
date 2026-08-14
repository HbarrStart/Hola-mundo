#!/usr/bin/env python3
"""Build the public MOS dataset from gated claims only.

This script intentionally publishes zero records when the input claims are
missing or unsafe. It never invents emergency facts and never merges
conflicting observations.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.json"
OUT = ROOT / "data" / "public_situation.json"

ALLOWED = {"CONFIRMED_EVENT", "CONFIRMED_FACT", "CORROBORATED_FACT"}
BLOCKED = {"CONFLICTING_REPORTS", "PENDING_VERIFICATION", "EXPIRED"}


def main() -> int:
    raw = json.loads(CLAIMS.read_text(encoding="utf-8")) if CLAIMS.exists() else {"claims": []}
    public = []
    for claim in raw.get("claims", []):
        state = claim.get("verification_state", claim.get("status"))
        if state not in ALLOWED or state in BLOCKED:
            continue
        if claim.get("risk") in {"HIGH", "CRITICAL"}:
            continue
        if not claim.get("source_url") or not claim.get("evidence_types"):
            continue
        public.append({
            "id": claim.get("id"),
            "title": claim.get("title"),
            "summary": claim.get("summary"),
            "verification_state": state,
            "risk": claim.get("risk", "LOW"),
            "published_at": claim.get("published_at"),
            "source": claim.get("source"),
            "source_url": claim.get("source_url"),
            "evidence_types": claim.get("evidence_types", []),
            "related_sources": claim.get("related_sources", [])
        })
    payload = {
        "version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "publication_policy": "SAFETY_GATE_ONLY",
        "situations": public,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
