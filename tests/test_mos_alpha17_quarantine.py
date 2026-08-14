import pytest
from scripts.mos_alpha17_quarantine import SourceRecord, quarantine, can_publish


def source():
    return SourceRecord(
        source_id='SRC-LIVE-001',
        url='https://example.invalid/emergency-update',
        retrieved_at='2026-08-14T16:00:00Z',
        content_hash='sha256:synthetic-test-hash',
        publisher='synthetic-public-source',
    )


def test_live_source_enters_quarantine_not_publication():
    record = quarantine(source())
    assert record.status.value == 'QUARANTINED'
    assert can_publish(record) is False


def test_missing_provenance_fails_closed():
    bad = SourceRecord('SRC-LIVE-002', 'https://example.invalid/x', '', 'hash', None)
    with pytest.raises(ValueError, match='incomplete_source_provenance'):
        quarantine(bad)
