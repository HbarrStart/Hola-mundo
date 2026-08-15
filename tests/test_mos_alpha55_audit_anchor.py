import pytest
from scripts.mos_alpha54_audit_integrity import make_record
from scripts.mos_alpha55_audit_anchor import Anchor,create_anchor,verify_anchor

def chain():
    a=make_record(0,{'x':1}); b=make_record(1,{'x':2},a.record_hash); return [a,b]

def test_create_and_verify_anchor():
    records=chain(); anchor=create_anchor(records); assert verify_anchor(records,anchor)

def test_tampered_chain_fails_anchor():
    records=chain(); anchor=create_anchor(records); object.__setattr__(records[1],'payload',{'x':9}); assert not verify_anchor(records,anchor)

def test_wrong_anchor_fails():
    records=chain(); assert not verify_anchor(records,Anchor(9,'0'*64))

def test_empty_chain_cannot_anchor():
    with pytest.raises(ValueError,match='empty_chain'): create_anchor([])

def test_invalid_chain_cannot_anchor():
    records=chain(); object.__setattr__(records[0],'payload',{'x':9})
    with pytest.raises(ValueError,match='invalid_chain'): create_anchor(records)

def test_malformed_anchor_rejected(): assert not verify_anchor(chain(),None)
