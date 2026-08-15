from scripts.mos_alpha70_official_ingest import OfficialSource,RawEvidence,SourceNotAllowed,allowed,ingest_all

def test_https_allowlist_requires_exact_domain():
 assert allowed(OfficialSource('SGC','https://www.sgc.gov.co/feed','www.sgc.gov.co'))
 assert not allowed(OfficialSource('bad','https://evil.example/feed','www.sgc.gov.co'))

def test_inactive_source_is_not_allowed():
 assert not allowed(OfficialSource('SGC','https://www.sgc.gov.co/feed','www.sgc.gov.co',False))

def test_non_https_source_is_rejected():
 assert not allowed(OfficialSource('SGC','http://www.sgc.gov.co/feed','www.sgc.gov.co'))

def test_ingest_all_uses_only_allowed_sources():
 sources=[OfficialSource('a','https://a.gov/feed','a.gov'),OfficialSource('bad','https://evil.example/feed','a.gov')]
 def fake_fetch(s): return RawEvidence(s.name,s.url,'raw','text/plain')
 assert ingest_all(sources,fake_fetch)==(RawEvidence('a','https://a.gov/feed','raw','text/plain'),)
