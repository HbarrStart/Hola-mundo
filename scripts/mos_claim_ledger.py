#!/usr/bin/env python3
"""MOS Claim Ledger: append-only, timestamp-aware claim records.

This module does not decide truth. It preserves provenance, timestamps,
versions and explicit review state so later verification can be audited.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any

VALID_STATES = {
    "PENDING_VERIFICATION",
    "CORROBORATED",
    "CONFIRMED",
    "CONFLICTING",
    "SUPERSEDED",
    "EXPIRED",
}


def validate_claim(claim: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("id", "statement", "observed_at", "received_at", "source")
    for key in required:
        if not claim.get(key):
            errors.append(f"missing:{key}")
    if claim.get("verification_state") not in VALID_STATES:
        errors.append("invalid:verification_state")
    for key in ("observed_at", "received_at"):
        if claim.get(key):
            try:
                datetime.fromisoformat(str(claim[key]).replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"invalid_datetime:{key}")
    if not claim.get("source_url"):
        errors.append("missing:source_url")
    return errors


def relation_for_versions(previous: dict[str, Any], current: dict[str, Any]) -> str:
    """Conservative temporal relation; never silently merges numerical changes."""
    if previous.get("statement") == current.get("statement"):
        return "DUPLICATE_OR_RESTATEMENT"
    if previous.get("topic") == current.get("topic"):
        return "UPDATE_OR_CONFLICT_REQUIRES_REVIEW"
    return "UNRELATED"
