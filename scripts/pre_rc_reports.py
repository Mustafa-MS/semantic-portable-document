"""Build reviewable change and coverage reports from the versioned evidence."""
import hashlib
import json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'

def write(name,text): (OUT/name).write_text(text.rstrip()+'\n',encoding='utf-8')

def main():
    manifest=json.loads((ROOT/'tests/corpus-0.1.2/manifest.json').read_text())
    new=[f for f in manifest['fixtures'] if f['category']=='security']
    write('ARCHITECTURE_DECISION.md','''# Architecture decision implemented

Option A is retained: SPD 0.1 uses a conforming EPUB 3.3 publication/package profile, pinned to Recommendation 13 January 2026. SPD is a distinct semantic document model with a passive content profile and EPUB-compatible packaging layer. The decision was not reopened.

No new internal marker, MIME type, mandatory extension, container manifest, Forms/Interactive capability, signature, reader, editor or renderer was introduced. Semantic XHTML remains authoritative for SEALED documents. Generic reading is distinct from verified state/fixed presentation. Fixed-Experimental and Archive-Experimental remain experimental. No RC1 was created.

Document/revision/node identity, both digest algorithms, lifecycle, Mapping, annotations, transactional editing and Accessible 0.1 meaning are unchanged. Baseline preservation and final integrity checks identify exact bytes. Changes are approved clarifications, stricter subset rules, processor obligations, upstream pins and validation-closure fixes; they are not all editorial.
''')
    write('UPSTREAM_PINNING.md','''# Upstream pinning and tool reconciliation

The normative ledger is spec/UPSTREAM_DEPENDENCY_BASELINE_0.1.md. EPUB 3.3 REC 2026-01-13 and the explicitly relied-on Reading Systems 3.3 REC 2024-10-17 are separate publication/processor baselines. Accessible remains EPUB Accessibility 1.1 REC 2024-10-17 plus WCAG 2.2 REC 2024-12-12 AA and human evaluation.

HTML and URL are living references with the approved audit's reviewed baseline; no immutable commit is fabricated. CSS modules, SVG, MathML, XML/Namespaces, Unicode, ZIP/URI dependencies, JSON Schema, JCS and SHA-256 have explicit roles, incorporation and update policies. Future changes require a recorded SPD maintenance decision and reconvergence. EPUB 3.4 is not inherited.

EPUBCheck 5.3.0 was released 2025-09-01 and advertises EPUB 3.3 validation. Its version is an implementation identity, not the 2026 specification edition. The dated EPUB change log lists post-2023 substantive changes for viewport XML whitespace and SVG epub:type placement (2023/2024); the tool changelog includes later SVG/schema updates. No newly mandatory post-tool construct was identified in the approved scope. This is bounded reconciliation, not proof that the checker implements every prose/editorial point. Sources: [EPUB dated edition/change log](https://www.w3.org/TR/2026/REC-epub-33-20260113/#change-log), [versioned EPUBCheck changelog](https://raw.githubusercontent.com/w3c/epubcheck/v5.3.0/CHANGELOG.md).

An observed tool limitation is recorded rather than hidden: S02's escaped CSS import is decoded by both standards-aware native parsers, while EPUBCheck 5.3.0 reports RSC-020/RSC-007 for a literal backslash interpretation. This deliberately SPD-invalid fixture still fails the EPUB evaluation gate; no valid fixture is exempted or relabeled PASS. S23's remote MathML glyph is EPUBCheck-PASS but rejected by SPD's native no-network/local-resource rules. EPUBCheck alone is not the passive-security validator.

The agreed profile invokes the official 5.3.0 JAR on complete packages with default ERROR/FATAL semantics, no fail-on-warning switch and no external diagnostic suppressions. A completed run is required. Errors add BASE-002; warnings remain evidence; a crash/timeout/incomplete run is operational NOT_TESTED. Raw diagnostics and JAR SHA-256 are retained. No Base-PASS fixture may carry an unresolved EPUB error.
''')
    write('VALIDATOR_A_CHANGES.md','''# Validator A 0.1.0-draft.3

The frozen 0.1.0-draft.2 sources and historical reports are archived before editing. Rust independently implements the clarified contract using roxmltree namespace parsing, cssparser 0.35 CSS Syntax tokens and percent-decoding/package resolution. The production regex security function is replaced by src/passive.rs; no Python implementation code is imported or translated.

Inspection covers scripts/data blocks/events/executable URLs, contexts/controls/navigation, inline/external CSS, imports, escapes/comments/nested functions/custom-property URL tokens, SVG contexts and local fragments, MathML resources, local media and transitive package resources. Dynamic string URL consumers that cannot be resolved are NOT_TESTED. Human static meaning and reader requirements remain untested and cannot be advertised as automatic PASS.

ZIP preflight compares local/central names and bounds, rejects overlaps, compares percent-decoded/NFC entry identities, reports symlink/device modes and bounds actual expanded reads. Resource ceilings remain operational. External conformance errors now add BASE-002, with specific IDs additive; incomplete tool output cannot produce a document failure. Source and JAR identities, strict lint/tests/build results and complete corpus output are recorded separately.

Tests: src/passive.rs includes escaped/nested CSS, inert strings, unresolved dynamic consumers, extensionless namespaced SVG and property-generated CSS; tests/corpus.rs evaluates all 107 native fixture expectations; historical algorithm/identity/mapping tests remain. Processor behavior and decoder exploitation resistance are not established by these tests.
''')
    write('VALIDATOR_B_CHANGES.md','''# Validator B 0.1.2

The frozen 0.1.1 sources/wheel and historical evidence are retained. Python independently uses lxml and tinycss2 in spd_validator_b/passive.py. It inspects namespace-qualified nested XHTML/SVG/MathML, style elements/attributes, stylesheet tokens/imports/font roles, custom-property resource tokens, fragments, graph cycles and remote/unsafe references. Existing semantic/identity/integrity/mapping algorithms remain separate and unchanged in meaning. No Rust parser code is reused.

The ZIP scanner adds decoded-name identity checks, symlink/device policy, local/central header comparisons and overlap/bounds checks. Malformed and resource-limited input retain operational status and untested predicates. Whole-publication EPUB errors add BASE-002; XHTML-specific mappings do not attribute OPF title errors to SEM-002. Crashes, partial diagnostics and timeouts are NOT_TESTED/TOOL_UNAVAILABLE. Reader/human portions remain untested.

tests/test_passive.py exercises token obfuscation, inert text, namespace/fragment behavior, dynamic resource uncertainty and property-generated CSS. Existing package/schema/security/property/Unicode/algorithm tests and all 107 native expectations are retained. The versioned wheel bundles attribution data 0.1.2. Runtime authority and semantic completeness require the separate reader/manual plan.
''')
    rows=[]
    for f in new:
        e=json.loads((ROOT/f['expectedResult']).read_text())
        rows.append(f"| {f['auditCase']} | {f['id']} | {e['base']} | {', '.join(e['nativeViolationRequirementIds']) or 'no native failure'} | {e.get('epubcheckExpected','pending')} |")
    write('CORPUS_CHANGES.md','''# Corpus 0.1.2 changes

70 historical packages retain their original bytes. Historical 0.1.1 manifest/expected files/oracles are not overwritten; new expectations live under tests/corpus-0.1.2/historical. The new version has **107 fixtures**: 70 retained plus **37 additions**.

S01–S30 implement the audit's enumerated Option-A plan. S31–S37 isolate seven explicitly required families: standalone SVG script, SVG event handler, bare iframe, authoritative canvas, ordinary hyperlink, nested CSS rule resource and annotation-xml active content. Existing script/event/remote font/stylesheet/image fixtures are retained. The count is 37 rather than 30 for these targeted reasons, not arbitrary bulk coverage.

The final local MathML glyph fixture uses a token-element child permitted by MathML. An exploratory misplacement was corrected before oracle finalization; no policy was weakened. S29 removes only the required OPF title and rebinds existing inventory/state; it produces BASE-002 without a more-specific native attribution. S27 tests local/central header mismatch; unit/scanner logic also rejects overlapping intervals. S28 is a small bounded ratio-limit fixture, not a universal format maximum.

Native expectations were authored from the profile before validator comparison. Direct EPUBCheck findings are reviewed through the shared attribution contract. Full A/B outputs are evidence, not the oracle. Human/processor NOT_TESTED portions are explicit. Every manifest row records package and expected-result SHA-256; manifest-sha256.txt pins the final manifest.

| Audit label | Fixture | Base | Native failed predicates | Direct EPUBCheck |
|---|---|---|---|---|
'''+'\n'.join(rows))
    groups=[
      ('Scripts, inert script blocks, events, executable URLs and executable resource types','SEC-001; PASS-001','XHTML/SVG; passive resource contract','S07/S08/S30/S31/S32/S37; historical javascript/event-handler','R1/R8'),
      ('iframe/srcdoc, object/embed/plugins, service-worker/application contexts','SEC-002; PASS-002','XHTML passive restrictions','S09/S10/S33','R1/R2'),
      ('Forms, inert labeled input/button, authoritative canvas, base overrides','PASS-002','XHTML passive restrictions','S11/S13/S18/S34','R6'),
      ('Automatic navigation, ping/prefetch/preconnect and remote preload','SEC-003; PASS-002; RS-001','XHTML/passive resource contract','S12/S14; parser preload role checks','R1/R3'),
      ('Optional/decorative/required remote images, stylesheets and fonts','SEC-003–006/008','CSS/XHTML/passive resource contract','S01/S02/S03/S04/S36; historical external-required-*','R1'),
      ('Local CSS imports, packaged fonts/images, static complex CSS','SEC-004–006/008','CSS specific rules','S15/S16/S21; token/parser tests','R5/R6'),
      ('CSS escapes, comments, nested rules/functions, custom properties and inline style','SEC-003–008','CSS resource/token rules','S02/S03/S04/S36; Rust/Python property and unresolved-consumer tests','R1/R5'),
      ('SVG inline/standalone/nested references, foreignObject, scripts/events','SEC-001/007/008; PASS-002','SVG uniform embedding','S05/S06/S07/S17/S31/S32','R1/R7'),
      ('Static SVG paths/shapes/text/gradients/clips/masks/transforms/symbols/local fragments','SEC-007/008','SVG static profile','S17; historical figure-svg; fragment unit test','R5/R7'),
      ('MathML static semantics, mglyph/href, annotation-xml and maction static meaning','SEM-009; SEC-001/003/006/008; PASS-003','MathML passive profile','S22/S23/S37; historical mathml; manual maction completeness','R1/R6'),
      ('Local audio/video/poster/tracks, no autoplay, equivalent semantics','SEC-008; PASS-003','XHTML media policy','S19/S20; common src/poster/track resolver; semantic alternatives manual','R6'),
      ('External HTTP/HTTPS hyperlinks; no file/UNC/data/blob/executable authority','SEC-001/008; RS-001','Passive resource contract','S08/S35; common scheme/containment resolver','R2/R3'),
      ('Transitive package closure and terminating imports/references','SEC-008','Passive resource graph contract','S05/S15/S16/S17/S22/S23/S37','R1/R5'),
      ('Optional time-dependent declarations, static meaning and generated content','PASS-003','CSS/SVG/XHTML profiles','S21; human completeness remains NOT_TESTED','R6'),
      ('Hostile metadata/annotation text and namespace IRIs as inert identifiers','PASS-001; RS-001','Passive resource contract','S24; no identifier fetching','R8'),
      ('ZIP malicious paths/modes/headers/overlap and expansion limits','BASE-002; RES-002; operational limits','OCF profile','S25/S26/S27/S28; historical path/collision and property tests','R5/R8'),
      ('Inherited whole-publication EPUB failure and warning/tool-error distinction','BASE-002','Draft §5; attribution 0.1.2','S29; all 107 whole packages; adapter timeout/crash tests','not reader evidence'),
      ('No network/filesystem/device/cookie/storage authority; host-owned state separate','RS-001','READING_SYSTEM_SECURITY.md','Package evidence cannot prove runtime behavior','R1/R2/R3'),
      ('Unverified generic/SEALED/fixed view, authentication distinction, no source sanitization','BASE-004; RS-002','Draft §§6–7; reader security','Read-only validators; historical SEALED/stale/fixed fixtures; UI NOT_TESTED','R4/R8'),
    ]
    coverage='# Security coverage\n\nEvery row separates executable package evidence from reader/manual obligations. No claim of exhaustive exploit resistance is made. Full native fixture expectations are enforced by A tests/corpus.rs and B tests/test_convergence.py.\n\n| Policy | Normative rule (SPD prefix) | Profile | Fixture/test evidence | Reader scenario | A implementation | B implementation |\n|---|---|---|---|---|---|---|\n'
    for topic,ids,profile,fixtures,reader in groups:
        a='src/package.rs' if topic.startswith('ZIP') else 'src/epubcheck.rs + policy.rs' if topic.startswith('Inherited') else 'src/passive.rs + module tests'
        b='package.py' if topic.startswith('ZIP') else 'epubcheck.py + policy.py + adapter tests' if topic.startswith('Inherited') else 'passive.py + test_passive.py'
        if topic.startswith(('No network/','Unverified')):a=b='processor plan; no automatic reader PASS'
        coverage+=f'| {topic} | {ids} | {profile} | {fixtures} | {reader} | {a} | {b} |\n'
    coverage+='\nPASS-001 and PASS-002 combine deterministic syntax with processor/semantic-label judgments; PASS-003 additionally requires human static completeness. RS-001/002 are processor conformance. All five remain explicitly NOT_TESTED for their unevaluated portions. No new universal implementation ceiling was introduced. Fonts/images/media and declarative renderers still require hardened decoders; package checks do not prove them safe.\n'
    write('SECURITY_COVERAGE.md',coverage)
    write('NEW_SPEC_BLOCKERS.md','''# New specification blockers

No NEW_SPEC_BLOCKER was identified. No prohibited construct was found mandatory for the pinned EPUB profile, and no semantic/revision/mapping rule was changed to obtain convergence.

The corrected MathML fixture was an authoring defect, the OPF-title attribution was a validator-contract defect, and the escaped-import discrepancy is an EPUBCheck implementation limitation on an intentionally invalid fixture. None changes the approved packaging architecture. Reader scenarios and human static completeness remain unevaluated and are not mislabeled blockers or PASS results.
''')
    sys_path=ROOT/'validator-b'
    import sys
    sys.path.insert(0,str(sys_path))
    from spd_validator_b.coverage import build_coverage
    (OUT/'validator-b-requirement-coverage.json').write_bytes(encoded(build_coverage(ROOT/'spec/requirements.yaml')))
    (OUT/'validator-a-requirement-coverage.json').write_bytes((ROOT/'validator-a/requirements-coverage.json').read_bytes())
    # Copy only the result schema, not canonical package schemas.
    schema=json.loads((ROOT/'validation/conformance-result-0.1.1.schema.json').read_text())
    schema['$id']=schema.get('$id','').replace('0.1.1','0.1.2')
    (ROOT/'validation/conformance-result-0.1.2.schema.json').write_bytes(encoded(schema))
    print('Prepared architecture, changes, pinning, coverage and blocker reports')

def encoded(data):return (json.dumps(data,indent=2)+'\n').encode()
if __name__=='__main__':main()
