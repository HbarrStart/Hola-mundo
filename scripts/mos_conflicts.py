#!/usr/bin/env python3
"""MOS contradiction detector.

Different values are not merged into a synthetic value. They are preserved as
separate observations and flagged for human review.
"""
from __future__ import annotations


def detect_conflicts(observations: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for obs in observations:
        key = obs.get("claim_key")
        if key:
            grouped.setdefault(key, []).append(obs)

    conflicts = []
    for key, items in grouped.items():
        values = {str(i.get("value")) for i in items if i.get("value") is not None}
        if len(values) > 1:
            conflicts.append({
                "claim_key": key,
                "type": "CONFLICTING_REPORTS",
                "values": sorted(values),
                "sources": sorted({i.get("source_url") for i in items if i.get("source_url")}),
                "requires_human_review": True,
            })
    return conflicts
