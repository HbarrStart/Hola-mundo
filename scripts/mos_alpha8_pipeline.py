#!/usr/bin/env python3
"""MOS Alpha-8 end-to-end pipeline harness.

This is a deterministic integration harness: it wires the existing layers and
returns a publication decision. It does not fetch live sources or publish data.
Live adapters must enter through the Source Connector and preserve raw evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
from scripts.mos_corroboration_engine import EvidenceItem, evaluate
from scripts.mos_risk_engine import RiskInput, assess
from scripts.mos_safety_gate_v2 import GateInput, decide

@dataclass(frozen=True)
class Alpha8Input:
    claim_type: str
    evidence: tuple[EvidenceItem, ...]
    potential_harm: str
    operational: bool = False
    sensitive_location: bool = False
    personal_data: bool = False
    rapidly_changing: bool = False
    source_registered: bool = True
    evidence_hash_present: bool = True
    stale: bool = False
    contradiction: bool = False


def run(x: Alpha8Input):
    corr = evaluate(x.claim_type, x.evidence)
    risk = assess(RiskInput(x.claim_type, corr.status, x.potential_harm,
                            x.operational, x.sensitive_location,
                            x.personal_data, x.rapidly_changing))
    gate = decide(GateInput(corr.status, risk.action, x.evidence_hash_present,
                            x.source_registered, x.stale, x.contradiction))
    return {'corroboration': corr, 'risk': risk, 'gate': gate}

if __name__ == '__main__':
    print('MOS Alpha-8 harness loaded: end-to-end / fail-closed / no live publication')
