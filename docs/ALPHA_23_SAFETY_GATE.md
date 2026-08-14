# MOS Alpha-23 — Safety Gate

The Safety Gate is a fail-closed decision boundary between verification and downstream publication.

## Decisions
- `ALLOW`: all required checks pass.
- `ALLOW_WITH_CONTEXT`: lower-risk claim may be surfaced only with explicit uncertainty/context.
- `HUMAN_REVIEW`: mandatory human decision before publication.
- `HOLD`: evidence, temporal validity, or freshness is insufficient.
- `BLOCK`: provenance or another hard safety requirement fails.

## Hard rules
1. Missing provenance blocks.
2. Missing evidence holds.
3. Stale or temporally unresolved claims hold.
4. Critical risk requires human review.
5. High risk without corroboration requires human review.
6. The gate never publishes content; `can_publish()` only indicates whether a downstream publisher may proceed.

This phase uses synthetic inputs and has no live publishing capability.
