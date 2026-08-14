#!/usr/bin/env python3
"""MOS Alpha-22: consequence-based risk classification.

Risk changes the verification burden; it never changes a claim into truth.
"""
from enum import Enum

class RiskLevel(str, Enum):
    LOW = 'LOW'
    MODERATE = 'MODERATE'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

class VerificationTier(str, Enum):
    STANDARD = 'STANDARD'
    ENHANCED = 'ENHANCED'
    STRICT = 'STRICT'
    HUMAN_REVIEW = 'HUMAN_REVIEW'


def classify_risk(impact: int, uncertainty: int) -> RiskLevel:
    score = max(0, min(100, impact * uncertainty))
    if score >= 80:
        return RiskLevel.CRITICAL
    if score >= 50:
        return RiskLevel.HIGH
    if score >= 25:
        return RiskLevel.MODERATE
    return RiskLevel.LOW


def required_verification(risk: RiskLevel) -> VerificationTier:
    return {
        RiskLevel.LOW: VerificationTier.STANDARD,
        RiskLevel.MODERATE: VerificationTier.ENHANCED,
        RiskLevel.HIGH: VerificationTier.STRICT,
        RiskLevel.CRITICAL: VerificationTier.HUMAN_REVIEW,
    }[risk]
