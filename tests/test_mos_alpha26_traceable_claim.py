import pytest
from scripts.mos_alpha26_traceable_claim import EvidenceRef, EvidenceRelation, TraceableClaim


def valid_claim():
    return TraceableClaim(
        'C-001', 'Synthetic emergency claim', ('SRC-001',),
        (EvidenceRef('E-001', EvidenceRelation.SUPPORTS),),
        '2026-08-14T16:00:00Z')


def test_valid_claim_exposes_audit_path():
    path = valid_claim().audit_path()
    assert path['claim_id'] == 'C-001'
    assert path['source_ids'] == ('SRC-001',)
    assert path['evidence'][0]['evidence_id'] == 'E-001'
    assert path['evidence'][0]['relation'] == 'SUPPORTS'


@pytest.mark.parametrize('field', ['claim_id', 'text', 'retrieved_at'])
def test_missing_core_metadata_fails_closed(field):
    c = valid_claim()
    values = {field: ''}
    broken = TraceableClaim(c.claim_id if field != 'claim_id' else '',
                            c.text if field != 'text' else '',
                            c.source_ids, c.evidence,
                            c.retrieved_at if field != 'retrieved_at' else '')
    with pytest.raises(ValueError, match='incomplete_claim'):
        broken.validate()


def test_missing_source_trace_fails_closed():
    c = valid_claim()
    broken = TraceableClaim(c.claim_id, c.text, (), c.evidence, c.retrieved_at)
    with pytest.raises(ValueError, match='missing_source_trace'):
        broken.validate()


def test_missing_evidence_trace_fails_closed():
    c = valid_claim()
    broken = TraceableClaim(c.claim_id, c.text, c.source_ids, (), c.retrieved_at)
    with pytest.raises(ValueError, match='missing_evidence_trace'):
        broken.validate()


def test_invalid_evidence_reference_fails_closed():
    c = valid_claim()
    broken = TraceableClaim(c.claim_id, c.text, c.source_ids,
                            (EvidenceRef('', EvidenceRelation.SUPPORTS),), c.retrieved_at)
    with pytest.raises(ValueError, match='invalid_evidence_trace'):
        broken.validate()
