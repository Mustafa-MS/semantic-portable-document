"""Independent executions against the reviewed oracle; no diagnostic filtering."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'
JAR = ROOT / 'validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar'
FIELDS = ['base', 'normativeCapabilities', 'violationRequirementIds', 'notTestedRequirementIds', 'operationalStatus', 'authoritativeClaimsStatus']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance(side):
    paths = [ROOT / 'spec/FORMAT_0.1_DRAFT.md', ROOT / 'spec/requirements.yaml', ROOT / 'tests/corpus-manifest.json', OUT / 'reviewed-oracle-0.1.1.json', Path(__file__), JAR]
    for folder, pattern in [('schemas', '*.json'), ('validation', '*'), ('validator-a/src', '*.rs'), ('validator-a/tests', '*.rs'), ('validator-b/spd_validator_b', '*.py'), ('validator-b/tests', '*.py')]:
        paths.extend(p for p in (ROOT / folder).rglob(pattern) if p.is_file())
    paths.extend(ROOT / p for p in ['validator-a/Cargo.toml', 'validator-a/Cargo.lock', 'validator-b/pyproject.toml'])
    if side == 'a':
        paths.append(ROOT / 'validator-a/target/release/spd-validator.exe')
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('side', choices=['a', 'b'])
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--tag', default='candidate')
    args = parser.parse_args()
    output_path = OUT / f'{args.tag}-{args.side}.json'
    detail_path = OUT / f'{args.tag}-detailed-{args.side}.json'
    if args.tag != 'candidate' and (output_path.exists() or detail_path.exists()):
        raise RuntimeError('Refusing to overwrite versioned evaluation evidence')
    started = datetime.now(timezone.utc).isoformat()
    source_before = provenance(args.side)
    manifest = json.loads((ROOT / 'tests/corpus-manifest.json').read_text(encoding='utf-8'))
    oracle = {r['fixture']: r for r in json.loads((OUT / 'reviewed-oracle-0.1.1.json').read_text(encoding='utf-8'))['results']}
    if args.side == 'b':
        sys.path.insert(0, str(ROOT / 'validator-b'))
        from spd_validator_b.validator import validate
        from spd_validator_b.models import ValidationOptions, ResourceLimits
        limits = ResourceLimits(max_package_bytes=536870912, max_entry_bytes=268435456, max_total_decompressed_bytes=1073741824, max_xml_bytes=33554432, max_json_bytes=67108864)
        options = ValidationOptions(epubcheck_jar=str(JAR), limits=limits)

    def run(fixture):
        fid = fixture['id']
        package = ROOT / fixture['package']
        assert hashlib.sha256(package.read_bytes()).hexdigest() == fixture['packageSha256']
        if args.side == 'a':
            completed = subprocess.run([str(ROOT / 'validator-a/target/release/spd-validator.exe'), 'validate', str(package), '--format', 'json', '--epubcheck', str(JAR)], capture_output=True, text=True, encoding='utf-8', errors='strict', timeout=200)
            report = json.loads(completed.stdout)
            normalized = {'fixture': fid, 'base': report['base'],
                          'normativeCapabilities': {c: report['capabilities'].get(c, 'UNKNOWN') for c in ['Accessible', 'Mapping']},
                          'experimentalCapabilities': {c: report['capabilities'].get(c, 'UNKNOWN') for c in ['Archive-Experimental', 'Fixed-Experimental']},
                          'violationRequirementIds': sorted({r['requirementId'] for r in report['findings'] if r['outcome'] == 'FAIL'}),
                          'notTestedRequirementIds': sorted(set(report['notTestedRequirements'])), 'operationalStatus': report['operationalStatus'],
                          'authoritativeClaimsStatus': report['authoritativeClaimsStatus'], 'experimentalReporting': report['experimentalReporting']}
            external = report['externalTools'][0]
        else:
            actual = validate(package, options)
            normalized = actual.normalized(fid)
            report = actual.detailed()
            external = report['metadata'].get('epubcheck', {})
        differences = {key: {'expected': oracle[fid][key], 'actual': normalized[key]} for key in FIELDS if oracle[fid][key] != normalized[key]}
        return {'normalized': normalized, 'external': external, 'report': report, 'oracleDifferences': differences}

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for fixture, value in zip(manifest['fixtures'], pool.map(run, manifest['fixtures'])):
            results.append(value)
            print(args.side.upper(), fixture['id'], 'OK' if not value['oracleDifferences'] else json.dumps(value['oracleDifferences']), flush=True)
    payload = {'validator': args.side.upper(), 'version': '0.1.0-draft.2' if args.side == 'a' else '0.1.1', 'contractVersion': '0.1.1', 'fixtureCount': len(results),
               'results': [r['normalized'] for r in results], 'externalEvaluations': [{'fixture': r['normalized']['fixture'], **r['external']} for r in results],
               'oracleDifferences': {r['normalized']['fixture']: r['oracleDifferences'] for r in results if r['oracleDifferences']}}
    source_after = provenance(args.side)
    payload['environment'] = {'startedAt': started, 'completedAt': datetime.now(timezone.utc).isoformat(),
        'sourceAndInputSha256': source_before, 'sourceStableDuringRun': source_before == source_after,
        'fixturePackageSha256': {f['id']: f['packageSha256'] for f in manifest['fixtures']},
        'unicodeVersion': '17.0.0' if args.side == 'a' else '15.1.0',
        'pythonVersion': sys.version, 'externalToolVersion': '5.3.0', 'externalScope': 'every corpus fixture; native failures do not suppress external evaluation',
        'externalAttributionVersion': '0.1.1', 'workers': args.workers,
        'validationOptions': {'maxPackageBytes': 536870912, 'maxEntryBytes': 268435456, 'maxTotalDecompressedBytes': 1073741824, 'maxXmlBytes': 33554432, 'maxJsonBytes': 67108864, 'maxCompressionRatio': 1000, 'epubcheckTimeoutSeconds': 120}}
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    detail_path.write_text(json.dumps([r['report'] for r in results], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert source_before == source_after, 'Source/input changed during evaluation; evidence is not freeze eligible'
    print('SUMMARY', args.side.upper(), len(results), 'fixtures;', len(payload['oracleDifferences']), 'oracle disagreements', flush=True)
    return bool(payload['oracleDifferences'])


if __name__ == '__main__': sys.exit(main())
