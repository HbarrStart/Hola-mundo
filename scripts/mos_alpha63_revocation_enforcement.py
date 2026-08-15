#!/usr/bin/env python3
"""MOS Alpha-63: enforce revocation during attestation verification."""
from scripts.mos_alpha60_anchor_attestation import verify_attestation
from scripts.mos_alpha62_attestation_revocation import RevocationRegistry

def verify_with_revocation(attestation, secret:bytes, registry:RevocationRegistry)->bool:
    if registry is None or registry.is_revoked(attestation.signer): return False
    return verify_attestation(attestation,secret)
