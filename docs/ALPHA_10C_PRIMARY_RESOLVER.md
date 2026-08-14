# MOS Alpha-10C — Primary Resolver

## Purpose
Record attempts to resolve a claim against a primary source without converting absence of a record into falsity.

## Resolution states
- `PRIMARY_FOUND`: primary record identified and evidence reference retained.
- `PRIMARY_UPDATED`: an existing primary record supersedes an earlier primary record.
- `PRIMARY_NOT_FOUND`: the resolver searched the configured primary channel and did not find a matching record.
- `PRIMARY_UNAVAILABLE`: the primary channel could not be queried or retrieved.
- `PRIMARY_CONFLICT`: primary channels contain incompatible records.
- `PRIMARY_RECORD_INVALID`: a candidate record fails structural/provenance validation.

## Required fields on success
A successful resolution must include both a primary `record_id` and an `evidence_ref`.

## Safety rule
`PRIMARY_NOT_FOUND` and `PRIMARY_UNAVAILABLE` are **not false**. They are evidence gaps and remain non-public until the normal MOS pipeline resolves them.

## Resolver methods
- `API`
- `OFFICIAL_PAGE`
- `OFFICIAL_DOCUMENT`

The resolver does not guess identifiers, coordinates, magnitude, dates, or other event attributes.
