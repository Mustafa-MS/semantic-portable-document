"""Read-only audits independent of either validator's conformance implementation."""
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import jsonschema
import rfc8785
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'


def sha(data): return hashlib.sha256(data).hexdigest()
def tagged(data): return 'sha256:' + sha(data)
def read(name): return json.loads((ROOT / name).read_text(encoding='utf-8'))


def main():
    baseline = read('validator-convergence/baseline.json')
    protected = {name: digest for name, digest in baseline['files'].items() if name.startswith(('spec/', 'schemas/', 'validator-differential/', 'validator-a/reports/', 'validator-b/reports/')) or name == 'validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md'}
    for name, digest in protected.items():
        assert sha((ROOT / name).read_bytes()) == digest, name
    with zipfile.ZipFile(OUT / 'historical-inputs.zip') as archive:
        for name, digest in baseline['files'].items():
            assert sha(archive.read(name)) == digest, 'archive: ' + name
        old_multi = archive.read('tests/valid/multi-spine/document.epub')
    manifest = read('tests/corpus-manifest.json')
    expected_schema = read('validation/conformance-result-0.1.1.schema.json')
    assert len(manifest['fixtures']) == manifest['fixtureCount'] == 70
    assert len({f['id'] for f in manifest['fixtures']}) == 70
    unchanged_packages = 0
    for fixture in manifest['fixtures']:
        for key, digest in [('package', 'packageSha256'), ('expectedResult', 'expectedResultSha256')]:
            assert sha((ROOT / fixture[key]).read_bytes()) == fixture[digest], fixture['id']
        jsonschema.Draft202012Validator(expected_schema).validate(read(fixture['expectedResult']))
        old = baseline['files'].get(fixture['package'])
        if old == fixture['packageSha256']: unchanged_packages += 1
        elif old is not None: assert fixture['id'] == 'valid/multi-spine'
    assert unchanged_packages == 68
    assert (ROOT / 'tests/invalid/cross-spine-duplicate-node-id/document.epub').read_bytes() == old_multi
    multi = ROOT / 'tests/valid/multi-spine/document.epub'
    with zipfile.ZipFile(multi) as package:
        inventory = json.loads(package.read('META-INF/spd/inventory.json'))
        document = json.loads(package.read('META-INF/spd/document-state.json'))
        state = json.loads(package.read('META-INF/spd/state.json'))
        bindings = []
        for entry in inventory['resources']:
            data = package.read(entry['path'])
            assert len(data) == entry['byteLength'], entry['path']
            assert tagged(data) == entry['sha256'], entry['path']
            bindings.append({'path': entry['path'], 'byteLength': len(data), 'sha256': entry['sha256']})
        for key, effects in [('semanticStateDigest', {'semantic'}), ('renditionInputDigest', {'semantic', 'rendering'})]:
            rows = sorted((r for r in inventory['resources'] if effects.intersection(r['affects'])), key=lambda r: r['path'].encode('utf-8'))
            data = b''.join((r['path'] + '\0' + str(r['byteLength']) + '\0' + r['sha256'] + '\n').encode('utf-8') for r in rows)
            assert document[key] == state[key] == tagged(data), key
        assert state['inventory']['sha256'] == tagged(package.read('META-INF/spd/inventory.json'))
        assert state['descriptorDigest'] == tagged(rfc8785.dumps({k: v for k, v in state.items() if k != 'descriptorDigest'}))
        ids = []
        for name in ['EPUB/chapter1.xhtml', 'EPUB/chapter2.xhtml']:
            tree = etree.fromstring(package.read(name), etree.XMLParser(resolve_entities=False, no_network=True))
            local = tree.xpath('//@id')
            assert len(set(local)) == len(local)
            ids.extend(local)
        assert len(set(ids)) == len(ids)
    with zipfile.ZipFile(io.BytesIO(old_multi)) as package:
        chapter_ids = [etree.fromstring(package.read(name)).xpath('//@id') for name in ['EPUB/chapter1.xhtml', 'EPUB/chapter2.xhtml']]
        assert all(len(x) == len(set(x)) for x in chapter_ids)
        assert set(chapter_ids[0]) & set(chapter_ids[1]) == {'n_article01'}
    sys.path.insert(0, str(ROOT / 'validator-b'))
    from spd_validator_b.coverage import build_coverage
    b_coverage = build_coverage(ROOT / 'spec/requirements.yaml')
    a_coverage = read('validator-a/requirements-coverage.json')
    assert len(a_coverage) == b_coverage['summary']['represented'] == 113
    assert b_coverage['summary']['automatedImplemented'] == 74
    # Run the installed wheel from a directory where repository policy lookup cannot succeed.
    smoke = "import sys,json; sys.path.insert(0,sys.argv[1]); import spd_validator_b; from spd_validator_b.policy import policy,external_ids; assert 'installed-b' in spd_validator_b.__file__; assert policy()['version']=='0.1.1'; assert external_ids('ERROR(OPF-060): Duplicate entry in the ZIP file')==['SPD-BASE-002']; print(json.dumps({'version':spd_validator_b.__version__,'path':spd_validator_b.__file__,'bundledPolicy':True}))"
    completed = subprocess.run([sys.executable, '-c', smoke, str(OUT / 'installed-b')], cwd=OUT, capture_output=True, text=True, timeout=30)
    assert completed.returncode == 0, completed.stderr
    result = {'status': 'PASS', 'protectedFilesVerified': len(protected), 'archivedFilesVerified': len(baseline['files']),
        'fixturePackageDigestsVerified': 70, 'expectedResultDigestsAndSchemasVerified': 70, 'unchangedHistoricalPackages': unchanged_packages,
        'newNegativeEqualsHistoricalMultiSpine': True, 'multiSpineBindings': bindings,
        'multiSpineState': state, 'multiSpineDocument': document, 'positiveRevisionUnique': True,
        'negativeLocallyUniqueButRevisionDuplicate': 'n_article01', 'oldMultiSpineSha256': sha(old_multi), 'newMultiSpineSha256': sha(multi.read_bytes()),
        'requirements': {'A': {'represented': len(a_coverage), 'automatedImplemented': 74, 'verification': 'cargo test all_requirements_have_coverage_registration'}, 'B': b_coverage['summary']},
        'installedWheelSmoke': json.loads(completed.stdout), 'protectedFileSha256': protected}
    (OUT / 'integrity-checks.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS: historical evidence, all 70 package/expected hashes and schemas, multi-spine bindings, coverage, installed wheel policy')


if __name__ == '__main__': main()
