#!/usr/bin/env python3
"""MOS Alpha-59: threshold quorum for anchor observations."""
from dataclasses import dataclass
from scripts.mos_alpha55_audit_anchor import Anchor

@dataclass(frozen=True)
class AnchorObservation:
    source: str
    anchor: Anchor

def reach_quorum(observations, quorum:int):
    if not isinstance(quorum,int) or quorum<=0: raise ValueError('invalid_quorum')
    if not observations: raise ValueError('empty_observations')
    if any(not isinstance(o,AnchorObservation) or not o.source.strip() or not isinstance(o.anchor,Anchor) for o in observations):
        raise ValueError('invalid_observation')
    counts={}
    for o in observations: counts[o.anchor]=counts.get(o.anchor,0)+1
    winners=[a for a,n in counts.items() if n>=quorum]
    if len(winners)!=1: raise ValueError('quorum_conflict')
    return winners[0]

def verify_quorum(observations,expected:Anchor,quorum:int)->bool:
    if not isinstance(expected,Anchor): return False
    try: return reach_quorum(observations,quorum)==expected
    except ValueError: return False
