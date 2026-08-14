#!/usr/bin/env python3
"""Conservative, claim-type-aware corroboration scoring for MOS.

This engine ranks evidence; it does not declare truth. A high score only means
that a claim meets the configured evidence requirements. Publication remains
the responsibility of the Safety Gate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class EvidenceItem:
    id: str
    claim_id: str
    independent_upstream: bool
    evidence_type: str
    source_class: str
    temporal_match: bool = True
    spatial_match: bool = True
    contradicted: bool = False

@dataclass(frozen=True)
class CorroborationResult:
    claim_type: str
    status: str
    score: int
    independent_sources: int
    reasons: tuple[str, ...]

RULES = {
    'EVENT_EXISTENCE': {'min_independent': 1, 'types': {'official_record','instrumental','direct_observation'}},
    'CASUALTY_COUNT': {'min_independent': 2, 'types': {'official_record','hospital_record','rescue_record','direct_observation'}},
    'DAMAGE_REPORT': {'min_independent': 2, 'types': {'official_record','engineering_assessment','direct_observation','geolocated_media'}},
    'ACCESS_STATUS': {'min_independent': 2, 'types': {'official_record','responder_report','direct_observation'}},
    'RESOURCE_AVAILABILITY': {'min_independent': 2, 'types': {'official_record','provider_report','direct_observation'}},
}


def evaluate(claim_type: str, evidence: Iterable[EvidenceItem]) -> CorroborationResult:
    rule = RULES.get(claim_type)
    if not rule:
        return CorroborationResult(claim_type,'UNSUPPORTED_TYPE',0,0,('no_rule_for_claim_type',))
    items = [e for e in evidence if e.claim_id]
    independent = {e.id for e in items if e.independent_upstream and e.temporal_match and e.spatial_match and not e.contradicted}
    valid_types = {e.id for e in items if e.evidence_type in rule['types'] and not e.contradicted}
    score = 0
    reasons = []
    if len(independent) >= rule['min_independent']:
        score += 60
        reasons.append('minimum_independent_evidence_met')
    else:
        reasons.append('minimum_independent_evidence_not_met')
    if valid_types:
        score += 20
        reasons.append('acceptable_evidence_type_present')
    else:
        reasons.append('no_acceptable_evidence_type')
    if any(e.temporal_match and e.spatial_match for e in items):
        score += 10
        reasons.append('temporal_spatial_alignment_present')
    if any(e.contradicted for e in items):
        score -= 30
        reasons.append('contradictory_evidence_present')
    status = 'READY_FOR_SAFETY_GATE' if score >= 80 and len(independent) >= rule['min_independent'] else 'NEEDS_REVIEW'
    return CorroborationResult(claim_type,status,max(0,score),len(independent),tuple(reasons))

if __name__ == '__main__':
    print('MOS Corroboration Engine loaded: claim-type aware / safety-gate dependent')
