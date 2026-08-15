#!/usr/bin/env python3
"""MOS Alpha-48: bounded replay protection with deterministic timestamps."""
from dataclasses import dataclass
from scripts.mos_alpha46_secure_envelope import Envelope, verify

@dataclass
class ReplayWindow:
    ttl_seconds: int
    _seen: dict

    def __init__(self, ttl_seconds: int):
        if not isinstance(ttl_seconds, int) or ttl_seconds <= 0:
            raise ValueError('invalid_ttl')
        self.ttl_seconds = ttl_seconds
        self._seen = {}

    def accept(self, envelope: Envelope, secret: bytes, now: int) -> bool:
        if not isinstance(now, int) or now < 0 or not verify(envelope, secret):
            return False
        fingerprint=f'{envelope.key_id}:{envelope.signature}'
        timestamp=self._seen.get(fingerprint)
        if timestamp is not None:
            if now - timestamp < self.ttl_seconds:
                return False
            del self._seen[fingerprint]
        self._seen[fingerprint]=now
        return True
