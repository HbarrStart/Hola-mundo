#!/usr/bin/env python3
"""Conservative identity matching for emergency event observations.

This module NEVER confirms an event relationship from proximity alone. It
returns a candidate when independent observations are compatible and leaves
ambiguous cases unresolved for corroboration/human review.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from math import asin, cos, radians, sin, sqrt

@dataclass(frozen=True)
class Observation:
    id: str
    source: str
    event_type: str
    observed_at: str
    latitude: float | None = None
    longitude: float | None = None
    magnitude: float | None = None
    external_event_id: str | None = None

@dataclass(frozen=True)
class IdentityDecision:
    relation: str
    confidence: str
    reasons: tuple[str, ...]


def _distance_km(a: Observation, b: Observation) -> float | None:
    if None in (a.latitude, a.longitude, b.latitude, b.longitude):
        return None
    lat1, lon1, lat2, lon2 = map(radians, [a.latitude, a.longitude, b.latitude, b.longitude])
    dlat, dlon = lat2-lat1, lon2-lon1
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 6371.0 * 2 * asin(sqrt(h))


def _minutes(a: str, b: str) -> float | None:
    try:
        da = datetime.fromisoformat(a.replace('Z', '+00:00'))
        db = datetime.fromisoformat(b.replace('Z', '+00:00'))
        return abs((da - db).total_seconds()) / 60
    except (TypeError, ValueError):
        return None


def compare(a: Observation, b: Observation) -> IdentityDecision:
    if a.event_type != b.event_type:
        return IdentityDecision('DIFFERENT_EVENT', 'HIGH', ('event_type_mismatch',))

    if a.external_event_id and b.external_event_id and a.source == b.source:
        if a.external_event_id == b.external_event_id:
            return IdentityDecision('SAME_EVENT', 'HIGH', ('same_source_event_id',))
        return IdentityDecision('DIFFERENT_EVENT', 'HIGH', ('different_same_source_event_ids',))

    mins = _minutes(a.observed_at, b.observed_at)
    dist = _distance_km(a, b)
    mag_diff = None if None in (a.magnitude, b.magnitude) else abs(a.magnitude-b.magnitude)

    # These are intentionally only candidate thresholds, not confirmation rules.
    # Confirmation belongs to corroboration + Safety Gate, not this identity module.
    if a.event_type == 'earthquake':
        available = []
        if mins is not None: available.append(mins <= 10)
        if dist is not None: available.append(dist <= 80)
        if mag_diff is not None: available.append(mag_diff <= 0.6)
        if len(available) == 3 and all(available):
            return IdentityDecision('SAME_EVENT_CANDIDATE', 'MEDIUM', ('compatible_time_location_magnitude',))

    return IdentityDecision('AMBIGUOUS', 'LOW', ('insufficient_identity_evidence',))

if __name__ == '__main__':
    print('MOS Event Identity loaded: conservative / ambiguous-by-default')
