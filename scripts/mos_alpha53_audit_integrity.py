#!/usr/bin/env python3
"""MOS Alpha-53: hash-chain integrity for audit decisions."""
from dataclasses import dataclass, asdict
import hashlib,json

@dataclass(frozen=True)
class IntegrityEvent:
    sequence:int
    decision:dict
    previous_hash:str=''
    def digest(self)->str:
        raw=json.dumps(asdict(self),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        return hashlib.sha256(raw).hexdigest()

def verify_chain(events):
    previous=''
    expected=0
    for event in events:
        if not isinstance(event,IntegrityEvent) or event.sequence!=expected or event.previous_hash!=previous:return False
        previous=event.digest(); expected+=1
    return True
