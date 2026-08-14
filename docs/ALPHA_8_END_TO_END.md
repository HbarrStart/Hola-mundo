# MOS Alpha-8 — End-to-End Safety Harness

## Scope
Alpha-8 wires corroboration, risk, and Safety Gate into one deterministic harness. It is an integration test harness, not a live publisher.

## Scenarios
1. Valid low-risk event existence -> `ALLOW`.
2. Insufficient casualty evidence -> `HOLD`.
3. High-harm operational claim -> `HUMAN_REVIEW`.
4. Stale evidence -> `HOLD`.
5. Unresolved contradiction -> `HUMAN_REVIEW`.
6. Personal data -> `BLOCK`.
7. Unregistered source -> `BLOCK`.

## Critical boundary
Alpha-8 does not fetch, infer, or publish live emergency facts. A live adapter must provide registered source metadata, raw evidence, timestamps, and evidence integrity metadata before entering this harness.

## Exit criterion
Alpha-8 is not considered production-ready until the same scenarios pass using the actual source connector and real fixtures, with automated tests and an independent human review of the gate rules.
