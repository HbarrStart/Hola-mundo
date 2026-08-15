#!/usr/bin/env python3
"""MOS Alpha-70: bounded, allowlisted ingestion of official sources."""
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MAX_BYTES = 1_000_000
ALLOWED_CONTENT_TYPES = ("text/", "application/json", "application/xml")

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

class SourceNotAllowed(ValueError): pass
class IngestError(RuntimeError): pass

def allowed(source: OfficialSource) -> bool:
    p=urlparse(source.url)
    return source.active and p.scheme == "https" and p.hostname == source.domain

def ingest(source: OfficialSource, timeout: float = 10.0, max_bytes: int = MAX_BYTES) -> RawEvidence:
    if not allowed(source): raise SourceNotAllowed(source.url)
    try:
        req=Request(source.url, headers={"User-Agent":"MOS-official-ingest/1.0"})
        with urlopen(req, timeout=timeout) as response:
            ct=response.headers.get("Content-Type", "").split(";",1)[0].lower()
            if not any(ct.startswith(x) for x in ALLOWED_CONTENT_TYPES):
                raise IngestError(f"unsupported content type: {ct}")
            body=response.read(max_bytes + 1)
            if len(body) > max_bytes: raise IngestError("response exceeds size limit")
            text=body.decode("utf-8", errors="replace")
            return RawEvidence(source.name, source.url, text, ct)
    except (SourceNotAllowed, IngestError): raise
    except Exception as exc: raise IngestError(f"ingest failed: {type(exc).__name__}") from exc

def ingest_all(sources, fetch=ingest):
    results=[]
    for source in sources:
        if not allowed(source): continue
        try: results.append(fetch(source))
        except IngestError: continue
    return tuple(results)
