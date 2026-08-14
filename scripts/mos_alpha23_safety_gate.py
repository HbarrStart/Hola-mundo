#!/usr/bin/env python3
"""MOS Alpha-23: fail-closed publication safety gate.

The gate authorizes a downstream publication layer; it never publishes itself.
"""
from dataclasses import dataclass
from enum import Enum

class GateDecision(str, Enum):
    ALLOW = 'ALLOW'
    ALLOW_WITH_CONTEXT = 'ALLOW_WITH_CONTEXT'
    HUMAN_REVIEW = 'HUMAN_REVIEW'
    HOLD = 'HOLD'
    BLOCK = 'BLOCK'

@dataclass(frozen=True)
class GateInput:
    provenance_ok: bool
    evidence_ok: bool
    corroboration_ok: bool
    temporal_ok: bool
    freshness_ok: bool
    risk: str
    human_review_complete: bool = False


def evaluate(g: GateInput) -> GateDecision:
    if not g.provenance_ok:
        return GateDecision.BLOCK
    if not g.evidence_ok:
        return GateDecision.HOLD
    if not g.temporal_ok or not g.freshness_ok:
        return GateDecision.HOLD
    if g.risk == 'CRITICAL' and not g.human_review_complete:
        return GateDecision.HUMAN_REVIEW
    if g.risk == 'HIGH' and not g.corroboration_ok:
        return GateDecision.HUMAN_REVIEW
    if not g.corroboration_ok:
        return GateDecision.ALLOW_WITH_CONTEXT
    return GateDecision.ALLOW


def can_publish(decision: GateDecision) -> bool:
    return decision in {GateDecision.ALLOW, GateDecision.ALLOW_WITH_CONTEXT}
