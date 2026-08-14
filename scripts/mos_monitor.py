from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'sources.json'
OUT = ROOT / 'data' / 'source_snapshot.json'


def fetch(url: str) -> dict:
    req = Request(url, headers={'User-Agent': 'MOS-Emergency-Monitor/0.1'})
    try:
        with urlopen(req, timeout=20) as response:
            body = response.read()
            return {
                'ok': True,
                'status': response.status,
                'sha256': hashlib.sha256(body).hexdigest(),
                'bytes': len(body),
            }
    except Exception as exc:
        return {'ok': False, 'error': str(exc)[:300]}


def main() -> None:
    cfg = json.loads(SOURCES.read_text(encoding='utf-8'))
    snapshot = {
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'policy': 'Network reachability only. No automatic publication or factual confirmation is performed here.',
        'sources': []
    }
    for source in cfg['sources']:
        result = fetch(source['url']) if source.get('enabled') else {'ok': False, 'error': 'disabled'}
        snapshot['sources'].append({
            'id': source['id'],
            'name': source['name'],
            'type': source['type'],
            'url': source['url'],
            'check': result,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
