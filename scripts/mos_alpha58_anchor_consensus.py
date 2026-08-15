#!/usr/bin/env python3
"""MOS Alpha-58: deterministic consensus for anchor observations."""
from dataclasses import dataclass
from scripts.mos_alpha55_audit_anchor import Anchor

@dataclass(frozen=True)
class AnchorObservation:
    source: str
    anchor: Anchor

def reach_consensus(observations):
    if not observations: raise ValueError('empty_observations')
    if any(not isinstance(o,AnchorObservation) or not o.source.strip() for o in observations): raise ValueError('invalid_observation')
    anchors={o.anchor for o in observations}
    if len(anchors)!=1: raise ValueError('anchor_conflict')
    return next(iter(anchors))

def verify_consensus(observations,expected:Anchor)->bool:
    if not isinstance(expected,Anchor): return False
    try: return reach_consensus(observations)==expected
    except ValueError: return False
