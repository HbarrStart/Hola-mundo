import pytest
from scripts.mos_alpha55_audit_anchor import Anchor
from scripts.mos_alpha58_anchor_consensus import AnchorObservation,reach_consensus,verify_consensus

def obs(a): return [AnchorObservation('a',a),AnchorObservation('b',a)]
def test_consensus():
    a=Anchor(3,'3'*64); assert reach_consensus(obs(a))==a; assert verify_consensus(obs(a),a)
def test_conflict_rejected():
    with pytest.raises(ValueError,match='anchor_conflict'): reach_consensus([AnchorObservation('a',Anchor(1,'1'*64)),AnchorObservation('b',Anchor(2,'2'*64))])
def test_empty_rejected():
    with pytest.raises(ValueError,match='empty_observations'): reach_consensus([])
def test_invalid_observation_rejected():
    with pytest.raises(ValueError,match='invalid_observation'): reach_consensus([AnchorObservation('',Anchor(1,'1'*64))])
def test_wrong_expected_fails(): assert not verify_consensus(obs(Anchor(3,'3'*64)),Anchor(4,'4'*64))
def test_malformed_expected_fails(): assert not verify_consensus(obs(Anchor(3,'3'*64)),None)
