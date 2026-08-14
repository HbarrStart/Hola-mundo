#!/usr/bin/env python3
"""MOS Alpha-25: append-only evidence ledger primitives.

Synthetic/local records only. The ledger records provenance and relationships;
it does not itself establish truth or publish emergency instructions.
"""
from dataclasses import dataclass
from enum import Enum
import hashlib

class EvidenceRelation(str, Enum):
    SUPPORTS = 'SUPPORTS'
    CONTRADICTS = 'CONTRADICTS'
    QUALIFIES = 'QUALIFIES'
    SUPERSEDES = 'SUPERSEDES'

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    claim_id: str
    source_id: str
    location: str
    retrieved_at: str
    content_hash: str
    evidence_type: str
    pointer: str
    relation: EvidenceRelation

def content_hash(content: str) -> str:
    if not content:
        raise ValueError('empty_evidence_content')
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def create_evidence(evidence_id: str, claim_id: str, source_id: str, location: str,
                    retrieved_at: str, content: str, evidence_type: str,
                    pointer: str, relation: EvidenceRelation) -> Evidence:
    fields = [evidence_id, claim_id, source_id, location, retrieved_at,
              evidence_type, pointer]
    if any(not x for x in fields):
        raise ValueError('incomplete_evidence_record')
    return Evidence(evidence_id, claim_id, source_id, location, retrieved_at,
                    content_hash(content), evidence_type, pointer, relation)
