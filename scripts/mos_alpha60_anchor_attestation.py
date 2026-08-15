#!/usr/bin/env python3
"""MOS Alpha-60: signed-style attestation for a consensus anchor."""
from dataclasses import dataclass
import hashlib,hmac
from scripts.mos_alpha55_audit_anchor import Anchor

@dataclass(frozen=True)
class Attestation:
    anchor: Anchor
    signer: str
    mac: str

def _payload(anchor,signer): return f'{anchor.seq}:{anchor.record_hash}:{signer}'.encode()
def attest(anchor:Anchor,signer:str,secret:bytes)->Attestation:
    if not isinstance(anchor,Anchor) or not signer.strip(): raise ValueError('invalid_attestation')
    if not isinstance(secret,bytes) or not secret: raise ValueError('invalid_secret')
    mac=hmac.new(secret,_payload(anchor,signer),hashlib.sha256).hexdigest()
    return Attestation(anchor,signer,mac)
def verify_attestation(a:Attestation,secret:bytes)->bool:
    if not isinstance(a,Attestation) or not isinstance(secret,bytes) or not secret: return False
    expected=hmac.new(secret,_payload(a.anchor,a.signer),hashlib.sha256).hexdigest()
    return hmac.compare_digest(a.mac,expected)
