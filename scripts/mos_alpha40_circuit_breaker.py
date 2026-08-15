#!/usr/bin/env python3
"""MOS Alpha-40: fail-closed circuit breaker for unstable dependencies."""
from dataclasses import dataclass
from enum import Enum

class State(str, Enum):
    CLOSED='CLOSED'; OPEN='OPEN'; HALF_OPEN='HALF_OPEN'

@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    recovery_successes: int = 2
    state: State = State.CLOSED
    failures: int = 0
    successes: int = 0

    def __post_init__(self):
        if self.failure_threshold < 1 or self.recovery_successes < 1:
            raise ValueError('invalid_configuration')

    def allow(self) -> bool:
        return self.state != State.OPEN

    def record_failure(self) -> None:
        if self.state == State.OPEN:
            return
        self.failures += 1; self.successes = 0
        if self.failures >= self.failure_threshold:
            self.state = State.OPEN

    def probe(self) -> bool:
        if self.state != State.OPEN:
            return self.allow()
        self.state = State.HALF_OPEN
        self.successes = 0
        return True

    def record_success(self) -> None:
        if self.state == State.OPEN:
            return
        self.failures = 0
        if self.state == State.HALF_OPEN:
            self.successes += 1
            if self.successes >= self.recovery_successes:
                self.state = State.CLOSED
        else:
            self.successes = 0
