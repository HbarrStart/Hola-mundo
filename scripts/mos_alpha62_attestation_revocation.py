#!/usr/bin/env python3
"""MOS Alpha-62: deterministic attestation revocation registry."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Revocation:
    signer: str
    reason: str
    timestamp: int

class RevocationRegistry:
    def __init__(self): self._revoked={}
    def revoke(self,signer:str,reason:str,timestamp:int):
        if not isinstance(signer,str) or not signer.strip() or not isinstance(reason,str) or not reason.strip() or not isinstance(timestamp,int) or timestamp<0: raise ValueError('invalid_revocation')
        self._revoked[signer]=Revocation(signer,reason,timestamp)
        return self._revoked[signer]
    def is_revoked(self,signer:str)->bool: return signer in self._revoked
    def get(self,signer:str): return self._revoked.get(signer)
    def active_signers(self,signers): return tuple(s for s in signers if not self.is_revoked(s))
