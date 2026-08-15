from scripts.mos_alpha42_audit_integrity import AuditEvent, append_event, verify_chain

def test_alpha42_ci_probe():
    chain=[]
    h=append_event(chain, AuditEvent('probe-1','CI','github',{}))
    append_event(chain, AuditEvent('probe-2','CI','github',{},h))
    assert verify_chain(chain)
