import pytest
from scripts.mos_alpha39_rate_limiting import RateLimiter

def test_burst_is_bounded():
    r=RateLimiter(2,1)
    assert r.allow(0) and r.allow(0) and not r.allow(0)

def test_refill_restores_capacity():
    r=RateLimiter(2,1)
    assert r.allow(0) and r.allow(0) and not r.allow(0)
    assert r.allow(1)

def test_never_exceeds_capacity_after_long_idle():
    r=RateLimiter(2,1)
    assert r.allow(0) and r.allow(0)
    with pytest.raises(ValueError,match='invalid_request'): r.allow(100, 3)

def test_invalid_configuration_fails_closed():
    with pytest.raises(ValueError,match='invalid_rate_limit'): RateLimiter(0,1)
    with pytest.raises(ValueError,match='invalid_rate_limit'): RateLimiter(1,0)

def test_time_cannot_move_backward():
    r=RateLimiter(2,1); r.allow(10)
    with pytest.raises(ValueError,match='invalid_request'): r.allow(9)

def test_invalid_cost_fails_closed():
    r=RateLimiter(2,1)
    with pytest.raises(ValueError,match='invalid_request'): r.allow(0,0)
    with pytest.raises(ValueError,match='invalid_request'): r.allow(0,3)
