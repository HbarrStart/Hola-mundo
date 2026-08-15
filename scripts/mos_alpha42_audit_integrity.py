#!/usr/bin/env python3
"""MOS Alpha-42: tamper-evident audit chain."""
from dataclasses import dataclass, asdict
import hashlib, json

@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    action: str
    actor: str
    payload: dict
    previous_hash: str = ''

def event_hash(event: AuditEvent) -> str:
    if not all(isinstance(v, str) and v.strip() for v in (event.event_id, event.action, event.actor)):
        raise ValueError('invalid_event')
    if not isinstance(event.payload, dict):
        raise ValueError('invalid_payload')
    raw=json.dumps(asdict(event), sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(raw.encode()).hexdigest()

def append_event(chain, event):
    expected=chain[-1]["hash"] if chain else ''
    if event.previous_hash != expected:
        raise ValueError('invalid_previous_hash')
    digest=event_hash(event)
    chain.append({"event":event,"hash":digest})
    return digest

def verify_chain(chain):
    previous=''
    for item in chain:
        event=item.get('event'); stored=item.get('hash')
        if not isinstance(event, AuditEvent) or event.previous_hash != previous or event_hash(event) != stored:
            return False
        previous=stored
    return True
