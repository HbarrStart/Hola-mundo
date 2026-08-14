from scripts.mos_alpha13_summary import Claim, build_summary

CASES = [
    Claim('r1','claim without evidence','ALLOW','LOW','2026-08-14T15:00:00Z',()),
    Claim('r2','unsupported confirmed state','CONFIRMED','LOW','2026-08-14T15:00:00Z',('e2',)),
    Claim('r3','victim count insufficiently supported','HOLD','HIGH','2026-08-14T15:00:00Z',('e3',)),
    Claim('r4','sensitive location','BLOCK','CRITICAL','2026-08-14T15:00:00Z',('e4',)),
]


def test_red_team_cases_do_not_become_public_summary():
    for case in CASES:
        try:
            result = build_summary([case])
        except ValueError:
            continue
        assert result == [], f'unsafe case escaped: {case.claim_id}'


def test_safe_claim_is_traceable():
    safe = Claim('r5','public low-risk event','ALLOW','LOW','2026-08-14T15:00:00Z',('e5',))
    result = build_summary([safe])
    assert len(result) == 1
    assert result[0].claim_id == 'r5'
    assert result[0].evidence_refs == ('e5',)
