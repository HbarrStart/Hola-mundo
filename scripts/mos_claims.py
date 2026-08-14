#!/usr/bin/env python3
"""Deterministic MOS claim pipeline.

Reads normalized observations and assigns a transparent verification state.
It never turns a social/citizen signal into CONFIRMED by itself.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "observations.json"
OUT = ROOT / "data" / "claims.json"

PRIMARY = {"official", "territorial"}
SECONDARY = {"independent_media", "investigator", "community"}


def classify(obs):
    sources = {o.get("source_id") for o in obs if o.get("source_id")}
    types = {o.get("source_type") for o in obs}
    evidence = {e for o in obs for e in o.get("evidence_types", [])}
    if len(sources) >= 2 and types & PRIMARY and evidence:
        return "CONFIRMED", "TWO_SOURCES"
    if len(sources) >= 2 and evidence:
        return "CORROBORATED", "TWO_SOURCES"
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
        status, corr = classify(observations)
        first = observations[0]
        claims.append({
            "id": first["id"], "status": status, "corroboration_level": corr,
            "title": first.get("title", key), "summary": first.get("summary", ""),
            "source": first.get("source_name", first.get("source_id", "unknown")),
            "source_type": first.get("source_type", "social_signal"),
            "source_url": first.get("source_url", "https://www.gestiondelriesgo.gov.co/"),
            "published_at": first.get("published_at"), "updated_at": first.get("updated_at"),
            "evidence_types": sorted({e for o in observations for e in o.get("evidence_types", [])}),
            "related_sources": sorted({o.get("source_url") for o in observations if o.get("source_url")})
        })
    OUT.write_text(json.dumps({"version":"0.2","claims":claims}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
