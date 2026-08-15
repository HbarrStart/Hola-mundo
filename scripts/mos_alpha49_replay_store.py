#!/usr/bin/env python3
"""MOS Alpha-49: bounded replay store with explicit pruning."""
from dataclasses import dataclass
from scripts.mos_alpha46_secure_envelope import Envelope, verify

@dataclass
class ReplayStore:
    ttl_seconds: int
    _seen: dict

    def __init__(self, ttl_seconds:int):
        if not isinstance(ttl_seconds,int) or ttl_seconds<=0: raise ValueError('invalid_ttl')
        self.ttl_seconds=ttl_seconds; self._seen={}

    def _key(self,e:Envelope)->str: return f'{e.key_id}:{e.signature}'

    def accept(self,e:Envelope,secret:bytes,now:int)->bool:
        if not isinstance(now,int) or now<0 or not verify(e,secret): return False
        self.prune(now)
        key=self._key(e)
        if key in self._seen: return False
        self._seen[key]=now; return True

    def prune(self,now:int)->int:
        if not isinstance(now,int) or now<0: return 0
        cutoff=now-self.ttl_seconds
        stale=[k for k,t in self._seen.items() if t < cutoff]
        for k in stale: del self._seen[k]
        return len(stale)

    def size(self)->int: return len(self._seen)
