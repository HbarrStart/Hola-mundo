#!/usr/bin/env python3
"""MOS Alpha-20: conservative corroboration.

Corroboration requires distinct source identities. Matching claims from sources
that share a parent/origin are not treated as independent evidence.
"""
from dataclasses import dataclass
from enum import Enum

class Corroboration(str, Enum):
    CONSISTENT = 'CONSISTENT'
    UNRESOLVED = 'UNRESOLVED'
    INDEPENDENCE_INSUFFICIENT = 'INDEPENDENCE_INSUFFICIENT'

@dataclass(frozen=True)
class ClaimObservation:
    claim_id: str
    source_id: str
    claim_text: str
    value: str
    origin_id: str | None = None


def corroborate(a: ClaimObservation, b: ClaimObservation) -> Corroboration:
    if a.source_id == b.source_id:
        return Corroboration.INDEPENDENCE_INSUFFICIENT
    if a.origin_id and b.origin_id and a.origin_id == b.origin_id:
        return Corroboration.INDEPENDENCE_INSUFFICIENT
    if a.value == b.value:
        return Corroboration.CONSISTENT
    return Corroboration.UNRESOLVED
