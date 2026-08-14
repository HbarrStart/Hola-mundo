# MOS Alpha-7 — Risk Engine + Safety Gate v2

## Purpose
Separate evidence quality from publication risk. A well-supported claim can still be unsafe to publish without context.

## Risk dimensions
- potential harm
- operational consequence
- sensitive location
- personal data
- rate of change
- corroboration completeness

## Actions
- `ALLOW`: low consequence and all gate conditions satisfied.
- `ALLOW_WITH_CONTEXT`: publish only with required context.
- `HUMAN_REVIEW`: human review required before publication.
- `HOLD`: evidence is incomplete/stale or a required integrity condition is missing.
- `BLOCK`: publication prohibited by the current safety rules.

## Fail-closed conditions
The Safety Gate blocks or holds when:
- source is not registered;
- evidence hash is missing;
- evidence is stale;
- corroboration is incomplete;
- contradiction remains unresolved;
- risk engine blocks publication;
- risk action is unknown.

## Important boundary
The Risk Engine and Safety Gate are publication controls, not truth or political-judgment engines. They do not decide whether a source is ideologically acceptable, whether a government is right, or whether a claim is true by popularity.
