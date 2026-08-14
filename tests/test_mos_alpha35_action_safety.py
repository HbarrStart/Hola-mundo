import pytest
from scripts.mos_alpha35_action_safety import ActionType,ActionOutcome,ActionRequest,authorize_action

def req(**kw):
    d=dict(action=ActionType.PUBLISH,decision='ALLOW',audit_valid=True,reversible=True,policy_allows=True,human_approved=False); d.update(kw); return ActionRequest(**d)

def test_valid_reversible_action_executes(): assert authorize_action(req()) is ActionOutcome.EXECUTE

def test_invalid_audit_holds(): assert authorize_action(req(audit_valid=False)) is ActionOutcome.HOLD

def test_hold_cannot_execute(): assert authorize_action(req(decision='HOLD')) is ActionOutcome.HOLD

def test_block_cannot_execute(): assert authorize_action(req(decision='BLOCK')) is ActionOutcome.BLOCK

def test_review_requires_human(): assert authorize_action(req(decision='HUMAN_REVIEW')) is ActionOutcome.HUMAN_REVIEW

def test_policy_denial_blocks(): assert authorize_action(req(policy_allows=False)) is ActionOutcome.BLOCK

def test_irreversible_requires_human(): assert authorize_action(req(reversible=False)) is ActionOutcome.HUMAN_REVIEW

def test_human_approved_irreversible_can_execute(): assert authorize_action(req(reversible=False,human_approved=True)) is ActionOutcome.EXECUTE

def test_none_action_is_never_executed(): assert authorize_action(req(action=ActionType.NONE)) is ActionOutcome.BLOCK

def test_review_with_human_approval_can_execute(): assert authorize_action(req(decision='HUMAN_REVIEW',human_approved=True)) is ActionOutcome.EXECUTE
