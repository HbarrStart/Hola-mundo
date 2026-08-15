#!/usr/bin/env python3
"""MOS Alpha-70: safe ingestion of allowlisted official sources.

Collection only: fetched material is returned as raw evidence and is never
promoted to a publishable claim by this module.
"""
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen

@dataclass(frozen=True)
class OfficialSource:
    name: str
    url: str
    domain: str
    active: bool = True

@dataclass(frozen=True)
class RawEvidence:
    source: str
    url: str
    body: str
    content_type: str

class SourceNotAllowed(ValueError):
    pass

def allowed(source: OfficialSource) -> bool:
    parsed = urlparse(source.url)
    return source.active and parsed.scheme == "https" and parsed.hostname == source.domain

def ingest(source: OfficialSource, timeout: float = 10.0) -> RawEvidence:
    if not allowed(source):
        raise SourceNotAllowed(source.url)
    request = Request(source.url, headers={"User-Agent": "MOS-official-ingest/1.0"})
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        content_type = response.headers.get("Content-Type", "")
    return RawEvidence(source.name, source.url, body, content_type)

def ingest_all(sources, fetch=ingest):
    results=[]
    for source in sources:
        if allowed(source):
            results.append(fetch(source))
    return tuple(results)
