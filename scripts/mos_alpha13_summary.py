#!/usr/bin/env python3
"""MOS Alpha-13 traceable public situation summary.

Only claims already cleared for public presentation are summarized. The
summary layer never creates facts, inferred locations, numbers, or causal
explanations and cannot bypass the Safety Gate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

ALLOWED = {'ALLOW', 'ALLOW_WITH_CONTEXT', 'HUMAN_REVIEW', 'HOLD', 'BLOCK'}
PUBLIC = {'ALLOW', 'ALLOW_WITH_CONTEXT'}

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
        # Public summary is presentation-only: review, hold and block never escape.
        if c.status not in PUBLIC:
            continue
        if not c.evidence_refs:
            raise ValueError('summary_item_missing_evidence_refs')
        items.append(SummaryItem(c.claim_id, c.text, c.status, c.updated_at, c.evidence_refs))
    return sorted(items, key=lambda x: x.updated_at, reverse=True)


def assert_traceable(item: SummaryItem) -> bool:
    return bool(item.claim_id and item.evidence_refs and item.updated_at)

if __name__ == '__main__':
    print('MOS Alpha-13 loaded: public-only / ledger-only / traceable summary')
