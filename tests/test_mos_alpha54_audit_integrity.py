from scripts.mos_alpha54_audit_integrity import make_record,verify_chain

def test_chain_verifies():
    a=make_record(0,{'x':1}); b=make_record(1,{'x':2},a.record_hash); assert verify_chain([a,b])
def test_payload_tamper_fails():
    a=make_record(0,{'x':1}); b=make_record(1,{'x':2},a.record_hash); object.__setattr__(b,'payload',{'x':9}); assert not verify_chain([a,b])
def test_previous_link_tamper_fails():
    a=make_record(0,{'x':1}); b=make_record(1,{'x':2},a.record_hash); object.__setattr__(b,'prev_hash','0'*64); assert not verify_chain([a,b])
def test_sequence_gap_fails():
    a=make_record(0,{'x':1}); b=make_record(2,{'x':2},a.record_hash); assert not verify_chain([a,b])
def test_anchor_is_verified():
    a=make_record(0,{'x':1},'anchor'); assert verify_chain([a],'anchor'); assert not verify_chain([a])
def test_empty_chain_is_valid(): assert verify_chain([])
def test_invalid_record_rejected():
    assert not verify_chain([None])
