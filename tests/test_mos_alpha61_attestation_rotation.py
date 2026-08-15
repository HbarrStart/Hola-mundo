import pytest
from scripts.mos_alpha60_anchor_attestation import attest
from scripts.mos_alpha61_attestation_rotation import Rotation,rotate,active_signer

def test_rotation():
    a=attest(__import__('scripts.mos_alpha55_audit_anchor',fromlist=['Anchor']).Anchor(3,'3'*64),'old',b's'); r=rotate(a,'new',5,b's'); assert active_signer(r,4)=='old'; assert active_signer(r,5)=='new'
def test_bad_attestation():
    a=attest(__import__('scripts.mos_alpha55_audit_anchor',fromlist=['Anchor']).Anchor(3,'3'*64),'old',b's'); object.__setattr__(a,'mac','0'*64)
    with pytest.raises(ValueError,match='invalid_attestation'): rotate(a,'new',5,b's')
def test_bad_rotation():
    a=attest(__import__('scripts.mos_alpha55_audit_anchor',fromlist=['Anchor']).Anchor(3,'3'*64),'old',b's')
    with pytest.raises(ValueError,match='invalid_rotation'): rotate(a,'',5,b's')
    with pytest.raises(ValueError,match='invalid_rotation'): rotate(a,'new',3,b's')
def test_malformed_query():
    a=attest(__import__('scripts.mos_alpha55_audit_anchor',fromlist=['Anchor']).Anchor(3,'3'*64),'old',b's'); r=rotate(a,'new',5,b's'); assert active_signer(r,-1)==''
