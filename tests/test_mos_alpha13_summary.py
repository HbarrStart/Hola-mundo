from scripts.mos_alpha13_summary import Claim, build_summary, assert_traceable


def test_summary_is_ledger_only_and_traceable():
    claims = [Claim('c1','evento de prueba','ALLOW','LOW','2026-08-14T15:00:00Z',('e1',))]
    items = build_summary(claims)
    assert len(items) == 1
    assert assert_traceable(items[0])


def test_blocked_claim_is_not_public_by_default():
    claims = [Claim('c2','dato bloqueado','BLOCK','CRITICAL','2026-08-14T15:00:00Z',('e2',))]
    assert build_summary(claims) == []


def test_unknown_status_fails_closed():
    claims = [Claim('c3','dato','CONFIRMED','LOW','2026-08-14T15:00:00Z',('e3',))]
    try:
        build_summary(claims)
    except ValueError as e:
        assert str(e) == 'unknown_gate_status'
    else:
        raise AssertionError('unknown status must fail closed')


def test_missing_evidence_fails_closed():
    claims = [Claim('c4','dato','ALLOW','LOW','2026-08-14T15:00:00Z',())]
    try:
        build_summary(claims)
    except ValueError as e:
        assert str(e) == 'summary_item_missing_evidence_refs'
    else:
        raise AssertionError('summary item without evidence must fail closed')
