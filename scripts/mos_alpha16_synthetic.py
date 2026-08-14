#!/usr/bin/env python3
"""MOS Alpha-16 synthetic end-to-end fixture.

Synthetic data only. No real emergency data is embedded here.
"""
from dataclasses import dataclass
from enum import Enum

class Relation(str, Enum):
    UPDATE = 'UPDATE'
    UNRESOLVED_CHANGE = 'UNRESOLVED_CHANGE'

@dataclass(frozen=True)
class SyntheticClaim:
    claim_id: str
    source_id: str
    observed_at: str
    value: str
    evidence_id: str


def relate(a: SyntheticClaim, b: SyntheticClaim) -> Relation:
    if a.value == b.value:
        return Relation.UPDATE
    return Relation.UNRESOLVED_CHANGE


def trace(claim: SyntheticClaim) -> dict:
    return {
        'claim_id': claim.claim_id,
        'evidence_id': claim.evidence_id,
        'source_id': claim.source_id,
        'observed_at': claim.observed_at,
    }


if __name__ == '__main__':
    a = SyntheticClaim('CLAIM-0007','SYNTH-OFFICIAL','2026-08-14T15:00:00Z','100','EVIDENCE-0019')
    b = SyntheticClaim('CLAIM-0008','SYNTH-INDEPENDENT','2026-08-14T15:10:00Z','150','EVIDENCE-0020')
    print(relate(a,b).value)
