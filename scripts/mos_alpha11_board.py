#!/usr/bin/env python3
"""MOS Alpha-11: auditable human-facing board projection.

This is a projection layer only. It cannot bypass the Safety Gate.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json

ALLOWED = {'ALLOW','ALLOW_WITH_CONTEXT','HUMAN_REVIEW','HOLD','BLOCK'}

@dataclass(frozen=True)
class BoardCard:
    claim_id: str
    title: str
    gate_decision: str
    risk_level: str
    source_id: str
    primary_status: str
    last_updated: str
    evidence_refs: tuple[str, ...]
    history_refs: tuple[str, ...] = ()


def project(card: BoardCard) -> dict:
    if card.gate_decision not in ALLOWED:
        raise ValueError('invalid_gate_decision')
    # Board is a read-only projection; no card can be silently promoted here.
    return asdict(card)


def render_json(cards: list[BoardCard]) -> str:
    return json.dumps([project(c) for c in cards], ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('MOS Alpha-11 board loaded: read-only safety-gated projection')
