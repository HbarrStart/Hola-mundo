#!/usr/bin/env python3
"""MOS Alpha-10C: primary-source resolution state machine.

This module records what happened when MOS tried to resolve a claim against a
primary source. It never treats search failure as falsity and never invents a
primary event identifier.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ResolutionStatus(str, Enum):
    PRIMARY_FOUND = 'PRIMARY_FOUND'
    PRIMARY_UPDATED = 'PRIMARY_UPDATED'
    PRIMARY_NOT_FOUND = 'PRIMARY_NOT_FOUND'
    PRIMARY_UNAVAILABLE = 'PRIMARY_UNAVAILABLE'
    PRIMARY_CONFLICT = 'PRIMARY_CONFLICT'
    PRIMARY_RECORD_INVALID = 'PRIMARY_RECORD_INVALID'

@dataclass(frozen=True)
class PrimaryAttempt:
    source_id: str
    resolver_method: str  # API, OFFICIAL_PAGE, OFFICIAL_DOCUMENT
    attempted_at: str
    status: ResolutionStatus
    record_id: str | None = None
    evidence_ref: str | None = None
    notes: str | None = None


def resolve(attempt: PrimaryAttempt) -> PrimaryAttempt:
    if not attempt.source_id or not attempt.resolver_method or not attempt.attempted_at:
        raise ValueError('invalid_primary_resolution_attempt')
    if attempt.status in {ResolutionStatus.PRIMARY_FOUND, ResolutionStatus.PRIMARY_UPDATED} and not attempt.record_id:
        raise ValueError('primary_success_requires_record_id')
    if attempt.status in {ResolutionStatus.PRIMARY_FOUND, ResolutionStatus.PRIMARY_UPDATED} and not attempt.evidence_ref:
        raise ValueError('primary_success_requires_evidence_ref')
    return attempt

if __name__ == '__main__':
    print('MOS Primary Resolver loaded: no-found-is-not-false')
