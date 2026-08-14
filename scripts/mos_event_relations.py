#!/usr/bin/env python3
"""Conservative event relationship vocabulary for MOS."""
from __future__ import annotations
from enum import Enum

class Relation(str, Enum):
    SAME_EVENT = 'SAME_EVENT'
    UPDATE = 'UPDATE'
    AFTERSHOCK_CANDIDATE = 'AFTERSHOCK_CANDIDATE'
    AFTERSHOCK_CONFIRMED = 'AFTERSHOCK_CONFIRMED'
    RELATED_EVENT = 'RELATED_EVENT'
    DIFFERENT_EVENT = 'DIFFERENT_EVENT'
    AMBIGUOUS = 'AMBIGUOUS'


def classify_aftershock_candidate(*, same_event: bool, temporal_order_known: bool, evidence_supports: bool) -> Relation:
    """Only classify a possible aftershock; never auto-confirm it."""
    if same_event:
        return Relation.SAME_EVENT
    if temporal_order_known and evidence_supports:
        return Relation.AFTERSHOCK_CANDIDATE
    return Relation.AMBIGUOUS
