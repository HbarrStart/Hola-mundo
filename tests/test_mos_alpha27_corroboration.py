import pytest
from scripts.mos_alpha27_corroboration import EvidenceItem, EvidenceRelation, CorroborationStatus, assess

def ev(i, key, rel=EvidenceRelation.SUPPORTS):
    return EvidenceItem(i, 'SRC-'+i, rel, key)

def test_empty_is_insufficient():
    r=assess(())
    assert r.status is CorroborationStatus.INSUFFICIENT

def test_independent_support_is_consistent():
    r=assess((ev('1','A'),ev('2','B')))
    assert r.status is CorroborationStatus.CONSISTENT
    assert r.independent_support == 2

def test_repeated_same_independence_key_does_not_inflate_support():
    r=assess((ev('1','A'),ev('2','A')))
    assert r.independent_support == 1
    assert r.evidence_count == 2

def test_independent_contradiction_is_visible():
    r=assess((ev('1','A'),ev('2','B',EvidenceRelation.CONTRADICTS)))
    assert r.status is CorroborationStatus.MIXED
    assert r.independent_support == 1
    assert r.independent_contradictions == 1

def test_only_contradictions_are_contradicted():
    r=assess((ev('1','A',EvidenceRelation.CONTRADICTS),))
    assert r.status is CorroborationStatus.CONTRADICTED
