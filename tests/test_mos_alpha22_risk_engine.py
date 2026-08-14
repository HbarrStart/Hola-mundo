from scripts.mos_alpha22_risk_engine import RiskLevel, VerificationTier, classify_risk, required_verification


def test_low_risk_uses_standard_verification():
    risk = classify_risk(2, 2)
    assert risk == RiskLevel.LOW
    assert required_verification(risk) == VerificationTier.STANDARD


def test_high_risk_requires_strict_verification():
    risk = classify_risk(8, 7)
    assert risk == RiskLevel.HIGH
    assert required_verification(risk) == VerificationTier.STRICT


def test_critical_risk_requires_human_review():
    risk = classify_risk(10, 9)
    assert risk == RiskLevel.CRITICAL
    assert required_verification(risk) == VerificationTier.HUMAN_REVIEW


def test_score_is_bounded():
    assert classify_risk(100, 100) == RiskLevel.CRITICAL
