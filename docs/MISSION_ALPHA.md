# Mission Alpha — execution record

## Objective
Demonstrate the complete MOS path from an observation to a safety-gated public dataset without inventing or promoting emergency facts.

## Run
The pipeline consumes `data/alpha_observations.json` and writes `data/alpha_result.json`.

## Result
**HOLD**.

The fixture intentionally contains only a reference to the official SGC source and explicitly states that it is not a seismic event. MOS therefore creates an observation/claim in `PENDING_VERIFICATION` and publishes zero public facts.

This is a successful safety result: the system did not manufacture a disaster fact merely because a source was present.

## Live-data gate
A real SGC event must be ingested from an authoritative machine-readable source or a captured official bulletin whose retrieval timestamp and original URL can be preserved. Search results alone are not accepted as the event record.

Until that source payload is available and validated, Mission Alpha remains **HOLD — LIVE SOURCE PENDING**.

## Prohibited shortcuts
- no manually invented earthquake magnitude, location, casualties or damage;
- no conversion of a source reference into a confirmed event;
- no publication from search snippets;
- no automatic operational instructions;
- no merging of conflicting reports.
