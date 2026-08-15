import pytest
from scripts.mos_alpha46_secure_envelope import seal
from scripts.mos_alpha48_replay_window import ReplayWindow

def test_replay_rejected_inside_window():
    w=ReplayWindow(10); e=seal({'x':1},'v1',b's'); assert w.accept(e,b's',100); assert not w.accept(e,b's',109)

def test_replay_allowed_after_window_expires():
    w=ReplayWindow(10); e=seal({'x':1},'v1',b's'); assert w.accept(e,b's',100); assert w.accept(e,b's',110)

def test_exact_boundary_is_expired():
    w=ReplayWindow(10); e=seal({'x':1},'v1',b's'); assert w.accept(e,b's',100); assert w.accept(e,b's',110)

def test_invalid_time_rejected():
    w=ReplayWindow(10); e=seal({'x':1},'v1',b's'); assert not w.accept(e,b's',-1)

def test_invalid_ttl_fails_closed():
    with pytest.raises(ValueError,match='invalid_ttl'): ReplayWindow(0)

def test_invalid_envelope_does_not_enter_state():
    w=ReplayWindow(10); e=seal({'x':1},'v1',b's'); object.__setattr__(e,'signature','bad'); assert not w.accept(e,b's',100); object.__setattr__(e,'signature',seal({'x':1},'v1',b's').signature); assert w.accept(e,b's',100)
