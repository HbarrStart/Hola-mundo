import pytest
from scripts.mos_alpha43_signed_events import SignedEvent,sign_event,verify_event

def e(payload=None): return SignedEvent('1','WRITE','agent',{} if payload is None else payload)

def test_sign_and_verify():
    s=sign_event(e({'x':1}),b'secret'); assert verify_event(e({'x':1}),s,b'secret')

def test_tampering_fails():
    s=sign_event(e({'x':1}),b'secret'); assert not verify_event(e({'x':2}),s,b'secret')

def test_wrong_secret_fails():
    s=sign_event(e(),b'secret'); assert not verify_event(e(),s,b'other')

def test_signature_is_deterministic(): assert sign_event(e(),b'secret') == sign_event(e(),b'secret')

def test_invalid_secret_fails_closed():
    with pytest.raises(ValueError,match='invalid_secret'): sign_event(e(),b'')

def test_invalid_event_fails_closed():
    with pytest.raises(ValueError,match='invalid_event'): sign_event(SignedEvent('','','',{}),b'x')

def test_invalid_payload_fails_closed():
    with pytest.raises(ValueError,match='invalid_payload'): sign_event(SignedEvent('1','WRITE','a',[]),b'x')

def test_malformed_signature_rejected(): assert not verify_event(e(),'bad',b'secret')
