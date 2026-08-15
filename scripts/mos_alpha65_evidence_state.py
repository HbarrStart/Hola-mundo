#!/usr/bin/env python3
"""MOS Alpha-65: explicit evidence state machine for emergency reporting."""
from enum import Enum
class EvidenceState(str, Enum):
    UNVERIFIED='unverified'; VERIFIED='verified'; CORROBORATED='corroborated'; REVOKED='revoked'
def evidence_state(*,verified:bool,corroborated:bool,revoked:bool)->EvidenceState:
    if revoked:return EvidenceState.REVOKED
    if not verified:return EvidenceState.UNVERIFIED
    if not corroborated:return EvidenceState.VERIFIED
    return EvidenceState.CORROBORATED
def is_publishable(state:EvidenceState)->bool:return state is EvidenceState.CORROBORATED
