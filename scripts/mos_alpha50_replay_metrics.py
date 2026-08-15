#!/usr/bin/env python3
"""MOS Alpha-50: observable replay-store metrics."""
from dataclasses import dataclass
from scripts.mos_alpha49_replay_store import ReplayStore

@dataclass(frozen=True)
class ReplayMetrics:
    accepted:int=0
    rejected:int=0
    pruned:int=0

class InstrumentedReplayStore:
    def __init__(self, ttl_seconds:int):
        self.store=ReplayStore(ttl_seconds)
        self.metrics=ReplayMetrics()

    def accept(self, envelope, secret:bytes, now:int)->bool:
        before=self.store.size()
        ok=self.store.accept(envelope,secret,now)
        after=self.store.size()
        removed=max(0,before+1-after) if ok else 0
        self.metrics=ReplayMetrics(self.metrics.accepted+int(ok),self.metrics.rejected+int(not ok),self.metrics.pruned+removed)
        return ok

    def prune(self, now:int)->int:
        n=self.store.prune(now)
        self.metrics=ReplayMetrics(self.metrics.accepted,self.metrics.rejected,self.metrics.pruned+n)
        return n
