"""Capture the pre-clarification inputs once; never replace historical evidence."""
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/pre_rc_passive_security'

def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'BASELINE_FREEZE.md').exists(), 'Baseline already exists'
    paths = []
    for directory in ('spec', 'schemas', 'validator-a', 'validator-b', 'validation', 'tests', 'validator-convergence', 'reports/epub_boundary_security_gate'):
        for path in (ROOT / directory).rglob('*'):
            if path.is_file() and not set(path.parts) & {'.venv', 'target', '__pycache__', '.pytest_cache', '.ruff_cache', 'tools', '.hypothesis'}:
                paths.append(path)
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    assert hashes['spec/FORMAT_0.1_DRAFT.md'] == 'fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849'
    with zipfile.ZipFile(OUT / 'pre-clarification-inputs.zip', 'x', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(paths):
            z.write(p, p.relative_to(ROOT).as_posix())
    (OUT / 'baseline-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
    manifests = list((ROOT / 'tests').rglob('*manifest*.json'))
    manifest_rows = '\n'.join(f'- `{p.relative_to(ROOT).as_posix()}`: `{hashlib.sha256(p.read_bytes()).hexdigest()}`' for p in manifests)
    schemas = '\n'.join(f'- `{p}`: `{h}`' for p, h in hashes.items() if p.startswith('schemas/'))
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip() or 'No HEAD commit; source SHA-256 inventory is authoritative.'
    (OUT / 'BASELINE_FREEZE.md').write_text(f'''# Pre-clarification baseline freeze

Captured before normative edits. Do not overwrite this file or its archive.

- Draft SHA-256: `{hashes['spec/FORMAT_0.1_DRAFT.md']}` (expected hash verified).
- Registry SHA-256: `{hashes['spec/requirements.yaml']}`.
- Validator A: 0.1.0-draft.2; Validator B: 0.1.1. Exact source identities in baseline-sha256.json and pre-clarification-inputs.zip.
- Git identity: {commit}
- Corpus 0.1.1: 70 fixtures, historical A/B/oracle 70/70 exact agreement; experimental 70/70. This is preserved evidence, not a new run.
- EPUBCheck 5.3.0: 70/70 executed by each; 62 PASS, 8 FAIL; all 40 historical Base-PASS fixtures passed. Environment and JAR identity are preserved in validator-convergence/environment.json within the archive.
- Historical freezes, oracle, differential artifacts and audit reports remain in place.

## Corpus manifests

{manifest_rows}

## Canonical schema identities

{schemas}
''', encoding='utf-8')
    print('Frozen', len(paths), 'files')

if __name__ == '__main__':
    main()
