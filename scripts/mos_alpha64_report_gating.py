#!/usr/bin/env python3
"""MOS Alpha-64: fail-closed gating for emergency reports."""
from dataclasses import dataclass

@dataclass(frozen=True)
class GateResult:
    allowed: bool
    reason: str

def gate_report(*, verified:bool, revoked:bool, corroborated:bool)->GateResult:
    if revoked: return GateResult(False,'revoked_source')
    if not verified: return GateResult(False,'unverified_source')
    if not corroborated: return GateResult(False,'insufficient_corroboration')
    return GateResult(True,'confirmed')
