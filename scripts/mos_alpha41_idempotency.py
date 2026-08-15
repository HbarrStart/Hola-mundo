#!/usr/bin/env python3
"""MOS Alpha-41: deterministic idempotency keys and replay protection."""
from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class Operation:
    actor: str
    action: str
    resource: str
    payload: dict

def idempotency_key(op: Operation) -> str:
    if not all(isinstance(v, str) and v.strip() for v in (op.actor, op.action, op.resource)):
        raise ValueError('invalid_operation')
    if not isinstance(op.payload, dict):
        raise ValueError('invalid_payload')
    raw=json.dumps({'actor':op.actor,'action':op.action,'resource':op.resource,'payload':op.payload},sort_keys=True,ensure_ascii=False,separators=(',',':'))
    return hashlib.sha256(raw.encode()).hexdigest()

class ReplayGuard:
    def __init__(self): self._seen={}
    def accept(self, op: Operation) -> bool:
        key=idempotency_key(op)
        if key in self._seen: return False
        self._seen[key]=True
        return True
