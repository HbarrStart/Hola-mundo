#!/usr/bin/env python3
"""MOS Alpha-29: provenance and source-dependency analysis.
Synthetic/local records only. Provenance does not establish truth.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class ProvenanceStatus(str, Enum):
    INDEPENDENT='INDEPENDENT'; DEPENDENT='DEPENDENT'; UNKNOWN='UNKNOWN'; CONFLICTING='CONFLICTING'

@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    upstream_source_ids: Tuple[str, ...] = ()

def classify(source: SourceRecord, known_sources: Tuple[SourceRecord, ...]) -> ProvenanceStatus:
    known = {s.source_id: s for s in known_sources}
    if not source.source_id.strip():
        raise ValueError('invalid_source_id')
    if source.source_id in source.upstream_source_ids:
        raise ValueError('self_dependency')
    if not source.upstream_source_ids:
        return ProvenanceStatus.INDEPENDENT
    if any(up in known for up in source.upstream_source_ids):
        return ProvenanceStatus.DEPENDENT
    return ProvenanceStatus.UNKNOWN

def dependency_closure(source_id: str, records: Tuple[SourceRecord, ...]) -> Tuple[str, ...]:
    graph = {r.source_id: r.upstream_source_ids for r in records}
    if source_id not in graph:
        return ()
    seen, stack = set(), list(graph[source_id])
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(graph.get(current, ()))
    return tuple(sorted(seen))
