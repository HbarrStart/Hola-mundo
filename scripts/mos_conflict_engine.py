#!/usr/bin/env python3
"""MOS Alpha-4: conservative claim relation engine.

The engine does not decide which claim is true. It classifies the relationship
between two claims using explicit temporal/source/evidence signals. Ambiguity
is preserved and escalated for review.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

RELATIONS = {"DUPLICATE", "UPDATE", "CORRECTION", "CONFLICT", "UNRESOLVED"}

@dataclass(frozen=True)
class Claim:
    id: str
    subject: str
    value: str
    unit: str | None
    source_id: str
    published_at: str
    observed_at: str | None = None
    evidence_ref: str | None = None
    supersedes: str | None = None


def _dt(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def classify(a: Claim, b: Claim) -> str:
    if a.subject != b.subject or a.unit != b.unit:
        return "UNRESOLVED"
    if a.value == b.value:
        return "DUPLICATE"
    if b.supersedes == a.id:
        return "UPDATE"
    da, db = _dt(a.published_at), _dt(b.published_at)
    if da and db and db < da:
        a, b = b, a
    # Explicit correction metadata is stronger than inference.
    if b.supersedes == a.id and b.evidence_ref:
        return "CORRECTION"
    # Different values for the same subject/time window are not resolved by
    # source popularity or repetition. Keep the conflict visible.
    if da and db and abs((db - da).total_seconds()) <= 24 * 3600:
        return "CONFLICT"
    return "UNRESOLVED"
