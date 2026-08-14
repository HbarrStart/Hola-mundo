#!/usr/bin/env python3
"""MOS Risk Engine: conservative publication-risk classification.

Risk is about consequences of publishing an incorrect or overly specific claim,
not about political agreement or source popularity. This module does not publish.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskInput:
    claim_type: str
    corroboration_status: str
    potential_harm: str  # LOW, MEDIUM, HIGH, CRITICAL
    operational: bool = False
    sensitive_location: bool = False
    personal_data: bool = False
    rapidly_changing: bool = False

@dataclass(frozen=True)
class RiskDecision:
    level: str
    action: str
    reasons: tuple[str, ...]

_HARM = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2, 'CRITICAL': 3}


def assess(x: RiskInput) -> RiskDecision:
    reasons = []
    score = _HARM.get(x.potential_harm, 3)
    if x.operational:
        score += 2; reasons.append('operational_consequence')
    if x.sensitive_location:
        score += 2; reasons.append('sensitive_location')
    if x.personal_data:
        score += 3; reasons.append('personal_data')
    if x.rapidly_changing:
        score += 1; reasons.append('rapidly_changing')
    if x.corroboration_status != 'READY_FOR_SAFETY_GATE':
        score += 2; reasons.append('corroboration_incomplete')

    if x.personal_data or score >= 6:
        return RiskDecision('CRITICAL', 'BLOCK', tuple(reasons + ['high_consequence_publication']))
    if score >= 4:
        return RiskDecision('HIGH', 'HUMAN_REVIEW', tuple(reasons + ['requires_human_review']))
    if score >= 2:
        return RiskDecision('MEDIUM', 'ALLOW_WITH_CONTEXT', tuple(reasons + ['context_required']))
    return RiskDecision('LOW', 'ALLOW', tuple(reasons))

if __name__ == '__main__':
    print('MOS Risk Engine loaded: consequence-aware / no auto-publication')
