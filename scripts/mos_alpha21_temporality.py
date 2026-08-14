#!/usr/bin/env python3
"""MOS Alpha-21: temporal validity without inventing supersession."""
from dataclasses import dataclass
from enum import Enum

class TemporalState(str, Enum):
    CURRENT = 'CURRENT'
    HISTORICAL = 'HISTORICAL'
    UNRESOLVED = 'UNRESOLVED'

@dataclass(frozen=True)
class Observation:
    observation_id: str
    observed_at: str
    value: str
    supersedes_id: str | None = None


def classify(previous: Observation, later: Observation) -> TemporalState:
    if later.supersedes_id == previous.observation_id:
        return TemporalState.CURRENT
    if later.value == previous.value:
        return TemporalState.CURRENT
    return TemporalState.UNRESOLVED


def displayable_now(observation: Observation, state: TemporalState) -> bool:
    return state == TemporalState.CURRENT
