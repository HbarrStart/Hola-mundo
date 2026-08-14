import pytest
from scripts.mos_alpha29_provenance import SourceRecord, ProvenanceStatus, classify, dependency_closure

def test_root_source_is_independent():
    assert classify(SourceRecord('A'), (SourceRecord('A'),)) is ProvenanceStatus.INDEPENDENT

def test_known_upstream_is_dependent():
    assert classify(SourceRecord('B', ('A',)), (SourceRecord('A'), SourceRecord('B',))) is ProvenanceStatus.DEPENDENT

def test_unknown_upstream_is_unknown():
    assert classify(SourceRecord('B', ('A',)), (SourceRecord('B'),)) is ProvenanceStatus.UNKNOWN

def test_self_dependency_fails_closed():
    with pytest.raises(ValueError, match='self_dependency'):
        classify(SourceRecord('A', ('A',)), (SourceRecord('A'),))

def test_dependency_closure_follows_chain_without_duplicates():
    records=(SourceRecord('A'), SourceRecord('B',('A',)), SourceRecord('C',('B','A')))
    assert dependency_closure('C', records) == ('A','B')

def test_missing_source_has_empty_closure():
    assert dependency_closure('Z', (SourceRecord('A'),)) == ()
