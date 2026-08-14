from scripts.mos_event_identity import Observation, compare


def obs(i, t, lat=5.0, lon=-76.0, mag=7.4, source='A', eid=None):
    return Observation(i, source, 'earthquake', t, lat, lon, mag, eid)


def test_same_source_event_id_is_same():
    a = obs('1','2026-08-10T18:00:00Z',source='SGC',eid='abc')
    b = obs('2','2026-08-10T18:01:00Z',source='SGC',eid='abc')
    assert compare(a,b).relation == 'SAME_EVENT'


def test_conflicting_same_source_ids_are_not_merged():
    a = obs('1','2026-08-10T18:00:00Z',source='SGC',eid='abc')
    b = obs('2','2026-08-10T18:01:00Z',source='SGC',eid='xyz')
    assert compare(a,b).relation == 'DIFFERENT_EVENT'


def test_compatible_independent_observations_are_only_candidates():
    a = obs('1','2026-08-10T18:00:00Z',source='SGC')
    b = obs('2','2026-08-10T18:05:00Z',source='AP')
    d = compare(a,b)
    assert d.relation == 'SAME_EVENT_CANDIDATE'
    assert d.confidence == 'MEDIUM'


def test_insufficient_evidence_stays_ambiguous():
    a = obs('1','2026-08-10T18:00:00Z',source='A',lat=None,lon=None,mag=None)
    b = obs('2','2026-08-10T19:00:00Z',source='B',lat=None,lon=None,mag=None)
    assert compare(a,b).relation == 'AMBIGUOUS'
