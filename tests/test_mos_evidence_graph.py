from scripts.mos_evidence_graph import Source, Evidence, analyze_claim


def test_republished_same_upstream_is_not_independent():
    sources = {
        'ungrd': Source('ungrd','UNGRD','PRIMARY'),
        'news-a': Source('news-a','News A','SECONDARY','ungrd'),
        'news-b': Source('news-b','News B','SECONDARY','ungrd'),
    }
    evidence = [
        Evidence('e1','news-a','c1','article','2026-08-14T10:00:00Z'),
        Evidence('e2','news-b','c1','article','2026-08-14T10:05:00Z'),
    ]
    r = analyze_claim('c1', evidence, sources)
    assert r.independent_source_count == 1
    assert r.repeated_upstream_evidence == ['e2']


def test_distinct_upstreams_count_independently():
    sources = {
        'ungrd': Source('ungrd','UNGRD','PRIMARY'),
        'sgc': Source('sgc','SGC','PRIMARY'),
    }
    evidence = [
        Evidence('e1','ungrd','c1','bulletin','2026-08-14T10:00:00Z'),
        Evidence('e2','sgc','c1','bulletin','2026-08-14T10:05:00Z'),
    ]
    r = analyze_claim('c1', evidence, sources)
    assert r.independent_source_count == 2
