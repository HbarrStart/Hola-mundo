# MOS Alpha-16 — Synthetic End-to-End Test

This phase uses synthetic data only. It must not be presented as evidence about any real emergency.

## Test scenario
- Source A reports value `100`.
- Source B later reports value `150`.
- Neither record states that B supersedes A.

Expected relation: `UNRESOLVED_CHANGE`.

## Traceability requirement
Every synthetic claim retains `claim_id`, `source_id`, `evidence_id`, and `observed_at`.

## Safety boundary
This fixture does not connect to live sources and cannot publish real-world claims. It exists to test identity preservation and conservative temporal handling before live ingestion is attempted.
