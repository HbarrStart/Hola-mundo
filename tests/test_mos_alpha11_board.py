from scripts.mos_alpha11_board import BoardCard, project


def card(decision='HOLD'):
    return BoardCard('c1','Estado del evento',decision,'LOW','sgc','PRIMARY_FOUND','2026-08-14T14:00:00Z',('e1',),('h1',))


def test_board_preserves_gate_decision():
    assert project(card('HOLD'))['gate_decision'] == 'HOLD'


def test_board_allows_all_safety_states_without_promotion():
    for state in ['ALLOW','ALLOW_WITH_CONTEXT','HUMAN_REVIEW','HOLD','BLOCK']:
        assert project(card(state))['gate_decision'] == state


def test_invalid_gate_state_fails_closed():
    try:
        project(card('CONFIRMED'))
    except ValueError as e:
        assert str(e) == 'invalid_gate_decision'
    else:
        raise AssertionError('board must reject unknown gate state')
