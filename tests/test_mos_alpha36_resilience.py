import pytest
from scripts.mos_alpha36_resilience import ServiceState,SafeMode,choose_mode

def test_healthy_normal(): assert choose_mode(ServiceState.HEALTHY,True,True) is SafeMode.NORMAL

def test_degraded_requires_human_review(): assert choose_mode(ServiceState.DEGRADED,True,True) is SafeMode.HUMAN_REVIEW

def test_unavailable_holds(): assert choose_mode(ServiceState.UNAVAILABLE,True,True) is SafeMode.HOLD

def test_missing_evidence_holds(): assert choose_mode(ServiceState.HEALTHY,True,False) is SafeMode.HOLD

def test_invalid_audit_always_holds():
    for state in ServiceState:
        assert choose_mode(state,False,True) is SafeMode.HOLD

def test_no_automatic_execution_in_degraded_mode(): assert choose_mode(ServiceState.DEGRADED,True,True) is not SafeMode.NORMAL
