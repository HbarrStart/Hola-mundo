#!/usr/bin/env python3
"""MOS Alpha-32: explicit, auditable human oversight state machine."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ReviewDecision(str, Enum):
    APPROVE='APPROVE'; REJECT='REJECT'; HOLD='HOLD'
class ReviewState(str, Enum):
    REQUIRED='REQUIRED'; APPROVED='APPROVED'; REJECTED='REJECTED'; HELD='HELD'

@dataclass(frozen=True)
class ReviewRequest:
    request_id: str
    reason: str
    risk: str
    reviewer: Optional[str] = None

@dataclass(frozen=True)
class ReviewRecord:
    request_id: str
    reviewer: str
    decision: ReviewDecision
    rationale: str
    timestamp: str

def create_review(request: ReviewRequest) -> ReviewRecord:
    if not request.request_id.strip() or not request.reason.strip(): raise ValueError('invalid_review_request')
    if not request.reviewer or not request.reviewer.strip(): raise ValueError('reviewer_required')
    return ReviewRecord(request.request_id, request.reviewer, ReviewDecision.HOLD, 'PENDING_REVIEW', '')

def resolve_review(record: ReviewRecord, decision: ReviewDecision, rationale: str, timestamp: str) -> ReviewRecord:
    if record.decision is not ReviewDecision.HOLD: raise ValueError('review_already_resolved')
    if decision not in ReviewDecision: raise ValueError('invalid_review_decision')
    if not rationale.strip() or not timestamp.strip(): raise ValueError('audit_metadata_required')
    return ReviewRecord(record.request_id, record.reviewer, decision, rationale, timestamp)
