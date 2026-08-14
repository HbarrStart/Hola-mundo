#!/usr/bin/env python3
"""MOS Chronos: immutable, source-linked event timeline builder."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class TimelineEntry:
    claim_id: str
    observed_at: str
    received_at: str
    verification_state: str
    source: str
    source_url: str
    version: int = 1
    supersedes: str | None = None
    relation: str | None = None


def build_timeline(entries: Iterable[TimelineEntry]) -> list[TimelineEntry]:
    """Return entries sorted by the time the underlying fact was observed.

    Entries are never deduplicated or overwritten here. Chronos is a history
    layer; identity and verification belong to earlier pipeline stages.
    """
    return sorted(entries, key=lambda e: (e.observed_at, e.received_at, e.claim_id))


def current_entries(entries: Iterable[TimelineEntry]) -> list[TimelineEntry]:
    """Return latest non-superseded versions without deleting history."""
    all_entries = list(entries)
    superseded = {e.supersedes for e in all_entries if e.supersedes}
    return [e for e in all_entries if e.claim_id not in superseded]
