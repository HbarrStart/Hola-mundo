#!/usr/bin/env python3
"""MOS Alpha-13 traceable situation summary.

Only summarizes claims already present in the supplied ledger. Public output is
fail-closed: only explicitly publishable statuses are emitted. It never creates
new facts, inferred locations, numbers, or causal explanations.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

ALLOWED = {'ALLOW','ALLOW_WITH_CONTEXT','HUMAN_REVIEW','HOLD','BLOCK'}
PUBLIC_STATUSES = {'ALLOW','ALLOW_WITH_CONTEXT'}

@dataclass(frozen=True)
class Claim:
    claim_id: str
    text: str
    status: str
    risk: str
    updated_at: str
    evidence_refs: tuple[str, ...]
    location: str | None = None

@dataclass(frozen=True)
class SummaryItem:
    claim_id: str
    text: str
    status: str
    updated_at: str
    evidence_refs: tuple[str, ...]


def build_summary(claims: Iterable[Claim], include_blocked: bool = False) -> list[SummaryItem]:
    items = []
    for c in claims:
        if c.status not in ALLOWED:
            raise ValueError('unknown_gate_status')
        if c.status not in PUBLIC_STATUSES:
            continue
        if not c.evidence_refs:
            raise ValueError('summary_item_missing_evidence_refs')
        items.append(SummaryItem(c.claim_id, c.text, c.status, c.updated_at, c.evidence_refs))
    return sorted(items, key=lambda x: x.updated_at, reverse=True)


def assert_traceable(item: SummaryItem) -> bool:
    return bool(item.claim_id and item.evidence_refs and item.updated_at)

if __name__ == '__main__':
    print('MOS Alpha-13 loaded: ledger-only / traceable summary')
