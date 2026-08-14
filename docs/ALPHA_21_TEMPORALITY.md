# MOS Alpha-21 — Temporal Validity

A claim can be true at one time and obsolete later. MOS therefore separates `observed_at` from present validity.

## States
- `CURRENT`: later observation explicitly supersedes the earlier one, or reports the same value.
- `HISTORICAL`: reserved for observations known to be no longer current through a validated transition.
- `UNRESOLVED`: observations conflict and no explicit supersession relationship exists.

## Safety rule
A conflicting later observation is not automatically the current truth. It remains non-displayable as current until the relationship is established.

This phase uses synthetic data only and has no live fetching or publication capability.
