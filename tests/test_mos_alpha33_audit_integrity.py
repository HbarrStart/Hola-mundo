import pytest
from scripts.mos_alpha33_audit_integrity import make_record,verify_record,verify_chain

def chain():
    a=make_record('A','2026-08-14T12:00:00Z','CLAIM',{'x':'uno'})
    b=make_record('B','2026-08-14T12:01:00Z','DECISION',{'allow':True},a.record_hash)
    return a,b

def test_valid_chain(): assert verify_chain(chain())
def test_payload_tampering_detected():
    a,b=chain(); bad=type(b)(b.event_id,b.timestamp,b.event_type,{'allow':False},b.previous_hash,b.record_hash)
    assert not verify_record(bad) and not verify_chain((a,bad))
def test_timestamp_tampering_detected():
    a,b=chain(); bad=type(b)(b.event_id,'2026-08-14T12:02:00Z',b.event_type,b.payload,b.previous_hash,b.record_hash)
    assert not verify_chain((a,bad))
def test_previous_hash_tampering_detected():
    a,b=chain(); bad=type(b)(b.event_id,b.timestamp,b.event_type,b.payload,'0'*64,b.record_hash)
    assert not verify_chain((a,bad))
def test_record_hash_tampering_detected():
    a,b=chain(); bad=type(b)(b.event_id,b.timestamp,b.event_type,b.payload,b.previous_hash,'0'*64)
    assert not verify_chain((a,bad))
def test_duplicate_event_detected():
    a,b=chain(); assert not verify_chain((a,b,a))
def test_missing_first_link_detected():
    a,b=chain(); bad=type(b)(b.event_id,b.timestamp,b.event_type,b.payload,'',b.record_hash)
    assert not verify_chain((bad,))
def test_unicode_payload_is_deterministic():
    a=make_record('U','2026-08-14T12:00:00Z','NOTE',{'texto':'áéñ 🚨'})
    b=make_record('U','2026-08-14T12:00:00Z','NOTE',{'texto':'áéñ 🚨'})
    assert a.record_hash==b.record_hash

def test_invalid_metadata_fails_closed():
    with pytest.raises(ValueError): make_record('','','X',{})
