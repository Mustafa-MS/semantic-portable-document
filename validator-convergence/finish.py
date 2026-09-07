"""Gate the immutable convergence freezes and render evidence-backed reports."""
import difflib
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-convergence'
FIELDS = ['base', 'normativeCapabilities', 'violationRequirementIds', 'notTestedRequirementIds', 'operationalStatus', 'authoritativeClaimsStatus']
EXPERIMENTAL = ['experimentalCapabilities', 'experimentalReporting']
DECISION = 'READY FOR FORMAT 0.1 RELEASE CANDIDATE PREPARATION'


def read(name): return json.loads((OUT / name).read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, value): (OUT / name).write_text(value.rstrip() + '\n', encoding='utf-8')
def write_json(name, value): write(name, json.dumps(value, ensure_ascii=False, indent=2))
def ids(values): return ', '.join(values) or '—'
def table(headers, rows):
    def clean(x): return str(x).replace('|', '\\|').replace('\n', ' ')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] + ['| ' + ' | '.join(map(clean, row)) + ' |' for row in rows])


def main():
    a, b = read('final-0.1.1-a.json'), read('final-0.1.1-b.json')
    oracle = read('reviewed-oracle-0.1.1.json')
    integrity = read('integrity-checks.json')
    checks = read('checks.json')
    baseline = read('baseline.json')
    manifest = json.loads((ROOT / 'tests/corpus-manifest.json').read_text(encoding='utf-8'))
    policy = json.loads((ROOT / 'validation/REQUIREMENT_ATTRIBUTION_0.1.1.json').read_text(encoding='utf-8'))
    old = json.loads((ROOT / 'validator-differential/raw-diff.json').read_text(encoding='utf-8'))
    old_rows = {r['fixture']: r for r in old['fixtures']}
    indexes = [{r['fixture']: r for r in payload['results']} for payload in [a, b, oracle]]
    assert all(set(index) == {f['id'] for f in manifest['fixtures']} for index in indexes)
    assert a['fixtureCount'] == b['fixtureCount'] == oracle['fixtureCount'] == manifest['fixtureCount'] == 70
    assert not a['oracleDifferences'] and not b['oracleDifferences']
    assert all(c['exitCode'] == 0 for c in checks) and len(checks) == 8
    assert integrity['status'] == 'PASS'
    assert not (OUT / 'NEW_SPEC_BLOCKERS.md').exists(), 'Review new normative blockers before releasing'
    for payload in [a, b]:
        assert payload['environment']['sourceStableDuringRun']
        for name, digest in payload['environment']['sourceAndInputSha256'].items():
            assert sha(ROOT / name) == digest, 'post-run change: ' + name
    detailed_a = read('final-0.1.1-detailed-a.json')
    detailed_b = read('final-0.1.1-detailed-b.json')
    assert all('17.0.0' in r['reproducibility']['unicodeVersion'] for r in detailed_a)
    assert all(r['metadata']['unicodeData'] == '15.1.0' for r in detailed_b)
    for name, digest in integrity['protectedFileSha256'].items():
        assert sha(ROOT / name) == digest, 'historical change: ' + name
    for name, digest in baseline['pins'].items(): assert sha(ROOT / name) == digest
    assert '57 passed' in (OUT / 'b-tests.log').read_text(encoding='utf-8')
    assert 'Ran 21 tests' in (OUT / 'repository-tests.log').read_text(encoding='utf-8')
    a_test_counts = list(map(int, re.findall(r'test result: ok\. (\d+) passed', (OUT / 'a-tests.log').read_text(encoding='utf-8'))))
    assert sum(a_test_counts) == 17
    ext_indexes = [{r['fixture']: r for r in payload['externalEvaluations']} for payload in [a, b]]
    compared = []
    for fixture in manifest['fixtures']:
        fid = fixture['id']
        rows = [index[fid] for index in indexes]
        equal = {field: rows[0][field] == rows[1][field] == rows[2][field] for field in FIELDS}
        experimental_equal = all(rows[0][key] == rows[1][key] == rows[2][key] for key in EXPERIMENTAL)
        assert all(equal.values()), (fid, equal)
        assert experimental_equal, ('experimental', fid)
        assert 'SPD-STATE-001' not in rows[0]['violationRequirementIds']
        external = [index[fid] for index in ext_indexes]
        for record in external:
            assert record['executed'] and record['skipReason'] is None, fid
            assert record['version'] == '5.3.0' and record['attributionVersion'] == '0.1.1'
            assert record['fixtureSha256'] == fixture['packageSha256']
            assert isinstance(record['exitCode'], int) and record['exitCode'] in [0, 1]
        assert external[0]['exitCode'] == external[1]['exitCode'], fid
        assert external[0]['diagnosticCodes'] == external[1]['diagnosticCodes'], fid
        assert external[0]['normalizedSpdAttributionIds'] == external[1]['normalizedSpdAttributionIds'], fid
        compared.append({'fixture': fid, 'packageSha256': fixture['packageSha256'], 'A': rows[0], 'B': rows[1], 'expected': rows[2],
            'threeWayEqualFields': equal, 'completeNormativeAgreement': all(equal.values()), 'experimentalAgreement': experimental_equal,
            'externalAgreement': True, 'stage2CompleteAgreement': old_rows.get(fid, {}).get('completeSurfaceAgreement')})
    target = indexes[0]
    assert target['valid/multi-spine']['base'] == 'PASS' and not target['valid/multi-spine']['violationRequirementIds']
    assert target['invalid/cross-spine-duplicate-node-id']['base'] == 'FAIL'
    assert target['invalid/cross-spine-duplicate-node-id']['violationRequirementIds'] == ['SPD-ID-006']
    assert all(index['valid/multi-spine']['exitCode'] == index['invalid/cross-spine-duplicate-node-id']['exitCode'] == 0 for index in ext_indexes)
    for fid in ['invalid/stale-fixed-rendition', 'invalid/mapping-with-stale-fixed']:
        assert target[fid]['violationRequirementIds'] == ['SPD-STATE-007']
    for fid in ['invalid/descriptor-discovery-missing', 'invalid/descriptor-discovery-conflict']:
        assert target[fid]['authoritativeClaimsStatus'] == 'UNKNOWN'
        assert set(target[fid]['normativeCapabilities'].values()) == {'UNKNOWN'}
    assert 'SPD-STATE-002' not in target['invalid/bad-resource-hash']['violationRequirementIds']
    for name in ['mutation-css', 'mutation-fixed', 'mutation-mapping', 'sealed-after-annotation-modification']:
        assert 'SPD-STATE-003' not in target['invalid/' + name]['violationRequirementIds']
    settled_ids = {rid for row in old['fixtures'] if not row['completeSurfaceAgreement'] for side in ['A', 'B'] for rid in row[side]['violationRequirementIds']}
    assert settled_ids <= {r['requirementId'] for r in policy['rules']}
    # Everything above is a gate. No frozen output is written until it passes.
    freeze_dir = OUT / 'freezes'
    freeze_dir.mkdir(exist_ok=True)
    frozen = {}
    for side, payload in [('a', a), ('b', b)]:
        name = f'validator-{side}-{payload["version"]}-corpus-0.1.1.json'
        path = freeze_dir / name
        if '--verify-existing' in sys.argv:
            assert json.loads(path.read_text(encoding='utf-8')) == payload, 'Existing freeze differs; never overwrite it'
        else:
            with path.open('x', encoding='utf-8') as stream:
                json.dump(payload, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
        frozen[side.upper()] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}
    metrics = {'fixtureCount': 70, 'fixtureIdentityAgreement': 70,
        **{field + 'Agreement': sum(r['threeWayEqualFields'][field] for r in compared) for field in FIELDS},
        'completeNormativeAgreement': 70, 'A_expected': 70, 'B_expected': 70, 'A_B': 70,
        'experimentalAgreement': 70, 'externalEvaluationAgreement': 70, 'externalExecutionsA': 70, 'externalExecutionsB': 70,
        'openNormativeBlockers': 0}
    write_json('differential-results.json', {'contractVersion': '0.1.1', 'corpusVersion': '0.1.1', 'metrics': metrics, 'stage2Metrics': old['metrics'], 'freezes': frozen, 'fixtures': compared})
    # Runtime evidence is supplemental; the input/source hashes are captured inside each freeze.
    commands = {}
    for label, command in [('java', ['java', '-version']), ('rust', ['rustc', '--version']), ('cargo', ['cargo', '--version'])]:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        commands[label] = (result.stdout + result.stderr).strip()
    write_json('environment.json', {'recordedAt': datetime.now(timezone.utc).isoformat(), 'python': sys.version, 'runtimes': commands,
        'pythonPackages': {name: importlib.metadata.version(name) for name in ['lxml', 'jsonschema', 'tinycss2', 'rfc8785', 'PyYAML', 'pytest', 'hypothesis', 'ruff', 'hatchling', 'build']},
        'A': a['environment'], 'B': b['environment'],
        'additionalValidationOptions': {'commonMaxEntries': 10000, 'epubcheckVersionProbeTimeoutSeconds': 20, 'A': {'maxMappingRecords': 1000000, 'toolOutputCaptureBytesPerStream': 1048576, 'mode': 'CLI validate --format json --epubcheck official JAR; remaining options defaults'}, 'B': {'maxJsonDepth': 128, 'lineageEvidence': False, 'requireEpubcheckVersion': '5.3.0', 'mode': 'Python validate API; explicit aligned ResourceLimits and official JAR'}},
        'knownDifferences': ['A Unicode 17.0.0; B Unicode 15.1.0. Different languages, parsers, dependency graphs and internal schema-bundle digest conventions.', 'A mapping-record ceiling 1000000; B JSON depth ceiling 128. Common package/XML/JSON size and ratio limits aligned; no corpus fixture reaches either implementation-specific ceiling.'],
        'bitIdenticalEnvironments': False})
    changes = source_changes(baseline)
    write_json('source-changes.json', changes)
    render_contract(policy)
    render_corpus(integrity, manifest, old_rows)
    render_sources(changes)
    render_external(a, b, ext_indexes, manifest, frozen)
    render_matrix(compared)
    render_gate(metrics, integrity, checks, frozen)
    write_json('release-evidence-sha256.json', {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(OUT.glob('*')) if p.is_file() and p.suffix in ['.md', '.json', '.py', '.log', '.xml', '.zip'] and p.name != 'release-evidence-sha256.json'} | {r['path']: r['sha256'] for r in frozen.values()} | {p.relative_to(ROOT).as_posix(): sha(p) for p in (OUT / 'dist').glob('*.whl')})
    print(json.dumps(metrics, indent=2))
    print(DECISION)


def source_changes(baseline):
    candidates = set()
    for directory in ['validator-a/src', 'validator-a/tests', 'validator-b/spd_validator_b', 'validator-b/tests']:
        candidates.update(p for p in (ROOT / directory).rglob('*') if p.is_file() and p.suffix in ['.rs', '.py'])
    for name in ['validator-a/Cargo.toml', 'validator-a/Cargo.lock', 'validator-a/README.md', 'validator-a/schemas/validator-report.schema.json', 'validator-b/pyproject.toml', 'validator-b/README.md', 'scripts/verify_conformance_model.ps1']:
        candidates.add(ROOT / name)
    result = []
    with zipfile.ZipFile(OUT / 'historical-inputs.zip') as archive:
        for path in sorted(candidates):
            name = path.relative_to(ROOT).as_posix()
            previous = baseline['files'].get(name)
            digest = sha(path)
            if previous == digest: continue
            old_text = archive.read(name).decode('utf-8').splitlines(True) if previous else []
            new_text = path.read_text(encoding='utf-8').splitlines(True)
            result.append({'path': name, 'oldSha256': previous, 'newSha256': digest, 'diff': ''.join(difflib.unified_diff(old_text, new_text, fromfile='historical/' + name, tofile=name))})
    return result


def render_contract(policy):
    original = ROOT / 'validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md'
    current = ROOT / 'validation/DIFFERENTIAL_VALIDATION_CONTRACT_0.1.1.md'
    diff = ''.join(difflib.unified_diff(original.read_text(encoding='utf-8').splitlines(True), current.read_text(encoding='utf-8').splitlines(True), fromfile=original.relative_to(ROOT).as_posix(), tofile=current.relative_to(ROOT).as_posix()))
    write('contract-changes.md', '# Contract changes\n\nNO FORMAT SEMANTICS CHANGED. Contract 0.1.1 is shared NON-NORMATIVE VALIDATION INFRASTRUCTURE, outside either validator. The original contract is unchanged. Both implementations consume the same versioned attribution JSON (Rust embeds it; Python loads it and packages it in the wheel).\n\n' + table(['Change category', 'Complete policy change'], [
        ['comparison precision', 'Fixture/package identity, explicit KNOWN/UNKNOWN claim authority, exact sorted unique sets, positive-evidence PASS, three-way oracle comparison, individual input/source hashes. Unicode differences are disclosed rather than falsely asserted identical.'],
        ['applicability', 'Lifecycle/capability guards; processor STATE-001 is outside document-only scope; NOT_APPLICABLE excluded from failed/NOT_TESTED sets. Current-revision Base scope excludes historical ID-013 and Accessible-only manual certification.'],
        ['dependency handling', 'Unavailable authority stays unknown; explicit blocking groups; retain independent OPF facts; false conjunct establishes FAIL; FAIL takes precedence over blocked NOT_TESTED for the same ID; declared projections are distinct from live integrity.'],
        ['external scope', 'All 70 safely eligible packages, including native failures; version, digest, execution/skip reason and complete diagnostics retained. Tool failure is operational, not document failure.'],
        ['attribution', 'Every independently disproved applicable predicate; RES-003/006 and MAP-011/012 overlaps; actual state/effects predicates; code-plus-message guarded external mapping, no blanket BASE-002 or normalization filtering.'],
        ['experimental reporting', 'Presence, explicit declaration and evaluation are distinct; UNKNOWN/null allowed; normative comparison excludes these fields and measures them separately.']]) + '\n\nThe section-by-section text below is the exact original-to-new difference; all new clauses fall into the six categories above.\n\n```diff\n' + diff + '```')
    rows = [[r['requirementId'], r['applicability'], ids(r['prerequisites']), r['predicate'], r['overlapBehavior']] for r in policy['rules']]
    external = [[r['code'], r['category'], r['pattern'], ids(r['ids'])] for r in policy['externalDiagnostics']]
    write('attribution-table.md', '# Shared attribution table 0.1.1\n\nNON-NORMATIVE VALIDATION INFRASTRUCTURE. The machine-readable source is `validation/REQUIREMENT_ATTRIBUTION_0.1.1.json`; both validators consume it. All IDs occurring in the 25 Stage 2 disagreements are covered.\n\n## Native predicate evidence\n\nRequired evidence is the registry-linked predicate plus the prerequisite objects below; the JSON retains explicit `requiredEvidence`, `prerequisites`, `predicate`, `applicability`, `overlapBehavior` and `externalToolAttribution` fields for each row. A counterexample must be independently evidenced, not inferred from another finding.\n\n' + table(['ID', 'Applicability', 'Prerequisites', 'Predicate / required evidence', 'Overlap'], rows) + '\n\nResource integrity uses readable exact bytes and inventory hash/length; declared projections use supplied inventory fields. STATE-003 additionally requires SEALED lifecycle and semantic-affecting resource evidence. MAP geometry needs a readable page/quad; fixed currentness needs its digest and current input bindings. Discovery blockers prevent authoritative claims comparisons but do not erase OCF/OPF facts. STATE-001 requires processor observations absent here.\n\n## External diagnostics\n\nOnly ERROR/FATAL diagnostics with both matching code and message guard can add these IDs. Unmatched diagnostics remain raw evidence.\n\n' + table(['Code', 'Predicate category', 'Message guard', 'SPD IDs'], external))


def render_corpus(integrity, manifest, old_rows):
    decisions = read('oracle-review-decisions.json')
    rows = [[r['fixture'], ids(r['oldIds']), ids(r['reviewedIds'])] for r in decisions if r['oldIds'] != r['reviewedIds']]
    state = integrity['multiSpineState']
    bindings = table(['Resource', 'Verified byteLength', 'Verified SHA-256'], [[r['path'], r['byteLength'], r['sha256']] for r in integrity['multiSpineBindings']])
    write('corpus-changes.md', f'''# Corpus 0.1.1 changes

{manifest['fixtureCount']} fixtures: 18 valid, 39 invalid, 13 edge. Exactly one historical package changed; 68 are byte-identical. One negative was added. All 70 expectations have versioned reporting fields and fresh hashes, validated by the versioned infrastructure report schema; canonical Format schemas were not edited.

## Multi-spine repair and negative regression

The old positive repeated `n_article01` in chapter1.xhtml and chapter2.xhtml (line 4 each). The repaired positive retains `n_article01` in chapter 1 and uses `n_article02` in chapter 2. All addressable IDs are revision-wide unique. Both validators independently return Base PASS with no failures.

Old package SHA-256: `{integrity['oldMultiSpineSha256']}`.

New package SHA-256: `{integrity['newMultiSpineSha256']}`.

The new `invalid/cross-spine-duplicate-node-id` is the exact old multi-spine package, preserving valid inventory and state bindings while isolating the duplicate. IDs are locally unique within each XHTML but `n_article01` repeats across the revision. Both return Base FAIL with exactly SPD-ID-006. EPUBCheck exits 0 for both packages: it does not treat cross-resource XML IDs as an EPUB error.

The chapter 2 resource hash/length, document projections, document resource binding, exact inventory binding and lifecycle descriptor JCS digest were recomputed and independently audited:

{bindings}

semanticStateDigest: `{state['semanticStateDigest']}`.

renditionInputDigest: `{state['renditionInputDigest']}`.

Exact inventory SHA-256: `{state['inventory']['sha256']}`.

descriptorDigest: `{state['descriptorDigest']}`.

Lifecycle is EDITABLE and fixed rendition is absent; there is no seal/fixed/mapping binding to regenerate. Existing document/revision identity is retained for this synthetic fixture repair.

## Oracle attribution changes

`invalid/stale-fixed-rendition` now expects SPD-STATE-007 instead of SPD-STATE-001. Mapping depends on current fixed output; the fixture supplies no processor-behavior evidence. Its package bytes and FAIL verdict did not change.

The oracle is authored by `build_corpus.py` from preserved expected files, actual descriptor bytes, the shared contract, and the explicit reviewed predicate table. It never reads either validator's outputs. `oracle-review-decisions.json` lists all 70 old/new failed-ID sets, including unchanged rows. These are every failed-ID expectation change:

{table(['Fixture', 'Historical expected IDs', 'Reviewed expected IDs'], rows)}

All expectations add corpusVersion, operational status, authority status and NOT_TESTED sets. All retain ID-013 NOT_TESTED for absent lineage evidence; Accessible adds ACC-001/004. Invalid XHTML blocks ID-006; missing/conflicting authority uses the contract's explicit blocked groups and UNKNOWN capabilities, not empty claims. Experimental expectations are derived from actual explicit declarations, separate from physical presence; legacy scenario metadata is not claim authority. No normative requirement was reclassified.

Use this versioned builder and oracle for convergence. Historical corpus/freezer scripts remain historical artifacts and must not be used to overwrite the old freezes. The historical archive preserves all pre-repair expectations and package bytes.
''')


def render_sources(changes):
    a_rows = [
        ['Revision scope / event exemption', 'ID-006, SEC-001', 'Per-XHTML index and event-handler exemption', 'Revision-wide index; both occurrences retain resource/line/node evidence; security failure does not exempt identity', 'revision_scope_and_duplicate_evidence; security_is_not_an_identity_exemption'],
        ['Stale/current document predicates', 'STATE-005/006/007; not STATE-001', 'Stale Mapping attributed to processor behavior', 'Document-only currentness attribution and SEALED/Mapping guards', 'stale_rules_are_document_not_processor_rules'],
        ['Independent integrity/projections', 'RES-002/003/004/006, INT-003/004/005, STATE-002/003, ANN-004', 'Primary failures suppressed readable independent predicates; effects conflated', 'Safe inventory inspection continues; supplied projections and live bytes remain separate; lifecycle/effects guard state rules', 'lifecycle_and_effects_guard_state_predicates; all_reviewed_overlaps_remain_visible'],
        ['Geometry overlap', 'MAP-011/012', 'Specific geometry label suppressed second applicable predicate', 'Both independently false predicates retained', 'all_reviewed_overlaps_remain_visible'],
        ['Unknown authority and prerequisite model', 'DISC-001/002, CAP-002/003, ID-006 and shared blocked groups', 'Incomplete authority did not expose stable unknown/blocked surface', 'Conflicting candidates quarantined; safe OPF facts retained; UNKNOWN not empty; malformed semantic XML blocks identity', 'unknown_claims_are_not_empty_and_xml_prerequisites_are_explicit'],
        ['External attribution / report representation', 'Guarded BASE-002, SEM-002, ID-006, SEC-004/005/006', 'Broad aggregate external failure; historical freezer suppressed BASE-002 beside native IDs', 'Shared guarded policy; every fixture keeps full external evidence; new runner never filters IDs', '70 real EPUBCheck integrations; production_report_matches_implementation_schema; unavailable_epubcheck_is_incomplete_not_pass_or_document_failure'],
        ['Reproducibility and experimental reporting', 'Non-normative report metadata', 'Physical fixed presence implied claim; hardcoded Unicode 16 label', 'Explicit declaration/presence/evaluation separate; actual crate Unicode 17.0.0 recorded', '70 separate experimental comparisons; source-stability and runtime checks'],
        ['Security regression / versioned corpus', 'Existing package/parser limits and coverage', '69-fixture corpus; no cross-spine negative', '70 fixtures, preserved old golden checks, bounded 128-input fuzz smoke', 'bounded_fuzz_smoke; corpus_normalized_classification; all_requirements_have_coverage_registration'],
    ]
    b_rows = [
        ['Missing/conflicting discovery', 'DISC-001/002; CAP-003; ARCH-001', 'Unavailable fields coerced to empty and invented architecture/capability failures', 'Quarantine candidates; unknown claim authority; use only discovered facts, no filename authority fallback', 'test_unknown_descriptor_facts (2 cases)'],
        ['SEALED applicability', 'STATE-002; INT-003/004/005; RES-004', 'EDITABLE bad-resource-hash received SEALED-only ID', 'Explicit lifecycle guard; retain all four real integrity/projection failures', 'test_editable_bad_hash_and_projection_failures'],
        ['Semantic effects', 'STATE-003; RES-004; INT-003', 'Every SEALED byte mutation treated as semantic change', 'Semantic-specific rule requires semantic-affecting resource; rendering/fixed/mapping/annotation mutations retain general integrity IDs only where appropriate', 'test_nonsemantic_integrity_is_not_semantic_mutation (4 cases)'],
        ['Stale/current document predicates', 'STATE-005/006/007; not STATE-001', 'Document state used to assert processor mispresentation', 'No STATE-001 without processor evidence; document currentness uses actual predicates', 'test_no_document_only_processor_finding (3 cases)'],
        ['Prerequisite/roll-up model', 'Shared blocked IDs; ACC-001/004; ID-013', 'Unknowns/defaults and automatic PASS ledger; transient Accessible Base-scope regression during repair', 'Unknowns explicit, failed wins blocked; unevaluated ledger entries not falsely PASS; current Base scope excludes history and Accessible manual work', 'test_accessible_manual_work_does_not_block_current_base_scope; 70-fixture full oracle comparison'],
        ['External attribution / experimental report', 'Guarded BASE-002, SEM-002, ID-006, SEC-004/005/006; experimental metadata', 'Blanket external BASE-002; physical presence/claims conflated', 'Same policy consumed independently; preserve raw unmatched diagnostics; explicit experimental claims', 'test_shared_external_policy_no_blanket_mapping; 6 adapter tests; 70 real integrations'],
        ['Revision uniqueness / overlap retention', 'ID-006, SEC-001, RES-003/006, MAP-011/012', 'Correct independent B behavior needed retention while other repairs landed', 'No cross-port from A; regression asserts positive and negative plus all reviewed native ID sets', 'test_revision_wide_positive_and_negative; test_current_corpus_against_independent_native_oracle'],
    ]
    descriptions = {
        'validator-a/Cargo.toml': 'Version draft.2; no dependency replacement.', 'validator-a/Cargo.lock': 'Root package version refresh only.',
        'validator-a/src/lib.rs': 'Wire shared policy module and report actual Unicode data version.', 'validator-a/src/model.rs': 'Unknown authority, experimental fields and complete tool-evidence structure.',
        'validator-a/src/policy.rs': 'Native Rust consumer of shared blocked groups and guarded attribution data.', 'validator-a/src/validator.rs': 'All A predicate/roll-up/identity repairs in the rows above.',
        'validator-a/src/epubcheck.rs': 'Version check and full execution evidence; retain bounded capture/drain/timeout; shared attribution.',
        'validator-a/tests/corpus.rs': 'Current manifest count 70; preserve historical oracle count 69 and retained external records 31.',
        'validator-a/tests/convergence.rs': 'Seven targeted regressions including bounded 128-input fuzz smoke.',
        'validator-a/schemas/validator-report.schema.json': 'Implementation report schema accepts explicit authority/experimental data; canonical schemas untouched.',
        'validator-a/README.md': 'Version/shared contract and historical-freezer warning.',
        'validator-b/pyproject.toml': 'Version 0.1.1 and shared attribution bundled in wheel.', 'validator-b/README.md': 'New reporting contract/version and preserved blind artifacts.',
        'validator-b/spd_validator_b/__init__.py': 'Version 0.1.1.', 'validator-b/spd_validator_b/cli.py': 'Version label 0.1.1.',
        'validator-b/spd_validator_b/epub.py': 'Candidate provenance and quarantine, no fallback authority.', 'validator-b/spd_validator_b/epubcheck.py': 'Guarded shared attribution plus complete external record.',
        'validator-b/spd_validator_b/integrity.py': 'Available-evidence checks, SEALED/effects guards and corrected state attribution.',
        'validator-b/spd_validator_b/mapping.py': 'Claim/state evidence guards; correct stale STATE-007 and SEALED-only mapping STATE-002.',
        'validator-b/spd_validator_b/models.py': 'New normalized fields; FAIL wins NOT_TESTED for same ID.', 'validator-b/spd_validator_b/semantics.py': 'Unavailable authoritative XML blocks revision ID index.',
        'validator-b/spd_validator_b/validator.py': 'Unknown claims, blocked groups, experimental separation and scoped roll-up; explicit top-level containment lint justification.',
        'validator-b/spd_validator_b/policy.py': 'Native Python shared data consumer plus packaged fallback; not copied from A.',
        'validator-b/tests/test_convergence.py': 'Fourteen targeted cases covering reviewed predicates and independent native oracle.',
        'validator-b/tests/test_corpus_security.py': 'Manifest count 70; preserve malformed-package/security assertions.',
        'validator-b/tests/test_epubcheck_integration.py': 'Expected external XML attribution SEM-002 instead of blanket BASE-002.',
        'validator-b/spd_validator_b/annotations.py': 'Ruff mechanical import cleanup only; no behavior change.',
        'validator-b/spd_validator_b/coverage.py': 'Ruff mechanical import/type-annotation cleanup only; registration/classification unchanged.',
        'validator-b/spd_validator_b/package.py': 'Ruff mechanical import cleanup only; security behavior unchanged.',
        'validator-b/tests/test_algorithms.py': 'Ruff mechanical import cleanup only; test behavior unchanged.',
        'scripts/verify_conformance_model.ps1': 'Use versioned reporting schema/new negative, and verify exact workspace temporary paths before native recursive cleanup.',
    }
    for side, rows in [('a', a_rows), ('b', b_rows)]:
        selected = [r for r in changes if r['path'].startswith('validator-' + side + '/')]
        assert all(r['path'] in descriptions for r in selected)
        write(f'validator-{side}-changes.md', f'# Validator {side.upper()} convergence changes\n\nImplemented against the frozen Draft, registry, reviewed Stage 2 findings and Contract 0.1.1. No other validator implementation was translated or ported. Exact before/after hashes and full per-file diffs are in `source-changes.json`; the archive contains original bytes.\n\n' + table(['Stage 2 finding / repair', 'Requirement IDs', 'Old behavior', 'New behavior', 'Targeted regression'], rows) + '\n\n## Complete changed/new file inventory\n\n' + table(['File', 'Reason / behavior', 'Verification'], [[r['path'], descriptions[r['path']], 'Targeted tests above; full suite and 70-fixture three-way comparison'] for r in selected]) + '\n\nNo unrelated functional refactor was included. B lint cleanup is mechanical and was necessary for the configured strict checks. The new runner retains raw native/external evidence without deleting IDs. Repository reporting schema selection and safe temporary-directory cleanup are documented in `source-changes.json`.\n')


def render_external(a, b, indexes, manifest, frozen):
    rows = []
    for fixture in manifest['fixtures']:
        fid = fixture['id']
        record = indexes[0][fid]
        rows.append([fid, record['exitCode'], record['exitCode'], ids(record['diagnosticCodes']), ids(record['normalizedSpdAttributionIds'])])
    write('external-evaluation.md', '# Controlled external evaluation\n\nBoth validators invoked official EPUBCheck 5.3.0 for all 70 fixtures, including native failures: 140 completed evaluations, zero skips and zero operational failures. Every record has fixture SHA-256, version, executed flag, skip reason, exit code, diagnostic codes, attributed SPD IDs and raw stdout/stderr. Exit, codes and attribution agree for all 70. Raw line endings/messages are not normative equality fields.\n\nThe exact per-fixture records are in each versioned freeze and full native reports are in `final-0.1.1-detailed-a.json` / `final-0.1.1-detailed-b.json`. Environment/source/schema hashes and aligned common limits are in each freeze and `environment.json`. Both use a 120-second evaluation timeout. A retains bounded output capture; B retains its prior subprocess containment. No parser or ZIP safety check was relaxed.\n\nOfficial JAR SHA-256: `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`. Its previously verified release ZIP SHA-256 is `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5`.\n\n## Attribution\n\nThe shared Contract 0.1.1 code-plus-message policy distinguishes ZIP/OCF, content XML, identity and offline resource predicates. OPF-014, OPF-074 and other unmatched diagnostics remain raw; they are not automatically BASE-002. No post-run primary-error filter is applied.\n\n## Historical evidence correction\n\nStage 2 correctly identified only 31 retained A external records versus 69 B records. Inspection of the old A freezer shows it actually invoked A with EPUBCheck for every fixture, then retained detailed logs only for valid/edge fixtures and removed BASE-002 whenever another failed ID existed. Thus 31 is a retained-evidence count, not proof of only 31 invocations. The historical script, freezes and Stage 2 reports remain unchanged. This new workflow records every invocation and never filters failed IDs.\n\nA second metadata correction: unicode-normalization 0.1.25 exports Unicode 17.0.0, not the historical hardcoded Unicode 16 label. A now reports the crate constant. B uses Unicode 15.1.0. These are controlled same-corpus/tool/policy runs, not bit-identical environments; no observed fixture outcome differs because of Unicode.\n\n## Every fixture\n\nBoth executed=true and skipReason=null throughout. Package digests appear beside these records in the machine-readable freezes.\n\n' + table(['Fixture', 'A exit', 'B exit', 'Diagnostic codes', 'Guarded SPD attribution'], rows))


def render_matrix(compared):
    rows = []
    for r in compared:
        actual = r['A']
        rows.append([r['fixture'], actual['base'], actual['normativeCapabilities']['Accessible'], actual['normativeCapabilities']['Mapping'], ids(actual['violationRequirementIds']), ids(actual['notTestedRequirementIds']), 'YES', 'YES'])
    write('fixture-matrix.md', '# Corpus 0.1.1 fixture matrix\n\nEvery value below is equal in A, B and the independently reviewed oracle. All operational statuses are COMPLETE. Missing/conflicting descriptor fixtures carry UNKNOWN authority and capabilities; all others have KNOWN authority. Full values, digests, pairwise fields and old Stage 2 outcomes are in `differential-results.json`. Experimental equality is measured separately.\n\n' + table(['Fixture', 'Base', 'Accessible', 'Mapping', 'Failed IDs', 'NOT_TESTED IDs', 'Three-way exact', 'Experimental exact'], rows))


def render_gate(metrics, integrity, checks, frozen):
    gates = [
        ['Open normative specification blockers', '0', 'PASS'], ['A ↔ B normative surface', '70/70', 'PASS'], ['A ↔ independently reviewed oracle', '70/70', 'PASS'], ['B ↔ independently reviewed oracle', '70/70', 'PASS'],
        ['Fixture identity and exact bytes', '70/70; package and expectation SHA-256 verified', 'PASS'], ['Valid multi-spine', 'Base PASS in both; no failures; EPUBCheck exit 0', 'PASS'], ['Cross-spine duplicate', 'Base FAIL, exactly SPD-ID-006 in both; EPUBCheck exit 0', 'PASS'],
        ['Stale Mapping attribution', 'STATE-007; no STATE-001 anywhere in document profile', 'PASS'], ['Unknown descriptor authority', 'UNKNOWN, not empty/NOT_CLAIMED; matching blocked sets', 'PASS'], ['Lifecycle/effects guards', 'No EDITABLE STATE-002; no non-semantic STATE-003', 'PASS'],
        ['Reviewed overlap attribution', 'RES-003+006, MAP-011+012, resource/projection and state bindings exact', 'PASS'], ['Requirement coverage', 'Each validator: 113/113 represented, 74/74 automated registered/implemented', 'PASS'],
        ['Full shared EPUBCheck scope', '70/70 each, version 5.3.0, same policy, zero skipped/operational failures', 'PASS'], ['Validator A checks', 'fmt, strict clippy, 17 tests, release; 128-input fuzz smoke included', 'PASS'], ['Validator B checks', '57 unit/property/security/integration tests, Ruff, wheel build and installed policy smoke', 'PASS'], ['Repository checks', '21 tests, schemas and 70-package integrity audit', 'PASS'],
        ['Draft and registry freeze', 'Both pinned SHA-256 values unchanged', 'PASS'], ['Historical evidence and canonical schemas', f'{integrity["protectedFilesVerified"]} protected live files; all 350 archived files verify', 'PASS'], ['Source/input stability', 'Start/end snapshots equal for each run and rechecked at final gate', 'PASS'], ['Experimental reporting (separate)', '70/70 A↔B↔oracle', 'PASS'],
    ]
    answers = [
        ['A. Format Draft changed?', 'NO. Exact pre/post digest unchanged; no Format semantics changed.'], ['B. Corpus fixtures?', '70: 18 valid, 39 invalid, 13 edge.'], ['C. Valid multi-spine passes?', 'YES, both validators and EPUBCheck.'], ['D. New duplicate fails ID-006?', 'YES, exactly that failed ID in both.'], ['E. Stale STATE-001 removed?', 'YES; STATE-007 is used; processor behavior is not inferred.'], ['F. Unknown facts remain unknown?', 'YES; explicit UNKNOWN authority/capabilities, matching NOT_TESTED prerequisites.'], ['G. Lifecycle rules guarded?', 'YES; targeted EDITABLE and resource-effects regressions pass.'], ['H. Same EPUBCheck scope?', 'YES, all 70 packages completed in each validator.'], ['I. Same external attribution?', 'YES, shared Contract 0.1.1 guarded code/message table.'], ['J. Every normative field agrees?', 'YES, 70/70 complete exact agreement.'], ['K. Both match independent oracle?', 'YES, 70/70 each, without oracle generation from validator output.'], ['L. Open Format blockers?', 'NO, zero.'], ['M. Experimental convergence?', 'YES, 70/70 separately; physical presence does not imply claim.'],
    ]
    pins = '\n'.join(f'- `{name}`: `{digest}`' for name, digest in read('baseline.json')['pins'].items())
    freeze_table = table(['Validator', 'Versioned immutable freeze', 'SHA-256'], [[side, row['path'], row['sha256']] for side, row in frozen.items()])
    write('RC_GATE.md', '# Format 0.1 Release Candidate preparation gate\n\n' + DECISION + '\n\nThis gate authorizes no rename or release. Format remains **Format 0.1 Draft**. RC1 preparation is a separate task.\n\n## Required gates\n\n' + table(['Gate', 'Evidence', 'Result'], gates) + '\n\n## Final questions A–M\n\n' + table(['Question', 'Answer'], answers) + '\n\n## Frozen normative inputs\n\n' + pins + '\n\n## New validator freezes\n\n' + freeze_table + '\n\nDetailed test commands and exit statuses: `checks.json`; complete outputs: the eight named `.log` files. Coverage registration is retained without reclassifying requirements. Document-only runs do not certify historical lineage, processor behavior, Accessible manual work or experimental PDF conformance. Unicode versions differ (A 17.0.0, B 15.1.0); no fixture behavior differs, and environments are not described as bit-identical.\n\n' + DECISION)
    comparison = [
        ['Fixtures', '69', '70'], ['Base agreement', '68/69', '70/70'], ['Normative capabilities', '69/69', '70/70'], ['Failed-ID sets', '44/69', '70/70'], ['NOT_TESTED sets', '69/69', '70/70'], ['Operational status', '69/69', '70/70'], ['Complete normative surface', '44/69', '70/70'], ['Experimental reporting (separate)', '45/69', '70/70'], ['Open normative blockers', '0', '0'],
    ]
    write('summary.md', '# Validator convergence and release gate\n\n' + DECISION + '\n\nValidator A **0.1.0-draft.2**, Validator B **0.1.1**, shared Contract **0.1.1**, Corpus **0.1.1**. All 70 fixtures agree exactly across A, B and the independently reviewed oracle. No Format Draft, requirement meaning/ID/classification, or canonical schema changed. No RC1 rename or release was performed.\n\n## Old versus new\n\n' + table(['Measure', 'Frozen Stage 2', 'Convergence'], comparison) + '\n\nThe repaired positive multi-spine passes both validators. The new cross-spine negative fails exactly SPD-ID-006 in both while EPUBCheck passes its per-resource XML IDs. Stale Mapping uses STATE-007, not processor STATE-001. Unknown authority stays unknown. SEALED/effects guards and reviewed independent overlaps are retained. Experimental presence, declaration and evaluation agree separately.\n\n## Verification\n\n- A: 17 tests, strict clippy, fmt check, release build; deterministic 128-input fuzz smoke included.\n- B: 57 tests including property/security/adapter checks, Ruff, wheel build and installed bundled-policy smoke.\n- Repository: 21 tests; 70 package hashes and 70 expected-file hashes/schemas verified; all multi-spine projections and bindings recompute.\n- EPUBCheck 5.3.0: 70 completed executions per validator, 140 total; zero skips or operational failures; identical guarded attribution.\n- Both: 113/113 requirements represented and 74/74 automated registrations/implementations retained.\n- Preservation: 71 protected live files and all 350 archived historical inputs verify; source snapshots remained stable during final runs.\n\nA preliminary B run exposed one Accessible/Base scope reporting regression introduced during repair. It was fixed and regression-tested before the final stable full run. Preliminary `candidate-*` files are not frozen release evidence.\n\nThe old A freezer retained only 31 external records but invoked the tool more broadly; it also filtered BASE-002 beside other IDs. The new runner records every execution and filters nothing. A\'s historical Unicode 16 label was incorrect: the installed crate uses 17.0.0. B uses 15.1.0. This difference is disclosed and did not affect observed fixture convergence; environments are not bit-identical.\n\n## Evidence\n\n[RC gate and answers A–M](RC_GATE.md), [contract changes](contract-changes.md), [attribution table](attribution-table.md), [corpus changes](corpus-changes.md), [A repairs](validator-a-changes.md), [B repairs](validator-b-changes.md), [external evaluation](external-evaluation.md), [fixture matrix](fixture-matrix.md), [machine-readable differential](differential-results.json).\n\n' + freeze_table + '\n\n' + DECISION)


if __name__ == '__main__': main()
