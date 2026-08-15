#!/usr/bin/env python3
"""MOS Alpha-51: auditable replay-store decisions."""
from dataclasses import dataclass
from scripts.mos_alpha46_secure_envelope import Envelope, verify

@dataclass(frozen=True)
class ReplayDecision:
    accepted: bool
    reason: str
    key_id: str
    timestamp: int

class ReplayAuditor:
    def __init__(self, ttl_seconds:int):
        if not isinstance(ttl_seconds,int) or ttl_seconds<=0: raise ValueError('invalid_ttl')
        self.ttl_seconds=ttl_seconds; self._seen={}; self._history=[]
    def accept(self,e:Envelope,secret:bytes,now:int)->ReplayDecision:
        if not isinstance(now,int) or now<0: return self._record(False,'invalid_time',e,now)
        if not verify(e,secret): return self._record(False,'invalid_signature',e,now)
        self.prune(now)
        key=f'{e.key_id}:{e.signature}'
        if key in self._seen: return self._record(False,'replay',e,now)
        self._seen[key]=now; return self._record(True,'accepted',e,now)
    def prune(self,now:int):
        cutoff=now-self.ttl_seconds
        for k,t in list(self._seen.items()):
            if t<cutoff: del self._seen[k]
    def _record(self,accepted,reason,e,now):
        d=ReplayDecision(accepted,reason,e.key_id,now); self._history.append(d); return d
    def history(self): return tuple(self._history)
