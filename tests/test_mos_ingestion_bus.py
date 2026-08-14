from scripts.mos_ingestion_bus import ingest


def test_new_observation_is_quarantined_and_hashed():
    o = ingest('sgc','https://example.invalid/source','evento de prueba', '2026-08-14T12:00:00Z')
    assert o.status == 'QUARANTINED'
    assert len(o.content_sha256) == 64
    assert o.observation_id.startswith('obs-')


def test_missing_provenance_fails_closed():
    try:
        ingest('','https://example.invalid/source','dato')
    except ValueError as e:
        assert str(e) == 'missing_required_provenance_or_content'
    else:
        raise AssertionError('ingestion should reject missing source id')
