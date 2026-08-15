#!/usr/bin/env python3
"""MOS Alpha-45: explicit key revocation and fail-closed verification."""
from dataclasses import dataclass
from scripts.mos_alpha43_signed_events import SignedEvent, _canonical
import hashlib, hmac

@dataclass(frozen=True)
class RevocationSet:
    revoked: frozenset[str] = frozenset()
    def __post_init__(self):
        if not isinstance(self.revoked, frozenset) or any(not isinstance(k,str) or not k for k in self.revoked):
            raise ValueError('invalid_revocations')
    def is_revoked(self, key_id:str)->bool: return key_id in self.revoked

def verify_event(e:SignedEvent,key_id:str,signature:str,keyring,revocations:RevocationSet)->bool:
    if revocations.is_revoked(key_id): return False
    if not isinstance(signature,str) or not signature or key_id not in keyring: return False
    try:
        expected=hmac.new(keyring[key_id],_canonical(e),hashlib.sha256).hexdigest()
    except (TypeError,ValueError): return False
    return hmac.compare_digest(expected,signature)
