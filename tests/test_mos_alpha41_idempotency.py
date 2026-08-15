import pytest
from scripts.mos_alpha41_idempotency import Operation,ReplayGuard,idempotency_key

def op(payload=None): return Operation('agent-1','WRITE','resource-1',{} if payload is None else payload)

def test_key_is_deterministic(): assert idempotency_key(op({'b':2,'a':1})) == idempotency_key(op({'a':1,'b':2}))

def test_replay_is_rejected():
    g=ReplayGuard(); assert g.accept(op({'x':1})); assert not g.accept(op({'x':1}))

def test_distinct_payloads_are_distinct():
    g=ReplayGuard(); assert g.accept(op({'x':1})); assert g.accept(op({'x':2}))

def test_invalid_operation_fails_closed():
    with pytest.raises(ValueError,match='invalid_operation'): idempotency_key(Operation('','WRITE','r',{}))

def test_invalid_payload_fails_closed():
    with pytest.raises(ValueError,match='invalid_payload'): idempotency_key(Operation('a','WRITE','r',[]))

def test_replay_guard_does_not_mutate_on_rejection():
    g=ReplayGuard(); item=op({'x':1}); assert g.accept(item); assert not g.accept(item); assert not g.accept(item)
