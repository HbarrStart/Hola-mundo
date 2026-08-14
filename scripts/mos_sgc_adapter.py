#!/usr/bin/env python3
"""MOS SGC adapter boundary.

This adapter deliberately does not guess the SGC endpoint. The endpoint is
configured externally and the raw response is preserved before normalization.
Network retrieval is kept separate from verification/publication.
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen

USER_AGENT = "MOS-Emergency/0.1 (+safety-gated research adapter)"


def fetch_json(url: str) -> dict | list:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"SGC endpoint HTTP {response.status}")
        return json.load(response)


def main() -> int:
    url = os.environ.get("MOS_SGC_ENDPOINT")
    if not url:
        print("MOS_SGC_ENDPOINT is not configured; no SGC data ingested.")
        return 0
    try:
        payload = fetch_json(url)
    except Exception as exc:
        print(f"SGC ingestion failed safely: {exc}", file=sys.stderr)
        return 0
    envelope = {
        "adapter": "sgc",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": url,
        "raw": payload,
        "verification_state": "PENDING_VERIFICATION",
    }
    print(json.dumps(envelope, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
