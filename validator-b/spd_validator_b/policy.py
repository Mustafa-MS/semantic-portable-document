"""Shared contract data, not shared validator implementation."""
import json
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def policy():
    path = Path(__file__).resolve().parents[2] / 'validation/REQUIREMENT_ATTRIBUTION_0.1.2.json'
    if not path.is_file():
        path = Path(__file__).resolve().parent / 'data/REQUIREMENT_ATTRIBUTION_0.1.2.json'
    return json.loads(path.read_text(encoding='utf-8'))


def external_ids(output: str) -> list[str]:
    found = set()
    for line in output.splitlines():
        diagnostic = re.search(r'\b(?:ERROR|FATAL)\(([A-Z]+-\d+[a-z]?)\)', line)
        if diagnostic:
            found.add('SPD-BASE-002')
            for rule in policy()['externalDiagnostics']:
                if rule['code'] == diagnostic[1] and re.search(rule['pattern'], line):
                    found.update(rule['ids'])
    return sorted(found)
