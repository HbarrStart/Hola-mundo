# MOS Claim Ledger

The Claim Ledger is the canonical audit layer for statements about an emergency.

## Required provenance

Every claim records:

- unique claim ID;
- exact statement;
- event/topic;
- observed time;
- received time;
- source identity;
- original source URL;
- verification state;
- version/replacement relationship when applicable.

## Critical rule

A newer number does not automatically replace an older number. MOS first determines whether the two statements refer to the same reporting period and underlying fact.

For example, `281 deaths` and `285 deaths` must remain separate claims until their timestamps and source context establish whether one is an update, a correction, or a conflict.

## Publication

The Claim Ledger is not itself the public board. Claims must still pass corroboration, risk assessment, and the Safety Gate before publication as confirmed operational information.

## Independent sources

Independent media, journalists, researchers, elected officials and citizen reports can all contribute claims. Source category is provenance metadata, not an automatic truth score.
