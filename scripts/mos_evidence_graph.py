#!/usr/bin/env python3
"""Build a conservative evidence graph for MOS claims.

The graph distinguishes independent evidence from repeated reporting of the
same upstream source. It never upgrades a claim to confirmed status by itself.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

@dataclass(frozen=True)
class Source:
    id: str
    name: str
    source_class: str
    upstream_source_id: str | None = None

@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: str
    claim_id: str
    evidence_type: str
    retrieved_at: str
    content_hash: str | None = None

@dataclass
class GraphResult:
    independent_source_count: int = 0
    supporting_evidence: list[str] = field(default_factory=list)
    repeated_upstream_evidence: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)


def analyze_claim(claim_id: str, evidence: Iterable[Evidence], sources: dict[str, Source]) -> GraphResult:
    result = GraphResult()
    seen_upstreams: set[str] = set()
    seen_sources: set[str] = set()
    for item in evidence:
        if item.claim_id != claim_id:
            continue
        src = sources.get(item.source_id)
        if not src:
            result.missing_evidence.append(item.id)
            continue
        upstream = src.upstream_source_id or src.id
        if upstream in seen_upstreams:
            result.repeated_upstream_evidence.append(item.id)
            continue
        seen_upstreams.add(upstream)
        seen_sources.add(src.id)
        result.supporting_evidence.append(item.id)
    result.independent_source_count = len(seen_upstreams)
    return result

if __name__ == '__main__':
    print('MOS Evidence Graph loaded: source lineage aware / no auto-confirmation')
