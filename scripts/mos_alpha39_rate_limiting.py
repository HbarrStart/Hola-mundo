#!/usr/bin/env python3
"""MOS Alpha-39: bounded rate limiting and burst protection."""
from dataclasses import dataclass

@dataclass
class RateLimiter:
    capacity: int
    refill_per_second: float
    tokens: float = 0.0
    last_time: float = 0.0

    def __post_init__(self):
        if self.capacity <= 0 or self.refill_per_second <= 0:
            raise ValueError('invalid_rate_limit')
        self.tokens = float(self.capacity)

    def allow(self, now: float, cost: float = 1.0) -> bool:
        if now < self.last_time or cost <= 0 or cost > self.capacity:
            raise ValueError('invalid_request')
        elapsed = now - self.last_time
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_per_second)
        self.last_time = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
