import pytest
from scripts.mos_alpha40_circuit_breaker import CircuitBreaker,State

def test_opens_at_threshold():
    c=CircuitBreaker(3,2)
    for _ in range(3): c.record_failure()
    assert c.state is State.OPEN and not c.allow()

def test_open_ignores_additional_failures():
    c=CircuitBreaker(2,1); c.record_failure(); c.record_failure(); c.record_failure()
    assert c.state is State.OPEN

def test_probe_enters_half_open():
    c=CircuitBreaker(1,2); c.record_failure(); assert c.probe() and c.state is State.HALF_OPEN

def test_recovery_requires_configured_successes():
    c=CircuitBreaker(1,2); c.record_failure(); c.probe(); c.record_success(); assert c.state is State.HALF_OPEN; c.record_success(); assert c.state is State.CLOSED

def test_failure_during_half_open_reopens():
    c=CircuitBreaker(1,2); c.record_failure(); c.probe(); c.record_failure(); assert c.state is State.OPEN and not c.allow()

def test_invalid_configuration_fails_closed():
    with pytest.raises(ValueError): CircuitBreaker(0,1)
    with pytest.raises(ValueError): CircuitBreaker(1,0)

def test_closed_success_resets_failures():
    c=CircuitBreaker(3,2); c.record_failure(); c.record_failure(); c.record_success(); assert c.failures == 0 and c.state is State.CLOSED
