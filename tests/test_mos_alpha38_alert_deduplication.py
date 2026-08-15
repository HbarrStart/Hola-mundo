import pytest
from scripts.mos_alpha38_alert_deduplication import Alert,deduplicate,fingerprint

def a(severity='HIGH',message='same'): return Alert('sensor-a','FLOOD','sector-1',message,severity)

def test_duplicate_alerts_collapse(): assert len(deduplicate((a(),a()))) == 1

def test_duplicate_keeps_highest_severity(): assert deduplicate((a('LOW'),a('CRITICAL')))[0].severity == 'CRITICAL'

def test_different_messages_remain_distinct(): assert len(deduplicate((a(message='x'),a(message='y')))) == 2

def test_fingerprint_is_deterministic(): assert fingerprint(a()) == fingerprint(a())

def test_invalid_alert_fails_closed():
    with pytest.raises(ValueError,match='invalid_alert'): fingerprint(Alert('','','','', 'HIGH'))

def test_invalid_severity_fails_closed():
    with pytest.raises(ValueError,match='invalid_severity'): deduplicate((a('UNKNOWN'),))

def test_duplicate_does_not_hide_critical():
    out=deduplicate((a('LOW'),a('MEDIUM'),a('CRITICAL')))
    assert len(out)==1 and out[0].severity=='CRITICAL'
