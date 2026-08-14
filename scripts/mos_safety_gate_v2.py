#!/usr/bin/env python3
"""MOS Safety Gate v2: final fail-closed publication decision.

No claim is published unless corroboration and risk conditions are satisfied.
High/critical consequence claims require human review or are blocked.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GateInput:
    corroboration_status: str
    risk_action: str
    evidence_hash_present: bool
    source_registered: bool
    stale: bool = False
    contradiction: bool = False

@dataclass(frozen=True)
class GateDecision:
    decision: str
    reasons: tuple[str, ...]


def decide(x: GateInput) -> GateDecision:
    reasons = []
    if not x.source_registered:
        return GateDecision('BLOCK', ('source_not_registered',))
    if not x.evidence_hash_present:
        return GateDecision('HOLD', ('evidence_hash_missing',))
    if x.contradiction:
        return GateDecision('HUMAN_REVIEW', ('unresolved_contradiction',))
    if x.stale:
        return GateDecision('HOLD', ('evidence_stale',))
    if x.corroboration_status != 'READY_FOR_SAFETY_GATE':
        return GateDecision('HOLD', ('corroboration_incomplete',))
    if x.risk_action == 'BLOCK':
        return GateDecision('BLOCK', ('risk_engine_blocked',))
    if x.risk_action == 'HUMAN_REVIEW':
        return GateDecision('HUMAN_REVIEW', ('risk_requires_human_review',))
    if x.risk_action == 'ALLOW_WITH_CONTEXT':
        return GateDecision('ALLOW_WITH_CONTEXT', ('context_required',))
    if x.risk_action == 'ALLOW':
        return GateDecision('ALLOW', ('all_gate_conditions_met',))
    return GateDecision('BLOCK', ('unknown_risk_action',))

if __name__ == '__main__':
    print('MOS Safety Gate v2 loaded: fail-closed')
