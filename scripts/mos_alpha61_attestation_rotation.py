#!/usr/bin/env python3
"""MOS Alpha-61: deterministic attestation-key rotation."""
from dataclasses import dataclass
from scripts.mos_alpha60_anchor_attestation import Attestation, attest, verify_attestation

@dataclass(frozen=True)
class Rotation:
    old_signer: str
    new_signer: str
    effective_seq: int

def rotate(a:Attestation,new_signer:str,effective_seq:int,secret:bytes)->Rotation:
    if not verify_attestation(a,secret): raise ValueError('invalid_attestation')
    if not new_signer.strip() or not isinstance(effective_seq,int) or effective_seq<=a.anchor.seq: raise ValueError('invalid_rotation')
    return Rotation(a.signer,new_signer,effective_seq)

def active_signer(rotation:Rotation,seq:int)->str:
    if not isinstance(rotation,Rotation) or not isinstance(seq,int) or seq<0: return ''
    return rotation.old_signer if seq < rotation.effective_seq else rotation.new_signer
