from scripts.mos_alpha46_secure_envelope import seal
from scripts.mos_alpha50_replay_metrics import InstrumentedReplayStore

def test_metrics_track_accept_and_reject():
    s=InstrumentedReplayStore(10); e=seal({'x':1},'v1',b'k')
    assert s.accept(e,b'k',100); assert not s.accept(e,b'k',101)
    assert (s.metrics.accepted,s.metrics.rejected)==(1,1)

def test_metrics_track_pruning():
    s=InstrumentedReplayStore(10); e=seal({'x':1},'v1',b'k'); s.accept(e,b'k',100)
    assert s.prune(111)==1; assert s.metrics.pruned==1

def test_invalid_event_is_rejection():
    s=InstrumentedReplayStore(10); e=seal({'x':1},'v1',b'k'); assert not s.accept(e,b'bad',100); assert s.metrics.rejected==1
