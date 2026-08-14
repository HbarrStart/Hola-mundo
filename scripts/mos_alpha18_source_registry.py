#!/usr/bin/env python3
"""MOS Alpha-18 source registry.

The registry describes provenance and operational metadata. It does not assign
truth to a source and it does not allow registry membership to bypass evidence
or the Safety Gate.
"""
from dataclasses import dataclass
from enum import Enum

class SourceClass(str, Enum):
    INSTITUTIONAL = 'INSTITUTIONAL'
    JOURNALISM = 'JOURNALISM'
    INDEPENDENT_RESEARCH = 'INDEPENDENT_RESEARCH'
    PUBLIC_OBSERVATION = 'PUBLIC_OBSERVATION'
    OTHER = 'OTHER'

@dataclass(frozen=True)
class SourceProfile:
    source_id: str
    name: str
    source_class: SourceClass
    url: str
    active: bool = True
    notes: str = ''


def register(profile: SourceProfile) -> SourceProfile:
    if not profile.source_id or not profile.name or not profile.url:
        raise ValueError('incomplete_source_profile')
    return profile


def source_is_publishable(profile: SourceProfile) -> bool:
    # Registry membership never grants publication authority.
    return False

if __name__ == '__main__':
    print('MOS Alpha-18: provenance registry only')
