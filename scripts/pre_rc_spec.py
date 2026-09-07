"""Apply the approved Option A clarification without changing semantic algorithms."""
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'spec'
OUT = ROOT / 'reports/pre_rc_passive_security'

CHANGES = {
 'SPD-BASE-001': 'A Format 0.1 Base document uses the EPUB-Compatible Packaging Profile 0.1 and SHALL satisfy applicable container/publication requirements of EPUB 3.3 Recommendation 13 January 2026 except where SPD explicitly imposes a stricter rule.',
 'SPD-BASE-002': 'Whole-publication EPUB conformance is required under the pinned baseline. Every completed EPUBCheck 5.3.0 conformance error or fatal error fails this requirement; specific diagnostic attribution is additive. Warnings alone do not fail it, and tool failure is NOT_TESTED rather than document failure.',
 'SPD-BASE-004': 'A processor MUST distinguish generic semantic compatibility/readability from SPD lifecycle, currentness, integrity, fixed-rendition, Mapping, authentication and transaction verification. Semantic XHTML remains authoritative even in SEALED documents; ordinary EPUB readers are not SPD processors.',
 'SPD-SEC-001': 'Base MUST NOT contain or depend on executable document code, executable macros, script elements (including inert data blocks), event-handler attributes, executable URLs or document-supplied code paths.',
 'SPD-SEC-002': 'Base MUST NOT contain active embedded/application contexts: iframe including srcdoc, object, embed, plugin execution, service-worker dependencies or document-created executable browsing contexts. Host-owned rendering frames are outside document content.',
 'SPD-SEC-003': 'Base MUST NOT initiate automatic publication-originated network access or navigation, including fetching, speculative loading, remote preload, prefetch, DNS preconnect, ping and automatic link checking. Explicit host-mediated user hyperlinks are separate.',
 'SPD-SEC-004': 'Every automatically loaded font MUST be inventoried and package-local, including optional fonts. Remote font fetching is prohibited; authoritative fonts MUST NOT depend on uncontrolled local() substitution.',
 'SPD-SEC-005': 'Every automatically loaded stylesheet or import MUST be inventoried and package-local, including optional and fallback styling. Remote stylesheet loading is prohibited.',
 'SPD-SEC-006': 'Every automatically loaded image or other visual/media resource MUST be inventoried and package-local, including decorative, optional, cursor, mask, filter, tracking and non-authoritative resources.',
 'SPD-SEC-007': 'All SVG contexts, including inline, standalone, image and nested resources, MUST exclude script, events, foreignObject, executable URLs, automatic remote dependencies and active behavior; ordinary static graphics and safe terminating local references remain allowed.',
 'SPD-SEC-008': 'Every automatically resolved rendered dependency MUST transitively terminate in verified inventoried package-local resources or valid local fragments. XHTML, CSS, SVG, MathML and nested embedding modes use the same containment policy; import and resource-expansion cycles are prohibited.',
}
NEW = [
 ('SPD-PASS-001', 'content-and-processor', 'PARTIALLY_AUTOMATED', 'SPD Base content is untrusted passive document data and SHALL NOT supply executable application behavior. A Base processor SHALL NOT execute document-supplied code or grant publication-originated application authority.'),
 ('SPD-PASS-002', 'content', 'PARTIALLY_AUTOMATED', 'Base SHALL obey the normative inert-control/embedded-context profiles: no forms, active contexts, automatic navigation, base overrides or authoritative interactive canvas; preserved controls SHALL be disabled, labeled inert representations without capture, form association, submission or activation behavior.'),
 ('SPD-PASS-003', 'content-and-processor', 'PARTIALLY_AUTOMATED', 'Base meaning SHALL be complete in a stable static presentation without animation, transitions, autoplay or interactive state changes. Processors SHALL suppress their execution. Local media MAY play only after user action with equivalent accessible semantics available without playback.'),
 ('SPD-RS-001', 'processor', 'MANUAL', 'An SPD reader SHALL deny publication-originated network, filesystem, camera, microphone, location, shared-cookie, persistent Web storage and service-worker authority. External HTTP/HTTPS hyperlinks require intentional user action and host mediation without destination access to the document context.'),
 ('SPD-RS-002', 'processor', 'MANUAL', 'An SPD processor SHALL distinguish displayed semantic content, declared SEALED, verified SEALED/current state and verified current fixed rendition. Unverified views MUST NOT be represented as verified sealed/fixed or authenticated; hash integrity is not signer or issuer authentication.'),
]

def write(path, text):
    path.write_text(text.rstrip() + '\n', encoding='utf-8')

def main():
    assert (OUT / 'BASELINE_FREEZE.md').exists()
    path = SPEC / 'requirements.yaml'
    raw = path.read_text(encoding='utf-8')
    old = yaml.safe_load(raw)
    assert len(old['requirements']) == 113
    for rid, wording in CHANGES.items():
        raw, count = re.subn(r'(?m)^(.*id: ' + rid + r',.*requirement: )"[^"]*"', lambda m: m[1] + json.dumps(wording), raw)
        assert count == 1, rid
    raw += '\n  # Pre-RC passive and processor obligations; package PASS never certifies reader behavior.\n'
    for rid, subject, automation, wording in NEW:
        raw += f'  - {{id: {rid}, section: 7, level: SHALL, capability: [Base], subject: {subject}, requirement: {json.dumps(wording)}, testability: {automation}, testType: SECURITY}}\n'
    write(path, raw)
    draft = (SPEC / 'FORMAT_0.1_DRAFT.md').read_text(encoding='utf-8')
    draft = draft.replace('Draft specification — clarified and frozen for validator implementation', 'Draft specification — pre-RC passive security clarification; not RC1')
    draft = draft.replace('The normative baseline is EPUB 3.3 OCF-compatible packaging,', 'The normative baseline is the EPUB 3.3 Recommendation of 13 January 2026,')
    draft = draft.replace('A Format 0.1 document MUST be an EPUB 3.3 OCF-compatible ZIP package and MUST satisfy the inherited OCF rules plus the stricter OCF profile.', CHANGES['SPD-BASE-001'] + '\n\n' + CHANGES['SPD-BASE-002'] + '\n\nSPD does not define a new ZIP dialect.')
    start = draft.index('# 6. EPUB Compatibility')
    end = draft.index('# 8. Authoritative Semantic Rendition')
    draft = draft[:start] + '''# 6. EPUB Compatibility and Verification

The 0.1 packaging/publication profile is a strict conforming subset of the pinned EPUB 3.3 baseline, allowing generic EPUB semantic fallback where a reading system supports the publication's otherwise-used content technologies. Universal reader compatibility is not claimed.

Semantic XHTML remains authoritative in EDITABLE and SEALED revisions, including when a current fixed rendition exists. Generic rendering establishes only semantic compatibility/readability where supported. It does not establish SPD lifecycle, currentness, integrity, fixed-rendition, Mapping, authentication or transaction verification (SPD-BASE-004).

An ordinary EPUB reader is not an SPD processor and cannot be required to display SPD verification UI. An SPD-aware processor MUST distinguish displayed semantic content, declared SEALED state, verified SEALED/current state, and verified current fixed rendition. It MUST NOT describe an unverified generic semantic view as verified sealed, verified fixed or authenticated. Hash integrity is not signer/issuer authentication (SPD-RS-002). Signatures remain deferred.

Sensitive workflows MAY use an SPD-aware viewer or an explicitly identified derivative EPUB reading copy. This is workflow guidance, not a new lifecycle state. No embedded warning is required and no warning may be silently retrofitted into an existing SEALED package.

The internal EPUB `mimetype` marker remains `application/epub+zip`. It is separate from external HTTP Content-Type, OS filename extension and a future SPD-specific association. No SPD-specific MIME type or mandatory extension is assigned. Safe SPD detection MUST verify internal discovery/state metadata using section 69; a filename suffix is not evidence of SPD identity or verification.

---

# 7. Passive Content and Reader Security Profile

The following layers form one Format 0.1 conformance bundle:

```text
SPD DOCUMENT MODEL
    ↓
SPD PASSIVE CONTENT PROFILE
    ↓
SPD EPUB-COMPATIBLE PACKAGING PROFILE 0.1
    ↓
EPUB 3.3 Recommendation 13 January 2026
```

SPD is a distinct semantic portable-document model whose Format 0.1 packaging/publication profile is a strict conforming subset of that dated EPUB baseline. Its identity, revision, lifecycle and mapping model is not reduced to packaging.

''' + '\n\n'.join(f'**{rid}.** {wording}' for rid, wording in CHANGES.items() if rid.startswith('SPD-SEC-')) + '\n\n' + '\n\n'.join(f'**{rid}.** {wording}' for rid, _, _, wording in NEW) + '''

Detailed technology restrictions in [XHTML](profiles/xhtml-profile.md), [CSS](profiles/css-profile.md), [SVG](profiles/svg-profile.md), [MathML](profiles/mathml-profile.md) and [resource resolution](profiles/passive-resource-profile.md) are normative. These profiles restrict capabilities of existing languages rather than defining replacement languages.

Document conformance constrains file constructs. SPD reading-system conformance constrains processor authority and verification representations. Implementation hardening sets operational budgets; no universal DOM, pixel, font, memory or timeout limit is introduced. [Reading-system security](READING_SYSTEM_SECURITY.md) separates these layers. Package validators report untested human/processor portions honestly; package PASS does not establish reader or complete static-meaning conformance.

Validators MUST use namespace-aware XML/SVG parsing and standards-aware CSS tokens/structure for normative resource decisions, including escapes, comments, inline styles, nested rules/functions and custom properties at resource use. Regex may optimize detection but MUST NOT be the authoritative security parser. Validation SHALL parse, inspect and report without rewriting source. A reader/validator MUST NOT sanitize a SEALED source and present the modified result as still verified; a repair workflow requires a new revision under existing rules.

Format 0.1 prohibits document-originated executable behavior and automatic external-resource authority in Base. Reader implementations remain responsible for safely processing hostile declarative content; passive conformance is not proof against exploits or a comparative safety claim.

---

''' + draft[end:]
    marker = '# 5. Package and Authoritative Package Document'
    draft = draft.replace(marker, 'The normative dependency and update policy is [UPSTREAM_DEPENDENCY_BASELINE_0.1.md](UPSTREAM_DEPENDENCY_BASELINE_0.1.md). EPUB Reading Systems 3.3 (17 October 2024) is incorporated only for explicitly relied-on processing behavior; publication conformance does not import every reading-system recommendation. Future EPUB or living-spec changes require an explicit SPD maintenance decision.\n\n' + marker)
    write(SPEC / 'FORMAT_0.1_DRAFT.md', draft)
    xhtml = (SPEC / 'profiles/xhtml-profile.md').read_text(encoding='utf-8')
    a, b = xhtml.index('## Prohibited for security'), xhtml.index('## Unsupported is not prohibited')
    xhtml = xhtml[:a] + '''## Normative passive restrictions (SEC-001–008; PASS-001–003)

Prohibited: every `script` including data blocks; event-handler attributes; executable URLs; `iframe` including `srcdoc`; `object`; `embed`; plugins; service-worker dependencies; `form`; authoritative interactive `canvas`; meta refresh; automatic redirects/navigation; `base` and `xml:base` resolution overrides; external embedded browsing contexts. A host's own rendering frame is outside document content.

`input` MAY preserve an inert semantic value only when disabled, accessibly labeled, with its value available, no password/file capture, form association, submission attributes or activation behavior. `button` MAY be preserved only disabled, labeled and without form submission/association, command, popover or activation behavior. Functional forms and interactive drawing are deferred; no new capability is defined here. Label correctness and completeness require human evaluation.

Packaged `audio`, `video`, `poster` and `track` resources MAY be used where EPUB permits. Autoplay is prohibited. Playback requires explicit user action; meaning necessary to understand the document MUST be accessibly available without relying solely on playback. All sources, posters, tracks, srcset candidates, styles and nested dependencies obey the [passive resolver](passive-resource-profile.md).

Explicit HTTP/HTTPS hyperlinks MAY be activated through host mediation. Validators MUST NOT visit them. Ping, prefetch, DNS prefetch/preconnect and remote preload declarations are prohibited. Namespace/vocabulary IRIs are identifiers, not fetch instructions. Inline SVG, MathML and annotation-xml content inherit the same passive restrictions.

''' + xhtml[b:]
    write(SPEC / 'profiles/xhtml-profile.md', xhtml)
    css = (SPEC / 'profiles/css-profile.md').read_text(encoding='utf-8').replace('any required remote URL', 'any automatically consumed remote URL').replace('and other required resources', 'and all other automatic resources, including optional/decorative resources').replace('Local `@import` is discouraged and must be inventoried and cycle-safe.', 'Local `@import` is allowed when inventoried and acyclic.')
    css += '''
## Passive resource and static presentation obligations

Every resource-consuming `url()` and string URL (including `@import`, font `src()` and image-set image strings) MUST use the passive package resolver. Package-local resources and valid fragments are allowed; network, executable, file, UNC, data/blob and package-escape resources are prohibited. This includes inline style elements/attributes, nested rules, imports, fonts, cursors, masks, filters and optional decorations. Font `local()` MUST NOT substitute an unbound authoritative font; package font resources instead.

Custom properties remain allowed. A token containing a resource reference remains subject to the resource policy, including when stored in a custom property or used through substitution. String-only values that do not consume a resource are inert. Dynamic string-to-URL consumers whose package locality cannot be established MUST be reported NOT_TESTED, never silently accepted. Validators inspect grammar tokens, decoded escapes and nested functions; comments and escaping cannot bypass checks.

Complex selectors, transforms and static filters are allowed. CSS-generated text MAY provide decoration/numbering but MUST NOT be the only source of primary semantic content, alternative text or table data. Animation, transitions and time-dependent declarations MAY remain only with a complete meaningful static state; their execution SHALL be suppressed in Base. Semantic completeness is PARTIALLY_AUTOMATED and requires human review, including for generated/hidden content. Existing stable-snapshot requirements for SEALED fixed rendering are unchanged.
'''
    write(SPEC / 'profiles/css-profile.md', css)
    svg = (SPEC / 'profiles/svg-profile.md').read_text(encoding='utf-8')
    svg += '''
## Uniform embedding and resolution

These normative rules apply to namespace-aware standalone SVG, inline SVG, SVG used as images, nested/referenced SVG and SVG embedded in other supported content, including fonts. Scripts (even data blocks), events, foreignObject, executable URLs, automatic remote dependencies and active document behavior are prohibited in every context. All href/xlink:href, paint, style, mask/filter, image and font references obey the transitive passive resolver. Safe terminating cross-file package references are allowed; valid local fragments must exist. Geometry, shapes, text, gradients, clipping, masks, transforms and symbols are retained.

Optional animation declarations require complete static meaning and suppressed Base execution (PASS-003). This profile reuses SVG processing concepts but does not claim exact SVG Secure Static mode conformance, since its mediated hyperlinks and package-local cross-file references have an explicitly bounded policy.
'''
    write(SPEC / 'profiles/svg-profile.md', svg)
    write(SPEC / 'profiles/mathml-profile.md', '''# Normative MathML passive profile

Retain the EPUB-inherited MathML 3 second-edition authoring model: Presentation MathML and permitted semantic annotations/Content MathML placement. MathML Core is not a replacement authoring contract.

Apply SEC-001–008 and PASS-001–003 to href, mglyph/src resources, annotation-xml nested markup and maction. Static mathematics and semantic annotations remain allowed. Resources use the same package resolver; external hyperlinks require explicit host-mediated action. Embedded annotations are data, never an escape into executable HTML. Interactive maction state required for primary meaning is deferred; complete static meaning requires human assessment. Math depth/shaping limits are implementation hardening, not a new mathematics language.
''')
    write(SPEC / 'profiles/passive-resource-profile.md', '''# Normative passive resource-reference contract

SEC-008 applies to every automatic rendered dependency, including optional/decorative dependencies. The referring context determines whether a value is an identifier, user hyperlink or resource. Namespace/vocabulary IRIs and JSON annotation strings alone are identifiers/data, not requests.

Parse XML with namespaces, entity expansion limited to safe built-in/character references and no external entity/XInclude fetching. Parse CSS tokens with decoded escapes and preserved grammar context. A resource reference records source package path, language/context, role (stylesheet/font/image/media/other), interpreted URL, resolved entry/fragment and dependent resources. This is a shared contract, not shared implementation code.

Strip URL-leading/trailing ASCII whitespace and interpret embedded tab/newline characters according to URL parsing before scheme checks. Author-supplied executable schemes, file/drive/UNC paths, data/blob resource documents and package escapes are prohibited. HTTP/HTTPS are allowed only in explicit user hyperlink roles; no validator performs network resolution. Other application-launching schemes have no Base authority.

Resolve relative URLs against the containing resource path, decode percent escapes strictly once, preserve case, require unambiguous NFC entry identity, reject absolute/escape/backslash/ambiguous decoded paths and query-bearing package resources. Dot segments in references may resolve within the package; archive entry names themselves cannot contain them. A fragment-only reference uses the containing resource; a nonempty fragment MUST identify an existing target in its parsed XML document. Inventory and byte integrity verification apply to every resolved resource.

Inspect all inventoried renderable resources, including resources reached by CSS imports, SVG references and nested MathML/annotation markup. Resource expansion and CSS-import graphs MUST terminate without cycles; ordinary navigational hyperlink cycles are not resource cycles. A visited set prevents repeated work and an active dependency stack detects cycles. Implementation work limits yield RESOURCE_LIMIT, not invented format limits. Unsupported resource syntax whose locality cannot be established yields NOT_TESTED. No embedding mode may escape these rules.

Attribution: executable constructs → SEC-001; application contexts → SEC-002 and PASS-002; automatic external authority → SEC-003; font/stylesheet/visual resource failures additionally → SEC-004/005/006 by role; unsafe or missing resource closure → SEC-008. SVG defects additionally → SEC-007. Controls/base/navigation/canvas → PASS-002; autoplay → PASS-003. PASS-001 is a grouped principle whose document syntax evidence is supplied by SEC rows; reader execution is separately untested. Specific EPUB diagnostic IDs are additive to BASE-002 for completed EPUB conformance errors. Human static meaning and reader authority never receive automatic PASS.
''')
    rows = yaml.safe_load(raw)['requirements']
    matrix = '# Format 0.1 Draft conformance matrix\n\n118 requirements: 11 existing meanings clarified/strengthened, 5 new groups, 102 existing rows unchanged. Canonical schemas and semantic algorithms unchanged.\n\n| Requirement | Capability | Automation | Subject | Normative requirement |\n|---|---|---|---|---|\n'
    matrix += '\n'.join(f"| {r['id']} | {', '.join(r['capability'])} | {r['testability']} | {r['subject']} | {r['requirement']} |" for r in rows)
    write(SPEC / 'CONFORMANCE_MATRIX.md', matrix)
    change_rows = []
    for r in old['requirements']:
        if r['id'] not in CHANGES:
            continue
        rid = r['id']
        kind = 'VALIDATION-CLOSURE FIX' if rid == 'SPD-BASE-002' else 'CLARIFICATION' if rid.startswith('SPD-BASE') else 'STRICTER SUBSET'
        change_rows.append(f"| §{r['section']} | {rid} | {kind} | {r['requirement']} | {CHANGES[rid]} | Approved Option A; close inherited-publication/passive authority gap | Both validators; see SECURITY_COVERAGE.md fixture mapping |")
    for rid, _, _, wording in NEW:
        change_rows.append(f'| §7 | {rid} | PROCESSOR CONFORMANCE ADDITION' + (' / STRICTER SUBSET' if rid.startswith('SPD-PASS') else '') + f' | No grouped obligation | {wording} | Approved P1–P5 | Package syntax subsets plus reader scenarios/human review |')
    write(OUT / 'SPEC_CHANGELOG.md', '''# Normative change log

113 → 118 requirements; 11 existing modified, 5 added, 102 unchanged, none removed. Existing automation classifications unchanged; PASS groups PARTIALLY_AUTOMATED, RS groups MANUAL processor conformance. No schema change. No RC1 created.

| Draft section | Requirement | Classification | Old meaning | New meaning | Reason/consequence | Evidence/validators |
|---|---|---|---|---|---|---|
''' + '\n'.join(change_rows) + '''

UPSTREAM VERSION PIN: §§4–5 and dependency ledger pin EPUB, relied-on Reading Systems, Accessibility/WCAG and dependency maintenance policy. No Accessible capability change. Detailed XHTML/CSS/SVG/MathML/resolver clauses implement the SEC/PASS rows above, including transitive resources, inert controls, local media and static completeness; automated syntax does not certify semantic judgment.

Unchanged: document/revision/node identity, semanticStateDigest, renditionInputDigest, EDITABLE/SEALED lifecycle, Mapping, authoritative semantic XHTML, annotations, transactional editing, fixed-rendition abstraction, Accessible capability definition, Fixed-Experimental and Archive-Experimental status. No new MIME, extension, signature, container, Forms/Interactive capability or reader implementation.
''')
    print('Updated normative Draft, 118-row registry/matrix and profiles')

if __name__ == '__main__':
    main()
