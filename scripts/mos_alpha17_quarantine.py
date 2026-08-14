#!/usr/bin/env python3
"""MOS Alpha-17 live-source quarantine boundary.

This module accepts metadata about a real public source but NEVER publishes it.
No network fetching occurs here. A future connector may populate SourceRecord.
"""
from dataclasses import dataclass
from enum import Enum

class QuarantineStatus(str, Enum):
    QUARANTINED = 'QUARANTINED'
    REJECTED = 'REJECTED'

@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    url: str
    retrieved_at: str
    content_hash: str
    publisher: str | None = None

@dataclass(frozen=True)
class QuarantineRecord:
    source: SourceRecord
    status: QuarantineStatus
    publishable: bool = False


def quarantine(source: SourceRecord) -> QuarantineRecord:
    if not source.source_id or not source.url or not source.retrieved_at or not source.content_hash:
        raise ValueError('incomplete_source_provenance')
    return QuarantineRecord(source=source, status=QuarantineStatus.QUARANTINED)


def can_publish(record: QuarantineRecord) -> bool:
    return record.publishable is True

if __name__ == '__main__':
    print('MOS Alpha-17: live-source quarantine boundary')
