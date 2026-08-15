#!/usr/bin/env python3
"""MOS Alpha-54: verified audit-chain integrity and anchoring."""
from dataclasses import dataclass
import hashlib,json

@dataclass(frozen=True)
class AuditRecord:
    seq:int; payload:dict; prev_hash:str; record_hash:str

def _canonical(seq,payload,prev_hash):
    return json.dumps({'seq':seq,'payload':payload,'prev_hash':prev_hash},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def make_record(seq,payload,prev_hash=''):
    if not isinstance(seq,int) or seq<0 or not isinstance(payload,dict) or not isinstance(prev_hash,str): raise ValueError('invalid_record')
    h=hashlib.sha256(_canonical(seq,payload,prev_hash)).hexdigest()
    return AuditRecord(seq,payload,prev_hash,h)

def verify_chain(records,anchor=''):
    expected_prev=anchor; expected_seq=0
    for r in records:
        if not isinstance(r,AuditRecord) or r.seq!=expected_seq or r.prev_hash!=expected_prev: return False
        if hashlib.sha256(_canonical(r.seq,r.payload,r.prev_hash)).hexdigest()!=r.record_hash: return False
        expected_prev=r.record_hash; expected_seq+=1
    return True
