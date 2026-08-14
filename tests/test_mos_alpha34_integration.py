import pytest
from scripts.mos_alpha30_risk import RiskInput
from scripts.mos_alpha34_integration import IntegrationInput, IntegrationDecision, decide

def low(): return RiskInput(1,1,1,0,1,5)
def inp(**kw):
    d=dict(risk=low(),corroboration='CONSISTENT',freshness='FRESH',provenance='INDEPENDENT',audit_valid=True); d.update(kw); return IntegrationInput(**d)

def test_clean_low_risk_allows(): assert decide(inp()) is IntegrationDecision.ALLOW

def test_medium_risk_allows_with_context(): assert decide(inp(risk=RiskInput(2,2,2,0,2,4))) is IntegrationDecision.ALLOW_WITH_CONTEXT

def test_critical_risk_requires_human(): assert decide(inp(risk=RiskInput(5,5,5,5,5,0))) is IntegrationDecision.HUMAN_REVIEW

def test_mixed_corroboration_requires_human(): assert decide(inp(corroboration='MIXED')) is IntegrationDecision.HUMAN_REVIEW

def test_stale_information_holds(): assert decide(inp(freshness='STALE')) is IntegrationDecision.HOLD

def test_unknown_provenance_requires_human(): assert decide(inp(provenance='UNKNOWN')) is IntegrationDecision.HUMAN_REVIEW

def test_invalid_audit_holds(): assert decide(inp(audit_valid=False)) is IntegrationDecision.HOLD

def test_missing_audit_holds(): assert decide(inp(audit_valid=None)) is IntegrationDecision.HOLD

def test_high_risk_requires_human(): assert decide(inp(risk=RiskInput(4,4,3,0,4,1))) is IntegrationDecision.HUMAN_REVIEW
