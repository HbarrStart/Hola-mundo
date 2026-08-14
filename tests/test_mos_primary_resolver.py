import pytest
from scripts.mos_primary_resolver import PrimaryAttempt, ResolutionStatus, resolve


def test_primary_not_found_is_valid_state():
    a = PrimaryAttempt('sgc','API','2026-08-14T00:00:00Z',ResolutionStatus.PRIMARY_NOT_FOUND)
    assert resolve(a).status == ResolutionStatus.PRIMARY_NOT_FOUND


def test_primary_success_requires_record_and_evidence():
    with pytest.raises(ValueError):
        resolve(PrimaryAttempt('sgc','API','2026-08-14T00:00:00Z',ResolutionStatus.PRIMARY_FOUND))


def test_unavailable_is_not_false():
    a = PrimaryAttempt('sgc','OFFICIAL_PAGE','2026-08-14T00:00:00Z',ResolutionStatus.PRIMARY_UNAVAILABLE)
    assert resolve(a).status == ResolutionStatus.PRIMARY_UNAVAILABLE
