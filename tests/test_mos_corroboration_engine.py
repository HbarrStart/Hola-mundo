from scripts.mos_corroboration_engine import EvidenceItem, evaluate


def ev(i, typ, independent=True, contradicted=False):
    return EvidenceItem(i,'c1',independent,typ,'PRIMARY',True,True,contradicted)


def test_event_can_use_one_instrumental_source():
    r = evaluate('EVENT_EXISTENCE',[ev('e1','instrumental')])
    assert r.status == 'READY_FOR_SAFETY_GATE'


def test_casualty_count_needs_two_independent_lines():
    r = evaluate('CASUALTY_COUNT',[ev('e1','official_record')])
    assert r.status == 'NEEDS_REVIEW'


def test_casualty_count_can_pass_corroboration_threshold():
    r = evaluate('CASUALTY_COUNT',[ev('e1','official_record'),ev('e2','rescue_record')])
    assert r.status == 'READY_FOR_SAFETY_GATE'


def test_contradiction_prevents_ready_state():
    r = evaluate('DAMAGE_REPORT',[ev('e1','official_record'),ev('e2','direct_observation'),ev('e3','direct_observation',contradicted=True)])
    assert r.status == 'NEEDS_REVIEW'


def test_unknown_claim_type_fails_closed():
    r = evaluate('UNKNOWN',[ev('e1','official_record')])
    assert r.status == 'UNSUPPORTED_TYPE'
