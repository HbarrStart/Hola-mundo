# MOS Alpha-13 — Traceable Emergency Situation Summary

## Purpose
Generate a human-readable situation summary only from claims already present in the MOS ledger.

## Hard rules
1. The summary engine never creates facts, numbers, locations, or causal explanations.
2. Every summary item must reference at least one evidence record.
3. Unknown gate statuses fail closed.
4. Blocked claims are excluded by default.
5. Every item preserves claim ID and update timestamp for traceability.
6. The summary is a presentation layer; it cannot bypass the Safety Gate.

## Traceability
`summary item -> claim_id -> evidence_refs -> source/document`

## AI boundary
An eventual language-model presentation layer may compress or phrase already-approved ledger content, but it must not add unsupported information. Generated text must retain claim/evidence references so a reviewer can reconstruct the basis of each statement.
