# MOS Alpha-12 — Common Operational Picture

## Purpose
Provide a geographic projection of claims that have already passed the publication Safety Gate.

## Non-negotiable rules
1. The COP never creates or verifies facts.
2. `HOLD`, `HUMAN_REVIEW`, and `BLOCK` claims are never projected publicly.
3. Sensitive locations are never exposed by default.
4. Unknown location precision hides coordinates rather than guessing them.
5. Vague text never becomes a precise coordinate automatically.
6. Public map data retains claim ID, risk, and update time so users can trace the information.

## Location precision
Recommended levels: `COUNTRY`, `DEPARTMENT`, `MUNICIPALITY`, `CITY`, `ZONE`, `EXACT`.
`EXACT` is subject to additional sensitivity controls and should normally remain private for operational resources, vulnerable persons, shelters, rescue teams, medical assets, and similar sensitive entities.

## Design principle
The map is a **projection**, not a source of truth. Its authority comes entirely from the upstream evidence and Safety Gate decisions.
