# MOS Alpha-18 — Source Registry

## Purpose
Maintain structured provenance metadata for institutional, journalism, independent-research, public-observation and other source classes.

## Critical rule
A source profile is metadata, not a truth score. Registration does not make a source authoritative and never bypasses evidence, corroboration, risk assessment, freshness checks, or human review.

## Safety behavior
`source_is_publishable()` always returns `False` at this layer. Publication belongs to the downstream Safety Gate.

## Bias control
MOS should not exclude a source solely because it is large, small, official, independent, a journalist, analyst, or citizen. Source class can inform context and risk, but individual claims require their own evidence assessment.
