#!/usr/bin/env python3
"""MOS Alpha-27: evidence corroboration without authority-by-count.

Synthetic/local records only. Corroboration is not a truth guarantee.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class EvidenceRelation(str, Enum):
    SUPPORTS='SUPPORTS'; CONTRADICTS='CONTRADICTS'; QUALIFIES='QUALIFIES'; SUPERSEDES='SUPERSEDES'

class CorroborationStatus(str, Enum):
    CONSISTENT='CONSISTENT'; MIXED='MIXED'; CONTRADICTED='CONTRADICTED'; INSUFFICIENT='INSUFFICIENT'

@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    source_id: str
    relation: EvidenceRelation
    independence_key: str

@dataclass(frozen=True)
class CorroborationResult:
    status: CorroborationStatus
    independent_support: int
    independent_contradictions: int
    evidence_count: int


def assess(evidence: Tuple[EvidenceItem, ...]) -> CorroborationResult:
    if not evidence:
        return CorroborationResult(CorroborationStatus.INSUFFICIENT, 0, 0, 0)
    support_keys = {e.independence_key for e in evidence if e.relation is EvidenceRelation.SUPPORTS}
    contradict_keys = {e.independence_key for e in evidence if e.relation is EvidenceRelation.CONTRADICTS}
    if support_keys and contradict_keys:
        status = CorroborationStatus.MIXED
    elif support_keys:
        status = CorroborationStatus.CONSISTENT
    elif contradict_keys:
        status = CorroborationStatus.CONTRADICTED
    else:
        status = CorroborationStatus.INSUFFICIENT
    return CorroborationResult(status, len(support_keys), len(contradict_keys), len(evidence))
