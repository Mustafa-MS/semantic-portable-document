import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'

scenarios=[
 ('R1','No automatic publication-originated network', ['SPD-SEC-003','SPD-RS-001'], 'Observe DNS/HTTP/WebSocket and speculative traffic from before import through preview and reading; exercise CSS imports/fonts/SVG/media/ping/prefetch and annotation contexts. Zero external requests.'),
 ('R2','No filesystem, device or Web storage authority', ['SPD-RS-001'], 'Probe file/UNC/drive paths, camera, microphone, location, cookies, localStorage/IndexedDB and service workers. No document authority or permission prompt; host preferences remain separate.'),
 ('R3','Explicit external hyperlink mediation', ['SPD-RS-001'], 'Before activation, zero contact. After intentional activation, trusted host shows interpreted HTTP/HTTPS destination and opens isolated context without opener, credentials or package-data access.'),
 ('R4','Truthful SEALED and fixed verification', ['SPD-BASE-004','SPD-RS-002'], 'Evaluate declared SEALED/current fixed, stale fixed, semantic-only SEALED, failed and unsupported verification. Semantic display is not verified SEALED; stale/unverified fixed is not verified current; no hash-only authentication.'),
 ('R5','Bounded hostile declarative processing', ['SPD-RS-001'], 'Exercise ZIP/XML/DOM/CSS/SVG/MathML work budgets and cancel operations. RESOURCE_LIMIT and effective worker cancellation; no invented universal format maximum.'),
 ('R6','Complete static presentation and local media', ['SPD-PASS-002','SPD-PASS-003'], 'Animations/transitions/autoplay suppressed; controls inert and labeled; meaningful static state and accessible equivalents manually assessed; local playback only after user action.'),
 ('R7','Font/image/media decoder containment', ['SPD-RS-001'], 'Use malformed decoder inputs and nested SVG. Observe isolated failure and bounded work with no privilege escalation or fabricated successful content.'),
 ('R8','Untrusted annotations and stable source identity', ['SPD-PASS-001','SPD-RS-002'], 'Render hostile-looking annotations/metadata as data; no trusted UI injection or context fetch. Detect source mutation and ambiguous paths; no sanitized SEALED view represented as verified original.'),
]
dest=ROOT/'tests/reader-security';dest.mkdir(exist_ok=True)
data={'version':'0.1.2','scope':'PROCESSOR_CONFORMANCE_NOT_PACKAGE_FIXTURES','status':'NOT_TESTED','reason':'Reference reader not built in this task','scenarios':[{'id':i,'title':t,'requirements':r,'procedureAndExpectedObservation':p,'status':'NOT_TESTED','automation':'MANUAL_PROCESSOR_PLAN'} for i,t,r,p in scenarios]}
(dest/'scenarios.json').write_text(json.dumps(data,indent=2)+'\n')
text='# Reader security scenarios\n\nEight processor scenarios, NOT ordinary package-validator fixtures. All remain NOT_TESTED until a reader exists; package PASS supplies no runtime evidence.\n\n'+ '\n'.join(f'- **{i}: {t}.** {p}' for i,t,r,p in scenarios)+'\n'
(dest/'README.md').write_text(text)
(OUT/'READER_SECURITY_SCENARIOS.md').write_text(text+'\nMachine-readable source: tests/reader-security/scenarios.json. R1–R8 retain the approved audit groups; R2 explicitly covers all device/storage boundaries and R4 both generic and stale-fixed representations.\n')
threat=(ROOT/'reports/epub_boundary_security_gate/threat_model.md').read_text(encoding='utf-8')
(ROOT/'spec/THREAT_MODEL.md').write_text('# Maintained SPD threat model\n\nMaintained baseline promoted from the approved architecture gate. Normative mitigation is now defined in Draft §7 and profiles; original audit observations below describe the **pre-clarification** implementation. Current testing evidence lives in reports/pre_rc_passive_security/SECURITY_COVERAGE.md. This document makes no exploit-proof or comparative PDF safety claim.\n\n'+threat.replace('../../spec/','').replace('../../validator-','../validator-'),encoding='utf-8')
with (ROOT/'spec/STANDARDS_TRACEABILITY.md').open('a',encoding='utf-8') as f:
    f.write('''\n## Pre-RC dated inheritance and passive profile

The normative edition/update policy is [UPSTREAM_DEPENDENCY_BASELINE_0.1.md](UPSTREAM_DEPENDENCY_BASELINE_0.1.md): EPUB 3.3 REC 2026-01-13; explicitly relied-on Reading Systems 3.3 REC 2024-10-17; EPUB Accessibility 1.1 REC 2024-10-17; WCAG 2.2 REC 2024-12-12, AA unchanged. Living HTML/URL and transitive CSS/SVG/MathML references are governed by explicit maintenance review, never silent future adoption. EPUB 3.4 remains monitored future work only.

SEC-001–008 and PASS-001–003 restrict capabilities of EPUB XHTML, CSS, SVG and MathML without replacing their languages. See the normative profiles and shared passive resource-reference contract. RS-001–002 add processor authority/verification obligations; document validation does not certify them. Passive restrictions do not prove Accessible conformance; equivalent labels, values and semantic alternatives require the existing human evaluation.
''')
with (ROOT/'spec/profiles/accessibility-profile.md').open('a',encoding='utf-8') as f:
    f.write('\nThe edition pins are EPUB Accessibility 1.1 REC 17 October 2024 and WCAG 2.2 REC 12 December 2024, AA. Accessible capability meaning and human evaluation are unchanged. Passive controls/media must preserve accessible labels, values and alternatives; the passive profile alone never establishes Accessible conformance.\n')
with (ROOT/'spec/profiles/ocf-profile.md').open('a',encoding='utf-8') as f:
    f.write('\nBASE-001/002 incorporate the complete EPUB 3.3 publication/container requirements from REC 13 January 2026, not only ZIP syntax. The internal application/epub+zip marker remains unchanged. Symlink/device entries, ambiguous decoded/NFC identities and inconsistent/overlapping ZIP entry bounds are rejected; malformed decoding is operational MALFORMED_INPUT, while proven profile defects fail BASE-002. Expansion ceilings are implementation RESOURCE_LIMIT, not universal format maxima.\n')
print('Reader plan and maintained documentation written')
