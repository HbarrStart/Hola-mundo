import pytest
from scripts.mos_alpha55_audit_anchor import Anchor
from scripts.mos_alpha57_anchor_chain import AnchorLink,link_anchor,verify_anchor_chain

def a(n): return Anchor(n,f'{n:064x}')

def test_chain_links_verify():
    x,y,z=a(1),a(2),a(3); links=[link_anchor(None,x),link_anchor(x,y),link_anchor(y,z)]; assert verify_anchor_chain(links)

def test_chain_rejects_wrong_previous():
    x,y=a(1),a(2); links=[AnchorLink(None,x),AnchorLink(a(9),y)]; assert not verify_anchor_chain(links)

def test_chain_rejects_non_monotonic():
    x,y=a(2),a(1); links=[AnchorLink(None,x),AnchorLink(x,y)]; assert not verify_anchor_chain(links)

def test_link_rejects_invalid_anchor():
    with pytest.raises(ValueError,match='invalid_anchor'): link_anchor(None,None)

def test_link_rejects_equal_sequence():
    x=a(1)
    with pytest.raises(ValueError,match='non_monotonic_anchor'): link_anchor(x,x)

def test_empty_chain_rejected(): assert not verify_anchor_chain([])
