# MOS Alpha-24 — Red Team Safety Attack

Synthetic adversarial fixtures only. No live emergency data is used.

## Attack cases
1. Trusted-looking source with missing evidence -> `HOLD`.
2. Critical claim without completed human review -> `HUMAN_REVIEW`.
3. Critical claim that is stale -> `HOLD`.
4. Many observations sharing an origin, without independent corroboration -> `HUMAN_REVIEW` for high risk.
5. Temporal conflict without explicit supersession -> `HOLD`.
6. Missing provenance -> `BLOCK`.

## Success criterion
Every attack must fail closed. No adversarial case may produce `ALLOW` or `ALLOW_WITH_CONTEXT`.

## Important limitation
This is a unit-level adversarial test of the current Safety Gate. It does not prove the complete system is secure, correct, or safe for live emergency deployment. Before live use, integration tests, dependency review, source-ingestion controls, human operational procedures, monitoring, and an independent safety review are required.
