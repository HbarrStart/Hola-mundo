from scripts.mos_cop import MapClaim, project


def test_hold_claim_never_appears_on_public_map():
    r = project(MapClaim('c1','daño reportado',5.0,-76.0,'HOLD','HIGH','2026-08-14T15:00:00Z','CITY'))
    assert r['visible'] is False


def test_public_claim_with_unknown_precision_hides_coordinates():
    r = project(MapClaim('c2','afectación',5.0,-76.0,'ALLOW','MEDIUM','2026-08-14T15:00:00Z','UNKNOWN'))
    assert r['visible'] is True
    assert r['location'] is None


def test_sensitive_location_is_not_projected():
    r = project(MapClaim('c3','recurso sensible',5.0,-76.0,'ALLOW_WITH_CONTEXT','HIGH','2026-08-14T15:00:00Z','EXACT',True))
    assert r['visible'] is False


def test_gated_city_level_location_can_be_projected():
    r = project(MapClaim('c4','afectación urbana',5.0,-76.0,'ALLOW','LOW','2026-08-14T15:00:00Z','CITY'))
    assert r['visible'] is True
    assert r['location']['precision'] == 'CITY'
