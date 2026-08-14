#!/usr/bin/env python3
"""MOS Alpha-30: risk classification, independent from truth assessment."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class RiskLevel(str, Enum):
    LOW='LOW'; MEDIUM='MEDIUM'; HIGH='HIGH'; CRITICAL='CRITICAL'; UNKNOWN='UNKNOWN'

@dataclass(frozen=True)
class RiskInput:
    impact: Optional[int]
    urgency: Optional[int]
    evidence_quality: Optional[int]
    contradiction: Optional[int]
    scope: Optional[int]
    reversibility: Optional[int]

def classify_risk(x: RiskInput) -> RiskLevel:
    vals=(x.impact,x.urgency,x.evidence_quality,x.contradiction,x.scope,x.reversibility)
    if any(v is None for v in vals): return RiskLevel.UNKNOWN
    if any(not isinstance(v,int) or v < 0 or v > 5 for v in vals): raise ValueError('invalid_risk_input')
    score=(x.impact*2+x.urgency+x.evidence_quality+x.contradiction+x.scope+(5-x.reversibility))
    if score >= 27: return RiskLevel.CRITICAL
    if score >= 20: return RiskLevel.HIGH
    if score >= 12: return RiskLevel.MEDIUM
    return RiskLevel.LOW
