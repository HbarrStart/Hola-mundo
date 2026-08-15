from scripts.mos_alpha55_audit_anchor import Anchor
from scripts.mos_alpha60_anchor_attestation import attest
from scripts.mos_alpha62_attestation_revocation import RevocationRegistry
from scripts.mos_alpha63_revocation_enforcement import verify_with_revocation

def test_active_attestation_verifies():
    a=attest(Anchor(1,'1'*64),'sgc',b'k'); assert verify_with_revocation(a,b'k',RevocationRegistry())
def test_revoked_attestation_rejected():
    a=attest(Anchor(1,'1'*64),'sgc',b'k'); r=RevocationRegistry(); r.revoke('sgc','compromised',1); assert not verify_with_revocation(a,b'k',r)
def test_wrong_secret_rejected():
    a=attest(Anchor(1,'1'*64),'sgc',b'k'); assert not verify_with_revocation(a,b'bad',RevocationRegistry())
def test_missing_registry_fails_closed():
    a=attest(Anchor(1,'1'*64),'sgc',b'k'); assert not verify_with_revocation(a,b'k',None)
