from scripts.mos_alpha53_audit_integrity import IntegrityEvent,verify_chain

def test_empty_chain_valid(): assert verify_chain([])
def test_valid_chain():
    a=IntegrityEvent(0,{'reason':'accepted'},''); b=IntegrityEvent(1,{'reason':'replay'},a.digest()); assert verify_chain([a,b])
def test_sequence_tamper_fails():
    a=IntegrityEvent(0,{'reason':'accepted'},''); b=IntegrityEvent(2,{'reason':'replay'},a.digest()); assert not verify_chain([a,b])
def test_previous_hash_tamper_fails():
    a=IntegrityEvent(0,{'reason':'accepted'},''); b=IntegrityEvent(1,{'reason':'replay'},'bad'); assert not verify_chain([a,b])
def test_decision_tamper_fails():
    a=IntegrityEvent(0,{'reason':'accepted'},''); original=a.digest(); b=IntegrityEvent(1,{'reason':'replay'},original); object.__setattr__(a,'decision',{'reason':'tampered'}); assert not verify_chain([a,b])
