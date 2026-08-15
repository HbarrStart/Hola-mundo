#!/usr/bin/env python3
"""MOS Alpha-66: deterministic source priority for emergency evidence."""
from dataclasses import dataclass
from enum import IntEnum
class SourceTier(IntEnum): PRIMARY=1; SECONDARY=2; COMMUNITY=3
@dataclass(frozen=True)
class Source:
    name:str
    tier:SourceTier
    active:bool=True
def prioritize(sources):
    active=[s for s in sources if s.active]
    return tuple(sorted(active,key=lambda s:(s.tier,s.name)))
def primary_sources(sources): return tuple(s for s in prioritize(sources) if s.tier is SourceTier.PRIMARY)
