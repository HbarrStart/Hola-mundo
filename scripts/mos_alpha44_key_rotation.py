#!/usr/bin/env python3
"""MOS Alpha-44: versioned HMAC key rotation with grace-period verification."""
from dataclasses import dataclass
import hashlib,hmac
from scripts.mos_alpha43_signed_events import SignedEvent,_canonical

@dataclass(frozen=True)
class KeyRing:
    active_id:str
    keys:dict
    previous_id:str|None=None

    def __post_init__(self):
        if not self.active_id or self.active_id not in self.keys: raise ValueError('invalid_active_key')
        if self.previous_id is not None and self.previous_id not in self.keys: raise ValueError('invalid_previous_key')
        if not all(isinstance(k,str) and k and isinstance(v,bytes) and v for k,v in self.keys.items()): raise ValueError('invalid_key_material')

def sign_event(e:SignedEvent, ring:KeyRing)->tuple[str,str]:
    key=ring.keys[ring.active_id]
    return ring.active_id,hmac.new(key,_canonical(e),hashlib.sha256).hexdigest()

def verify_event(e:SignedEvent,key_id:str,signature:str,ring:KeyRing)->bool:
    if key_id not in ring.keys or not isinstance(signature,str) or not signature:return False
    if key_id not in (ring.active_id,ring.previous_id):return False
    expected=hmac.new(ring.keys[key_id],_canonical(e),hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,signature)
