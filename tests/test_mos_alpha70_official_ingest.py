from scripts.mos_alpha70_official_ingest import OfficialSource,RawEvidence,SourceNotAllowed,IngestError,allowed,ingest_all

def test_https_allowlist_requires_exact_domain():
 assert allowed(OfficialSource('SGC','https://www.sgc.gov.co/feed','www.sgc.gov.co'))
 assert not allowed(OfficialSource('bad','https://evil.example/feed','www.sgc.gov.co'))

def test_inactive_and_non_https_rejected():
 assert not allowed(OfficialSource('SGC','https://www.sgc.gov.co/feed','www.sgc.gov.co',False))
 assert not allowed(OfficialSource('SGC','http://www.sgc.gov.co/feed','www.sgc.gov.co'))

def test_ingest_all_uses_only_allowed_sources():
 sources=[OfficialSource('a','https://a.gov/feed','a.gov'),OfficialSource('bad','https://evil.example/feed','a.gov')]
 def fake_fetch(s): return RawEvidence(s.name,s.url,'raw','text/plain')
 assert ingest_all(sources,fake_fetch)==(RawEvidence('a','https://a.gov/feed','raw','text/plain'),)

def test_ingest_all_isolates_ingest_failure():
 sources=[OfficialSource('a','https://a.gov/feed','a.gov'),OfficialSource('b','https://b.gov/feed','b.gov')]
 def fake_fetch(s):
  if s.name=='a': raise IngestError('timeout')
  return RawEvidence(s.name,s.url,'raw','text/plain')
 assert tuple(x.source for x in ingest_all(sources,fake_fetch))==('b',)
