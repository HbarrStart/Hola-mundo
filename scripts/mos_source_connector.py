#!/usr/bin/env python3
"""MOS source connector: fail-closed acquisition and evidence fingerprinting.

The connector retrieves a configured source, preserves the raw payload, records
retrieval metadata and hashes the exact bytes. It does not classify truth.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_evidence"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def retrieve(url: str, source_id: str, timeout: int = 15) -> dict:
    if not url.startswith(("https://", "http://")):
        raise ValueError("unsupported_url_scheme")
    req = urllib.request.Request(url, headers={"User-Agent": "MOS/0.1 evidence-connector"})
    retrieved_at = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read()
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"SOURCE_UNAVAILABLE:{exc}") from exc
    if status < 200 or status >= 300 or not body:
        raise RuntimeError("SOURCE_RESPONSE_NOT_USABLE")
    digest = hashlib.sha256(body).hexdigest()
    raw_path = RAW_DIR / f"{source_id}-{digest}.bin"
    raw_path.write_bytes(body)
    return {
        "source_id": source_id,
        "url": url,
        "retrieved_at": retrieved_at,
        "http_status": status,
        "content_type": content_type,
        "sha256": digest,
        "raw_path": str(raw_path.relative_to(ROOT)),
        "verification_state": "PENDING_VERIFICATION",
    }


def main() -> int:
    url = os.environ.get("MOS_SOURCE_URL")
    source_id = os.environ.get("MOS_SOURCE_ID", "source")
    if not url:
        print(json.dumps({"status": "HOLD", "reason": "MOS_SOURCE_URL_NOT_CONFIGURED"}))
        return 2
    try:
        result = retrieve(url, source_id)
    except Exception as exc:
        print(json.dumps({"status": "HOLD", "reason": str(exc)}))
        return 3
    print(json.dumps({"status": "ACQUIRED", "evidence": result}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
