#!/usr/bin/env python3
"""MOS Alpha-36: fail-closed resilience and degradation policy."""
from enum import Enum

class ServiceState(str, Enum):
    HEALTHY='HEALTHY'; DEGRADED='DEGRADED'; UNAVAILABLE='UNAVAILABLE'
class SafeMode(str, Enum):
    NORMAL='NORMAL'; HOLD='HOLD'; HUMAN_REVIEW='HUMAN_REVIEW'

def choose_mode(state: ServiceState, audit_valid: bool, evidence_available: bool) -> SafeMode:
    if not audit_valid:
        return SafeMode.HOLD
    if state is ServiceState.UNAVAILABLE or not evidence_available:
        return SafeMode.HOLD
    if state is ServiceState.DEGRADED:
        return SafeMode.HUMAN_REVIEW
    return SafeMode.NORMAL
