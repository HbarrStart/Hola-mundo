from scripts.mos_alpha24_red_team import ATTACKS, run_red_team


def test_all_adversarial_cases_fail_closed_as_expected():
    results = run_red_team()
    assert len(results) == len(ATTACKS)
    for name, actual, expected in results:
        assert actual == expected, f'{name}: expected {expected}, got {actual}'


def test_no_attack_case_is_allow():
    for name, actual, _ in run_red_team():
        assert actual.value not in {'ALLOW', 'ALLOW_WITH_CONTEXT'}, name
