#!/usr/bin/env python3
"""MOS Alpha-38: deterministic alert deduplication without losing severity."""
from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class Alert:
    source: str
    event_type: str
    entity: str
    message: str
    severity: str

def _severity(value):
    levels={'LOW':0,'MEDIUM':1,'HIGH':2,'CRITICAL':3}
    if value not in levels:
        raise ValueError('invalid_severity')
    return levels[value]

def fingerprint(alert: Alert) -> str:
    if not all(isinstance(v, str) and v.strip() for v in (alert.source, alert.event_type, alert.entity, alert.message, alert.severity)):
        raise ValueError('invalid_alert')
    _severity(alert.severity)
    payload=json.dumps({'source':alert.source,'event_type':alert.event_type,'entity':alert.entity,'message':alert.message},sort_keys=True,ensure_ascii=False,separators=(',',':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def deduplicate(alerts):
    grouped={}
    for alert in alerts:
        key=fingerprint(alert)
        if key not in grouped:
            grouped[key]=alert
        elif _severity(alert.severity) > _severity(grouped[key].severity):
            grouped[key]=alert
    return tuple(grouped.values())
