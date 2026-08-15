from scripts.mos_alpha65_evidence_state import EvidenceState,evidence_state,is_publishable

def test_unverified(): assert evidence_state(verified=False,corroborated=False,revoked=False) is EvidenceState.UNVERIFIED
def test_verified_not_corroborated(): assert evidence_state(verified=True,corroborated=False,revoked=False) is EvidenceState.VERIFIED
def test_corroborated_publishable():
    s=evidence_state(verified=True,corroborated=True,revoked=False); assert s is EvidenceState.CORROBORATED; assert is_publishable(s)
def test_revoked_wins(): assert evidence_state(verified=True,corroborated=True,revoked=True) is EvidenceState.REVOKED
def test_non_corroborated_not_publishable(): assert not is_publishable(EvidenceState.VERIFIED)
def test_unverified_not_publishable(): assert not is_publishable(EvidenceState.UNVERIFIED)
def test_revoked_not_publishable(): assert not is_publishable(EvidenceState.REVOKED)
