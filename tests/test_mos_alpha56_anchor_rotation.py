import pytest
from scripts.mos_alpha54_audit_integrity import make_record
from scripts.mos_alpha55_audit_anchor import create_anchor
from scripts.mos_alpha56_anchor_rotation import AnchorRotation,rotate_anchor,verify_rotation

def records(n=2):
    out=[]; prev=None
    for i in range(n):
        r=make_record(i,{'x':i},prev.record_hash if prev else None); out.append(r); prev=r
    return out

def test_first_rotation():
    rs=records(); rot=rotate_anchor(rs); assert verify_rotation(rot,rs); assert rot.previous is None

def test_rotation_requires_monotonic_sequence():
    rs=records(); prev=create_anchor(rs)
    with pytest.raises(ValueError,match='non_monotonic_anchor'): rotate_anchor(rs,prev)

def test_newer_anchor_rotates():
    old=records(2); prev=create_anchor(old); newer=records(3); rot=rotate_anchor(newer,prev); assert verify_rotation(rot,newer); assert rot.current.seq>prev.seq

def test_tampered_current_fails():
    rs=records(2); rot=rotate_anchor(rs); object.__setattr__(rs[1],'payload',{'x':99}); assert not verify_rotation(rot,rs)

def test_malformed_rotation_rejected(): assert not verify_rotation(None,records())
