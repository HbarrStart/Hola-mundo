#!/usr/bin/env python3
"""MOS Alpha-67: deterministic corroboration window for emergency evidence."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

@dataclass(frozen=True)
class Evidence:
    source: str
    observed_at: datetime
    verified: bool = False
    revoked: bool = False

def in_window(evidence: Evidence, now: datetime, window: timedelta) -> bool:
    if evidence.revoked or not evidence.verified: return False
    return now - window <= evidence.observed_at <= now

def corroborated(evidence, now, window, minimum=2) -> bool:
    valid=[e for e in evidence if in_window(e,now,window)]
    return len({e.source for e in valid}) >= minimum
