# MOS Situation Board

The board is a **situation view**, not a news feed.

## Display order

1. Active critical/high-risk information requiring human review.
2. Confirmed event facts.
3. Confirmed facts with current evidence.
4. Corroborated facts.
5. Conflicting reports.
6. Pending verification.
7. Expired information only in history.

## Never merge automatically

- casualty counts from different timestamps;
- missing-person counts from different reporting periods;
- road/open-route status from different timestamps;
- shelter capacity from different timestamps;
- citizen reports with official facts.

## Every visible fact must expose

- claim ID;
- verification state;
- risk level;
- source count;
- latest verification time;
- original source links;
- evidence type when available.

## Unknowns are first-class data

The board must explicitly show what MOS does **not** know. Absence of evidence must never be rendered as evidence of absence.

## Operational safety

The first public board does not issue autonomous evacuation, routing, medical, rescue, or structural-safety instructions. Such content remains human-reviewed and source-attributed.
