import pytest
from scripts.mos_alpha43_signed_events import SignedEvent
from scripts.mos_alpha44_key_rotation import KeyRing,sign_event,verify_event

def e(): return SignedEvent('1','WRITE','agent',{'x':1})

def ring(): return KeyRing('v2',{'v1':b'old','v2':b'new'},'v1')

def test_active_key_signs_and_verifies():
    r=ring(); kid,s=sign_event(e(),r); assert kid=='v2' and verify_event(e(),kid,s,r)

def test_previous_key_has_grace_verification():
    r=ring(); old=KeyRing('v1',{'v1':b'old','v2':b'new'}); kid,s=sign_event(e(),old); assert verify_event(e(),kid,s,r)

def test_retired_key_is_rejected():
    r=KeyRing('v3',{'v2':b'new','v3':b'next'},'v2'); old=KeyRing('v1',{'v1':b'old'}); kid,s=sign_event(e(),old); assert not verify_event(e(),kid,s,r)

def test_wrong_signature_fails():
    r=ring(); assert not verify_event(e(),'v2','bad',r)

def test_invalid_configuration_fails_closed():
    with pytest.raises(ValueError): KeyRing('missing',{'v1':b'x'})
    with pytest.raises(ValueError): KeyRing('v2',{'v2':b''})

def test_tampering_fails():
    r=ring(); kid,s=sign_event(e(),r); assert not verify_event(SignedEvent('1','WRITE','agent',{'x':2}),kid,s,r)
