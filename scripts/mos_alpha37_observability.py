#!/usr/bin/env python3
"""MOS Alpha-37: deterministic operational health/observability signals."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Health(str, Enum):
    HEALTHY='HEALTHY'; DEGRADED='DEGRADED'; DOWN='DOWN'; UNKNOWN='UNKNOWN'

@dataclass(frozen=True)
class HealthSnapshot:
    service: str
    latency_ms: Optional[int]
    error_rate_pct: Optional[float]
    dependency_ok: Optional[bool]

def classify_health(s: HealthSnapshot) -> Health:
    if not s.service.strip(): raise ValueError('invalid_service')
    if s.latency_ms is None or s.error_rate_pct is None or s.dependency_ok is None:
        return Health.UNKNOWN
    if s.latency_ms < 0 or not 0 <= s.error_rate_pct <= 100:
        raise ValueError('invalid_health_metrics')
    if not s.dependency_ok:
        return Health.DOWN
    if s.error_rate_pct >= 10 or s.latency_ms >= 2000:
        return Health.DEGRADED
    return Health.HEALTHY

def safe_mode(health: Health) -> bool:
    return health in (Health.DOWN, Health.UNKNOWN)
