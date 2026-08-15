from scripts.mos_alpha68_source_quorum import source_quorum

def test_two_sources_reach_quorum(): assert source_quorum(['a','b']).reached
def test_one_source_fails_quorum(): assert not source_quorum(['a']).reached
def test_duplicates_do_not_inflate_quorum(): assert not source_quorum(['a','a']).reached
def test_result_is_deterministic(): assert source_quorum(['b','a','b']).sources==('a','b')
def test_custom_minimum(): assert source_quorum(['a','b'],minimum=3).reached is False
