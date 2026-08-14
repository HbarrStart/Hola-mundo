import pytest
from scripts.mos_alpha32_human_oversight import ReviewRequest,ReviewDecision,create_review,resolve_review

def req(): return ReviewRequest('R-1','conflicting evidence','HIGH','human-1')

def test_reviewer_required():
    with pytest.raises(ValueError,match='reviewer_required'): create_review(ReviewRequest('R','reason','HIGH',None))

def test_review_starts_pending(): assert create_review(req()).decision is ReviewDecision.HOLD

def test_approval_requires_rationale_and_timestamp():
    r=create_review(req())
    with pytest.raises(ValueError,match='audit_metadata_required'): resolve_review(r,ReviewDecision.APPROVE,'','')

def test_approval_is_auditable():
    r=resolve_review(create_review(req()),ReviewDecision.APPROVE,'verified evidence','2026-08-14T12:00:00Z')
    assert r.decision is ReviewDecision.APPROVE and r.reviewer=='human-1'

def test_rejection_is_supported():
    r=resolve_review(create_review(req()),ReviewDecision.REJECT,'insufficient support','2026-08-14T12:01:00Z')
    assert r.decision is ReviewDecision.REJECT

def test_review_cannot_be_resolved_twice():
    r=resolve_review(create_review(req()),ReviewDecision.APPROVE,'verified','2026-08-14T12:00:00Z')
    with pytest.raises(ValueError,match='review_already_resolved'): resolve_review(r,ReviewDecision.REJECT,'change','2026-08-14T12:02:00Z')

def test_invalid_request_fails_closed():
    with pytest.raises(ValueError,match='invalid_review_request'): create_review(ReviewRequest('','','HIGH','human'))
