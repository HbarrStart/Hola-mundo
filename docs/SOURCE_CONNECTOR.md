# MOS Source Connector

## Safety contract

The connector is an acquisition layer only. It does not decide whether content is true, relevant, current, or publishable.

For every successful retrieval MOS records:

- source identifier;
- original URL;
- retrieval timestamp;
- HTTP status;
- content type;
- SHA-256 hash of the exact response bytes;
- path to the preserved raw evidence;
- `PENDING_VERIFICATION` state.

## Fail-closed behavior

If the URL is missing, the scheme is unsupported, the source times out/fails, the response is not successful, or the body is empty, the connector returns `HOLD` and produces no observation for publication.

## Important operational rule

Do not configure a source URL from a search-result snippet, social post, mirror, or guessed endpoint when the official source endpoint is not known. The connector must receive a verified source endpoint before live ingestion is enabled.
