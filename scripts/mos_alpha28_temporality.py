#!/usr/bin/env python3
"""MOS Alpha-28: conservative temporal freshness classification."""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

class TemporalStatus(str, Enum):
    FRESH='FRESH'; STALE='STALE'; EXPIRED='EXPIRED'; UNKNOWN='UNKNOWN'; SUPERSEDED='SUPERSEDED'

@dataclass(frozen=True)
class TemporalPolicy:
    freshness_seconds: int
    expiry_seconds: int | None = None


def classify(retrieved_at: str | None, now: datetime, policy: TemporalPolicy, superseded: bool=False) -> TemporalStatus:
    if superseded: return TemporalStatus.SUPERSEDED
    if not isinstance(retrieved_at, str) or not retrieved_at.strip(): return TemporalStatus.UNKNOWN
    try: ts=datetime.fromisoformat(retrieved_at.replace('Z','+00:00'))
    except (ValueError, TypeError): return TemporalStatus.UNKNOWN
    if ts.tzinfo is None: return TemporalStatus.UNKNOWN
    now_utc=now.astimezone(timezone.utc); ts_utc=ts.astimezone(timezone.utc)
    age=(now_utc-ts_utc).total_seconds()
    if age < 0: return TemporalStatus.UNKNOWN
    if policy.expiry_seconds is not None and age > policy.expiry_seconds: return TemporalStatus.EXPIRED
    if age > policy.freshness_seconds: return TemporalStatus.STALE
    return TemporalStatus.FRESH
