"""Render reviewed Stage 2 classifications; never imports either validator."""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
N = 'NORMALIZATION_CONTRACT_BUG'
B = 'VALIDATOR_B_BUG'
A = 'VALIDATOR_A_BUG'
C = 'CORPUS_ORACLE_BUG'
decisions = {}


def add(name, primary, family, conclusion, target, extra, secondary=()):
    fid = ('valid/' if name == 'multi-spine' else 'invalid/') + name
    decisions[fid] = dict(primaryClassification=primary, secondaryClassifications=list(secondary),
                          family=family, severity='RC_BLOCKER' if name == 'multi-spine' else 'RC_DIAGNOSTIC_CONVERGENCE',
                          correctInterpretation=conclusion, recommendedTarget=target, additionalFindingAssessment=extra)


add('multi-spine', C, 'NODE_ID_SCOPE',
    'Invalid: n_article01 is repeated across two authoritative spine resources in one revision (Draft §§8,14; SPD-ID-006).',
    'Corpus; Validator A', {'SPD-ID-006': 'ESTABLISHED: chapter1.xhtml:4 and chapter2.xhtml:4 both identify html/body/article as n_article01; unrelated non-spine IDs are excluded.'}, [A])
add('bad-resource-hash', B, 'STATE_INTEGRITY_CASCADE',
    'Byte/hash and both declared-inventory projection mismatches are directly measurable. STATE-002 is a sealed-state rule but lifecycle is EDITABLE (Draft §§27–29,70,72).',
    'Validator B; Differential contract', {
        'SPD-RES-004': 'ESTABLISHED: content.xhtml is 516 bytes; declared hash is all zero, actual is 51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935.',
        'SPD-INT-004': 'ESTABLISHED: declared-inventory projection d774ef728e31b285e4f10985af261ed70550723d3401f6ad65f722587dd13aa3 differs from descriptor 36f4e697ebaa31e51e1b1789afe3b611aa5ee284785c4117c9929bdcef5ba0d6.',
        'SPD-INT-005': 'ESTABLISHED: declared-inventory projection f2d76f12b5ef7cda3db25403375d4a7419dedcf1b176e7d41968b2b5940594ec differs from descriptor 6c4b44d7572730c76f1ca20a7b0b079df75beed8a4e9f7875040d779cb72f5d7.',
        'SPD-STATE-002': 'WRONG REQUIREMENT/APPLICABILITY: exact inventory binding does mismatch, but this is EDITABLE, not SEALED. General integrity failure is established; a sealed-state failure is not.'}, [N])
add('descriptor-discovery-missing', B, 'DESCRIPTOR_DISCOVERY_CASCADE',
    'No descriptor links exist. OPF and spine are independently discoverable; descriptor claims are unknown, not an empty set. No filename fallback is permitted (§69).',
    'Validator B; Differential contract', {
        'SPD-ARCH-001': 'NOT ESTABLISHED: missing Base declaration is not evidence of zero/multiple authoritative semantic representations; OPF has one spine.',
        'SPD-CAP-002': 'BLOCKED: authoritative capability array unavailable; do not treat unavailable as known empty.',
        'SPD-CAP-003': 'BLOCKED: OPF claim Base is known, authoritative descriptor claim set is not. Equality cannot be tested.'}, [N])
add('descriptor-discovery-conflict', B, 'DESCRIPTOR_DISCOVERY_CASCADE',
    'Document-state and lifecycle links both target state.json. That candidate fails document-state schema, but its fields cannot establish authoritative capability equality or architecture (§69).',
    'Validator B; Differential contract', {
        'SPD-ARCH-001': 'NOT ESTABLISHED: no Base claim in the wrong-type candidate does not establish absence of the authoritative semantic rendition.',
        'SPD-BASE-005': 'ESTABLISHED AT CANDIDATE/STRUCTURAL LEVEL: the explicitly linked document-state candidate fails required descriptor shape. It does not show a missing OPF spine.',
        'SPD-CAP-002': 'CANDIDATE FAILURE ONLY: state.json lacks required capabilities. Reporting a candidate-schema failure is defensible; authoritative claims remain unavailable.',
        'SPD-CAP-003': 'BLOCKED: invalid/conflicting descriptor authority does not supply a valid known-empty capability set to compare with OPF.',
        'SPD-ID-002': 'CANDIDATE FAILURE ONLY: state.json has flat revisionId, not required document-state /revision/revisionId. This is not proof the semantic state has no Revision ID.'}, [N])

external = {
    'duplicate-node-id': ('SPD-ID-006', 'content.xhtml:6,7 repeats n_paragraph01; EPUBCheck RSC-005.'),
    'event-handler': ('SPD-SEC-001', 'content.xhtml:4 has two h1 elements with n_heading01, one with onclick; EPUBCheck OPF-014 and RSC-005.'),
    'external-required-css': ('SPD-SEC-005', 'content.xhtml:3 links https://example.org/x.css; EPUBCheck RSC-006.'),
    'external-required-font': ('SPD-SEC-004', 'style.css:2 has remote x.woff2 without manifest declaration; EPUBCheck OPF-014 and RSC-008.'),
    'external-required-image': ('SPD-SEC-006', 'content.xhtml:7 has remote x.png; OPF omits remote-resources; EPUBCheck OPF-014 and RSC-006.'),
    'invalid-xhtml': ('SPD-SEM-002', 'content.xhtml:1 has an unclosed p and missing head; EPUBCheck RSC-005 and RSC-016.'),
    'javascript': ('SPD-SEC-001', 'content.xhtml:7 contains script; OPF c1 omits scripted; EPUBCheck OPF-014.'),
}
for name, (_, evidence) in external.items():
    extra = {'SPD-BASE-002': 'INDEPENDENT EXTERNAL FAILURE: ' + evidence + ' Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.'}
    if name == 'event-handler':
        extra['SPD-ID-006'] = 'ESTABLISHED: duplicate n_heading01 occurs twice in a well-formed authoritative XHTML DOM at line 4. The onclick attribute does not exempt either ID.'
    add(name, A if name == 'event-handler' else N, 'XHTML_AND_EXTERNAL_EVALUATION',
        evidence + ' Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.',
        'Validator A; Differential contract' if name == 'event-handler' else 'Differential contract; A oracle-generation workflow', extra, [N] if name == 'event-handler' else [])

for name, path, reason in [
    ('duplicate-normalized-path', 'EPUB/cafe\\u0301.txt and EPUB/caf\\u00e9.txt', 'One inventory path is decomposed, not NFC, and the ZIP has a normalized collision.'),
    ('path-traversal', '../escape.txt', 'The inventory explicitly contains a prohibited parent component; the path schema independently rejects it.')]:
    add(name, N, 'RESOURCE_INVENTORY_CASCADE', f'{path}: {reason} Package rejection does not prevent inspecting the inventory string (§§5,28,70).',
        'Differential contract; Validator A reporting', {'SPD-RES-002': 'ESTABLISHED: ' + reason})
for name, extraid, resource in [('unlisted-normative-resource', 'SPD-RES-006', 'EPUB/extra.css'), ('unlisted-non-normative-resource', 'SPD-RES-003', 'EPUB/cache.bin')]:
    add(name, N, 'RESOURCE_INVENTORY_CASCADE', resource + ' exists outside inventory and is neither self-reference exception. Both RES-003 and RES-006 apply; the former explicitly includes caches (§28).',
        'Differential contract; Validator A reporting', {extraid: 'ESTABLISHED: all package entries, including non-normative caches, must be inventoried; role/manifest membership does not partition these two requirements.'})

for name, resource, semantic in [('mutation-asset', 'EPUB/figure.svg', True), ('mutation-css', 'EPUB/style.css', False), ('mutation-semantic', 'EPUB/content.xhtml', True), ('mutation-mapping', 'META-INF/spd/mapping.json', False), ('mutation-fixed', 'EPUB/fixed.pdf', False)]:
    extra = {'SPD-RES-004': 'ESTABLISHED: exact bytes and length for ' + resource + ' disagree with its inventory entry.',
             'SPD-STATE-003': ('ESTABLISHED as integrity coverage of a semantic-affecting resource: SEALED and affects includes semantic; the committed exact bytes changed. This does not prove visible text changed.' if semantic else 'WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.')}
    if name == 'mutation-mapping':
        extra['SPD-STATE-002'] = 'ESTABLISHED: SEALED mapping binding hash 54a9175f… differs from exact mapping hash 3104fb6a…; a trailing byte still matters under exact-byte hashing.'
    if name == 'mutation-fixed':
        extra.update({
            'SPD-STATE-001': 'PROCESSOR CLAIM NOT ESTABLISHED: false current token is established and covered by STATE-005, but no reader execution proves the processor exposed it as current.',
            'SPD-STATE-005': 'ESTABLISHED: status=current but fixed resource hash c9bd22e9… differs from actual df6cb8ce…; currentness is disproved directly.',
            'SPD-STATE-006': 'ESTABLISHED: SEALED has fixed output whose exact digest does not verify, so it cannot be current.',
            'SPD-STATE-007': 'ESTABLISHED: Mapping is explicitly claimed and required current fixed output is disproved by its own hash mismatch.'})
    add(name, N if semantic else B, 'STATE_INTEGRITY_CASCADE', resource + ': exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).',
        'Differential contract; Validator A reporting' if semantic else 'Validator B; Differential contract', extra, [] if semantic else [N])
add('sealed-after-semantic-modification', N, 'STATE_INTEGRITY_CASCADE',
    'SEALED authoritative content.xhtml differs in exact bytes; resource hash and seal invalidity are separately established (§§27–29).', 'Differential contract; Validator A reporting',
    {'SPD-INT-003': 'ESTABLISHED: covered authoritative bytes changed without rebinding.', 'SPD-RES-004': 'ESTABLISHED: content.xhtml declared 516 bytes, actual 525, and SHA-256 differs.'})
add('sealed-after-annotation-modification', B, 'STATE_INTEGRITY_CASCADE',
    'annotations.json changed from 465 to 466 bytes in SEALED. Seal invalidity and ANN-004 are clear, but annotation bytes have affects=[] and are not semantic content (§§27,73).',
    'Validator B; Differential contract', {
        'SPD-INT-003': 'ESTABLISHED: packaged annotation modification breaks covered integrity.',
        'SPD-RES-004': 'ESTABLISHED: exact annotation bytes/hash differ, even if the extra byte is whitespace.',
        'SPD-STATE-003': 'WRONG REQUIREMENT ATTRIBUTION: non-semantic annotation mutation invalidates the seal, not the semantic-content-specific predicate.'}, [N])
add('mapping-with-stale-fixed', B, 'STATE_INTEGRITY_CASCADE',
    'EDITABLE explicitly says stale and fixed input digest differs from current. Mapping must fail STATE-007; a Mapping claim alone does not establish reader mispresentation under STATE-001 (§§26,56,71).',
    'Validator B', {'SPD-STATE-001': 'NOT ESTABLISHED: declared stale is not declared current, and this fixture supplies no reader behavior evidence.'})
add('stale-fixed-rendition', A, 'STATE_INTEGRITY_CASCADE',
    'EDITABLE explicitly says stale although its numerical bindings match. Mapping requires current, not merely equal hashes. B adds the correct STATE-007; both sides share unsupported processor-level STATE-001 attribution (§§26,56).',
    'Validator A; Validator B; Corpus', {'SPD-STATE-007': 'ESTABLISHED: Mapping is claimed but fixed is explicitly stale. A incorrectly routes this Mapping failure to the processor rule STATE-001.'}, [B, C])
add('mapping-invalid-geometry', N, 'MAPPING_GEOMETRY',
    'Page p_1 is 816×1056; quad [-1,0,900,0,900,1200,-1,1200] is finite, structurally valid and TL-TR-BR-BL ordered, but out of bounds. §§36 and 56 both prohibit it.',
    'Differential contract; Validator A reporting', {'SPD-MAP-012': 'ESTABLISHED under its linked §36 geometry rule, which explicitly requires visible bounds. Registry shorthand emphasizes coordinates/dimensions; MAP-011 explicitly names page bounds. This is overlapping rule attribution, not a parser cascade or undefined geometry.'})


def write(name, text):
    (OUT / name).write_text(text.rstrip() + '\n', encoding='utf-8')


def main():
    raw = json.loads((OUT / 'raw-diff.json').read_text(encoding='utf-8'))
    evidence = {x['fixture']: x for x in json.loads((OUT / 'fixture-byte-evidence.json').read_text(encoding='utf-8'))}
    differing = [x for x in raw['fixtures'] if not x['completeSurfaceAgreement']]
    assert set(decisions) == {x['fixture'] for x in differing}
    for x in differing:
        assert set(x['B_ONLY']) == set(decisions[x['fixture']]['additionalFindingAssessment'])
        x['analysis'] = decisions[x['fixture']]
    raw['classificationCounts'] = dict(sorted(collections.Counter(d['primaryClassification'] for d in decisions.values()).items()))
    raw['severityCounts'] = dict(sorted(collections.Counter(d['severity'] for d in decisions.values()).items()))
    write('raw-diff.json', json.dumps(raw, ensure_ascii=False, indent=2))
    header = '# Fixture differences\n\nAll 25 differing fixtures; A_ONLY is empty in every row. A = COMMON; B = COMMON plus B_ONLY. Capability and NOT_TESTED fields remain equal; full values are in raw-diff.json. “ESTABLISHED” means a testable failed predicate, not proof that every frozen ID is the best attribution. Secondary classifications do not inflate counts.\n\n'
    table = '| Fixture | A | B | Difference | Classification | RC Severity | Correct Interpretation | Recommended Target |\n|---|---|---|---|---|---|---|---|\n'
    details = []
    for x in differing:
        d = decisions[x['fixture']]
        a = x['A']['base'] + '; ' + (', '.join(x['COMMON']) or 'no violations')
        b = x['B']['base'] + '; ' + ', '.join(x['B']['violationRequirementIds'])
        table += '| ' + ' | '.join([x['fixture'], a, b, 'B_ONLY: ' + ', '.join(x['B_ONLY']), d['primaryClassification'], d['severity'], d['correctInterpretation'], d['recommendedTarget']]) + ' |\n'
        ev = evidence[x['fixture']]
        block = f"## {x['fixture']}\n\nPrimary: {d['primaryClassification']}. Secondary: {', '.join(d['secondaryClassifications']) or 'none'}. Severity: {d['severity']}.\n\nPackage SHA-256: `{ev['packageSha256']}`. Evidence paths are ZIP-entry paths inside `tests/{x['fixture']}/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.\n\nA_ONLY: none. COMMON: {', '.join(x['COMMON']) or 'none'}. B_ONLY: {', '.join(x['B_ONLY'])}.\n\n{d['correctInterpretation']}\n\n"
        block += '\n'.join(f'- `{key}`: {value}' for key, value in d['additionalFindingAssessment'].items()) + '\n'
        if ev['badResources']:
            block += '\nMeasured resource mismatches:\n\n'
            for bad in ev['badResources']:
                block += f"- `{bad['path']}`: {bad['declaredLength']} → {bad['actualLength']} bytes; affects={bad['affects']}; `{bad['declaredSha256']}` → `{bad['actualSha256']}`.\n"
        details.append(block)
    write('fixture-differences.md', header + table + '\n' + '\n'.join(details))
    by_id = collections.defaultdict(list)
    for x in differing:
        for rid in x['B_ONLY']:
            by_id[rid].append(x['fixture'])
    reqs = {}
    for line in (ROOT / 'spec/requirements.yaml').read_text(encoding='utf-8').splitlines():
        if 'id: SPD-' in line:
            reqs[line.split('id: ')[1].split(',')[0]] = line.strip()
    text = '# Requirement differences\n\nOnly B_ONLY occurrences count below; no A_ONLY occurrences exist. COMMON findings are not automatically correct: STATE-001 in stale-fixed-rendition is an identified shared misattribution. See fixture details for every per-ID assessment.\n\n'
    for rid, fixtures in sorted(by_id.items()):
        text += f'## {rid} — {len(fixtures)} differing fixtures\n\nFrozen registry entry:\n\n```yaml\n{reqs[rid]}\n```\n\n'
        text += '\n'.join('- ' + f + ': ' + decisions[f]['additionalFindingAssessment'][rid] for f in fixtures) + '\n\n'
    write('requirement-differences.md', text)
    ex = [x for x in raw['fixtures'] if not x['experimental']['equal']]
    text = '# Experimental capability reporting — NON_NORMATIVE\n\n24 of 69 fixtures differ; 45 agree. All differences are Fixed-Experimental: A=PRESENT_EXPERIMENTAL, B=NOT_CLAIMED. Archive-Experimental agrees throughout. These statuses are excluded from every normative agreement metric.\n\nIn every differing package the authoritative declaration is exactly Base + Mapping, without an explicit Fixed-Experimental claim; fixed.pdf exists. A reports physical fixed-rendition presence; B reports explicit capability claims. The Draft permits Mapping without a separate Fixed-Experimental declaration (§§34,54,56–57). Neither presence nor a Mapping dependency creates that explicit claim.\n\nSource explanation, after byte inspection: A validator.rs:1296–1307 tests fixed status != absent; B validator.py:94–97 tests capability membership. This is a future report-model consistency issue, not a normative conformance failure. Prefer separate fixedRenditionPresent and fixedExperimentalClaimed fields; neither means PDF conformance was tested.\n\n| Fixture | Explicit claims | Fixed status | A | B | Severity |\n|---|---|---|---|---|---|\n'
    for x in ex:
        ev = evidence[x['fixture']]
        assert [c['id'] for c in ev['claims']] == ['Base', 'Mapping']
        text += f"| {x['fixture']} | Base, Mapping | {ev['fixed']['status']} | PRESENT_EXPERIMENTAL | NOT_CLAIMED | NON_NORMATIVE |\n"
    write('experimental-capability-differences.md', text)
    text = '# Disagreement families\n\nFamilies partition the 25 normative-surface differences. Experimental overlap is listed separately, not added to 25.\n\n'
    descriptions = {
        'NODE_ID_SCOPE': ('Does uniqueness span the authoritative revision?', 'Per-XHTML ID set.', 'Shared spine-wide ID index.', 'Draft §14 is revision-wide. Corpus and A wrong.'),
        'DESCRIPTOR_DISCOVERY_CASCADE': ('Which facts remain knowable after failed descriptor authority?', 'Early return after discovery failure.', 'Continue with absent or wrong-type descriptor treated as claim data.', 'Keep OPF/spine facts; do not substitute empty claims or infer architecture. Candidate schema diagnostics can remain with explicit provenance.'),
        'XHTML_AND_EXTERNAL_EVALUATION': ('Are extra findings independent and was external scope equal?', 'Golden/native surface plus 31 successful valid/edge external runs; event-ID exemption.', 'Run EPUBCheck on all 69 and retain duplicate-ID finding.', 'Seven extra external aggregate findings are scope/reporting differences; the event duplicate is real and the exemption is a defect.'),
        'RESOURCE_INVENTORY_CASCADE': ('Do ZIP rejection or resource roles suppress inventory rules?', 'Return on package errors; choose RES-003 or RES-006 by OPF filename presence.', 'Inspect inventory and report all overlaps.', 'Unsafe/non-NFC strings are directly testable. Both inventory coverage rules include caches; no role-based division.'),
        'STATE_INTEGRITY_CASCADE': ('Which equality failures and lifecycle predicates are established?', 'Often choose primary integrity or state finding and suppress overlaps.', 'Emit multiple equalities, plus generic sealed and stale-mapping labels.', 'Retain measurable independent equalities; honor EDITABLE/SEALED, effects, and processor applicability. Do not infer semantic mutation from arbitrary seal failure.'),
        'MAPPING_GEOMETRY': ('Can both linked geometry predicates be evaluated?', 'Bounds failure reported as MAP-011.', 'Bounds failure reported as MAP-011 and MAP-012.', 'Valid finite quad shape does not prevent checking bounds; §§36 and 56 overlap. Define stable ID attribution in contract.'),
    }
    for family, description in descriptions.items():
        fs = [f for f, d in decisions.items() if d['family'] == family]
        ids = sorted({r for x in differing if x['fixture'] in fs for r in x['B']['violationRequirementIds']})
        text += f'## {family} — {len(fs)} fixtures\n\nAffected fixtures: ' + ', '.join(sorted(fs)) + '.\n\nAffected IDs: ' + ', '.join(ids) + '.\n\n'
        for label, value in zip(['Root normative question', 'A interpretation', 'B interpretation', 'Resolved interpretation'], description):
            text += f'{label}: {value}\n\n'
        text += 'Primary classifications: ' + ', '.join(sorted({decisions[f]['primaryClassification'] for f in fs})) + '. Per-fixture exceptions and secondary classes are in fixture-differences.md.\n\n'
    text += '## EXPERIMENTAL_CAPABILITY_REPORTING — 24 fixtures\n\nSee experimental-capability-differences.md for the complete fixture list. Affected field: Fixed-Experimental presence/status; no normative requirement-ID difference is attributed to this field. A uses presence, B uses explicit claim. Resolved as a NON_NORMATIVE report-model consistency issue, outside the comparison contract.\n'
    write('disagreement-families.md', text)
    print('Classified', len(differing), 'fixtures:', raw['classificationCounts'])


if __name__ == '__main__':
    main()
