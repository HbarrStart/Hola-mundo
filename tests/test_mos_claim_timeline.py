from scripts.mos_claim_timeline import ClaimVersion, classify_relation


def c(i,v,s='ungrd',sup=None,corr=None,p='2026-08-14T10:00:00Z'):
    return ClaimVersion(i,'casualties',v,s,None,p,sup,corr)


def test_explicit_supersedes_is_update():
    assert classify_relation(c('c1','281'), c('c2','285',sup='c1')) == 'UPDATE'


def test_explicit_correction_is_correction():
    assert classify_relation(c('c1','281'), c('c2','285',corr='c1')) == 'CORRECTION'


def test_changed_value_without_relation_is_unresolved():
    assert classify_relation(c('c1','281'), c('c2','285')) == 'UNRESOLVED_CHANGE'


def test_same_value_is_duplicate():
    assert classify_relation(c('c1','281'), c('c2','281')) == 'DUPLICATE'
