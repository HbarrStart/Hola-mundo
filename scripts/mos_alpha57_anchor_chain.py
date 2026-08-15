#!/usr/bin/env python3
"""MOS Alpha-57: explicit anchor-chain verification."""
from dataclasses import dataclass
from scripts.mos_alpha55_audit_anchor import Anchor

@dataclass(frozen=True)
class AnchorLink:
    previous: Anchor | None
    current: Anchor

def link_anchor(previous: Anchor | None, current: Anchor) -> AnchorLink:
    if not isinstance(current, Anchor): raise ValueError('invalid_anchor')
    if previous is not None and current.seq <= previous.seq: raise ValueError('non_monotonic_anchor')
    return AnchorLink(previous,current)

def verify_anchor_chain(links)->bool:
    if not isinstance(links,(list,tuple)) or not links: return False
    prev=None
    for link in links:
        if not isinstance(link,AnchorLink): return False
        if link.previous != prev: return False
        if prev is not None and link.current.seq <= prev.seq: return False
        prev=link.current
    return True
