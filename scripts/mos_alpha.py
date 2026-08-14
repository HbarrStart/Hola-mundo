#!/usr/bin/env python3
"""Mission Alpha: deterministic end-to-end MOS pipeline using supplied observations.

Safety rule: no network calls, no invented observations, no autonomous publication.
The script demonstrates the complete data path and emits HOLD unless a claim
has explicit source/evidence and passes the configured safety conditions.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'data'/'alpha_observations.json'
OUT=ROOT/'data'/'alpha_result.json'


def main():
    raw=json.loads(INPUT.read_text(encoding='utf-8'))
    observations=raw.get('observations',[])
    claims=[]
    for o in observations:
        claim={
            'id': f"ALPHA-{o.get('id')}",
            'title': o.get('title'),
            'summary': o.get('summary'),
            'observed_at': o.get('observed_at'),
            'received_at': datetime.now(timezone.utc).isoformat(),
            'verification_state':'PENDING_VERIFICATION',
            'risk':'MEDIUM',
            'sources':[{'name':o.get('source'),'url':o.get('source_url'),'retrieved_at':datetime.now(timezone.utc).isoformat()}],
            'evidence_types':o.get('evidence_types',[]),
            'event_id':o.get('event_id')
        }
        # Alpha deliberately stops here: source data is not promoted to fact
        # without an explicit corroboration record and Safety Gate decision.
        claims.append(claim)
    result={
        'mission':'ALPHA',
        'status':'HOLD',
        'reason':'No claim is promoted automatically from ingestion to public fact.',
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'claims':claims,
        'public_situation':[]
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
