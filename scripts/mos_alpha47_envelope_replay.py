#!/usr/bin/env python3
"""MOS Alpha-47: replay protection for authenticated envelopes."""
from dataclasses import dataclass
from scripts.mos_alpha46_secure_envelope import Envelope, seal, verify

@dataclass
class EnvelopeReplayGuard:
    _seen: set[str]

    def __init__(self):
        self._seen=set()

    def accept(self, envelope: Envelope, secret: bytes) -> bool:
        if not verify(envelope, secret):
            return False
        fingerprint=f'{envelope.key_id}:{envelope.signature}'
        if fingerprint in self._seen:
            return False
        self._seen.add(fingerprint)
        return True
