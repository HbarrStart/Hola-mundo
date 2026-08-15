import pytest
from scripts.mos_alpha46_secure_envelope import Envelope,seal,verify

def test_seal_and_verify():
    e=seal({'x':1},'v1',b'secret'); assert verify(e,b'secret')
def test_tampered_payload_fails():
    e=seal({'x':1},'v1',b'secret'); object.__setattr__(e,'payload',{'x':2}); assert not verify(e,b'secret')
def test_tampered_signature_fails():
    e=seal({'x':1},'v1',b'secret'); object.__setattr__(e,'signature','0'*64); assert not verify(e,b'secret')
def test_wrong_secret_fails():
    e=seal({'x':1},'v1',b'secret'); assert not verify(e,b'other')
def test_algorithm_downgrade_fails():
    e=seal({'x':1},'v1',b'secret'); object.__setattr__(e,'algorithm','none'); assert not verify(e,b'secret')
def test_invalid_inputs_fail_closed():
    with pytest.raises(ValueError,match='invalid_payload'): seal([], 'v1', b'x')
    with pytest.raises(ValueError,match='invalid_key_id'): seal({}, '', b'x')
    with pytest.raises(ValueError,match='invalid_secret'): seal({}, 'v1', b'')
def test_malformed_envelope_rejected(): assert not verify({'key_id':'v1'},b'secret')
