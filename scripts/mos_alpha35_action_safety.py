#!/usr/bin/env python3
"""MOS Alpha-35: action safety gate.
A decision is not an executable action. Actions require explicit policy,
valid decision state, audit integrity, and reversibility constraints.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ActionType(str, Enum):
    NONE='NONE'; PUBLISH='PUBLISH'; ALERT='ALERT'; ESCALATE='ESCALATE'
class ActionOutcome(str, Enum):
    EXECUTE='EXECUTE'; HOLD='HOLD'; BLOCK='BLOCK'; HUMAN_REVIEW='HUMAN_REVIEW'

@dataclass(frozen=True)
class ActionRequest:
    action: ActionType
    decision: str
    audit_valid: Optional[bool]
    reversible: bool
    policy_allows: bool
    human_approved: bool = False

def authorize_action(x: ActionRequest) -> ActionOutcome:
    if x.action is ActionType.NONE:
        return ActionOutcome.BLOCK
    if x.audit_valid is not True:
        return ActionOutcome.HOLD
    if x.decision in {'BLOCK','HOLD'}:
        return ActionOutcome.BLOCK if x.decision == 'BLOCK' else ActionOutcome.HOLD
    if x.decision == 'HUMAN_REVIEW' and not x.human_approved:
        return ActionOutcome.HUMAN_REVIEW
    if not x.policy_allows:
        return ActionOutcome.BLOCK
    if not x.reversible and not x.human_approved:
        return ActionOutcome.HUMAN_REVIEW
    return ActionOutcome.EXECUTE
