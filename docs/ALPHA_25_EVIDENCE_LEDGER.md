# MOS Alpha-25 — Evidence Ledger

The Evidence Ledger stores traceable evidence records linked to claims and sources.

## Required provenance
- `evidence_id`
- `claim_id`
- `source_id`
- `location`
- `retrieved_at`
- `content_hash` (SHA-256)
- `evidence_type`
- `pointer`
- `relation`

## Relations
`SUPPORTS`, `CONTRADICTS`, `QUALIFIES`, `SUPERSEDES`.

## Safety boundary
A ledger entry is evidence metadata, not proof of truth. Hashing provides integrity checking for the captured content; it does not establish authenticity, accuracy, or freshness. No live ingestion or publication is enabled by Alpha-25.

All current tests use synthetic evidence.
