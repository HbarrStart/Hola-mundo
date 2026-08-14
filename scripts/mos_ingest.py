#!/usr/bin/env python3
"""MOS ingestion skeleton.

This first implementation deliberately does not auto-publish claims. It collects
source metadata and creates a deterministic ingestion report. Parsers for each
source are added only after the source's public format is confirmed.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FEEDS = ROOT / "data" / "feeds.json"
OUT = ROOT / "data" / "ingestion_report.json"


def fetch(url: str) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": "MOS-Emergency-Monitor/0.1"})
    with urlopen(req, timeout=20) as response:  # noqa: S310 - URLs are repository-controlled
        body = response.read()
        return response.status, hashlib.sha256(body).hexdigest()


def main() -> int:
    config = json.loads(FEEDS.read_text(encoding="utf-8"))
    results = []
    now = datetime.now(timezone.utc).isoformat()

    for feed in config["feeds"]:
        item = {
            "feed_id": feed["id"],
            "source_id": feed["source_id"],
            "checked_at": now,
            "url": feed["url"],
            "enabled": feed.get("enabled", True),
        }
        if not item["enabled"]:
            item["status"] = "DISABLED"
        else:
            try:
                status, digest = fetch(feed["url"])
                item.update({"status": "REACHABLE" if status < 400 else "HTTP_ERROR", "http_status": status, "content_sha256": digest})
            except Exception as exc:  # keep one failing source from blocking the whole monitor
                item.update({"status": "FETCH_ERROR", "error": type(exc).__name__})
        results.append(item)

    OUT.write_text(json.dumps({"generated_at": now, "results": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
