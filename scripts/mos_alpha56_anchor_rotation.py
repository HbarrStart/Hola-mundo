#!/usr/bin/env python3
"""MOS Alpha-56: deterministic audit-anchor rotation."""
from dataclasses import dataclass
from scripts.mos_alpha55_audit_anchor import Anchor,create_anchor,verify_anchor

@dataclass(frozen=True)
class AnchorRotation:
    previous: Anchor
    current: Anchor
    sequence: int

def rotate_anchor(records, previous: Anchor | None = None):
    current=create_anchor(records)
    if previous is not None and current.seq <= previous.seq:
        raise ValueError('non_monotonic_anchor')
    return AnchorRotation(previous,current,current.seq)

def verify_rotation(rotation: AnchorRotation, records)->bool:
    if not isinstance(rotation,AnchorRotation): return False
    if not verify_anchor(records,rotation.current): return False
    if rotation.previous is not None and rotation.current.seq <= rotation.previous.seq: return False
    return rotation.sequence == rotation.current.seq
