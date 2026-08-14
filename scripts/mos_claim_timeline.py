#!/usr/bin/env python3
"""MOS timeline for evolving emergency claims.

Separates temporal updates from contradictions. It never decides truth; it
records explicit source timing and requires an explicit supersedes relation to
call one value an update of another.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ClaimVersion:
    claim_id: str
    claim_key: str
    value: str
    source_id: str
    observed_at: str | None
    published_at: str | None
    supersedes: str | None = None
    correction_of: str | None = None


def classify_relation(previous: ClaimVersion | None, current: ClaimVersion) -> str:
    if previous is None:
        return 'INITIAL'
    if current.correction_of == previous.claim_id:
        return 'CORRECTION'
    if current.supersedes == previous.claim_id:
        return 'UPDATE'
    if current.value == previous.value:
        return 'DUPLICATE'
    return 'UNRESOLVED_CHANGE'


def sort_versions(versions: list[ClaimVersion]) -> list[ClaimVersion]:
    return sorted(versions, key=lambda x: (x.published_at or '', x.claim_id))
