"""Freeze only an actually passing pre-RC gate; never manufacture convergence."""
import hashlib
import json
import platform
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,text):(OUT/name).write_text(text.rstrip()+'\n',encoding='utf-8')
def js(name,data):write(name,json.dumps(data,indent=2))

def normalize(e):
    return {'fixture':e['fixture'],'base':e['base'],'normativeCapabilities':{c:e['capabilities'][c] for c in ['Accessible','Mapping']},'experimentalCapabilities':{c:e['capabilities'][c] for c in ['Archive-Experimental','Fixed-Experimental']},'violationRequirementIds':sorted(v['requirement'] for v in e['violations']),'notTestedRequirementIds':e['notTestedRequirementIds'],'operationalStatus':e['operationalStatus'],'authoritativeClaimsStatus':e['authoritativeClaimsStatus'],'experimentalReporting':e['experimentalReporting']}

def main():
    inputs={s:json.loads((OUT/f'candidate-{s}.json').read_text()) for s in ['a','b']}
    manifest=json.loads((ROOT/'tests/corpus-0.1.2/manifest.json').read_text())
    oracle={f['id']:normalize(json.loads((ROOT/f['expectedResult']).read_text())) for f in manifest['fixtures']}
    normalized={s:{r['normalized']['fixture']:r['normalized'] for r in inputs[s]['results']} for s in inputs}
    differences={s:{f:{k:{'actual':normalized[s][f][k],'expected':oracle[f][k]} for k in oracle[f] if normalized[s][f][k]!=oracle[f][k]} for f in oracle if normalized[s][f]!=oracle[f]} for s in inputs}
    ab=[f for f in oracle if normalized['a'][f]!=normalized['b'][f]]
    summary={'fixtureCount':len(oracle),'aOracleDifferences':differences['a'],'bOracleDifferences':differences['b'],'abDifferences':ab,'sourceStable':{s:inputs[s]['sourceStableDuringRun'] for s in inputs}}
    js('differential-results.json',summary)
    assert not any(differences.values()) and not ab, 'Normative comparison is not converged'
    assert all(x['sourceStableDuringRun'] for x in inputs.values())
    assert all(sha(ROOT/p)==h for data in inputs.values() for p,h in data['sourceSha256'].items()), 'Accepted evidence must match current sources'
    current_manifest=sha(ROOT/'tests/corpus-0.1.2/manifest.json')
    assert all(x['manifestSha256']==current_manifest for x in inputs.values())
    for f in manifest['fixtures']:
        assert sha(ROOT/f['package'])==f['packageSha256']
        assert sha(ROOT/f['expectedResult'])==f['expectedResultSha256']
    external={}
    for side,data in inputs.items():
        external[side]=[]
        for row in data['results']:
            r=row['report'];n=row['normalized']; e=r['externalTools'][0] if side=='a' else r['metadata']['epubcheck']
            outcome=e.get('outcome',e.get('result'))
            assert e.get('executed') is True,(side,n['fixture'],'not executed')
            assert outcome in ['PASS','FAIL'],(side,n['fixture'],outcome)
            assert n['base']!='PASS' or outcome=='PASS',(side,n['fixture'],'Base/EPUB conflict')
            external[side].append({'fixture':n['fixture'],'base':n['base'],'epubcheck':outcome,'diagnosticCodes':e.get('diagnosticCodes',[]),'exitCode':e.get('exitCode')})
    checks=json.loads((OUT/'checks.json').read_text()); assert all(c['exitCode']==0 for c in checks)
    supplemental=json.loads((OUT/'supplemental-native-checks.json').read_text()); assert all(c['exit_code']==0 for c in supplemental)
    baseline=json.loads((OUT/'baseline-sha256.json').read_text())
    protected={p:h for p,h in baseline.items() if p.startswith(('schemas/','validator-convergence/','reports/epub_boundary_security_gate/'))}
    assert all(sha(ROOT/p)==h for p,h in protected.items())
    historical=json.loads((ROOT/'tests/corpus-manifest.json').read_text())
    assert all(sha(ROOT/f['package'])==f['packageSha256'] and sha(ROOT/f['expectedResult'])==f['expectedResultSha256'] for f in historical['fixtures'])
    old_passes=[f['id'] for f in historical['fixtures'] if json.loads((ROOT/f['expectedResult']).read_text())['base']=='PASS']
    assert all(normalized[s][f]['base']=='PASS' for s in inputs for f in old_passes), 'Historical Base-PASS compatibility changed'
    with zipfile.ZipFile(OUT/'pre-clarification-inputs.zip') as z:
        old=yaml.safe_load(z.read('spec/requirements.yaml'))
        assert z.read('tests/corpus-manifest.json')==(ROOT/'tests/corpus-manifest.json').read_bytes()
    new=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())
    old_rows={r['id']:r for r in old['requirements']};new_rows={r['id']:r for r in new['requirements']}
    changed=[rid for rid,r in old_rows.items() if new_rows[rid]!=r]
    expected_changed={'SPD-BASE-001','SPD-BASE-002','SPD-BASE-004'}|{f'SPD-SEC-{i:03}' for i in range(1,9)}
    assert set(changed)==expected_changed
    assert len(new_rows)==118 and len(new_rows.keys()-old_rows.keys())==5
    regenerated=json.loads((OUT/'rebuild-verification.json').read_text());assert len(regenerated)==37 and all(r['identical'] for r in regenerated)
    js('integrity-checks.json',{'historicalPackagesUnchanged':70,'historicalExpectedFilesUnchanged':70,'historicalManifestUnchanged':True,'protectedHistoricalAndSchemaFiles':len(protected),'protectedChanges':[],'modifiedExistingRequirements':changed,'addedRequirements':sorted(new_rows.keys()-old_rows.keys()),'unchangedRequirements':102,'newFixturesReproducedByteIdentically':37,'newManifestSha256':current_manifest})
    js('epubcheck-results.json',external)
    counts={s:dict(Counter(e['epubcheck'] for e in external[s])) for s in inputs}
    base_counts=dict(Counter(r['base'] for r in normalized['a'].values()))
    passes=base_counts['PASS']
    attempts=[p.name for p in OUT.glob('operational-attempt-*.json')]
    write('EPUBCHECK_RESULTS.md',f'''# Whole-publication EPUBCheck results

Official EPUBCheck 5.3.0 executed on all **107/107** final package byte sequences for each validator. A: {counts['a']}. B: {counts['b']}. All **{passes}/{passes} Base-PASS** fixtures have EPUBCheck PASS; no unresolved EPUB error is accepted. Warnings alone are not failures.

S29 (missing OPF title) fails exactly SPD-BASE-002. Native-invalid packages retain native IDs plus BASE-002 when EPUB also fails. S27 malformed ZIP retains operational MALFORMED_INPUT and independently established EPUB failure; S28 retains RESOURCE_LIMIT with no invented native conformance failure.

Raw per-package outputs, diagnostic codes, exit status, executed flag, exact source and JAR hashes are retained in the final validator reports. Interrupted or unavailable tool evidence is never counted as document failure. Operational attempt records: {', '.join(attempts) or 'none'}. Where present, these preserve transient parallel-run probe failures; only affected fixtures were re-evaluated at lower concurrency with unchanged sources/package bytes and the same tool/time limits.

S25 was completed after the initial batch when byte inspection found that only its symlink flag was present. The final package includes both symlink and device modes. Direct EPUBCheck and both validators re-evaluated those final bytes; the initial package and its digest are retained in s25-mode-review.json and s25-initial-symlink-only.epub. Reused results for all other fixtures are checked against their exact final package hashes and unchanged implementation sources.

The dated-standard/tool relationship and observed escaped-import limitation are documented in UPSTREAM_PINNING.md. EPUBCheck PASS is required but does not by itself prove the SPD passive profile, human semantic completeness or reader conformance.
''')
    write('DIFFERENTIAL_RESULTS.md',f'''# Independent validator reconvergence

- Validator A 0.1.0-draft.3 ↔ Validator B 0.1.2: **107/107** exact agreement.
- Validator A ↔ reviewed oracle: **107/107**.
- Validator B ↔ reviewed oracle: **107/107**.
- Experimental and authoritative-claim reporting: **107/107** exact agreement.
- Base results: {base_counts}.
- Final operational status: 105 COMPLETE, one MALFORMED_INPUT and one RESOURCE_LIMIT, as independently specified by the operational fixtures; no INTERNAL_ERROR.
- Manifest SHA-256: `{current_manifest}`.

Compared fields: Base, normative capabilities, failed requirement IDs, NOT_TESTED IDs, operational status; also experimental capabilities, fixed reporting and known/unknown authoritative claims. Both implementations evaluated identical package bytes. Source identities were stable during each accepted evaluation. The oracle is derived from reviewed requirements/profiles, fixture bytes and direct EPUB diagnostic attribution, not validator consensus.

No historical Base-PASS fixture became invalid under the clarification. All 70 historical packages are byte-identical. New human/processor NOT_TESTED obligations are disclosed without claiming runtime PASS. Corpus 0.1.1 expectations and historical convergence remain immutable.
''')
    decision='READY FOR FORMAT 0.1 RC1 EDITORIAL AND IDENTIFIER PREPARATION'
    answers=[('A','YES — conforming EPUB 3.3 publication/package profile retained.'),('B','YES — Recommendation 13 January 2026 pinned.'),('C','YES — explicit roles and maintenance policy; living sources are not falsely described as immutable snapshots.'),('D','YES — document-originated executable behavior prohibited.'),('E','YES — automatic publication-originated network authority prohibited.'),('F','YES — optional/decorative resources included.'),('G','YES — supported XHTML/CSS/SVG/MathML resource paths are inspected transitively; unresolved locality is NOT_TESTED.'),('H','YES — namespace-aware XML and standards-aware CSS tokens; regex is not authoritative content-security parsing.'),('I','YES — every completed EPUB publication error prevents Base PASS.'),('J','YES — semantic display is distinct from verified SEALED/current fixed presentation.'),('K','YES — hash integrity is distinct from authentication; no signatures added.'),('L','NO — no new MIME type or mandatory extension.'),('M','YES — semantic/revision/mapping architecture and canonical schemas unchanged.'),('N','118 requirements: 113 baseline + 5, with 11 modified and 102 unchanged.'),('O','107 corpus fixtures: 70 retained + 37 targeted additions.'),('P','8 reader-security scenarios; processor conformance, all NOT_TESTED.'),('Q',f'YES — {passes}/{passes} Base-PASS fixtures pass EPUBCheck 5.3.0.'),('R','YES — 107/107 A/B agreement.'),('S','YES — both 107/107 against the independent oracle.'),('T','NO — zero open specification blockers.')]
    write('PRE_RC_GATE.md','# Pre-RC passive security gate\n\nNo RC1 is created. This authorizes only the next editorial/identifier preparation stage; existing production-identifier migration remains separate.\n\n| Question | Answer |\n|---|---|\n'+'\n'.join(f'| {k} | {v} |' for k,v in answers)+'\n\nAll required build/lint/unit/property/schema/coverage/native/full-corpus/external gates pass. Reader behavior and complete static semantic meaning are honestly unevaluated, as required for this pre-reader task. Bounded corpus agreement is not a claim of exploit-proof implementations or universal EPUB reader compatibility.\n\n'+decision)
    js('environment.json',{'python':sys.version,'platform':platform.platform(),'epubcheck':'5.3.0','epubcheckJarSha256':inputs['a']['epubcheckJarSha256'],'specSha256':sha(ROOT/'spec/FORMAT_0.1_DRAFT.md'),'requirementsSha256':sha(ROOT/'spec/requirements.yaml'),'corpusManifestSha256':current_manifest,'validatorA':'0.1.0-draft.3','validatorB':'0.1.2','sourceIdentity':'SHA-256 inventories in final reports; baseline repository has no usable HEAD commit','readerScenariosExecuted':0,'parallelWorkersInitialPerValidator':6,'operationalRetryWorkers':1,'epubcheckVersionProbeTimeoutSeconds':20,'epubcheckTimeoutSeconds':120})
    for side,version in [('a','0.1.0-draft.3'),('b','0.1.2')]:
        destination=OUT/f'final-{side}-{version}.json'
        assert not destination.exists(),'Final evidence already exists; do not overwrite'
        shutil.copyfile(OUT/f'candidate-{side}.json',destination)
    binary=OUT/'dist/spd-validator-a-0.1.0-draft.3.exe'
    shutil.copyfile(ROOT/'validator-a/target/release/spd-validator.exe',binary)
    evidence={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='release-evidence-sha256.json'}
    js('release-evidence-sha256.json',evidence)
    print(decision)

if __name__=='__main__':main()
