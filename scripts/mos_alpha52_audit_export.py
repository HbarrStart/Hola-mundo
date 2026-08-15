#!/usr/bin/env python3
"""MOS Alpha-52: deterministic audit-history export."""
import json
from scripts.mos_alpha51_replay_audit import ReplayDecision

def export_history(history):
    if history is None: raise ValueError('invalid_history')
    rows=[]
    for d in history:
        if not isinstance(d,ReplayDecision): raise ValueError('invalid_decision')
        rows.append({'accepted':d.accepted,'reason':d.reason,'key_id':d.key_id,'timestamp':d.timestamp})
    return json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False)
