from scripts.mos_alpha20_corroboration import ClaimObservation, Corroboration, corroborate


def obs(cid, sid, value, origin=None):
    return ClaimObservation(cid, sid, 'synthetic claim', value, origin)


def test_independent_matching_sources_are_consistent():
    assert corroborate(obs('c1','A','100'), obs('c2','B','100')) == Corroboration.CONSISTENT


def test_conflicting_independent_sources_remain_unresolved():
    assert corroborate(obs('c1','A','100'), obs('c2','B','150')) == Corroboration.UNRESOLVED


def test_same_source_is_not_independent_corroboration():
    assert corroborate(obs('c1','A','100'), obs('c2','A','100')) == Corroboration.INDEPENDENCE_INSUFFICIENT


def test_republished_origin_is_not_independent_corroboration():
    assert corroborate(obs('c1','A','100','WIRE-1'), obs('c2','B','100','WIRE-1')) == Corroboration.INDEPENDENCE_INSUFFICIENT
