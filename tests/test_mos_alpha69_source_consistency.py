from scripts.mos_alpha69_source_consistency import Observation,consistent,consistent_sources

def test_matching_verified_claims():
 o=[Observation('a','quake',True),Observation('b','quake',True)]; assert consistent(o)
def test_conflicting_claims_fail_closed():
 o=[Observation('a','quake',True),Observation('b','fire',True)]; assert not consistent(o)
def test_revoked_ignored():
 o=[Observation('a','quake',True),Observation('b','quake',True,True),Observation('c','quake',True)]; assert consistent(o)
def test_unverified_ignored():
 o=[Observation('a','quake',True),Observation('b','quake',False)]; assert consistent(o)
def test_no_valid_observations_fail(): assert not consistent([])
def test_sources_are_unique_and_sorted():
 o=[Observation('z','quake',True),Observation('a','quake',True),Observation('a','quake',True)]; assert consistent_sources(o)==('a','z')
