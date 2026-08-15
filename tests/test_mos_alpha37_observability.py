import pytest
from scripts.mos_alpha37_observability import Health,HealthSnapshot,classify_health,safe_mode

def test_healthy(): assert classify_health(HealthSnapshot('api',100,1.0,True)) is Health.HEALTHY

def test_degraded_latency(): assert classify_health(HealthSnapshot('api',2000,1.0,True)) is Health.DEGRADED

def test_degraded_errors(): assert classify_health(HealthSnapshot('api',100,10,True)) is Health.DEGRADED

def test_down_dependency(): assert classify_health(HealthSnapshot('api',100,1,False)) is Health.DOWN

def test_missing_signal_is_unknown(): assert classify_health(HealthSnapshot('api',None,1,True)) is Health.UNKNOWN

def test_unknown_and_down_trigger_safe_mode():
    assert safe_mode(Health.UNKNOWN) and safe_mode(Health.DOWN)

def test_healthy_does_not_trigger_safe_mode(): assert not safe_mode(Health.HEALTHY)

def test_invalid_metrics_fail_closed():
    with pytest.raises(ValueError,match='invalid_health_metrics'): classify_health(HealthSnapshot('api',-1,1,True))
    with pytest.raises(ValueError,match='invalid_health_metrics'): classify_health(HealthSnapshot('api',100,101,True))

def test_invalid_service_fails_closed():
    with pytest.raises(ValueError,match='invalid_service'): classify_health(HealthSnapshot('',100,1,True))
