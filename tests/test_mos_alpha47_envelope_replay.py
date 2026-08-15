import pytest
from scripts.mos_alpha46_secure_envelope import seal
from scripts.mos_alpha47_envelope_replay import EnvelopeReplayGuard

def test_first_valid_envelope_is_accepted():
    g=EnvelopeReplayGuard(); e=seal({'x':1},'v1',b'secret')
    assert g.accept(e,b'secret')

def test_exact_replay_is_rejected():
    g=EnvelopeReplayGuard(); e=seal({'x':1},'v1',b'secret')
    assert g.accept(e,b'secret'); assert not g.accept(e,b'secret')

def test_different_payload_is_not_replay():
    g=EnvelopeReplayGuard(); e1=seal({'x':1},'v1',b'secret'); e2=seal({'x':2},'v1',b'secret')
    assert g.accept(e1,b'secret'); assert g.accept(e2,b'secret')

def test_invalid_signature_never_enters_replay_set():
    g=EnvelopeReplayGuard(); e=seal({'x':1},'v1',b'secret'); object.__setattr__(e,'signature','bad')
    assert not g.accept(e,b'secret'); object.__setattr__(e,'signature',seal({'x':1},'v1',b'secret').signature); assert g.accept(e,b'secret')

def test_wrong_secret_rejected():
    g=EnvelopeReplayGuard(); e=seal({'x':1},'v1',b'secret'); assert not g.accept(e,b'wrong')

def test_replay_state_is_scoped_to_guard():
    e=seal({'x':1},'v1',b'secret'); a=EnvelopeReplayGuard(); b=EnvelopeReplayGuard()
    assert a.accept(e,b'secret'); assert b.accept(e,b'secret')
