#!/usr/bin/env python3
"""MOS Alpha-68: quorum decision over corroborated evidence."""
from dataclasses import dataclass
@dataclass(frozen=True)
class QuorumResult:
    reached: bool
    sources: tuple[str,...]
def source_quorum(sources, minimum=2):
    unique=tuple(sorted(set(sources)))
    return QuorumResult(len(unique)>=minimum, unique)
