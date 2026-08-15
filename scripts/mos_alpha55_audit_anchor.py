#!/usr/bin/env python3
"""MOS Alpha-55: immutable audit-chain anchoring."""
from dataclasses import dataclass
import hashlib,json
from scripts.mos_alpha54_audit_integrity import AuditRecord,make_record,verify_chain

@dataclass(frozen=True)
class Anchor:
    seq:int
    record_hash:str

def create_anchor(records):
    if not verify_chain(records): raise ValueError('invalid_chain')
    if not records: raise ValueError('empty_chain')
    last=records[-1]
    return Anchor(last.seq,last.record_hash)

def verify_anchor(records,anchor:Anchor)->bool:
    if not isinstance(anchor,Anchor): return False
    if not records: return False
    if not verify_chain(records): return False
    last=records[-1]
    return last.seq==anchor.seq and last.record_hash==anchor.record_hash
