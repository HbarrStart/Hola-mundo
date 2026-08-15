#!/usr/bin/env python3
"""MOS Alpha-43: tamper-evident signed audit events."""
from dataclasses import dataclass, asdict
import hashlib,hmac,json

@dataclass(frozen=True)
class SignedEvent:
    event_id:str
    action:str
    actor:str
    payload:dict
    previous_hash:str=''

def _canonical(e):
    return json.dumps(asdict(e),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()

def sign_event(e:SignedEvent, secret:bytes)->str:
    if not isinstance(secret,bytes) or not secret: raise ValueError('invalid_secret')
    if not all(isinstance(v,str) and v.strip() for v in (e.event_id,e.action,e.actor)): raise ValueError('invalid_event')
    if not isinstance(e.payload,dict): raise ValueError('invalid_payload')
    return hmac.new(secret,_canonical(e),hashlib.sha256).hexdigest()

def verify_event(e:SignedEvent, signature:str, secret:bytes)->bool:
    if not isinstance(signature,str) or not signature: return False
    try: expected=sign_event(e,secret)
    except ValueError: return False
    return hmac.compare_digest(expected,signature)
