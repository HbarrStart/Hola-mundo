from scripts.mos_alpha8_pipeline import Alpha8Input, run
from scripts.mos_corroboration_engine import EvidenceItem


def e(i, typ, independent=True, temporal=True, spatial=True, contradicted=False):
    return EvidenceItem(i, 'c1', independent, typ, 'PRIMARY', temporal, spatial, contradicted)


def test_valid_low_risk_claim_can_pass():
    r = run(Alpha8Input('EVENT_EXISTENCE',(e('e1','instrumental'),),'LOW'))
    assert r['gate'].decision == 'ALLOW'


def test_insufficient_casualty_evidence_holds():
    r = run(Alpha8Input('CASUALTY_COUNT',(e('e1','official_record'),),'HIGH'))
    assert r['gate'].decision == 'HOLD'


def test_operational_high_harm_requires_human_review():
    r = run(Alpha8Input('ACCESS_STATUS',(e('e1','official_record'),e('e2','responder_report')),'HIGH',operational=True))
    assert r['gate'].decision == 'HUMAN_REVIEW'


def test_stale_data_holds():
    r = run(Alpha8Input('EVENT_EXISTENCE',(e('e1','instrumental'),),'LOW',stale=True))
    assert r['gate'].decision == 'HOLD'


def test_contradiction_requires_review():
    r = run(Alpha8Input('DAMAGE_REPORT',(e('e1','official_record'),e('e2','direct_observation')),'HIGH',contradiction=True))
    assert r['gate'].decision == 'HUMAN_REVIEW'


def test_personal_data_blocks():
    r = run(Alpha8Input('CASUALTY_COUNT',(e('e1','official_record'),e('e2','hospital_record')),'HIGH',personal_data=True))
    assert r['gate'].decision == 'BLOCK'


def test_unregistered_source_blocks():
    r = run(Alpha8Input('EVENT_EXISTENCE',(e('e1','instrumental'),),'LOW',source_registered=False))
    assert r['gate'].decision == 'BLOCK'
