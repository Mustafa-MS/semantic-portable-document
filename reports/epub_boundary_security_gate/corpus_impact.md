# Corpus impact and evidence retention

The authoritative enumeration is [tests/corpus-manifest.json](../../tests/corpus-manifest.json): **70 fixtures = 18 valid + 39 invalid + 13 edge**. All 70 package hashes and all 70 expectation hashes were checked against that manifest during this audit; all matched. The two frozen normalized result arrays also matched exactly. No package, expected result, oracle or corpus script was changed.

## Exact current observations

- **40 Base PASS, 30 Base FAIL.** “invalid” is a fixture category, not always a Base failure: Mapping-only negatives can have Base PASS.
- **62 EPUBCheck PASS, 8 FAIL per validator**, with 70 completed executions each; no newly executed EPUBCheck runs in this audit.
- **70/70** packages contain the EPUB marker, and **70/70** inventory it with `affects: []`.
- A targeted read-only scan of all markup/style resources found no current form/input/button/audio/video/canvas/iframe/object/embed/foreignObject/base/animate/set, @import or animation/transition declaration matches. This bounded scan helps estimate migration; it is not a complete passive-security validator. Existing intentional scripts/event handlers and remote-resource negatives remain.
- All **70 semantic test intents remain reusable** under B-min. New byte-level execution evidence is still required after conversion.

The manifest's primaryRequirements hints are not the complete oracle; e.g. its stale-fixed hint retains STATE-001 while the converged failure is STATE-007. This audit uses [the reviewed result surface](../../validator-convergence/fixture-matrix.md), not stale hints, when describing convergence.

## Delta definitions and counts

“Unchanged” below means exact package bytes, not merely unchanged semantic source. Counts describe the specified plan and do not include the separate pre-existing stable-identifier migration.

| Scenario | Current package fixtures unchanged | Modified | Replaced | Allocation unresolved | New proposed package fixtures | Existing fixtures requiring rerun |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A, boundary only | 70 | 0 | 0 | 0 | 0 | 0 newly required by boundary decision |
| A plus specified passive/completeness clarification | 70 planned | 0 planned | 0 | 0 | 30 | 70 |
| B retaining all current bytes and only dropping EPUB obligation | 70 | 0 | 0 | 0 | Depends on chosen exceptions | 70 for new conformance claim |
| B-min, changed internal identity marker | 0 | 70 | 0 | 0 | 38 = 30 shared + 8 B | 70 |
| C, distinct serialization | 0 certified | 0 assigned | 0 assigned | 70 conversion/replacement decisions | 42 named planning cases; final suite open | 70 |

A's 70 unchanged plan follows the reviewed content and preserves existing negative fixtures; no new rule requires a warning page or profile field in every package. Exact future expected finding sets remain subject to the revised attribution policy and actual reruns. “0 modified planned” is not a claim that new validator versions have already reproduced the oracle.

C has no defined binary/publication schema, so reporting exactly how many of its 70 cases are “modified” versus “replaced” would invent a design. All 70 are allocated explicitly to unresolved conversion/replacement; none is counted twice. The same 70 semantic scenarios can be retained even if every envelope is replaced.

## Why the marker change affects bindings but not semantic algorithms

For B-min, update each coherent source package's marker, its inventory record (length/hash and media type if needed), exact inventory digest and lifecycle descriptor digest. Because `mimetype` has `affects: []` in all 70, that change alone does **not** change semanticStateDigest, renditionInputDigest, Revision ID or the actual XHTML/fixed/mapping bytes. It does change full package bytes and the state-to-inventory binding. Do not silently preserve a prior seal as though no bound resource changed.

Regenerate valid baselines, then reapply each negative's deliberate mutation. Blindly recomputing every bad hash, bad state or stale mapping in-place would destroy negative tests. Preserve duplicate ZIP entries, missing/conflicting discovery, stale fixed cases and malformed content intentionally. The two missing/conflicting discovery cases still require UNKNOWN/blocked facts. The SEALED/currentness algorithms remain unchanged.

## Every existing fixture

A column: proposed package bytes retained. B-min column: envelope/marker and binding migration; test intent retained. C column: adapter/serialization conversion or replacement unresolved for every existing envelope. E marks current whole-file EPUBCheck FAIL; all others PASS.

| Fixture | A bytes | B-min bytes | C envelope | Current EPUBCheck |
| --- | --- | --- | --- | --- |
| edge/cjk-vertical | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/combining-character-range | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/css-change-stales-fixed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/deep-lists | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/emoji-range | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/empty-section | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/font-change-stales-fixed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/node-not-visible | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/partial-mapping | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/rtl-range | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/table-spanning-pages | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/unsupported-mapping | unchanged | modified; intent retained | convert/replace TBD | PASS |
| edge/very-long-paragraph | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/bad-resource-hash | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/capability-status-not-user-controlled | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/cross-spine-duplicate-node-id | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/descriptor-discovery-conflict | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/descriptor-discovery-missing | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/duplicate-node-id | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/duplicate-normalized-path | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/event-handler | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/external-required-css | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/external-required-font | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/external-required-image | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/invalid-table-semantics | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/invalid-xhtml | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/javascript | unchanged | modified; intent retained | convert/replace TBD | FAIL |
| invalid/mapping-invalid-geometry | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mapping-invalid-page | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mapping-invalid-range | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mapping-with-stale-fixed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mapping-wrong-rendition | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mapping-wrong-revision | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/missing-document-id | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/missing-revision-id | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/missing-root-direction | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/missing-root-language | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/multiple-rootfiles | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mutation-asset | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mutation-css | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mutation-fixed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mutation-mapping | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/mutation-semantic | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/not-visible-reason | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/partial-mapping-reason | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/path-traversal | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/sealed-after-annotation-modification | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/sealed-after-semantic-modification | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/stale-fixed-rendition | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/unlisted-non-normative-resource | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/unlisted-normative-resource | unchanged | modified; intent retained | convert/replace TBD | PASS |
| invalid/visual-order-arabic-source | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/accessible | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/annotations | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/arabic | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/figure-svg | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/fixed-without-mapping | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/lineage-scoped-annotation | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/mapped | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/mapping-with-current-fixed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/mathml | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/minimal-base | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/mixed-bidi | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/multi-spine | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/revision-scoped-annotation | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/same-semantic-different-revision-id | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/sealed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/semantic-change-new-revision | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/semantic-only-sealed | unchanged | modified; intent retained | convert/replace TBD | PASS |
| valid/table | unchanged | modified; intent retained | convert/replace TBD | PASS |

## Exact external-result sensitivity

These eight whole-EPUB failures remain historical evidence. Under B, their content/path predicates must be covered by retained native/imported rules; marker failure on every converted input must not drown out them or be treated as a new semantic defect.

| Fixture | Current codes | Current external SPD attribution |
| --- | --- | --- |
| invalid/duplicate-node-id | RSC-005 | SPD-ID-006 |
| invalid/duplicate-normalized-path | OPF-060, OPF-074 | SPD-BASE-002 |
| invalid/event-handler | OPF-014, RSC-005 | SPD-ID-006 |
| invalid/external-required-css | RSC-006 | SPD-SEC-005 |
| invalid/external-required-font | OPF-014, RSC-008 | SPD-SEC-004 |
| invalid/external-required-image | OPF-014, RSC-006 | SPD-SEC-006 |
| invalid/invalid-xhtml | RSC-005, RSC-016 | SPD-SEM-002 |
| invalid/javascript | OPF-014 | none; native script check fails |

The other **62** EPUBCheck successes remain facts about original EPUB bytes. They do not become B-source conformance results. Seven cases have mapped external IDs, six unique IDs in total. All 70 acceptance/rejection intents can be retained if B-min faithfully incorporates the same relevant content/package predicates. That is a migration target, not an executed result.

## Thirty shared proposed package fixtures

The following list is exactly **30 proposed fixtures**. It is a targeted addition plan, not an assertion of exhaustive adversarial coverage. Multi-trigger cases are explicitly noted; implementation tests should also isolate predicates where attribution could otherwise be ambiguous. These labels are not committed corpus IDs.

| Label | Concrete proposed fixture | Requirement/policy target | Expected classification or observation |
| --- | --- | --- | --- |
| S01 | Optional/decorative remote image | SEC-003/006 | FAIL: optional status does not authorize fetch |
| S02 | Escaped remote CSS @import | SEC-003/005 | FAIL after tokenization |
| S03 | Remote url() in inline style | SEC-003/005/006 | FAIL; same policy as stylesheet files |
| S04 | Remote URL through a custom property | SEC-003/005/006 | FAIL at resource use; do not prohibit custom properties generally |
| S05 | Standalone SVG remote image/filter reference | SEC-007 | FAIL |
| S06 | Inline SVG foreignObject | SEC-007, P2 | FAIL in every embedding context |
| S07 | Namespace-prefixed SVG script | SEC-001/007 | FAIL after namespace-aware parsing |
| S08 | Character-reference/escaped executable hyperlink | SEC-001, P4 | FAIL after URL interpretation |
| S09 | iframe srcdoc | SEC-002, P2 | FAIL |
| S10 | object/embed dispatch | SEC-002, P2 | FAIL; exercise both embedding routes in one package |
| S11 | Form submission/associated submit control | P2 | FAIL in Base; future Forms behavior deferred |
| S12 | meta refresh navigation | SEC-003, P2 | FAIL |
| S13 | HTML base and xml:base overrides | P2, B4 if applicable | FAIL under proposed one-base policy |
| S14 | Remote hints and hyperlink tracking declarations | SEC-003, P4 | FAIL for prefetch/preconnect/ping declarations in one package |
| S15 | Local CSS import, local image and packaged font | SEC-004/005/006/008 | PASS if inventoried and otherwise conforming |
| S16 | Local CSS import cycle | SEC-008 / existing CSS profile | FAIL terminating-import rule |
| S17 | Static local SVG symbols/gradients/clips/masks | SEC-007/008 | PASS with safe terminating references |
| S18 | Inert labeled preserved controls | P2 | PASS; functional form behavior absent |
| S19 | Local media without autoplay, with semantic alternatives | P2/P3 | PASS; playback needs R6 user-action observation |
| S20 | Local media autoplay | P3 | FAIL |
| S21 | Optional CSS/SVG time-dependent declarations with complete static state | P3 | File allowed under proposed retention policy; Base runtime suppression tested in R6 |
| S22 | Static MathML with local glyph resource and mediated link | SEC-008, SEM-009, P4 | PASS within inherited MathML rules; no active input |
| S23 | MathML remote mglyph resource | SEC-003/006/008 | FAIL |
| S24 | Hostile-looking annotation/metadata text retained as inert data | P1/P4 | No code execution or automatic context fetch; file result depends on valid data structure, runtime R8 |
| S25 | ZIP symlink/device entry modes | BASE-002 | FAIL; exercise both mode classes in one package |
| S26 | Percent-decoded/NFC entry-name collision | BASE-002, RES-002 | FAIL; extends raw-NFC collision case |
| S27 | Overlapping entries/inconsistent local-central header bounds | BASE-002 / proposed explicit package clarification | Reject unsafe/malformed input; exact operational-versus-conformance attribution must be specified |
| S28 | Expansion bomb/false declared size | Existing resource-limit policy | Bounded RESOURCE_LIMIT or MALFORMED_INPUT as applicable, not a new universal format maximum |
| S29 | Unmapped EPUB error: missing required OPF title | BASE-002 | Must not yield unconditional Base PASS solely because the tool code is unmapped |
| S30 | Inert HTML script data block | SEC-001 | FAIL under uniform script-element prohibition; no claim it executes |

## Eight additional B fixtures

| Label | Independent-package case | Purpose |
| --- | --- | --- |
| B-T1 | Wrong independent internal marker | Reject identity mismatch without calling it an EPUB-source error |
| B-T2 | Missing independent marker | Exercise B1 detection rule |
| B-T3 | OPF version/namespace mismatch in B package | Prove incorporated grammar validation |
| B-T4 | Foreign resource requiring a missing fallback | Prove retained resource contract |
| B-T5 | Broken navigation target/spine relationship | Prove complete-publication relationships, not standalone XML only |
| B-T6 | Safe nested-directory URL resolution | Positive imported base/relative reference behavior |
| B-T7 | Accessible claim with missing required publication metadata | Verify B applicability mapping and manual status |
| B-T8 | B-to-EPUB conversion with bound SEALED resources | Export checker validates derivative; no silent transfer of verification claims |

C adds four further named planning cases: **C-T1** independent container structure/identity, **C-T2** independent manifest completeness, **C-T3** independent reading order/navigation binding, **C-T4** independent resource-addressing and EPUB export mapping. Together with the common 30 and B's eight responsibility cases these give **42 planning cases**; the final C fixtures cannot be specified without its architecture.

## Reader and operational evidence are separate

Eight runtime scenarios R1–R8 are specified in [reader security](reader_security_model.md). They are **not** included in the package-fixture counts and are not replaced by schema/EPUBCheck success. Expansion/decode timeouts require controlled operational harnesses, not simply a new normative maximum.

| Evidence | A | B-min | C |
| --- | --- | --- | --- |
| Historical 70 A/B/oracle agreement | Still valid unchanged for frozen inputs | Still valid historical model/input evidence | Still valid historical model/input evidence |
| Same algorithm vectors for IDs/digests/ranges/mapping | Retain | Retain; adapt package inputs | Retain; adapt package inputs |
| New-version whole-file conformance | Rerun after clarifications | Rerun all 70 after conversion | Rerun all 70 after serialization design |
| EPUBCheck 5.3.0 on original 70 | Retain | Obsolete as direct certification of B sources; useful for originals/exports | Obsolete as direct C certification |
| Historical epub.js/Foliate JS/calibre readability | Retain within tested scope | Does not establish opening B files; rerun acceptance/export tests | Does not establish opening C files |
| SEALED generic-reader verification | Never established | Never established | Never established |

No semantic/integrity/mapping evidence is discarded solely because the packaging label changes. Conversely no old full-package result is relabeled as evidence for bytes that were never validated.

