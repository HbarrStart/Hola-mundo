from scripts.mos_alpha64_report_gating import gate_report

def test_confirmed_report_allowed(): assert gate_report(verified=True,revoked=False,corroborated=True).allowed
def test_unverified_denied(): assert not gate_report(verified=False,revoked=False,corroborated=True).allowed
def test_revoked_denied(): assert not gate_report(verified=True,revoked=True,corroborated=True).allowed
def test_uncorroborated_denied(): assert not gate_report(verified=True,revoked=False,corroborated=False).allowed
def test_reason_confirmed(): assert gate_report(verified=True,revoked=False,corroborated=True).reason=='confirmed'
def test_revocation_precedes_verification(): assert gate_report(verified=False,revoked=True,corroborated=True).reason=='revoked_source'
def test_fail_closed_all_false(): assert not gate_report(verified=False,revoked=False,corroborated=False).allowed
