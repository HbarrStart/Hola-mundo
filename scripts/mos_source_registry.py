#!/usr/bin/env python3
"""Validate MOS source registry entries before a connector may use them."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'data/source_registry.json'
ALLOWED_CLASSES={'PRIMARY','SECONDARY','TERTIARY'}
BLOCKED_STATUS={'REVOKED','DISABLED'}

def load_registry():
    data=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if not isinstance(data.get('sources'),list):
        raise ValueError('invalid source registry')
    seen=set()
    for s in data['sources']:
        sid=s.get('id')
        if not sid or sid in seen: raise ValueError('missing or duplicate source id')
        seen.add(sid)
        if s.get('class') not in ALLOWED_CLASSES: raise ValueError(f'invalid source class: {sid}')
        if s.get('status') in BLOCKED_STATUS: raise ValueError(f'blocked source: {sid}')
    return data

if __name__=='__main__':
    registry=load_registry()
    print(f"MOS source registry OK: {len(registry['sources'])} source identities")
