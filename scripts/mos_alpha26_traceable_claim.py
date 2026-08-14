#!/usr/bin/env python3
"""MOS Alpha-26: auditable, traceable claims.

Synthetic/local records only. This layer assembles an audit trail; it does
not decide truth and it never publishes emergency instructions.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class EvidenceRelation(str, Enum):
    SUPPORTS = 'SUPPORTS'
    CONTRADICTS = 'CONTRADICTS'
    QUALIFIES = 'QUALIFIES'
    SUPERSEDES = 'SUPERSEDES'

@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    relation: EvidenceRelation

@dataclass(frozen=True)
class TraceableClaim:
    claim_id: str
    text: str
    source_ids: Tuple[str, ...]
    evidence: Tuple[EvidenceRef, ...]
    retrieved_at: str

    def validate(self) -> None:
        required = [self.claim_id, self.text, self.retrieved_at]
        if any(not isinstance(v, str) or not v.strip() for v in required):
            raise ValueError('incomplete_claim')
        if not self.source_ids or any(not isinstance(v, str) or not v.strip() for v in self.source_ids):
            raise ValueError('missing_source_trace')
        if not self.evidence:
            raise ValueError('missing_evidence_trace')
        for ref in self.evidence:
            if not ref.evidence_id.strip() or not isinstance(ref.relation, EvidenceRelation):
                raise ValueError('invalid_evidence_trace')

    def audit_path(self) -> dict:
        self.validate()
        return {
            'claim_id': self.claim_id,
            'source_ids': self.source_ids,
            'evidence': tuple({'evidence_id': r.evidence_id, 'relation': r.relation.value} for r in self.evidence),
            'retrieved_at': self.retrieved_at,
        }
