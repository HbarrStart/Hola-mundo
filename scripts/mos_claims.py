#!/usr/bin/env python3
"""MOS claim pipeline: event existence and claim verification are separate."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "observations.json"
OUT = ROOT / "data" / "claims.json"
PRIMARY = {"official", "territorial"}
SECONDARY = {"independent_media", "investigator", "community"}


def classify(observations):
    sources = {o.get("source_id") for o in observations if o.get("source_id")}
    types = {o.get("source_type") for o in observations}
    evidence = {e for o in observations for e in o.get("evidence_types", [])}
    claim_type = observations[0].get("claim_type", "fact")

    # Event existence is a distinct claim. A competent primary source or
    # multiple independent high-quality sources can establish the event.
    if claim_type == "event_existence":
        if types & PRIMARY and evidence:
            return "CONFIRMED_EVENT", "PRIMARY_SOURCE"
        if len(sources) >= 2 and evidence:
            return "CONFIRMED_EVENT", "MULTIPLE_INDEPENDENT_SOURCES"

    # Individual facts remain independently verifiable even when the event
    # itself is confirmed. Never inherit event confirmation automatically.
    if len(sources) >= 2 and evidence:
        return "CORROBORATED_FACT", "TWO_SOURCES"
    if types & SECONDARY or types & {"citizen_report", "social_signal", "elected_official"}:
        return "PENDING_VERIFICATION", "ONE_SOURCE"
    return "PENDING_VERIFICATION", "NONE"


def main():
    payload = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {"observations": []}
    grouped = {}
    for item in payload.get("observations", []):
        key = item.get("claim_key")
        if key:
            grouped.setdefault(key, []).append(item)
    claims = []
    for key, observations in grouped.items():
        status, basis = classify(observations)
        first = observations[0]
        claims.append({
            "id": first["id"], "status": status, "verification_basis": basis,
            "claim_type": first.get("claim_type", "fact"),
            "corroboration_level": "MULTIPLE_INDEPENDENT_SOURCES" if len({o.get("source_id") for o in observations if o.get("source_id")}) >= 2 else "ONE_SOURCE",
            "title": first.get("title", key), "summary": first.get("summary", ""),
            "source": first.get("source_name", first.get("source_id", "unknown")),
            "source_type": first.get("source_type", "social_signal"),
            "source_url": first.get("source_url", ""),
            "published_at": first.get("published_at"), "updated_at": first.get("updated_at"),
            "evidence_types": sorted({e for o in observations for e in o.get("evidence_types", [])}),
            "related_sources": sorted({o.get("source_url") for o in observations if o.get("source_url")})
        })
    OUT.write_text(json.dumps({"version":"0.3","claims":claims}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
