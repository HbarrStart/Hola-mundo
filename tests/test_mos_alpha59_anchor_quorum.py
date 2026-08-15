import pytest
from scripts.mos_alpha55_audit_anchor import Anchor
from scripts.mos_alpha59_anchor_quorum import AnchorObservation,reach_quorum,verify_quorum

def o(src,n): return AnchorObservation(src,Anchor(n,f'{n:064x}'))
def test_quorum_wins():
    a=Anchor(3,'3'*64); obs=[AnchorObservation('a',a),AnchorObservation('b',a),AnchorObservation('c',Anchor(2,'2'*64))]; assert reach_quorum(obs,2)==a; assert verify_quorum(obs,a,2)
def test_conflict_without_quorum():
    with pytest.raises(ValueError,match='quorum_conflict'): reach_quorum([o('a',1),o('b',2)],2)
def test_invalid_quorum():
    with pytest.raises(ValueError,match='invalid_quorum'): reach_quorum([o('a',1)],0)
def test_empty_observations():
    with pytest.raises(ValueError,match='empty_observations'): reach_quorum([],1)
def test_invalid_source():
    with pytest.raises(ValueError,match='invalid_observation'): reach_quorum([AnchorObservation('',Anchor(1,'1'*64))],1)
def test_wrong_expected(): assert not verify_quorum([o('a',1),o('b',1)],Anchor(2,'2'*64),2)
