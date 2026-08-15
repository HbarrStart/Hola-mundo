#!/usr/bin/env python3
"""MOS Alpha-69: deterministic consistency checks across corroborating sources."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Observation:
    source: str
    claim: str
    verified: bool = False
    revoked: bool = False

def consistent(observations: Iterable[Observation]) -> bool:
    valid=[o for o in observations if o.verified and not o.revoked]
    claims={o.claim for o in valid}
    return len(claims)==1 and bool(valid)

def consistent_sources(observations: Iterable[Observation]) -> tuple[str,...]:
    valid=[o for o in observations if o.verified and not o.revoked]
    if not consistent(valid): return ()
    return tuple(sorted({o.source for o in valid}))
