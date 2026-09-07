"""One-time, non-overwriting capture before convergence repairs."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'
PINS = {'spec/FORMAT_0.1_DRAFT.md': 'fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849',
        'spec/requirements.yaml': 'a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a'}


def main():
    assert not (OUT / 'baseline.json').exists(), 'Baseline already captured; never overwrite it'
    for name, value in PINS.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == value
    paths = set()
    for name in ['validator-a', 'validator-b', 'validator-differential', 'spec', 'schemas', 'tests', 'scripts']:
        for p in (ROOT / name).rglob('*'):
            if p.is_file() and not any(part in {'.venv', 'target', '__pycache__', '.pytest_cache', 'tools', '.hypothesis'} for part in p.relative_to(ROOT).parts):
                paths.add(p)
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    with zipfile.ZipFile(OUT / 'historical-inputs.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(paths):
            archive.write(p, p.relative_to(ROOT).as_posix())
    (OUT / 'baseline.json').write_text(json.dumps({'pins': PINS, 'files': hashes}, indent=2) + '\n', encoding='utf-8')
    print('Preserved', len(paths), 'files; Draft/registry pins verified.')


if __name__ == '__main__':
    main()
