# MOS Alpha-11 — Emergency Board

## Purpose
Provide a human-facing, read-only projection of claims after the safety pipeline. The board does not verify, promote, or rewrite claims.

## Visible states
- `ALLOW`: publishable under current gate conditions.
- `ALLOW_WITH_CONTEXT`: publishable only with required context.
- `HUMAN_REVIEW`: blocked from automatic publication pending review.
- `HOLD`: temporarily withheld because a required condition is incomplete/stale.
- `BLOCK`: prohibited by the current safety policy.

## Card fields
Each card preserves claim ID, title, gate decision, risk level, source, primary-source status, update time, evidence references, and history references.

## Safety invariant
`CONFIRMED` is deliberately not a board state. Confirmation is not inferred from a UI label. The board renders the decision produced by the Safety Gate.
