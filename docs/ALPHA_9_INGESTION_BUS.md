# MOS Alpha-9 — Ingestion Bus

## Goal
Provide a single entry point for incoming observations while guaranteeing provenance, hashing, and quarantine.

## Flow
`SOURCE -> INGESTION BUS -> RAW OBSERVATION -> QUARANTINED -> MOS PIPELINE`

## Invariants
1. A source ID and source URL are mandatory.
2. Empty content is rejected.
3. Every observation receives a SHA-256 digest of the exact received content.
4. Every observation records `received_at`.
5. `observed_at` is preserved when supplied; it is never inferred automatically.
6. Every new observation starts as `QUARANTINED`.
7. The ingestion bus never publishes and never promotes an observation to a fact.

## Emergency rule
If provenance or content integrity cannot be established, ingestion fails closed.
