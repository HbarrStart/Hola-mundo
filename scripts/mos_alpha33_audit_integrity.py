#!/usr/bin/env python3
"""MOS Alpha-33: tamper-evident audit chain."""
import hashlib, json
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class AuditRecord:
    event_id: str
    timestamp: str
    event_type: str
    payload: object
    previous_hash: str
    record_hash: str

def _canonical(event_id,timestamp,event_type,payload,previous_hash):
    return json.dumps({'event_id':event_id,'timestamp':timestamp,'event_type':event_type,'payload':payload,'previous_hash':previous_hash}, sort_keys=True, ensure_ascii=False, separators=(',',':'))

def make_record(event_id,timestamp,event_type,payload,previous_hash='') -> AuditRecord:
    if not all(isinstance(x,str) and x.strip() for x in (event_id,timestamp,event_type)):
        raise ValueError('invalid_audit_metadata')
    data=_canonical(event_id,timestamp,event_type,payload,previous_hash)
    digest=hashlib.sha256(data.encode('utf-8')).hexdigest()
    return AuditRecord(event_id,timestamp,event_type,payload,previous_hash,digest)

def verify_record(record: AuditRecord) -> bool:
    expected=make_record(record.event_id,record.timestamp,record.event_type,record.payload,record.previous_hash).record_hash
    return expected == record.record_hash

def verify_chain(records: Tuple[AuditRecord,...]) -> bool:
    previous=''
    seen=set()
    for record in records:
        if record.event_id in seen or not verify_record(record) or record.previous_hash != previous:
            return False
        seen.add(record.event_id); previous=record.record_hash
    return True
