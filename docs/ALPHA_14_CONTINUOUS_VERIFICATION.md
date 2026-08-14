# MOS Alpha-14 — Continuous Verification

## Objective
Every push and pull request runs the MOS Python test suite in GitHub Actions.

## Fail-closed rule
A failing test means the change is not considered verified. No claim of operational readiness may be made from a green-looking repository alone; deployment and real-world integration remain separate gates.

## Current workflow
`.github/workflows/mos-ci.yml`

The workflow:
1. checks out the repository;
2. installs Python 3.12;
3. installs pytest;
4. runs `python -m pytest -q`.

## Safety boundary
CI proves repeatable software tests, not truth of emergency data. Real-source provenance, freshness, corroboration, human review, and operational safety remain separate controls.
