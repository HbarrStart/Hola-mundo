#!/usr/bin/env python3
"""MOS Alpha-10D document evidence registry.

Registers official/public documents without treating document text as truth.
The registry preserves provenance and integrity metadata for later extraction.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib, json

@dataclass(frozen=True)
class DocumentEvidence:
    document_id: str
    source_id: str
    url: str
    publisher: str
    document_type: str
    published_at: str | None
    retrieved_at: str
    content_sha256: str
    status: str = 'QUARANTINED'


def register_document(source_id: str, url: str, publisher: str, document_type: str, content: bytes, published_at: str | None = None) -> DocumentEvidence:
    if not all([source_id, url, publisher, document_type]) or not content:
        raise ValueError('invalid_document_evidence')
    digest = hashlib.sha256(content).hexdigest()
    return DocumentEvidence('doc-' + digest[:16], source_id, url, publisher, document_type, published_at, datetime.now(timezone.utc).isoformat(), digest)


def to_json(doc: DocumentEvidence) -> str:
    return json.dumps(asdict(doc), ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('MOS Document Evidence loaded: provenance + hash + quarantine')
