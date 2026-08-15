from scripts.mos_alpha46_secure_envelope import seal
from scripts.mos_alpha51_replay_audit import ReplayAuditor

def test_decisions_are_audited():
    a=ReplayAuditor(10); e=seal({'x':1},'v1',b'k')
    assert a.accept(e,b'k',100).reason=='accepted'
    assert a.accept(e,b'k',101).reason=='replay'
    assert [d.reason for d in a.history()]==['accepted','replay']

def test_invalid_signature_is_audited():
    a=ReplayAuditor(10); e=seal({'x':1},'v1',b'k'); object.__setattr__(e,'signature','bad')
    assert a.accept(e,b'k',100).reason=='invalid_signature'
    assert len(a.history())==1

def test_invalid_time_is_audited():
    a=ReplayAuditor(10); e=seal({'x':1},'v1',b'k')
    assert a.accept(e,b'k',-1).reason=='invalid_time'

def test_history_is_immutable_view():
    a=ReplayAuditor(10); e=seal({'x':1},'v1',b'k'); a.accept(e,b'k',1)
    h=a.history(); assert isinstance(h,tuple); assert len(h)==1

def test_prune_does_not_remove_history():
    a=ReplayAuditor(10); e=seal({'x':1},'v1',b'k'); a.accept(e,b'k',100); a.prune(111)
    assert len(a.history())==1
