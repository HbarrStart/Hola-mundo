#!/usr/bin/env python3
"""MOS Alpha-24: adversarial Safety Gate fixtures.
Synthetic-only attack cases. The test harness verifies fail-closed behavior.
"""
from dataclasses import dataclass
from scripts.mos_alpha23_safety_gate import GateDecision, GateInput, evaluate

@dataclass(frozen=True)
class AttackCase:
    name: str
    gate_input: GateInput
    expected: GateDecision

ATTACKS = [
    AttackCase('trusted_source_missing_evidence', GateInput(True,False,True,True,True,'HIGH'), GateDecision.HOLD),
    AttackCase('critical_claim_no_human_review', GateInput(True,True,True,True,True,'CRITICAL'), GateDecision.HUMAN_REVIEW),
    AttackCase('stale_critical_claim', GateInput(True,True,True,True,False,'CRITICAL'), GateDecision.HOLD),
    AttackCase('same_origin_many_sources', GateInput(True,True,False,True,True,'HIGH'), GateDecision.HUMAN_REVIEW),
    AttackCase('temporal_conflict', GateInput(True,True,True,False,True,'HIGH'), GateDecision.HOLD),
    AttackCase('missing_provenance', GateInput(False,True,True,True,True,'LOW'), GateDecision.BLOCK),
]

def run_red_team() -> list[tuple[str, GateDecision, GateDecision]]:
    return [(a.name, evaluate(a.gate_input), a.expected) for a in ATTACKS]
