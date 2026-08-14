"""Controlled Alpha-15 failure injection.

This test intentionally fails. It exists only on the dedicated failure-injection
branch so CI can prove that a failing security test produces a failing gate.
"""

def test_injected_failure_must_fail_ci():
    assert False, 'ALPHA15_INTENTIONAL_FAILURE: CI must turn red'
