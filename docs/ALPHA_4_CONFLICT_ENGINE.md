# MOS Alpha-4 — Conflict Engine

## Mission
Classify the relationship between two claims without deciding which source is truthful by popularity, repetition, or source class.

## Relations
- `DUPLICATE`: same subject, unit and value.
- `UPDATE`: newer claim explicitly supersedes an earlier claim.
- `CORRECTION`: explicit supersession plus evidence reference; requires human review before publication.
- `CONFLICT`: materially different values for the same subject within the configured temporal window.
- `UNRESOLVED`: insufficient evidence or incompatible metadata.

## Safety rules
1. Never resolve a conflict by majority count.
2. Never treat a later publication as automatically correct.
3. Never infer a correction without explicit metadata/evidence.
4. Unknown timestamps keep the relationship unresolved.
5. The engine classifies relationships; the Safety Gate decides publication.

## Example
`281 deaths` and `285 deaths` on the same day are `CONFLICT` unless the newer claim explicitly identifies itself as a replacement/update of the earlier claim. This prevents MOS from silently choosing a number.
