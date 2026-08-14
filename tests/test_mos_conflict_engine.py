from scripts.mos_conflict_engine import Claim, classify


def c(i, value, published='2026-08-14T10:00:00Z', source='S1', supersedes=None, evidence='e1'):
    return Claim(i, 'deaths', value, 'persons', source, published, published, evidence, supersedes)


def test_duplicate():
    assert classify(c('a','281'), c('b','281')) == 'DUPLICATE'


def test_explicit_update():
    assert classify(c('a','281'), c('b','285', supersedes='a')) == 'UPDATE'


def test_unresolved_without_time_or_metadata():
    a = c('a','281', published='bad')
    b = c('b','285', published='bad')
    assert classify(a,b) == 'UNRESOLVED'


def test_different_values_in_same_window_remain_conflict():
    assert classify(c('a','281'), c('b','285')) == 'CONFLICT'
