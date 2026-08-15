import pytest
from scripts.mos_alpha46_secure_envelope import seal
from scripts.mos_alpha49_replay_store import ReplayStore

def test_accept_and_replay_reject():
    s=ReplayStore(10); e=seal({'x':1},'v1',b'k'); assert s.accept(e,b'k',100); assert not s.accept(e,b'k',101)

def test_prune_removes_expired_entries():
    s=ReplayStore(10); e=seal({'x':1},'v1',b'k'); assert s.accept(e,b'k',100); assert s.size()==1; assert s.prune(111)==1; assert s.size()==0

def test_prune_keeps_boundary_entry():
    s=ReplayStore(10); e=seal({'x':1},'v1',b'k'); assert s.accept(e,b'k',100); assert s.prune(110)==0; assert s.size()==1

def test_reuse_after_prune_is_allowed():
    s=ReplayStore(10); e=seal({'x':1},'v1',b'k'); assert s.accept(e,b'k',100); assert s.accept(e,b'k',111)

def test_invalid_time_does_not_mutate():
    s=ReplayStore(10); e=seal({'x':1},'v1',b'k'); assert not s.accept(e,b'k',-1); assert s.size()==0

def test_invalid_ttl():
    with pytest.raises(ValueError,match='invalid_ttl'): ReplayStore(0)
