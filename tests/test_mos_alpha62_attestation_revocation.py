import pytest
from scripts.mos_alpha62_attestation_revocation import RevocationRegistry

def test_revoke_and_lookup():
    r=RevocationRegistry(); x=r.revoke('sgc','compromised',10); assert r.is_revoked('sgc'); assert r.get('sgc')==x

def test_active_signers_filters_revoked():
    r=RevocationRegistry(); r.revoke('bad','incident',10); assert r.active_signers(['good','bad','other'])==('good','other')

def test_invalid_revocation_rejected():
    r=RevocationRegistry()
    with pytest.raises(ValueError,match='invalid_revocation'): r.revoke('', 'x', 1)

def test_negative_timestamp_rejected():
    r=RevocationRegistry()
    with pytest.raises(ValueError,match='invalid_revocation'): r.revoke('sgc','x',-1)

def test_unknown_signer_not_revoked():
    r=RevocationRegistry(); assert not r.is_revoked('unknown'); assert r.get('unknown') is None

def test_revoke_updates_reason_and_timestamp():
    r=RevocationRegistry(); r.revoke('sgc','old',1); x=r.revoke('sgc','new',2); assert x.reason=='new' and x.timestamp==2
