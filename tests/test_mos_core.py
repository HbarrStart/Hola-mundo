import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_normalizer_rejects_unknown_source_type():
    m = load("mos_normalize")
    try:
        m.normalize({"id":"x","title":"x","source_id":"x","source_type":"unknown","source_url":"https://example.org","published_at":"2026-08-14T00:00:00Z"})
        assert False
    except ValueError as exc:
        assert str(exc) == "invalid_source_type"


def test_normalizer_does_not_invent_evidence():
    m = load("mos_normalize")
    out = m.normalize({"id":"x","title":"x","source_id":"x","source_type":"citizen_report","source_url":"https://example.org","published_at":"2026-08-14T00:00:00Z"})
    assert out["evidence_types"] == []


def test_conflicting_values_are_not_merged():
    m = load("mos_conflicts")
    result = m.detect_conflicts([
        {"claim_key":"victims","value":10,"source_url":"https://a.example"},
        {"claim_key":"victims","value":12,"source_url":"https://b.example"},
    ])
    assert result[0]["type"] == "CONFLICTING_REPORTS"
    assert result[0]["requires_human_review"] is True
