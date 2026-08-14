from datetime import datetime, timezone, timedelta
from scripts.mos_alpha28_temporality import TemporalPolicy, TemporalStatus, classify

NOW=datetime(2026,8,14,16,0,tzinfo=timezone.utc)
POLICY=TemporalPolicy(freshness_seconds=3600, expiry_seconds=86400)

def stamp(seconds_ago): return (NOW-timedelta(seconds=seconds_ago)).isoformat().replace('+00:00','Z')

def test_fresh(): assert classify(stamp(3599),NOW,POLICY) is TemporalStatus.FRESH

def test_boundary_fresh(): assert classify(stamp(3600),NOW,POLICY) is TemporalStatus.FRESH

def test_stale(): assert classify(stamp(3601),NOW,POLICY) is TemporalStatus.STALE

def test_expired(): assert classify(stamp(86401),NOW,POLICY) is TemporalStatus.EXPIRED

def test_missing_or_invalid_timestamp_is_unknown():
    assert classify(None,NOW,POLICY) is TemporalStatus.UNKNOWN
    assert classify('not-a-time',NOW,POLICY) is TemporalStatus.UNKNOWN

def test_naive_timestamp_is_unknown(): assert classify('2026-08-14T15:00:00',NOW,POLICY) is TemporalStatus.UNKNOWN

def test_future_timestamp_is_unknown(): assert classify(stamp(-1),NOW,POLICY) is TemporalStatus.UNKNOWN

def test_superseded_takes_precedence(): assert classify(stamp(10),NOW,POLICY,True) is TemporalStatus.SUPERSEDED
