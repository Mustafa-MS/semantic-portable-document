"""Capture reproducible verification commands and their complete outputs."""
import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'
PY = str(ROOT / 'validator-b/.venv/Scripts/python.exe')
CHECKS = [
    ('a-fmt', ['cargo', 'fmt', '--check'], 'validator-a'),
    ('a-clippy', ['cargo', 'clippy', '--offline', '--all-targets', '--', '-D', 'warnings'], 'validator-a'),
    ('a-tests', ['cargo', 'test', '--offline'], 'validator-a'),
    ('a-release', ['cargo', 'build', '--release', '--offline'], 'validator-a'),
    ('b-lint', [PY, '-m', 'ruff', 'check', 'spd_validator_b', 'tests'], 'validator-b'),
    ('b-wheel', [PY, '-m', 'build', '--wheel', '--no-isolation', '--outdir', '../validator-convergence/dist'], 'validator-b'),
    ('b-tests', [PY, '-m', 'pytest', '--junitxml=../validator-convergence/validator-b-tests.xml'], 'validator-b'),
    ('repository-tests', ['pwsh', '-NoProfile', '-File', 'scripts/test.ps1'], '.'),
]


def run(item):
    name, command, cwd = item
    completed = subprocess.run(command, cwd=ROOT / cwd, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=900)
    (OUT / (name + '.log')).write_text(completed.stdout + '\n' + completed.stderr, encoding='utf-8')
    print(name, completed.returncode, flush=True)
    return {'name': name, 'command': command, 'cwd': cwd, 'exitCode': completed.returncode, 'log': name + '.log'}


def main():
    # Cargo serializes its own build lock; keep its sequence explicit.
    def a_checks(): return [run(c) for c in CHECKS[:4]]
    def other_checks(): return [run(c) for c in CHECKS[4:]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(a_checks), pool.submit(other_checks)]
        results = [r for future in futures for r in future.result()]
    (OUT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    assert all(r['exitCode'] == 0 for r in results), 'A required verification command failed'


if __name__ == '__main__': main()
