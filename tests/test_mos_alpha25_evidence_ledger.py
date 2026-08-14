import pytest
from scripts.mos_alpha25_evidence_ledger import EvidenceRelation, content_hash, create_evidence


def test_hash_is_deterministic_and_sha256():
    h1 = content_hash('synthetic evidence')
    h2 = content_hash('synthetic evidence')
    assert h1 == h2
    assert len(h1) == 64


def test_evidence_preserves_provenance_and_relation():
    e = create_evidence('E-001','C-001','SRC-001','synthetic://record/1',
                        '2026-08-14T16:00:00Z','synthetic evidence',
                        'DOCUMENT','paragraph-1',EvidenceRelation.SUPPORTS)
    assert e.claim_id == 'C-001'
    assert e.source_id == 'SRC-001'
    assert e.relation is EvidenceRelation.SUPPORTS
    assert e.content_hash == content_hash('synthetic evidence')


def test_empty_content_fails_closed():
    with pytest.raises(ValueError, match='empty_evidence_content'):
        content_hash('')


def test_incomplete_metadata_fails_closed():
    with pytest.raises(ValueError, match='incomplete_evidence_record'):
        create_evidence('E-001','C-001','','synthetic://record/1',
                        '2026-08-14T16:00:00Z','synthetic evidence',
                        'DOCUMENT','paragraph-1',EvidenceRelation.SUPPORTS)
