import pytest
from scripts.mos_alpha21_temporality import Observation, TemporalState, classify, displayable_now


def test_later_observation_without_supersession_is_unresolved():
    a = Observation('OBS-1','2026-08-14T14:00:00Z','closed')
    b = Observation('OBS-2','2026-08-14T15:20:00Z','open')
    assert classify(a,b) == TemporalState.UNRESOLVED
    assert displayable_now(b, TemporalState.UNRESOLVED) is False


def test_explicit_supersession_makes_later_observation_current():
    a = Observation('OBS-1','2026-08-14T14:00:00Z','closed')
    b = Observation('OBS-2','2026-08-14T15:20:00Z','open', supersedes_id='OBS-1')
    assert classify(a,b) == TemporalState.CURRENT
    assert displayable_now(b, TemporalState.CURRENT) is True


def test_same_value_can_remain_current():
    a = Observation('OBS-1','2026-08-14T14:00:00Z','closed')
    b = Observation('OBS-2','2026-08-14T15:20:00Z','closed')
    assert classify(a,b) == TemporalState.CURRENT
