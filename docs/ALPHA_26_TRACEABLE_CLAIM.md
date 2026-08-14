# MOS Alpha-26 — Traceable Claim

A traceable claim is an auditable representation linking a claim to its source IDs and evidence references.

## Fail-closed requirements
- core claim metadata must be present;
- at least one source trace is required;
- at least one evidence reference is required;
- every evidence reference must have an ID and valid relation.

`audit_path()` exposes the chain without asserting that the claim is true. Truth assessment remains the responsibility of corroboration, temporal, risk, and safety layers.

All current tests are synthetic. No live emergency ingestion or publication is enabled.
