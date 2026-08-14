#!/usr/bin/env python3
"""MOS Alpha-12 Common Operational Picture (COP).

The COP is a projection layer over already-gated claims. It never creates
facts, derives precise locations from vague text, or bypasses Safety Gate.
"""
from __future__ import annotations
from dataclasses import dataclass

ALLOWED = {'ALLOW','ALLOW_WITH_CONTEXT'}

@dataclass(frozen=True)
class MapClaim:
    claim_id: str
    title: str
    latitude: float | None
    longitude: float | None
    decision: str
    risk: str
    updated_at: str
    location_precision: str = 'UNKNOWN'
    sensitive: bool = False


def project(claim: MapClaim) -> dict:
    if claim.decision not in ALLOWED:
        return {'claim_id': claim.claim_id, 'visible': False, 'reason': 'not_publicly_gated'}
    if claim.sensitive:
        return {'claim_id': claim.claim_id, 'visible': False, 'reason': 'sensitive_location'}
    if claim.latitude is None or claim.longitude is None:
        return {'claim_id': claim.claim_id, 'visible': True, 'location': None,
                'reason': 'location_unresolved', 'title': claim.title,
                'risk': claim.risk, 'updated_at': claim.updated_at}
    if claim.location_precision == 'UNKNOWN':
        return {'claim_id': claim.claim_id, 'visible': True, 'location': None,
                'reason': 'precision_unknown', 'title': claim.title,
                'risk': claim.risk, 'updated_at': claim.updated_at}
    return {'claim_id': claim.claim_id, 'visible': True,
            'location': {'lat': claim.latitude, 'lon': claim.longitude,
                         'precision': claim.location_precision},
            'title': claim.title, 'risk': claim.risk, 'updated_at': claim.updated_at}

if __name__ == '__main__':
    print('MOS COP loaded: gated map projection')
