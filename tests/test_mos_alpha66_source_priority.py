from scripts.mos_alpha66_source_priority import Source,SourceTier,prioritize,primary_sources

def test_primary_before_secondary():
 s=[Source('b',SourceTier.SECONDARY),Source('a',SourceTier.PRIMARY)]; assert prioritize(s)==(s[1],s[0])
def test_inactive_excluded(): assert prioritize([Source('x',SourceTier.PRIMARY,False)])==()
def test_primary_filter():
 s=[Source('a',SourceTier.PRIMARY),Source('b',SourceTier.COMMUNITY)]; assert primary_sources(s)==(s[0],)
def test_tie_is_deterministic():
 s=[Source('z',SourceTier.PRIMARY),Source('a',SourceTier.PRIMARY)]; assert tuple(x.name for x in prioritize(s))==('a','z')
