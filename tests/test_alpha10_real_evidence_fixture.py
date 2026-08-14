import json
from pathlib import Path


def test_alpha10_real_evidence_stays_quarantined():
    p = Path('data/alpha10/real_evidence_event_2026-08-10.json')
    data = json.loads(p.read_text(encoding='utf-8'))
    assert data['status'] == 'QUARANTINED'
    assert data['claim_type'] == 'EVENT_EXISTENCE'
    assert data['source_class'] == 'SECONDARY'
    assert data['next_required_step'].startswith('Resolve and ingest')
