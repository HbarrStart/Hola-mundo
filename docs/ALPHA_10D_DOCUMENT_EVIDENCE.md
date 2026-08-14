# MOS Alpha-10D — Document Evidence

## Objective
Allow MOS to preserve official/public documents as auditable evidence even when no API exists.

## Supported document classes
`PDF`, `HTML`, `CSV`, `JSON`, `BULLETIN`, `PRESS_RELEASE`, `IMAGE`.

## Required provenance
- source ID
- URL
- publisher
- document type
- retrieval timestamp
- SHA-256 of exact retrieved bytes
- publication timestamp when explicitly available

## Safety
Every registered document starts as `QUARANTINED`. Registration does not validate the claims contained in the document and does not publish extracted facts.

## Emergency integrity rule
If the document bytes are empty or required provenance is missing, registration fails closed.
