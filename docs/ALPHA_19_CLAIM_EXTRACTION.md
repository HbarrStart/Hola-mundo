# MOS Alpha-19 — Claim Extraction

## Purpose
Convert a publication into discrete, traceable claims without treating the publication as established truth.

Example:
- `100 personas afectadas`
- `tres municipios con daños`
- `una vía cerrada`

## Critical distinction
`SOURCE_SAYS` is not `MOS_CONFIRMED`.

Claims enter with status `UNVERIFIED`. Verification, corroboration, risk assessment, freshness and publication happen downstream.

## Traceability
Each claim retains the source ID and original source text. A future parser may use NLP/LLM assistance, but extracted claims must be reviewable against the source text and must fail closed when required fields are missing.

## Safety
This phase contains synthetic examples only and has no live web fetching or publication capability.
