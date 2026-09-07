# Exact requirement impact matrix

Audit of all **113 unique rows** in [requirements.yaml](../../spec/requirements.yaml), SHA-256 `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`. There are **no SPD-PKG-* or SPD-OCF-* IDs**: package/OCF rules are under BASE and the profiles. Do not invent such IDs or count inherited EPUB clauses as if each already had a registry row.

The classification below is **B-min packaging-only** as defined in [standards reuse](standards_reuse_analysis.md). Common passive strengthening is a separate delta. “UNCHANGED” means the requirement text/contract can remain, not that migrated files or changed validators need no rerun. Dependency changes count even when most words and all semantic intent can remain.

## Classification counts

| Classification | Count among current 113 |
| --- | ---: |
| UNCHANGED | 103 |
| WORDING CHANGE ONLY | 1 |
| DEPENDENCY CHANGE | 6 |
| MUST BE RESTATED AS SPD-NATIVE | 3 |
| REMOVED | 0 |
| NEW REQUIREMENT NEEDED | 0 existing rows; 8 proposed additions listed separately |
| UNCERTAIN | 0 for the stated B-min scenario |
| Total current rows | 113 |

B's unchosen marker spelling does not prevent identifying its affected rule. The accessibility **schema representation** choice remains conditional, as explained separately; ACC-004's need for applicability restatement is not uncertain.

## Every current requirement

The original requirement text below is copied from the user-owned registry for review. It is not edited there. A “yes” in the A column identifies membership in the proposed common/pre-RC clarification package.

| ID | Draft § | Current requirement | B-min classification | Rationale | A clarification |
| --- | ---: | --- | --- | --- | --- |
| SPD-ARCH-001 | 3 | A conforming document has exactly one authoritative semantic representation. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-ARCH-002 | 3 | A fixed rendition is not an independently editable source of truth. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-ARCH-003 | 4 | Stable existing standards are reused where practical. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-BASE-001 | 5 | The document is an EPUB 3.3 OCF-compatible ZIP package. | MUST BE RESTATED AS SPD-NATIVE | Independent container identity replaces the EPUB/OCF-compatible package claim. | yes |
| SPD-BASE-002 | 5 | Applicable EPUB 3.3 OCF requirements apply unless this profile further restricts them. | MUST BE RESTATED AS SPD-NATIVE | Replace umbrella OCF/EPUB inheritance with an explicit incorporation and exception contract. | yes |
| SPD-BASE-003 | 5 | The format does not define a new ZIP dialect. | UNCHANGED | B-min still uses existing ZIP; changing a marker is not a new ZIP binary dialect. | — |
| SPD-BASE-004 | 6 | A processor does not assume an ordinary EPUB reader understands SPD lifecycle, identity, mapping, sealed-state, fixed-authority, or Agent API semantics. | UNCHANGED | The prohibition on assuming generic-reader SPD awareness remains true; B makes no generic compatibility promise. | yes |
| SPD-BASE-005 | 55 | A Base package includes navigation, an authoritative XHTML spine, identity metadata, inventory, offline required resources, semantic structure, logical text, and integrity digests. | DEPENDENCY CHANGE | Keep navigation and authoritative XHTML, but explicitly incorporate their publication rules. | — |
| SPD-BASE-006 | 5 | The OCF container contains exactly one rootfile package document, whose spine defines the authoritative semantic reading order. | DEPENDENCY CHANGE | Keep one rootfile and spine; bind the OCF-derived container to retained OPF semantics. | — |
| SPD-SEC-001 | 7 | Base does not require JavaScript or executable macros. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-002 | 7 | Base does not require plugins, service workers, iframes, or executable object content. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-003 | 7 | Base does not require automatic network access. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-004 | 7 | A font required for authoritative rendering is packaged and is not remote. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-005 | 7 | A stylesheet required for authoritative rendering is packaged and is not remote. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-006 | 7 | An image required for authoritative rendering is packaged and is not remote. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-007 | 7 | Base does not contain executable SVG content. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEC-008 | 7 | Every resource required to render the authoritative document is available within the package. | UNCHANGED | Same passive policy; packaging identity does not change this rule. Separate common strengthening is counted below. | yes |
| SPD-SEM-001 | 8 | Exactly one authoritative semantic rendition is identified. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-002 | 8 | The authoritative rendition consists of one or more ordered XHTML content documents. | DEPENDENCY CHANGE | Keep ordered XHTML; restate the applicability of the inherited EPUB XHTML content profile. | — |
| SPD-SEM-003 | 8 | The package spine defines primary reading order. | DEPENDENCY CHANGE | Keep the spine; explicitly incorporate its processing semantics outside EPUB publication conformance. | — |
| SPD-SEM-004 | 8 | Native HTML semantics are used where they exist. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-005 | 9 | Semantic XHTML is preferred to accessibility or custom metadata mechanisms. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-006 | 9 | ARIA does not replace correct native semantics. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-007 | 10 | Primary textual or structural content is not independently duplicated in another normative resource. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-008 | 10 | Supplemental structured data does not redefine authoritative textual content. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-009 | 18 | When semantic MathML exists, mathematical meaning is not required to be reconstructed from visual glyph positions. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-010 | 19 | Figure, caption, and reference relationships remain semantic. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-011 | 19 | Fixed coordinates do not define figure-caption-reference relationships. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-012 | 20 | Tables use semantic table structures. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-013 | 20 | Table header relationships are represented semantically rather than inferred only from visual position. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-SEM-014 | 21 | A supplemental relationship graph does not unnecessarily duplicate authoritative content. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-ID-001 | 11 | Every document has a persistent canonical lowercase RFC 9562 UUID URN Document ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-002 | 12 | Every committed semantic state has an opaque canonical lowercase RFC 9562 UUID URN Revision ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-003 | 12 | A change to normative semantic content creates a new Revision ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-004 | 12 | A change only to non-normative cache data does not create a new semantic Revision ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-005 | 13 | Every independently addressable semantic object carries a persistent Node ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-006 | 14 | Node IDs are unique in the current authoritative semantic revision. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-007 | 14 | Node IDs do not depend on page position, DOM path, visible numbering, or text content. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-008 | 14 | A content hash is not used as Node identity. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-009 | 15 | A copied node normally receives a new Node ID. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-010 | 20 | Addressable table cells have persistent Node IDs. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-011 | 15 | A conforming editor preserves Node identity according to lineage rules when supplied lineage history is available. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-012 | 15 | A conforming editor does not knowingly reuse a retired Node ID within supplied lineage history. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-ID-013 | 15 | A standalone validator reports history-dependent persistence and non-reuse checks as NOT_TESTED when lineage history is unavailable; absence of history does not fail Base. | UNCHANGED | Frozen persistent identity/revision/lineage semantics independent of publication inheritance. | — |
| SPD-I18N-001 | 16 | Semantic text is represented in logical Unicode order. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-I18N-002 | 16 | Visual placement does not determine semantic ordering. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-I18N-003 | 16 | The root authoritative XHTML html element has equivalent valid lang and xml:lang values. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-I18N-004 | 16 | The root authoritative XHTML html element explicitly declares dir ltr or rtl, and nested semantic elements declare direction when it differs from inherited direction. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-I18N-005 | 17 | A processor does not equate visual left-to-right position with logical reading order. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-I18N-006 | 17 | Mapping and editing APIs operate on logical text ranges. | UNCHANGED | Logical Unicode, language/direction and scalar-range behavior remain required. | — |
| SPD-ANN-001 | 23 | The StableNodeSelector vocabulary and namespace are registered before final 0.1 publication. | UNCHANGED | Frozen annotation scope/lifecycle/vocabulary requirement; no new selector model. | — |
| SPD-ANN-002 | 23 | A lineage-scoped StableNodeSelector contains Document ID and Node ID and omits Revision ID. | UNCHANGED | Frozen annotation scope/lifecycle/vocabulary requirement; no new selector model. | — |
| SPD-ANN-003 | 23 | A revision-scoped StableNodeSelector contains Document ID, Revision ID, and Node ID. | UNCHANGED | Frozen annotation scope/lifecycle/vocabulary requirement; no new selector model. | — |
| SPD-ANN-004 | 27 | Changing an in-package annotation does not create a semantic Revision ID but invalidates a sealed state whose inventory binds that annotation; external annotations evolve independently unless incorporated. | UNCHANGED | Frozen annotation scope/lifecycle/vocabulary requirement; no new selector model. | — |
| SPD-STATE-001 | 26 | A stale fixed rendition is not presented as the current authoritative fixed representation. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-002 | 27 | A sealed state binds the semantic Revision ID, normative inventory, any claimed fixed rendition, and any applicable mapping artifact. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-003 | 27 | Changing normative semantic content invalidates the sealed state. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-004 | 33 | A fixed rendition bound to a sealed revision is immutable for that revision. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-005 | 26 | A fixed rendition is current only when revision ID, renditionInputDigest, and resource digest match current verified state; otherwise it is stale. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-006 | 27 | A semantic-only revision may be SEALED; if fixed is present in SEALED it is current. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-STATE-007 | 56 | A Mapping claim requires a current fixed rendition and a bound mapping artifact; current fixed without Mapping is permitted. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-RES-001 | 28 | A document maintains exactly one normative resource inventory. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-RES-002 | 28 | Each inventory entry has a normalized NFC path, media type, byte length, SHA-256 digest, role, and explicit affects array. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-RES-003 | 28 | The inventory lists every ZIP entry including non-normative caches except the inventory itself and lifecycle state descriptor. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-RES-004 | 28 | Inventory digests cover the exact decompressed bytes returned for the named ZIP entry. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-RES-005 | 28 | Each resource explicitly declares whether it affects semantic state, rendering input, both, or neither; role alone is not effect classification. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-RES-006 | 28 | Any unlisted ZIP entry other than the two self-referential exceptions fails conformance. | UNCHANGED | Same ZIP resources, normalized paths, effects and exact-byte inventory contract in B-min. | — |
| SPD-INT-001 | 29 | The document provides digest-based integrity verification. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-INT-002 | 29 | SHA-256 is supported. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-INT-003 | 29 | Integrity detects modification of semantic content, normative styles/assets, mapping, fixed rendition, and state metadata when applicable. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-INT-004 | 29 | semanticStateDigest is computed by the normative UTF-8 inventory projection over resources whose affects contains semantic. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-INT-005 | 29 | renditionInputDigest is computed by the normative projection over resources affecting semantic or rendering; presentation-only change stales fixed without changing Revision ID. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-INT-006 | 29 | descriptorDigest is SHA-256 of RFC 8785 JCS state JSON with descriptorDigest omitted, producing a cycle-free digest graph. | UNCHANGED | Frozen integrity/currentness/lifecycle rule; changed bytes require rebinding, not a new algorithm. | — |
| SPD-FIX-001 | 31 | A fixed rendition identifies its source Revision ID and renditionInputDigest. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-FIX-002 | 32 | A Fixed capability claim is not interpreted as making PDF the permanent normative page model. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-FIX-003 | 46 | PDF/A-4 is not required for Base or ordinary Fixed conformance. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-MAP-001 | 34 | A processor claiming Mapping emits a mapping artifact during fixed rendering. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-002 | 34 | A mapping is bound to Document ID, Revision ID, and Fixed Rendition ID plus digest. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-003 | 35 | Backward reconstruction is not the required normative mapping-generation method. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-004 | 36 | A mapping does not contain glyph rendering, fonts, drawing operations, line-breaking, or page-layout instructions whose purpose is to recreate layout. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-005 | 38 | Mapping statuses enforce fragment and reason cardinalities for MAPPED, PARTIALLY_MAPPED, NOT_VISIBLE, UNMAPPABLE, and UNSUPPORTED. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-006 | 38 | A processor does not fabricate geometry to claim full coverage. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-007 | 39 | Each mapping record identifies generation mechanism or evidence class. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-008 | 40 | Mapping text ranges refer to semantic Unicode order. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-009 | 40 | Semantic text is not reordered to match page geometry. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-010 | 41 | Visual, mapping, fixed-text, and fixed-profile fidelity are not treated as interchangeable. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-011 | 56 | A Mapping claim includes valid page identifiers, status, provenance, logical ranges where used, and page-bounded geometry. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-MAP-012 | 36 | Mapping geometry uses finite page-local CSS reference pixels with top-left origin, x right, y down, TL-TR-BR-BL quads, and declared rendition-local page dimensions. | UNCHANGED | Frozen mapping/range/geometry semantics; package adapter changes do not change the predicate. | — |
| SPD-ACC-001 | 42 | Base accessibility is evaluated against the authoritative semantic XHTML rendition. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-ACC-002 | 43 | A standalone fixed export claiming accessibility independently satisfies the accessibility requirements of its fixed format. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-ACC-003 | 43 | Accessible XHTML is not used to claim that an independently distributed inaccessible PDF is accessible. | UNCHANGED | Semantic/accessibility authority remains XHTML; no packaging-specific change to this predicate. | — |
| SPD-ACC-004 | 58 | An SPD Accessible 0.1 claim satisfies EPUB Accessibility 1.1 and WCAG 2.2 Level AA, including applicable human evaluation. | MUST BE RESTATED AS SPD-NATIVE | Non-EPUB accessibility applicability and reporting need a mapping; WCAG 2.2 AA remains. | — |
| SPD-PROV-001 | 48 | Prompt transcripts and chain-of-thought are not required portable provenance. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-IMP-001 | 49 | Imported semantic information distinguishes asserted source semantics from inferred semantics. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-IMP-002 | 49 | An importer does not silently upgrade inferred structure to asserted structure. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-IMP-003 | 50 | The format does not claim lossless conversion of arbitrary PDF to semantic SPD. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-API-001 | 51 | The file format exposes stable structures suitable for a companion transactional API. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-CAP-001 | 60 | A processor does not silently misrepresent an unsupported capability. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-CAP-002 | 54 | Documents declare only capability ID and version; normative or experimental status is specification-controlled. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-CAP-003 | 54 | EPUB discovery metadata and the authoritative document-state capability declaration agree exactly. | WORDING CHANGE ONLY | Replace EPUB discovery metadata wording with retained OPF-based SPD discovery metadata; equality predicate unchanged. | — |
| SPD-DISC-001 | 69 | container.xml contains exactly one link for each required SPD document-state, resource-inventory, and lifecycle-state relationship. | DEPENDENCY CHANGE | Retain exact container.xml relationships; explicitly incorporate the container links grammar/context. | — |
| SPD-DISC-002 | 69 | Each SPD descriptor link has the exact provisional relationship token, application/json media type, and a safe path resolving to one existing resource. | DEPENDENCY CHANGE | Exact tokens/media type stay; safe href resolution must bind to the independent package model. | — |
| SPD-DISC-003 | 69 | Processors do not discover SPD descriptors by filename scanning or guessing. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-DISC-004 | 69 | Provisional descriptor, capability, schema, and annotation identifiers are replaced by stable project-controlled identifiers before Release Candidate. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-EXT-001 | 61 | Extensions use globally unique identifiers or namespaces. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-EXT-002 | 61 | Each extension declares whether it is required or optional. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-EXT-003 | 61 | An unknown required extension causes its affected capability to be reported unsupported. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-TEST-001 | 63 | Conformance development includes multilingual and structurally difficult fixtures. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-TEST-002 | 63 | The normative corpus includes Arabic and mixed-bidirectional text. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-GOV-001 | 59 | Archive rules are developed separately from Base conformance. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-GOV-002 | 66 | The experimental PDF annex does not alter Base conformance. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-GOV-003 | 67 | A fixed media format becomes normative only after the evidence gate in section 67 is met. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |
| SPD-GOV-004 | 68 | New mechanisms are introduced only for demonstrated architectural gaps. | UNCHANGED | No EPUB-parent dependency requiring a change to this predicate; retained frozen document/capability/governance rule. | — |

## Eight proposed new B rule groups

These are enumerated additions for a concrete migration plan, **not existing or assigned SPD requirement IDs**, and not an assertion that B intrinsically requires exactly eight atomic clauses. A final registry could split/group them differently. Their need is derived from the loss of BASE-002's umbrella and the dependency rows above.

| Audit label | Classification | Proposed obligation | Existing affected row / responsibility groups |
| --- | --- | --- | --- |
| B1 | NEW REQUIREMENT NEEDED | Independent package identification and mismatch behavior, with no MIME spelling selected | BASE-001; group 3 |
| B2 | NEW REQUIREMENT NEEDED | Incorporated OPF grammar, required metadata and manifest property rules | BASE-002/005, CAP-003; groups 7/8/19/23 |
| B3 | NEW REQUIREMENT NEEDED | Core/foreign resource admissibility and fallback rules | BASE-002/005; group 9 |
| B4 | NEW REQUIREMENT NEEDED | Explicit package URL/base/decoding/XML integration rules | BASE-002, DISC-002, SEM-002; groups 4/13–16 |
| B5 | NEW REQUIREMENT NEEDED | Navigation conformance, targets and spine/reachability semantics | BASE-005/006, SEM-003; groups 10/11 |
| B6 | NEW REQUIREMENT NEEDED | Independent complete-package conformance evaluation and imported-error attribution | BASE-002; group 22 |
| B7 | NEW REQUIREMENT NEEDED | Accessibility publication scope, metadata locations and honest conformance reporting | ACC-004; group 20 |
| B8 | NEW REQUIREMENT NEEDED | Versioned incorporation/exception table and processor applicability | BASE-002, DISC-001; groups 1/2/5/6/12/17/18/21/24 |

Some content in B1–B8 could live under a restated BASE-002 rather than a new ID. Counting them as eight **proposed groups** makes the planning estimate explicit without pretending the source registry determines future editorial granularity.

## Option A's smallest proposed clarification delta

Modify **11** existing rows: BASE-001, BASE-002, BASE-004 and SEC-001 through SEC-008. The two package rows explicitly settle whole-publication/datestamped inheritance; BASE-004 clarifies the unverified fallback contract. All eight SEC rows align the existing profiles and no-required-dependency wording with the uniform passive rule. SEC-004/005/006 retain local assets but cover optional/decorative fetches too. This is not all editorial: suppressing previously optional active/time-dependent behavior narrows accepted/processed content.

Add the **5** grouped candidate obligations P1–P5 in [passive profile](passive_content_profile.md): passive data, inert controls, stable presentation, reader authority, verification representation. Their placement may later be split between document and reading-system conformance. No new numeric implementation maximum is proposed.

This audit proposes **0** changes to Node/Document/Revision identities, semantic/rendition digests, mapping, annotations, transaction safety, semantic authority, lifecycle or fixed abstraction. The stable-identifier release requirement DISC-004 already exists; no identifiers are assigned here and its eventual migration is excluded from this audit's change counts.

## Delta accounting across options

“Modified” includes wording, dependency and native-restatement rows. The new column counts the specifically enumerated candidate groups, not already enacted requirements.

| Scenario | Current unchanged | Current modified | Current removed | Current unresolved | Proposed new groups | Requirement accounting to revalidate |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| A, package boundary only | 113 | 0 | 0 | 0 | 0 | 0 newly required by boundary choice |
| A plus specified pre-RC clarification | 102 | 11 | 0 | 0 | 5 | 113 existing + 5 new |
| B-min, packaging only | 103 | 10 | 0 | 0 | 8 | 113 existing + 8 new |
| B-min plus identical passive clarification | 94 | 19 | 0 | 0 | 13 | 113 existing + 13 new |
| C, packaging only, known/conditional partition | 99 | 10 known | 0 proven | 4 | Final total undefined; 12 enumerated work groups | All 113; conditional rows must first be resolved |

The B combined count is the **union**, not 10+11: BASE-001/002 occur in both sets, leaving 19 unique changed rows. All five passive additions and all eight B groups remain proposed. C's four conditional rows are BASE-003 and RES-003/004/006; their ZIP references may survive if C retains ZIP. C plus the shared clarification affects 19 known rows, with 4 conditional and 90 with no identified change. No exact final C new-ID/removal count is derivable without inventing its architecture.

For a changed validator/specification, revalidation includes all **74 currently automated registrations** plus review of the other **39 registry classifications/applicability outcomes**. It does not turn manual/historical/partially automated requirements into machine PASS. The entire 70-case regression suite should run after implementation; that is distinct from the number of requirements whose words change.

## Scope and evidence cautions

A small registry delta can conceal a large imported-standard burden: BASE-002 represents many EPUB rules. Conversely changing every package marker need not change any semantic algorithm. See [validator impact](validator_impact.md), [corpus impact](corpus_impact.md), and [accessibility/schema impact](accessibility_impact.md).

Counts above are mechanically tied to the 113-row inventory and explicit scenario definitions. Unknown final C design/editorial choices are identified rather than assigned invented exact numbers.

