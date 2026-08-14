from scripts.mos_alpha16_synthetic import SyntheticClaim, Relation, relate, trace


def test_different_values_without_supersession_are_unresolved():
    a = SyntheticClaim('CLAIM-0007','SYNTH-OFFICIAL','2026-08-14T15:00:00Z','100','EVIDENCE-0019')
    b = SyntheticClaim('CLAIM-0008','SYNTH-INDEPENDENT','2026-08-14T15:10:00Z','150','EVIDENCE-0020')
    assert relate(a, b) == Relation.UNRESOLVED_CHANGE


def test_trace_preserves_identity():
    c = SyntheticClaim('CLAIM-0007','SYNTH-OFFICIAL','2026-08-14T15:00:00Z','100','EVIDENCE-0019')
    assert trace(c) == {
        'claim_id':'CLAIM-0007',
        'evidence_id':'EVIDENCE-0019',
        'source_id':'SYNTH-OFFICIAL',
        'observed_at':'2026-08-14T15:00:00Z',
    }


def test_same_value_is_not_a_conflict():
    a = SyntheticClaim('CLAIM-0001','SYNTH-A','2026-08-14T15:00:00Z','100','E1')
    b = SyntheticClaim('CLAIM-0002','SYNTH-B','2026-08-14T15:01:00Z','100','E2')
    assert relate(a, b) == Relation.UPDATE
