from datetime import datetime,timedelta,timezone
from scripts.mos_alpha67_corroboration_window import Evidence,in_window,corroborated

def test_two_distinct_verified_sources_corroborate():
 n=datetime.now(timezone.utc); e=[Evidence('a',n,True),Evidence('b',n,True)]; assert corroborated(e,n,timedelta(minutes=10))
def test_duplicate_source_does_not_count_twice():
 n=datetime.now(timezone.utc); e=[Evidence('a',n,True),Evidence('a',n,True)]; assert not corroborated(e,n,timedelta(minutes=10))
def test_old_evidence_expires():
 n=datetime.now(timezone.utc); e=Evidence('a',n-timedelta(hours=1),True); assert not in_window(e,n,timedelta(minutes=10))
def test_revoked_is_excluded():
 n=datetime.now(timezone.utc); e=Evidence('a',n,True,True); assert not in_window(e,n,timedelta(minutes=10))
def test_unverified_is_excluded():
 n=datetime.now(timezone.utc); e=Evidence('a',n,False); assert not in_window(e,n,timedelta(minutes=10))
