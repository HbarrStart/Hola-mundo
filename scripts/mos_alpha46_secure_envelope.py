#!/usr/bin/env python3
"""MOS Alpha-46: authenticated envelope for signed audit events."""
from dataclasses import dataclass
import hashlib,hmac,json

@dataclass(frozen=True)
class Envelope:
    key_id:str
    algorithm:str
    payload:dict
    signature:str

def _canonical(key_id,algorithm,payload):
    return json.dumps({'key_id':key_id,'algorithm':algorithm,'payload':payload},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def seal(payload,key_id,secret):
    if not isinstance(payload,dict): raise ValueError('invalid_payload')
    if not isinstance(key_id,str) or not key_id.strip(): raise ValueError('invalid_key_id')
    if not isinstance(secret,bytes) or not secret: raise ValueError('invalid_secret')
    alg='HMAC-SHA256'
    sig=hmac.new(secret,_canonical(key_id,alg,payload),hashlib.sha256).hexdigest()
    return Envelope(key_id,alg,payload,sig)

def verify(envelope,secret):
    if not isinstance(envelope,Envelope) or envelope.algorithm!='HMAC-SHA256': return False
    if not isinstance(secret,bytes) or not secret: return False
    expected=hmac.new(secret,_canonical(envelope.key_id,envelope.algorithm,envelope.payload),hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,envelope.signature)
