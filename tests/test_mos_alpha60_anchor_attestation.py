import pytest
from scripts.mos_alpha55_audit_anchor import Anchor
from scripts.mos_alpha60_anchor_attestation import Attestation,attest,verify_attestation

def test_attestation_verifies():
    a=attest(Anchor(3,'3'*64),'sgc',b'secret'); assert verify_attestation(a,b'secret')
def test_wrong_secret_rejected():
    a=attest(Anchor(3,'3'*64),'sgc',b'secret'); assert not verify_attestation(a,b'wrong')
def test_tampered_mac_rejected():
    a=attest(Anchor(3,'3'*64),'sgc',b'secret'); object.__setattr__(a,'mac','0'*64); assert not verify_attestation(a,b'secret')
def test_tampered_anchor_rejected():
    a=attest(Anchor(3,'3'*64),'sgc',b'secret'); object.__setattr__(a,'anchor',Anchor(4,'4'*64)); assert not verify_attestation(a,b'secret')
def test_invalid_signer_rejected():
    with pytest.raises(ValueError,match='invalid_attestation'): attest(Anchor(1,'1'*64),'',b's')
def test_invalid_secret_rejected():
    with pytest.raises(ValueError,match='invalid_secret'): attest(Anchor(1,'1'*64),'sgc',b'')
