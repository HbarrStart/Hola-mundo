import pytest
from scripts.mos_alpha18_source_registry import SourceClass, SourceProfile, register, source_is_publishable


def test_registry_preserves_source_class_without_truth_claim():
    p = SourceProfile('SRC-001','Synthetic Independent Desk',SourceClass.JOURNALISM,'https://example.invalid/source')
    assert register(p) == p
    assert source_is_publishable(p) is False


def test_incomplete_profile_fails_closed():
    p = SourceProfile('','','', 'https://example.invalid/source')
    with pytest.raises(ValueError, match='incomplete_source_profile'):
        register(p)


def test_all_source_classes_are_non_authoritative():
    for cls in SourceClass:
        p = SourceProfile(f'SRC-{cls.value}','Synthetic Source',cls,'https://example.invalid/source')
        assert source_is_publishable(register(p)) is False
