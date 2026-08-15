import pytest
from scripts.mos_alpha42_audit_integrity import AuditEvent,event_hash,append_event,verify_chain

def ev(i, prev='', payload=None): return AuditEvent(str(i),'WRITE','agent-1',{} if payload is None else payload,prev)

def test_chain_appends_and_verifies():
    c=[]; h1=append_event(c,ev(1)); append_event(c,ev(2,h1)); assert verify_chain(c)

def test_wrong_previous_hash_rejected():
    with pytest.raises(ValueError,match='invalid_previous_hash'): append_event([],ev(1,'wrong'))

def test_tampering_is_detected():
    c=[]; h=append_event(c,ev(1)); append_event(c,ev(2,h)); c[0]['event']=ev(1,payload={'tampered':True}); assert not verify_chain(c)

def test_stored_hash_tampering_is_detected():
    c=[]; append_event(c,ev(1)); c[0]['hash']='0'*64; assert not verify_chain(c)

def test_invalid_event_fails_closed():
    with pytest.raises(ValueError,match='invalid_event'): event_hash(ev(''))

def test_invalid_payload_fails_closed():
    with pytest.raises(ValueError,match='invalid_payload'): event_hash(AuditEvent('1','WRITE','agent',[]))

def test_empty_chain_is_valid(): assert verify_chain([])
