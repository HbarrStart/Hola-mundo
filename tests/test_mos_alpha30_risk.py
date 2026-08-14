import pytest
from scripts.mos_alpha30_risk import RiskInput,RiskLevel,classify_risk

def base(**kw):
    d=dict(impact=1,urgency=1,evidence_quality=1,contradiction=0,scope=1,reversibility=5); d.update(kw); return RiskInput(**d)

def test_missing_data_is_unknown(): assert classify_risk(base(impact=None)) is RiskLevel.UNKNOWN

def test_low_risk(): assert classify_risk(base()) is RiskLevel.LOW

def test_critical_impact_is_critical(): assert classify_risk(base(impact=5,urgency=5,evidence_quality=5,contradiction=5,scope=5,reversibility=0)) is RiskLevel.CRITICAL

def test_high_risk(): assert classify_risk(base(impact=4,urgency=4,evidence_quality=3,contradiction=3,scope=4,reversibility=1)) is RiskLevel.HIGH

def test_urgency_does_not_imply_truth(): assert classify_risk(base(urgency=5,evidence_quality=0)) is not RiskLevel.UNKNOWN

@pytest.mark.parametrize('field',[-1,6])
def test_out_of_range_fails_closed(field):
    with pytest.raises(ValueError,match='invalid_risk_input'): classify_risk(base(impact=field))

def test_non_integer_fails_closed():
    with pytest.raises(ValueError,match='invalid_risk_input'): classify_risk(base(scope='5'))
