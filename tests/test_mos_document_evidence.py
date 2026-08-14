from scripts.mos_document_evidence import register_document


def test_document_is_hashed_and_quarantined():
    d = register_document('ungrd','https://example.invalid/bulletin.pdf','UNGRD','PDF',b'official bulletin')
    assert d.status == 'QUARANTINED'
    assert len(d.content_sha256) == 64
    assert d.document_id.startswith('doc-')


def test_empty_document_fails_closed():
    try:
        register_document('ungrd','https://example.invalid/bulletin.pdf','UNGRD','PDF',b'')
    except ValueError as e:
        assert str(e) == 'invalid_document_evidence'
    else:
        raise AssertionError('empty document should be rejected')
