#!/usr/bin/env python3
"""MOS Alpha-34: deterministic integration gate across core safety signals."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from scripts.mos_alpha30_risk import RiskLevel, RiskInput, classify_risk

class IntegrationDecision(str, Enum):
    ALLOW='ALLOW'; ALLOW_WITH_CONTEXT='ALLOW_WITH_CONTEXT'; HUMAN_REVIEW='HUMAN_REVIEW'; HOLD='HOLD'; BLOCK='BLOCK'

@dataclass(frozen=True)
class IntegrationInput:
    risk: RiskInput
    corroboration: str
    freshness: str
    provenance: str
    audit_valid: Optional[bool]

def decide(x: IntegrationInput) -> IntegrationDecision:
    if x.audit_valid is not True: return IntegrationDecision.HOLD
    risk=classify_risk(x.risk)
    if risk is RiskLevel.CRITICAL: return IntegrationDecision.HUMAN_REVIEW
    if risk is RiskLevel.UNKNOWN: return IntegrationDecision.HOLD
    if x.corroboration in {'MIXED','CONTRADICTED'}: return IntegrationDecision.HUMAN_REVIEW
    if x.freshness in {'STALE','EXPIRED','UNKNOWN'}: return IntegrationDecision.HOLD
    if x.provenance in {'UNKNOWN','CONFLICTING'}: return IntegrationDecision.HUMAN_REVIEW
    if risk is RiskLevel.HIGH: return IntegrationDecision.HUMAN_REVIEW
    if risk is RiskLevel.MEDIUM: return IntegrationDecision.ALLOW_WITH_CONTEXT
    return IntegrationDecision.ALLOW
