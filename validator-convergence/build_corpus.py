"""Corpus 0.1.1 oracle authored from reviewed predicates, never validator outputs."""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
import rfc8785

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'
REVIEWED = {
    'bad-resource-hash': ['SPD-RES-004', 'SPD-INT-003', 'SPD-INT-004', 'SPD-INT-005'],
    'descriptor-discovery-conflict': ['SPD-DISC-002'],
    'descriptor-discovery-missing': ['SPD-DISC-001'],
    'duplicate-normalized-path': ['SPD-BASE-002', 'SPD-RES-002'],
    'event-handler': ['SPD-SEC-001', 'SPD-ID-006'],
    'mapping-invalid-geometry': ['SPD-MAP-011', 'SPD-MAP-012'],
    'mapping-with-stale-fixed': ['SPD-STATE-007'],
    'mutation-asset': ['SPD-INT-003', 'SPD-RES-004', 'SPD-STATE-003'],
    'mutation-css': ['SPD-INT-003', 'SPD-RES-004'],
    'mutation-fixed': ['SPD-INT-003', 'SPD-RES-004', 'SPD-STATE-005', 'SPD-STATE-006', 'SPD-STATE-007'],
    'mutation-mapping': ['SPD-INT-003', 'SPD-RES-004', 'SPD-STATE-002'],
    'mutation-semantic': ['SPD-INT-003', 'SPD-RES-004', 'SPD-STATE-003'],
    'path-traversal': ['SPD-BASE-002', 'SPD-RES-002'],
    'sealed-after-annotation-modification': ['SPD-ANN-004', 'SPD-INT-003', 'SPD-RES-004'],
    'sealed-after-semantic-modification': ['SPD-STATE-003', 'SPD-INT-003', 'SPD-RES-004'],
    'stale-fixed-rendition': ['SPD-STATE-007'],
    'unlisted-non-normative-resource': ['SPD-RES-003', 'SPD-RES-006'],
    'unlisted-normative-resource': ['SPD-RES-003', 'SPD-RES-006'],
}


def sha(data): return hashlib.sha256(data).hexdigest()
def tagged(data): return 'sha256:' + sha(data)
def encoded(obj): return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def repair_multi(source):
    import io
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        resources = {n: z.read(n) for n in z.namelist()}
    name = 'EPUB/chapter2.xhtml'
    assert resources[name].count(b'id="n_article01"') == 1
    resources[name] = resources[name].replace(b'id="n_article01"', b'id="n_article02"')
    ip, dp, sp = ['META-INF/spd/' + n for n in ['inventory.json', 'document-state.json', 'state.json']]
    inv, doc, state = [json.loads(resources[n]) for n in [ip, dp, sp]]
    for record in inv['resources']:
        if record['path'] == name:
            record.update(byteLength=len(resources[name]), sha256=tagged(resources[name]))
    for field, effects in [('semanticStateDigest', {'semantic'}), ('renditionInputDigest', {'semantic', 'rendering'})]:
        entries = sorted((r for r in inv['resources'] if effects.intersection(r['affects'])), key=lambda r: r['path'].encode())
        value = tagged(b''.join((r['path'] + '\0' + str(r['byteLength']) + '\0' + r['sha256'] + '\n').encode() for r in entries))
        doc[field] = state[field] = value
    resources[dp] = encoded(doc)
    for record in inv['resources']:
        if record['path'] == dp:
            record.update(byteLength=len(resources[dp]), sha256=tagged(resources[dp]))
    resources[ip] = encoded(inv)
    state['inventory']['sha256'] = tagged(resources[ip])
    projection = {k: v for k, v in state.items() if k != 'descriptorDigest'}
    state['descriptorDigest'] = tagged(rfc8785.dumps(projection))
    resources[sp] = encoded(state)
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        for name, data in resources.items():
            info = zipfile.ZipInfo(name, (2026, 9, 3, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if name == 'mimetype' else zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return out.getvalue()


def main():
    policy = json.loads((ROOT / 'validation/REQUIREMENT_ATTRIBUTION_0.1.1.json').read_text())
    with zipfile.ZipFile(OUT / 'historical-inputs.zip') as history:
        manifest = json.loads(history.read('tests/corpus-manifest.json'))
        old_multi = history.read('tests/valid/multi-spine/document.epub')
        repaired = repair_multi(old_multi)
        (ROOT / 'tests/valid/multi-spine/document.epub').write_bytes(repaired)
        negative = ROOT / 'tests/invalid/cross-spine-duplicate-node-id'
        negative.mkdir(exist_ok=True)
        (negative / 'document.epub').write_bytes(old_multi)
        fixture = copy.deepcopy(next(x for x in manifest['fixtures'] if x['id'] == 'valid/multi-spine'))
        fixture.update(id='invalid/cross-spine-duplicate-node-id', name=negative.name, category='invalid',
                       package='tests/invalid/cross-spine-duplicate-node-id/document.epub', expectedResult='tests/invalid/cross-spine-duplicate-node-id/expected.json',
                       primaryRequirements=['SPD-ID-006'], notes=['Each XHTML has locally unique IDs; n_article01 repeats across the authoritative revision.'])
        manifest['fixtures'].append(fixture)
        expected_rows = []
        changes = []
        for fixture in manifest['fixtures']:
            fid = fixture['id']
            if fid == 'invalid/cross-spine-duplicate-node-id':
                expected = json.loads(history.read('tests/valid/multi-spine/expected.json'))
                expected.update(fixture=fid, base='FAIL', violations=[{'requirement': 'SPD-ID-006'}])
                old_ids = []
            else:
                expected = json.loads(history.read(fixture['expectedResult']))
                old_ids = [v['requirement'] for v in expected['violations']]
            name = fid.split('/')[1]
            if name in REVIEWED:
                expected['violations'] = [{'requirement': r} for r in sorted(REVIEWED[name])]
            expected['notTestedRequirementIds'] = ['SPD-ID-013']
            expected['operationalStatus'] = 'COMPLETE'
            expected['authoritativeClaimsStatus'] = 'KNOWN'
            with zipfile.ZipFile(ROOT / fixture['package']) as z:
                doc = json.loads(z.read('META-INF/spd/document-state.json'))
                state = json.loads(z.read('META-INF/spd/state.json'))
                claims = {c['id'] for c in doc['capabilities']}
                present = state['fixedRendition'].get('path') in z.namelist()
            for cap in ['Fixed-Experimental', 'Archive-Experimental']:
                expected['capabilities'][cap] = 'PRESENT_EXPERIMENTAL' if cap in claims else 'NOT_CLAIMED'
            expected['experimentalReporting'] = {'physicalFixedRenditionPresent': present, 'fixedExperimentalCapabilityDeclared': 'Fixed-Experimental' in claims,
                                               'fixedExperimentalEvaluationStatus': 'NOT_TESTED' if 'Fixed-Experimental' in claims else 'NOT_CLAIMED'}
            if 'Accessible' in claims:
                expected['notTestedRequirementIds'] += ['SPD-ACC-001', 'SPD-ACC-004']
            if name == 'invalid-xhtml': expected['notTestedRequirementIds'].append('SPD-ID-006')
            if name in {'descriptor-discovery-missing', 'descriptor-discovery-conflict'}:
                groups = ['document', 'state'] + (['inventory'] if name.endswith('missing') else [])
                expected['notTestedRequirementIds'] += [r for g in groups for r in policy['blocked'][g]]
                expected['authoritativeClaimsStatus'] = 'UNKNOWN'
                expected['capabilities'] = {cap: 'UNKNOWN' for cap in expected['capabilities']}
                expected['experimentalReporting'] = {'physicalFixedRenditionPresent': None, 'fixedExperimentalCapabilityDeclared': None, 'fixedExperimentalEvaluationStatus': 'UNKNOWN'}
            expected['notTestedRequirementIds'] = sorted(set(expected['notTestedRequirementIds']))
            expected['corpusVersion'] = '0.1.1'
            (ROOT / fixture['expectedResult']).write_bytes(encoded(expected))
            ids = sorted({v['requirement'] for v in expected['violations']})
            fixture['packageSha256'] = sha((ROOT / fixture['package']).read_bytes())
            fixture['expectedResultSha256'] = sha((ROOT / fixture['expectedResult']).read_bytes())
            expected_rows.append({'fixture': fid, 'base': expected['base'],
                                  'normativeCapabilities': {c: expected['capabilities'][c] for c in ['Accessible', 'Mapping']},
                                  'experimentalCapabilities': {c: expected['capabilities'][c] for c in ['Archive-Experimental', 'Fixed-Experimental']},
                                  'violationRequirementIds': ids, 'notTestedRequirementIds': expected['notTestedRequirementIds'],
                                  'operationalStatus': 'COMPLETE', 'authoritativeClaimsStatus': expected['authoritativeClaimsStatus'],
                                  'experimentalReporting': expected['experimentalReporting']})
            changes.append({'fixture': fid, 'oldIds': sorted(old_ids), 'reviewedIds': ids, 'reason': 'Reviewed Stage 2 predicates plus Contract 0.1.1; validator outputs not read.'})
        manifest.update(corpusVersion='0.1.1', fixtureCount=len(manifest['fixtures']))
        manifest['fixtures'].sort(key=lambda x: x['id'])
        manifest['counts'] = {c: sum(x['category'] == c for x in manifest['fixtures']) for c in ['valid', 'invalid', 'edge']}
        (ROOT / 'tests/corpus-manifest.json').write_bytes(encoded(manifest))
        (OUT / 'reviewed-oracle-0.1.1.json').write_bytes(encoded({'corpusVersion': '0.1.1', 'contractVersion': '0.1.1', 'fixtureCount': len(expected_rows), 'results': sorted(expected_rows, key=lambda x: x['fixture'])}))
        (OUT / 'oracle-review-decisions.json').write_bytes(encoded(changes))
        print('Built independent reviewed oracle:', manifest['fixtureCount'], manifest['counts'])


if __name__ == '__main__': main()
