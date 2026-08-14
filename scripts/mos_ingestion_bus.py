#!/usr/bin/env python3
"""MOS Alpha-9 ingestion bus.

Every incoming item is quarantined first. Ingestion preserves provenance and
never promotes an observation to a public fact.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib, json

@dataclass(frozen=True)
class Observation:
    observation_id: str
    source_id: str
    source_url: str
    observed_at: str | None
    received_at: str
    content: str
    content_sha256: str
    status: str = 'QUARANTINED'


def ingest(source_id: str, source_url: str, content: str, observed_at: str | None = None) -> Observation:
    if not source_id or not source_url or not content.strip():
        raise ValueError('missing_required_provenance_or_content')
    received_at = datetime.now(timezone.utc).isoformat()
    digest = hashlib.sha256(content.encode('utf-8')).hexdigest()
    observation_id = 'obs-' + digest[:16]
    return Observation(observation_id, source_id, source_url, observed_at, received_at, content, digest)


def to_json(obs: Observation) -> str:
    return json.dumps(asdict(obs), ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('MOS Ingestion Bus loaded: default state QUARANTINED')
