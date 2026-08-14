# MOS Alpha-17 — Live Source Quarantine

## Objective
Introduce real-source metadata into MOS without allowing it to become public information automatically.

## Hard boundary
A source record must contain:
- stable source ID;
- URL;
- retrieval timestamp;
- content hash;
- publisher when known.

It enters `QUARANTINED` status and `publishable=false`.

## No-network rule in this phase
The Alpha-17 fixture does not fetch live content. A future ingestion connector may retrieve a public document, but ingestion must first store provenance and hash it before downstream processing.

## Publication gate
`can_publish()` remains false for quarantined records. Publication requires a later, separate Safety Gate decision based on evidence, corroboration, freshness, risk and—when required—human review.

## Important
This phase does not declare any real-world source truthful merely because it is official, independent, journalistic, or widely shared. Source identity and claim truth are separate properties.
