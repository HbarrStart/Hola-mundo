# MOS Alpha-5 — Evidence Graph

## Objective
Trace every claim to its evidence and preserve upstream-source lineage.

## Critical rule
Five articles that all reproduce one UNGRD bulletin count as **one upstream evidence lineage**, not five independent confirmations.

## Relationships
- `SUPPORTS`: evidence supports a claim.
- `REPEATS_UPSTREAM`: publication repeats an upstream source already represented.
- `INDEPENDENT_UPSTREAM`: evidence comes from a distinct upstream source.
- `MISSING_SOURCE`: evidence cannot be resolved to a registered source.

## Safety
The graph does **not** confirm, reject, or publish claims. It only provides evidence topology to the corroboration and Safety Gate layers.

## Minimum audit fields
Each evidence item should preserve source ID, claim ID, retrieval time, evidence type, and content hash when available.
