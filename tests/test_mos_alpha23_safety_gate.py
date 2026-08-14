from scripts.mos_alpha23_safety_gate import GateDecision, GateInput, can_publish, evaluate


def base(**overrides):
    values = dict(provenance_ok=True, evidence_ok=True, corroboration_ok=True,
                  temporal_ok=True, freshness_ok=True, risk='LOW', human_review_complete=False)
    values.update(overrides)
    return GateInput(**values)


def test_complete_low_risk_claim_is_allowed():
    d = evaluate(base())
    assert d == GateDecision.ALLOW
    assert can_publish(d) is True


def test_missing_provenance_blocks():
    d = evaluate(base(provenance_ok=False))
    assert d == GateDecision.BLOCK
    assert can_publish(d) is False


def test_missing_evidence_holds():
    d = evaluate(base(evidence_ok=False))
    assert d == GateDecision.HOLD
    assert can_publish(d) is False


def test_stale_or_temporally_unresolved_claim_holds():
    assert evaluate(base(freshness_ok=False)) == GateDecision.HOLD
    assert evaluate(base(temporal_ok=False)) == GateDecision.HOLD


def test_critical_claim_requires_human_review():
    d = evaluate(base(risk='CRITICAL'))
    assert d == GateDecision.HUMAN_REVIEW
    assert can_publish(d) is False
    assert evaluate(base(risk='CRITICAL', human_review_complete=True)) == GateDecision.ALLOW


def test_high_risk_without_corroboration_requires_human_review():
    d = evaluate(base(risk='HIGH', corroboration_ok=False))
    assert d == GateDecision.HUMAN_REVIEW
    assert can_publish(d) is False


def test_uncorroborated_lower_risk_can_only_pass_with_context():
    d = evaluate(base(corroboration_ok=False))
    assert d == GateDecision.ALLOW_WITH_CONTEXT
    assert can_publish(d) is True
