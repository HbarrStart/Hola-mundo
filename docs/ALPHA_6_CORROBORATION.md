# MOS Alpha-6 — Corroboration Engine

## Purpose
Evaluate whether the available evidence meets the minimum corroboration requirements for a specific claim type.

## Claim types
- `EVENT_EXISTENCE`: instrumental, official record, or direct observation can establish the existence of an event; one independent upstream may be sufficient for this stage.
- `CASUALTY_COUNT`: requires at least two independent upstream evidence lines and an accepted evidence type.
- `DAMAGE_REPORT`: requires at least two independent upstream evidence lines.
- `ACCESS_STATUS`: requires at least two independent upstream evidence lines.
- `RESOURCE_AVAILABILITY`: requires at least two independent upstream evidence lines.

## Important boundary
`READY_FOR_SAFETY_GATE` means only that the corroboration requirements were met. It is **not** `CONFIRMED` and does not publish anything.

The engine also rejects unsupported claim types and treats contradictions as a review condition.

## Anti-amplification rule
Multiple publications that share the same upstream source do not count as independent evidence. Evidence Graph supplies the lineage used by this engine.
