import pytest
from scripts.mos_alpha19_claim_extraction import extract_claims, is_verified

SOURCE = 'La fuente informa 100 personas afectadas, tres municipios con daños y una vía cerrada.'


def test_publication_becomes_separate_claims_without_verification():
    claims = extract_claims('SRC-SYNTH-001', SOURCE, [
        {'claim_text':'100 personas afectadas','observed_at':'2026-08-14T16:00:00Z'},
        {'claim_text':'tres municipios con daños','observed_at':'2026-08-14T16:00:00Z'},
        {'claim_text':'una vía cerrada','observed_at':'2026-08-14T16:00:00Z'},
    ])
    assert len(claims) == 3
    assert [c.claim_id for c in claims] == ['SRC-SYNTH-001-CLAIM-0001','SRC-SYNTH-001-CLAIM-0002','SRC-SYNTH-001-CLAIM-0003']
    assert all(c.status == 'UNVERIFIED' for c in claims)
    assert all(not is_verified(c) for c in claims)


def test_claim_keeps_source_text_for_traceability():
    claims = extract_claims('SRC-SYNTH-001', SOURCE, [{'claim_text':'100 personas afectadas','observed_at':'2026-08-14T16:00:00Z'}])
    assert claims[0].source_text == SOURCE
    assert claims[0].source_id == 'SRC-SYNTH-001'


def test_incomplete_claim_fails_closed():
    with pytest.raises(ValueError, match='incomplete_claim'):
        extract_claims('SRC-SYNTH-001', SOURCE, [{'claim_text':'100 personas afectadas'}])
