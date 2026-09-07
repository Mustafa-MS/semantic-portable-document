# Semantic Portable Document Format 0.1



## Draft Specification



**Working name:** SPD

**Version:** 0.1

**Status:** Draft specification — pre-RC passive security clarification; not RC1

**File extension:** Not yet assigned

**Media type:** Not yet assigned



The working name and identifiers are provisional and do not form part of conformance.



---



# 1. Scope



Semantic Portable Document Format 0.1 defines a portable document model in which structured semantic content is authoritative and presentation renditions are derived from that content.



The format is designed for:



* human reading;

* structured editing;

* responsive rendering;

* accessibility;

* offline distribution;

* machine interpretation;

* AI-agent operations;

* revision-safe editing;

* annotations;

* fixed visual renditions;

* document integrity.



The format does not attempt to define a new:



* compression format;

* markup language;

* browser engine;

* font format;

* vector graphics language;

* cryptographic algorithm;

* PDF implementation;

* accessibility vocabulary.



Existing standards SHALL be reused wherever practical.



---



# 2. Conformance Language



The key words:



```text

MUST

MUST NOT

REQUIRED

SHALL

SHALL NOT

SHOULD

SHOULD NOT

MAY

OPTIONAL

```



are normative requirements when written in uppercase.



---



# 3. Fundamental Principle



A conforming document SHALL have one authoritative semantic representation.



Presentation shall be derived from that semantic representation.



Conceptually:



```text

&#x20;              Semantic Document

&#x20;                     │

&#x20;             authoritative state

&#x20;                     │

&#x20;         ┌───────────┴───────────┐

&#x20;         │                       │

&#x20;         ▼                       ▼



&#x20;  Responsive Rendering      Fixed Rendition

&#x20;                                 optional/

&#x20;                               experimental

```



A fixed rendition SHALL NOT become a second independently editable source of truth.



---



# 4. Normative Technology Baseline

The normative baseline is the EPUB 3.3 Recommendation of 13 January 2026, XHTML, CSS, MathML, SVG, Unicode including UAX #9, W3C Web Annotation, native HTML semantics, WAI-ARIA/DPUB-ARIA where applicable, EPUB Accessibility 1.1, WCAG 2.2, SHA-256, RFC 9562 UUID URNs, RFC 8785 JCS, and JSON Schema Draft 2020-12 as profiled here.

EPUB 3.4 and EPUB Annotations 1.0 drafts MAY inform implementations but are not normative dependencies. Specification-development preferences are informative and appear in section 75; they do not create document conformance failures.

---

The normative dependency and update policy is [UPSTREAM_DEPENDENCY_BASELINE_0.1.md](UPSTREAM_DEPENDENCY_BASELINE_0.1.md). EPUB Reading Systems 3.3 (17 October 2024) is incorporated only for explicitly relied-on processing behavior; publication conformance does not import every reading-system recommendation. Future EPUB or living-spec changes require an explicit SPD maintenance decision.

# 5. Package and Authoritative Package Document

A Format 0.1 Base document uses the EPUB-Compatible Packaging Profile 0.1 and SHALL satisfy applicable container/publication requirements of EPUB 3.3 Recommendation 13 January 2026 except where SPD explicitly imposes a stricter rule.

Whole-publication EPUB conformance is required under the pinned baseline. Every completed EPUBCheck 5.3.0 conformance error or fatal error fails this requirement; specific diagnostic attribution is additive. Warnings alone do not fail it, and tool failure is NOT_TESTED rather than document failure.

SPD does not define a new ZIP dialect.

`META-INF/container.xml` MUST contain exactly one `rootfile` package document. The spine of that package document defines the authoritative semantic reading order. Multiple EPUB rootfiles MUST NOT be used for fixed renditions. Fixed renditions are generated resources bound through SPD state and mapping.

All entry paths MUST be relative, forward-slash-separated, Unicode NFC paths without dot segments, traversal, ambiguous normalized duplicates, or duplicate ZIP names. Stored and Deflate are the only compression methods. Section 69 defines deterministic SPD descriptor discovery.

---

# 6. EPUB Compatibility and Verification

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

**SPD-SEC-001.** Base MUST NOT contain or depend on executable document code, executable macros, script elements (including inert data blocks), event-handler attributes, executable URLs or document-supplied code paths.

**SPD-SEC-002.** Base MUST NOT contain active embedded/application contexts: iframe including srcdoc, object, embed, plugin execution, service-worker dependencies or document-created executable browsing contexts. Host-owned rendering frames are outside document content.

**SPD-SEC-003.** Base MUST NOT initiate automatic publication-originated network access or navigation, including fetching, speculative loading, remote preload, prefetch, DNS preconnect, ping and automatic link checking. Explicit host-mediated user hyperlinks are separate.

**SPD-SEC-004.** Every automatically loaded font MUST be inventoried and package-local, including optional fonts. Remote font fetching is prohibited; authoritative fonts MUST NOT depend on uncontrolled local() substitution.

**SPD-SEC-005.** Every automatically loaded stylesheet or import MUST be inventoried and package-local, including optional and fallback styling. Remote stylesheet loading is prohibited.

**SPD-SEC-006.** Every automatically loaded image or other visual/media resource MUST be inventoried and package-local, including decorative, optional, cursor, mask, filter, tracking and non-authoritative resources.

**SPD-SEC-007.** All SVG contexts, including inline, standalone, image and nested resources, MUST exclude script, events, foreignObject, executable URLs, automatic remote dependencies and active behavior; ordinary static graphics and safe terminating local references remain allowed.

**SPD-SEC-008.** Every automatically resolved rendered dependency MUST transitively terminate in verified inventoried package-local resources or valid local fragments. XHTML, CSS, SVG, MathML and nested embedding modes use the same containment policy; import and resource-expansion cycles are prohibited.

**SPD-PASS-001.** SPD Base content is untrusted passive document data and SHALL NOT supply executable application behavior. A Base processor SHALL NOT execute document-supplied code or grant publication-originated application authority.

**SPD-PASS-002.** Base SHALL obey the normative inert-control/embedded-context profiles: no forms, active contexts, automatic navigation, base overrides or authoritative interactive canvas; preserved controls SHALL be disabled, labeled inert representations without capture, form association, submission or activation behavior.

**SPD-PASS-003.** Base meaning SHALL be complete in a stable static presentation without animation, transitions, autoplay or interactive state changes. Processors SHALL suppress their execution. Local media MAY play only after user action with equivalent accessible semantics available without playback.

**SPD-RS-001.** An SPD reader SHALL deny publication-originated network, filesystem, camera, microphone, location, shared-cookie, persistent Web storage and service-worker authority. External HTTP/HTTPS hyperlinks require intentional user action and host mediation without destination access to the document context.

**SPD-RS-002.** An SPD processor SHALL distinguish displayed semantic content, declared SEALED, verified SEALED/current state and verified current fixed rendition. Unverified views MUST NOT be represented as verified sealed/fixed or authenticated; hash integrity is not signer or issuer authentication.

Detailed technology restrictions in [XHTML](profiles/xhtml-profile.md), [CSS](profiles/css-profile.md), [SVG](profiles/svg-profile.md), [MathML](profiles/mathml-profile.md) and [resource resolution](profiles/passive-resource-profile.md) are normative. These profiles restrict capabilities of existing languages rather than defining replacement languages.

Document conformance constrains file constructs. SPD reading-system conformance constrains processor authority and verification representations. Implementation hardening sets operational budgets; no universal DOM, pixel, font, memory or timeout limit is introduced. [Reading-system security](READING_SYSTEM_SECURITY.md) separates these layers. Package validators report untested human/processor portions honestly; package PASS does not establish reader or complete static-meaning conformance.

Validators MUST use namespace-aware XML/SVG parsing and standards-aware CSS tokens/structure for normative resource decisions, including escapes, comments, inline styles, nested rules/functions and custom properties at resource use. Regex may optimize detection but MUST NOT be the authoritative security parser. Validation SHALL parse, inspect and report without rewriting source. A reader/validator MUST NOT sanitize a SEALED source and present the modified result as still verified; a repair workflow requires a new revision under existing rules.

Format 0.1 prohibits document-originated executable behavior and automatic external-resource authority in Base. Reader implementations remain responsible for safely processing hostile declarative content; passive conformance is not proof against exploits or a comparative safety claim.

---

# 8. Authoritative Semantic Rendition



Each document SHALL identify exactly one authoritative semantic rendition.



That rendition SHALL consist of one or more ordered XHTML content documents.



The package spine SHALL define their primary reading order.



Semantic content SHALL use native HTML semantics wherever those semantics exist.



Examples include:



```text

article

section

nav



h1-h6



p



ol

ul

li



figure

figcaption



table

thead

tbody

tfoot

tr

th

td



blockquote

cite



code

pre



aside

```



---



# 9. Native-Semantics-First Rule



A document SHALL use semantic XHTML before accessibility or custom metadata mechanisms.



Preference order:



```text

1. Native XHTML semantics

2. Native XHTML attributes

3. WAI-ARIA

4. DPUB-ARIA

5. supplemental relationship metadata

```



ARIA SHALL NOT be used to replace correct native semantics.



---



# 10. Semantic Content Is the Source of Truth



Primary textual or structural content MUST NOT be independently duplicated in another normative resource.



For example, this is invalid:



```text

document.xhtml:



FROC = 0.906





graph.json:



FROC = 0.901

```



Supplemental structured data MAY reference semantic objects.



It MUST NOT redefine their authoritative textual content.



---



# 11. Document Identity

Every document MUST have a persistent Document ID identifying one lineage. It MUST be a lowercase UUID URN using RFC 9562 textual UUID syntax:

```text
urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Alphabetic hexadecimal digits MUST be lowercase. UUIDv4 or UUIDv7 are RECOMMENDED generation choices, but processors MUST treat UUID values as opaque and MUST NOT rely on generation-time or version semantics.

---

# 12. Revision Identity

Each committed semantic state MUST have a Revision ID using the Document-ID grammar. A Revision ID is opaque identity and MUST NOT encode semantic-state identity or be a content digest.

Semantic modification MUST create a new Revision ID. A change confined to a resource with `affects: []` MUST NOT by itself create a new semantic revision. Two independently committed, semantically identical states MAY have different Revision IDs and the same `semanticStateDigest`.

---

# 13. Node Identity and Syntax

Independently addressable semantic objects MUST carry persistent Node IDs, including sections, headings, paragraphs, list items, figures, captions, tables, rows, cells, equations, notes, citations, references, and preserved controls.

A Node ID has the grammar `n_<opaque-token>`. The token contains 1–128 lowercase ASCII characters from `[a-z0-9._-]`; the complete ID therefore has maximum length 130. The form is XML-ID compatible because it begins with `n_`. Additional inline structures MAY receive IDs.

---

# 14. Node ID Document Conformance

Node IDs MUST be unique in the current authoritative semantic revision. They MUST NOT depend on page position, DOM path, visible numbering, text content, or content hash. A logically persistent object MAY retain its Node ID when moved, restyled, renamed, or edited.

Current-revision uniqueness is fully automated document conformance. Historical persistence is governed separately by section 15.

---

# 15. Node Lineage Conformance

A conforming editor supplied with lineage history MUST preserve Node identity according to the copy, split, merge, and deletion rules and MUST NOT knowingly reuse a retired Node ID in that history. A copied logical object normally receives a new Node ID. Split/merge retention policy may be user-interface-specific but lineage provenance SHOULD be preserved.

When lineage history is unavailable, a standalone validator MUST report historical persistence and non-reuse checks as `NOT_TESTED`. Missing history MUST NOT make an otherwise conforming standalone package fail Base.

---

# 16. Logical Text, Language, and Direction

Semantic text MUST be stored in logical Unicode order. Visual placement MUST NOT determine semantic ordering.

The root `<html>` of every authoritative XHTML document MUST contain valid, equivalent `lang` and `xml:lang` values and MUST explicitly declare `dir="ltr"` or `dir="rtl"`. Root `dir="auto"` is prohibited. A nested semantic element MUST declare direction when its intended base direction differs from the inherited direction. `dir="auto"` MAY be used for appropriate nested or user-generated content.

---

# 17. Arabic, Bidirectional Text, and Detection Limits

Arabic and bidirectional behavior are normative conformance cases. Mapping and editing APIs MUST operate on logical text ranges and MUST NOT equate visual left-to-right position with logical order.

General natural-language intended order is `PARTIALLY_AUTOMATED`. Validators MUST use deterministic corpus/oracle checks and MAY report suspicious bidi controls or patterns, but MUST NOT claim they can always infer the intended logical order of arbitrary prose.

---

# 18. Mathematics



Mathematical expressions SHOULD use MathML.



Implementations MUST NOT require mathematical meaning to be reconstructed from visual glyph positions when semantic MathML exists.



A fixed rendition MAY map an equation as one semantic visual region without mapping every mathematical glyph individually.



---



# 19. Figures



A semantic figure SHOULD consist of:



```text

figure

asset

figcaption

alternative text where appropriate

```



The relationship between figure, caption and references SHALL remain semantic.



Fixed coordinates SHALL NOT define that relationship.



---



# 20. Tables



Tables SHALL use semantic table structures.



Table header relationships SHALL be represented semantically rather than inferred from visual position.



Addressable table cells SHALL have persistent Node IDs.



A cell that spans multiple fixed-page fragments retains one Node ID.



---



# 21. Supplemental Relationship Graph



A document MAY contain a supplemental relationship graph.



JSON-LD is the RECOMMENDED representation for Format 0.1.



It MAY describe relationships such as:



```text

paragraph → cites → reference



paragraph → discusses → figure



table → derivedFrom → dataset



claim → supportedBy → citation

```



The graph MUST NOT duplicate authoritative content unnecessarily.



A conforming Base reader is not required to implement a general RDF reasoning engine.



---



# 22. Annotations



Annotations SHOULD use the W3C Web Annotation Data Model.



Annotations are normally separate from primary semantic content.



An annotation MAY target:



* a Node ID;

* a text range;

* a figure;

* a table cell;

* an equation;

* a page region in a fixed rendition;

* another annotation.



---



# 23. StableNodeSelector

Format 0.1 defines a minimal W3C Web Annotation selector extension.

`scope: "lineage"` MUST contain Document ID and Node ID and MUST omit Revision ID. It follows the logical node across revisions while that Node ID survives.

`scope: "revision"` MUST contain Document ID, Revision ID, and Node ID and anchors the exact historical state.

The Draft provisional type name is `StableNodeSelector`. A stable public IRI/context is REQUIRED before Release Candidate (section 75).

---

# 24. Robust Text Annotation



Text annotations SHOULD include both:



```text

stable semantic target

+

fallback textual selector

```



where practical.



Fallback selectors MAY use mechanisms equivalent to:



* TextQuoteSelector;

* TextPositionSelector.



The stable Node ID remains preferable for semantic targeting.



---



# 25. Document States



Format 0.1 recognizes at least:



```text

EDITABLE



SEALED

```



---



# 26. Editable State and Fixed Status

In `EDITABLE`, semantic content is authoritative and may be committed as a new revision. Fixed status is `absent`, `current`, or `stale`.

`current` is valid only when the fixed Revision ID equals the current Revision ID, the fixed `renditionInputDigest` equals the current value, and the fixed resource digest verifies. A mismatch MUST be treated as stale regardless of the declared token. A reader MUST NOT expose stale fixed content as current.

---

# 27. Sealed State

A `SEALED` state finalizes one semantic revision and binds its Revision ID, semantic/rendition digests, inventory, and any present fixed/mapping artifacts.

A semantic-only revision MAY be SEALED. If a fixed rendition is present in SEALED, its status MUST be current. A fixed rendition MAY exist without Mapping. If Mapping is claimed, a current fixed rendition and mapping artifact are REQUIRED.

Changing any inventoried packaged resource invalidates the sealed state unless inventory and descriptor bindings are recomputed as a new internally consistent state. This is integrity, not signer authentication.

---

# 28. Resource Inventory and Effects

Exactly one normative inventory MUST be discovered through section 69. It MUST list every ZIP entry, including `mimetype`, `META-INF/container.xml`, controls, caches, annotations, fixed output, and mapping, except the inventory itself and lifecycle state descriptor.

Every entry MUST include normalized NFC `path`, `mediaType`, exact decompressed `byteLength`, lowercase SHA-256, `role`, and `affects`. `affects` is a unique subset of `semantic` and `rendering`; an empty array means neither input scope. Role describes authority/provenance and MUST NOT be used to infer effects.

Unknown or unlisted ZIP entries outside the two explicit self-reference exceptions MUST fail Base. Non-normative caches remain listed with role `non-normative` and normally `affects: []`.

---

# 29. Integrity

Resource SHA-256 covers exact decompressed ZIP-entry bytes without XML, JSON, Unicode, encoding, whitespace, or line-ending normalization. Compression method and ZIP timestamps do not affect resource digest identity.

Format 0.1 separately defines `semanticStateDigest`, `renditionInputDigest`, inventory digest, and `descriptorDigest` in sections 70–72. Integrity MUST detect covered semantic, style, font, asset, annotation, mapping, fixed, inventory, and state changes. Integrity is distinct from digital signature.

---

# 30. Digital Signatures



A normative outer-package digital-signature mechanism is NOT defined by Format 0.1.



Implementations MAY experiment with existing standardized signature systems.



No implementation may claim a Format 0.1 signature profile until such a profile is separately standardized.



---



# 31. Fixed Rendition Concept

A fixed rendition is an optional generated page appearance. It MUST identify an opaque `f_<token>` Fixed Rendition ID, source Revision ID, source `renditionInputDigest`, exact resource digest, path, and media type. Its token uses the Node-token grammar.

Presentation-only input changes do not introduce a Presentation Revision ID: they change `renditionInputDigest` and make the old fixed rendition stale.

---

# 32. Fixed Rendition Status in 0.1



Format 0.1 does NOT normatively require one specific fixed-page media format.



PDF 2.0 is the project reference fixed-rendition implementation during Format 0.1.



It remains an experimental profile.



A processor SHALL NOT interpret:



```text

Fixed capability

```



as meaning:



```text

PDF is the permanent normative page model

```



---



# 33. Fixed Rendition Immutability



Once a fixed rendition is associated with a sealed semantic revision, it SHALL be treated as immutable for that revision.



Regeneration produces a new fixed-rendition identity.



---



# 34. Semantic-to-Fixed Mapping

When Mapping is claimed, the renderer MUST emit a mapping artifact during fixed rendering. The mapping MUST bind Document ID, Revision ID, Fixed Rendition ID, and fixed resource digest.

Mapping requires Base, a current fixed rendition, and a mapping artifact. It does not require a separate `Fixed-Experimental` capability claim.

---

# 35. Mapping Generation



The mechanism used to generate mapping is implementation-specific and non-normative.



A conforming processor MAY use:



* browser layout information;

* paginated DOM;

* layout-engine APIs;

* another reliable forward-layout mechanism.



Mapping reconstruction from a fixed rendition MAY be used for:



* validation;

* recovery;

* legacy import.



It SHALL NOT be the required normative method of generating mappings.



---



# 36. Mapping and Geometry Model

A mapping is correspondence, not page description. It MAY contain Node ID, logical range, rendition-local Page ID, quad, optional affine transform, status, and provenance. It MUST NOT contain glyph rendering, font recreation, drawing operations, line breaking, or layout algorithms.

Geometry uses page-local CSS reference pixels, top-left origin, +x right, +y down. Each page MUST declare `p_<token>` ID, positive width, and positive height. Page IDs are unique only within that fixed rendition. Quad order is TL, TR, BR, BL. Values MUST be finite and visible fragments MUST be bounded by page space. A six-value affine transform MAY map to native fixed-medium coordinates. No precision field is defined; tolerance is validator/test policy.

---

# 37. Mapping Fragment



A semantic node MAY map to zero, one or multiple page fragments.



Example:



```text

Node n_123



fragment 1

&#x20;   page p1

&#x20;   logical range 0-74



fragment 2

&#x20;   page p2

&#x20;   logical range 75-161

```



This supports semantic objects crossing page boundaries.



---



# 38. Mapping Status

Mapping records use exactly one status:

- `MAPPED`: all required visible correspondence represented; at least one fragment.
- `PARTIALLY_MAPPED`: some represented and known required visible correspondence missing; at least one fragment and a reason.
- `NOT_VISIBLE`: intentionally no visible representation; zero fragments and a reason.
- `UNMAPPABLE`: supported feature class but reliable instance correspondence cannot be established; zero fragments and a reason.
- `UNSUPPORTED`: implementation does not support mapping this feature class; zero fragments and a reason.

`NOT_VISIBLE` MUST NOT mean algorithm failure. Geometry MUST NOT be fabricated to claim coverage.

---

# 39. Mapping Provenance



Mapping records SHALL identify the generation mechanism or evidence class.



Examples include:



```text

forward-layout

backward-recovery

inferred

manual

```



The exact registry of values will be defined with the mapping schema.



---



# 40. Logical Range Model

Mapping and annotation text ranges are zero-based, half-open `[start,end)` Unicode scalar-value offsets over the semantic text value. They are not UTF-8 bytes, UTF-16 code units, or grapheme counts.

For the selected Node, the semantic text value concatenates descendant XML text nodes in DOM logical order after character-reference expansion, excluding comments, processing instructions, `head`, `script`, `style`, and CSS-generated content. Source characters and whitespace are preserved; no whitespace collapse, Unicode normalization, shaping, or bidi reordering occurs.

`0 <= start <= end <= scalarLength`. Endpoints need not coincide with extended grapheme-cluster boundaries. Human-facing editors and annotation tools SHOULD avoid splitting extended grapheme clusters unless sub-grapheme addressing is intended.

---

# 41. Visual Fidelity, Mapping Fidelity and Text Fidelity



Format 0.1 distinguishes:



```text

VF — Visual Fidelity



MF — Mapping Fidelity



PF — fixed-rendition text fidelity



CF — fixed-rendition format/profile conformance

```



These properties SHALL NOT be treated as interchangeable.



For example:



```text

MF = PASS

PF = FAIL

```



is a valid reportable state.



---



# 42. Accessibility Authority

Base accessibility is evaluated against the authoritative semantic XHTML. Native-semantics applicability and qualitative accessibility remain partially automated; validators MAY detect known anti-patterns but MUST retain human evaluation where intent or quality cannot be inferred.

---

# 43. Accessible Fixed Export



A standalone fixed-format export that claims accessibility MUST satisfy the accessibility requirements of that fixed format independently.



For PDF this may include:



```text

PDF/UA

WTPDF accessibility

```



as appropriate.



Semantic XHTML accessibility SHALL NOT be used to claim that an independently distributed inaccessible PDF is accessible.



---



# 44. PDF Reference Rendition



The Format 0.1 reference implementation MAY generate PDF 2.0 fixed renditions.



Such PDFs MAY use:



* Tagged PDF;

* PDF/UA;

* WTPDF;

* semantic compilation;

* ActualText;

* structure trees.



These mechanisms are not required for Base Format 0.1 conformance.



---



# 45. PDF Text Interoperability Warning



Format 0.1 does not assume that formal Tagged PDF/PDF-UA/WTPDF conformance guarantees identical logical text extraction across all PDF consumers.



Implementations claiming a high-quality accessible PDF export SHOULD test:



* search;

* extraction;

* copy/paste;

* Arabic;

* mixed bidi;

* independent consumers.



---



# 46. Archive Capability



Long-term archival conformance is not part of Base 0.1.



An Archive capability MAY require:



* sealed state;

* all normative resources embedded;

* no active content;

* preservation metadata;

* fixed rendition;

* archival fixed-format profile.



PDF/A-4 is the current reference archival fixed-rendition target.



PDF/A-4 SHALL NOT be required for ordinary Base or Fixed documents.



---



# 47. Forms



Format 0.1 does not define a complete interoperable forms/workflow model.



Safe semantic form controls MAY be preserved.



Automatic submission, arbitrary calculations, workflow scripting and executable logic are outside Base 0.1.



---



# 48. Revision Provenance



A revision SHOULD record minimal provenance including:



```text

Revision ID

parent Revision ID

timestamp

generator

generator version

```



An implementation MAY record additional provenance.



Prompt transcripts and AI chain-of-thought SHALL NOT form part of required portable provenance.



---



# 49. Imported Semantics



Imported semantic information SHALL distinguish authoritative source semantics from inferred semantics.



Examples:



```text

native XHTML heading

→ ASSERTED



AI-inferred PDF heading

→ INFERRED

```



An importer MUST NOT silently upgrade inferred structure to asserted structure.



---



# 50. PDF Import



PDF import is inherently potentially lossy.



A PDF importer SHOULD preserve:



* original source PDF;

* extraction provenance;

* inferred Node IDs;

* confidence/evidence where applicable.



The format SHALL NOT claim that arbitrary PDF can be losslessly converted to semantic Format 0.1.



---



# 51. Agent Processing Model



The file format SHALL expose stable document structures suitable for a companion transactional API.



The file specification itself does not define programming-language method names.



The companion API MAY support operations conceptually equivalent to:



```text

query node

replace text

update table cell

move section

replace figure

insert citation

add annotation

validate

render

seal

```



---



# 52. Transaction Safety



A companion transactional processor SHOULD support revision preconditions.



Example concept:



```text

baseRevision = R105

```



If the current revision is:



```text

R106

```



the attempted mutation SHOULD fail rather than overwrite newer content.



---



# 53. Atomic Multi-Node Changes



Changes that semantically form one edit SHOULD be applied atomically.



For example:



```text

change table result

+

update paragraph discussing result

```



should either both commit or neither commit.



---



# 54. Conformance Capabilities and Declaration

The authoritative document-state descriptor declares only capability `id` and `version`. A document MUST NOT declare whether a capability is normative or experimental; this specification controls that status.

The capability claim set in EPUB `dcterms:conformsTo` discovery metadata MUST equal the authoritative descriptor set. Disagreement fails Base.

Format 0.1 defines Base (normative), Mapping (normative when claimed), Accessible (normative when claimed), Fixed-Experimental (experimental), and Archive-Experimental (experimental).

---

# 55. Base Capability



Base is normative in Format 0.1.



Base requires:



* valid OCF-compatible package;

* authoritative XHTML rendition;

* navigation;

* resource inventory;

* offline required resources;

* secure content restrictions;

* Document ID;

* Revision ID;

* persistent Node IDs;

* logical Unicode text;

* semantic structure;

* integrity digests.



---



# 56. Mapping Capability

Mapping requires Base, a current fixed rendition, a bound forward-emitted mapping artifact, valid page IDs/dimensions/geometry, status, provenance, and scalar logical ranges where used. A document need not claim Fixed-Experimental merely because Mapping targets a fixed rendition.

---

# 57. Fixed-Experimental Capability



Fixed rendering remains experimental in Format 0.1.



The specification defines its lifecycle and binding semantics but does not yet designate a permanent normative fixed-page encoding.



PDF 2.0 is the initial reference implementation.



---



# 58. Accessible Capability

SPD Accessible 0.1 is exactly EPUB Accessibility 1.1 plus WCAG 2.2 Level AA. A claiming document MUST declare that fixed target and satisfy it, including human evaluation for criteria that cannot be reliably automated. Additional claims MAY be present but do not redefine SPD Accessible 0.1.

Accessible requires Base. A standalone fixed export claiming accessibility independently satisfies its fixed-format accessibility profile.

---

# 59. Archive-Experimental Capability

Archive remains experimental and requires at least Base, SEALED lifecycle, and a current archive-appropriate fixed rendition. Accessibility is separately claimable and is not implied by Archive. PDF/A-4 remains the reference archival fixed target, not a Base requirement.

---

# 60. Graceful Degradation



A processor that does not implement an optional capability SHOULD still expose the authoritative semantic content where safe.



A processor MUST NOT silently misrepresent unsupported capabilities.



For example:



```text

Fixed rendition unavailable

```



is preferable to displaying a stale or incorrect fixed state.



---



# 61. Extensions



Extensions SHALL use globally unique identifiers or namespaces.



Extensions SHALL declare whether they are:



```text

required

optional

```



Unknown optional extensions SHOULD be preserved.



Unknown required extensions SHALL cause the affected capability to be reported as unsupported.



---



# 62. Conformance Reports



Validators SHOULD produce machine-readable conformance reports.



A report SHOULD distinguish at least:



```text

ERROR

WARNING

INFORMATION

NOT_TESTED

```



It SHOULD identify the relevant:



* resource;

* Node ID;

* revision;

* capability;

* rule.



---



# 63. Test Corpus



Format 0.1 conformance development SHALL include multilingual and structurally difficult fixtures.



Arabic and mixed bidirectional text SHALL be included in the normative test corpus.



Tests SHOULD include:



* long multipage text;

* tables across pages;

* figures;

* SVG;

* MathML;

* notes;

* citations;

* multi-column layout;

* Arabic;

* mixed Arabic/Latin;

* CJK where practical;

* Indic complex shaping where practical.



---



# 64. Explicit Non-Goals



Format 0.1 does not attempt to provide:



* universal office-suite compatibility;

* arbitrary scripting;

* browser applications inside documents;

* DRM;

* universal PDF round-trip;

* universal DOCX round-trip;

* a spreadsheet calculation engine;

* a presentation animation engine;

* a new page renderer;

* a new cryptographic trust infrastructure.



---



# 65. Format 0.1 Success Criterion



The primary technical purpose of Format 0.1 is to standardize:



```text

semantic authoritative content

+

persistent object identity

+

immutable revision identity

+

safe portable packaging

+

semantic-to-fixed correspondence

+

integrity binding

+

machine-safe structured processing

```



while continuing to reuse mature standards for everything else.



---



# 66. Experimental Fixed-PDF Annex



The reference implementation SHOULD maintain an experimental PDF fixed-rendition annex documenting:



* PDF 2.0 generation;

* Tagged PDF experiments;

* PDF/UA;

* WTPDF;

* ActualText behavior;

* Arabic and bidi extraction;

* semantic PDF compilation;

* visual-scene preservation.



This annex is informative for Format 0.1 and SHALL NOT alter Base conformance.



---



# 67. Future Standardization Gate



A fixed-rendition media format SHALL become normative only after evidence demonstrates:



1. stable fixed appearance;

2. cross-implementation rendering support;

3. acceptable international text behavior;

4. adequate accessibility strategy;

5. viable long-term maintenance;

6. independent implementation experience.



Until then, the fixed-rendition abstraction remains intentionally decoupled from one permanent encoding.



---



# 68. Governing Principle



Where a mature interoperable standard exists, Format 0.1 SHOULD profile or reuse it.



New mechanisms SHALL be introduced only when they address a demonstrated architectural gap.



The intended innovation is the document lifecycle and correspondence model, not reinvention of existing media technologies.

---

# 69. SPD Descriptor Discovery

Processors MUST discover SPD descriptors through the OCF `container.xml` `links` element and MUST NOT scan or guess filenames.

Exactly one link for each relationship is required:

| Relationship token | Media type | Target |
|---|---|---|
| `https://example.invalid/spd/rel/document-state` | `application/json` | document/revision/capability descriptor |
| `https://example.invalid/spd/rel/resource-inventory` | `application/json` | normative inventory |
| `https://example.invalid/spd/rel/lifecycle-state` | `application/json` | EDITABLE/SEALED state descriptor |

Each href MUST be a safe OCF root-relative path-relative-scheme-less URL resolving to exactly one existing entry. Duplicate, missing, wrong-media-type, unresolved, or conflicting links fail Base. The provisional relationship identifiers are replaced before Release Candidate.

---

# 70. Deterministic Inventory Digest Projections

All inventory paths are stored NFC normalized paths. For each selected entry serialize:

```text
UTF8(path) 0x00 ASCII(decimal byteLength) 0x00 ASCII(sha256:lowercase-hex) 0x0A
```

Sort records by unsigned lexicographic comparison of the UTF-8 path bytes. Concatenate them without a header or final transformation and compute SHA-256, serialized as `sha256:` plus lowercase hex.

`semanticStateDigest` selects entries whose `affects` contains `semantic`.

`renditionInputDigest` selects entries whose `affects` contains `semantic` or `rendering`. Generated fixed/mapping resources normally use `affects: []` and are excluded.

---

# 71. Resource Effects and Fixed Currentness

The creator explicitly assigns effects; processors do not infer them from media type or role. Incorrect classification that omits a real semantic/rendering dependency is a conformance failure.

Typical classification:

| Resource | affects |
|---|---|
| authoritative XHTML | semantic, rendering |
| semantic relationship graph | semantic |
| CSS/font | rendering |
| meaningful figure image | semantic, rendering |
| mapping/fixed output/cache/annotation/control descriptor | neither |

A fixed rendition is current only when Revision ID, renditionInputDigest, and exact resource digest all verify. CSS/font-only changes keep the semantic Revision ID and semanticStateDigest, change renditionInputDigest, and stale fixed output.

---

# 72. Cycle-Free Descriptor Digest Graph

```text
resource bytes
   ↓
resource digests
   ↓
inventory
   ├── semantic projection → semanticStateDigest
   └── render projection   → renditionInputDigest

exact inventory bytes → inventory digest → state descriptor

state descriptor with descriptorDigest omitted
   → RFC 8785 JCS UTF-8
   → SHA-256
   → descriptorDigest
```

The inventory omits itself and the lifecycle state descriptor. The state binds the exact inventory bytes. `descriptorDigest` is SHA-256 of RFC 8785 JCS serialization of the parsed state object with `descriptorDigest` omitted. JCS is used only for this small closed I-JSON descriptor; it MUST NOT canonicalize XHTML, CSS, inventory resource bytes, or other content.

---

# 73. Annotation Lifecycle

Annotations are separate from authoritative semantic content. Changing an annotation alone MUST NOT create a semantic Revision ID. Every packaged annotation is inventoried and therefore a packaged annotation change invalidates a sealed state until rebound. External annotation collections MAY evolve independently and are outside the sealed package unless incorporated. Signed annotation layers are deferred.

W3C Web Annotation is normative. EPUB Annotations 1.0 is informative/monitored while a Working Draft. Compatible serialization SHOULD be maintained without normatively depending on the draft.

---

# 74. Validation and Human-Judgment Limits

Schemas validate structure, not the entire format. ZIP safety, discovery, inventory completeness, effect correctness, digests, cross-resource identity, DOM uniqueness, logical-order oracles, range bounds, page references, geometry, capability dependencies, stale state, and accessibility require procedural checks.

General intended natural-language order and semantic intent cannot always be inferred. Validators MUST distinguish `NOT_TESTED`, partial automation, and manual evaluation from PASS.

---

# 75. Specification Governance and Release Candidate Blockers

This section is informative except for the explicit release gate.

Specification editors should reuse mature standards and introduce new mechanisms only for demonstrated architectural gaps. These directives do not create document-level conformance failures.

Before Format 0.1 Release Candidate, stable project-controlled identifiers MUST replace all `https://example.invalid/spd/` schema IDs, capability IRIs, container relationship identifiers, and the StableNodeSelector vocabulary/context. No production domain is assigned in this Draft.

---

# Appendix A. Candidate-to-Draft Change Log

| Decision | Draft sections | Normative result |
|---|---|---|
| A-001 | 4, 75 | Governance moved out of document conformance. |
| A-002–A-004 | 11–15 | Canonical UUID URNs; short opaque Node/Fixed/Page tokens; current-revision versus lineage conformance. |
| A-005 | 16 | Mandatory root language pair and explicit root direction. |
| A-006–A-007, A-022 | 28–29, 70–72 | Complete inventory, effects, exact resource bytes, separate semantic/render digests, cycle-free JCS state digest. |
| A-008–A-009, A-021 | 26–27, 31, 56 | Semantic-only seal, current/stale tests, fixed without Mapping, Mapping dependency. |
| A-010–A-012 | 36, 38, 40 | Scalar ranges, finite page-local geometry without precision, exact statuses. |
| A-013–A-014, A-020 | 54, 56, 58–59 | Specification-controlled capability status and exact Accessible target. |
| A-015–A-017, A-023 | 17, 23, 42, 73–74 | Annotation scope/lifecycle and honest partial/manual evaluation. |
| A-018–A-019 | 5, 69 | Deterministic OCF link discovery and exactly one authoritative rootfile. |

All changes have architecture impact `NONE` or `CLARIFICATION`. No material architecture change is introduced.
