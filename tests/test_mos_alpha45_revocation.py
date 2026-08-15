import hashlib,hmac,pytest
from scripts.mos_alpha43_signed_events import SignedEvent,_canonical
from scripts.mos_alpha45_revocation import RevocationSet,verify_event

def e(): return SignedEvent('1','WRITE','agent',{'x':1})
def sig(k=b'old'): return hmac.new(k,_canonical(e()),hashlib.sha256).hexdigest()

def test_valid_key_verifies():
    assert verify_event(e(),'v1',sig(),{'v1':b'old'},RevocationSet())
def test_revoked_key_is_rejected():
    assert not verify_event(e(),'v1',sig(),{'v1':b'old'},RevocationSet(frozenset({'v1'})))
def test_unknown_key_rejected():
    assert not verify_event(e(),'missing',sig(),{'v1':b'old'},RevocationSet())
def test_malformed_signature_rejected():
    assert not verify_event(e(),'v1','bad',{'v1':b'old'},RevocationSet())
def test_invalid_revocation_set_fails_closed():
    with pytest.raises(ValueError,match='invalid_revocations'): RevocationSet(frozenset({''}))
def test_tampering_rejected():
    assert not verify_event(SignedEvent('1','WRITE','agent',{'x':2}),'v1',sig(),{'v1':b'old'},RevocationSet())
