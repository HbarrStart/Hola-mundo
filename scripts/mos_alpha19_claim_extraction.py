#!/usr/bin/env python3
"""MOS Alpha-19: conservative claim extraction from a source publication.

This layer structures what a source says. It does not decide whether the claim
is true, corroborated, or publishable.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Claim:
    claim_id: str
    source_id: str
    source_text: str
    claim_text: str
    observed_at: str
    location: str | None = None
    evidence_refs: tuple[str, ...] = ()
    status: str = 'UNVERIFIED'


def extract_claims(source_id: str, source_text: str, claims: list[dict]) -> list[Claim]:
    if not source_id or not source_text:
        raise ValueError('incomplete_source_record')
    result = []
    for i, item in enumerate(claims, 1):
        text = item.get('claim_text')
        observed_at = item.get('observed_at')
        if not text or not observed_at:
            raise ValueError('incomplete_claim')
        result.append(Claim(
            claim_id=item.get('claim_id', f'{source_id}-CLAIM-{i:04d}'),
            source_id=source_id,
            source_text=source_text,
            claim_text=text,
            observed_at=observed_at,
            location=item.get('location'),
            evidence_refs=tuple(item.get('evidence_refs', ())),
        ))
    return result


def is_verified(claim: Claim) -> bool:
    return claim.status == 'VERIFIED'

if __name__ == '__main__':
    print('MOS Alpha-19: claim extraction / no truth inference')
