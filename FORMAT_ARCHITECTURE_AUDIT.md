# Standards and Architecture Audit for a Next-Generation Portable Document Format

**Audit date:** 2026-08-30  
**Status:** Architecture research only; no format or implementation is created by this document.  
**Evidence rule:** Claims about standards and projects are linked to primary specifications, project documentation, or authoritative repositories. “Not verified” is used where the available evidence does not support a firm conclusion.

## 1. Executive Summary

The proposal identifies a real integration gap, but it does **not** justify inventing a new container, markup language, page-description language, annotation model, accessibility vocabulary, cryptographic primitive, or rendering engine.

The technically defensible direction is a **hybrid conformance profile**, not a greenfield file format:

1. Use an **EPUB 3.3-compatible OCF package** as the outer container and publication model.
2. Make constrained semantic XHTML, CSS, SVG, MathML, and declared structured data the authoritative editable representation.
3. For a sealed document, include a **tagged PDF 2.0 fixed rendition** conforming to WTPDF’s reuse rules; require PDF/A-4 for an archive profile.
4. Define only three genuinely project-specific pieces: stable identity/lifecycle rules, an explicit semantic-to-fixed mapping, and a hash-linked state descriptor that says exactly which semantic state produced which fixed rendition.
5. Define agent operations in a **companion transactional API**, not as methods embedded in the file-format specification.

This conclusion is deliberately conservative. [EPUB 3.3](https://www.w3.org/TR/epub-33/) already packages structured and semantically enhanced web content, supports reflowable and fixed-layout publications, defines manifests, spines, navigation, resource fallbacks, metadata, OCF ZIP rules, fonts, scripting contexts, and XML signatures. Its [multiple-rendition note](https://www.w3.org/TR/epub-multi-rend-11/) already defines multiple renditions and cross-rendition mappings, although the W3C accessibility techniques warn that reading-system support is not broad. [PDF 2.0](https://pdfa.org/resource/iso-32000-2/), [WTPDF](https://pdfa.org/wtpdf), PDF/UA-2, and PDF/A-4 already cover exact pages, logical structure, accessibility, annotations, forms, associated files, signatures, incremental updates, and archival constraints far more deeply than the strawman acknowledges.

The core hypothesis remains plausible: an explicitly structured semantic source with persistent node identities is easier and safer for agents to edit than an arbitrary PDF. It is not universally true. A well-tagged PDF 2.0 substantially narrows the extraction and navigation gap, and many PDFs will remain better treated as immutable renditions. The claimed advantage must be demonstrated with a benchmark, not assumed.

The largest technical unknown is not ZIP packaging. It is whether two representations can remain synchronized, testably and affordably, across complex pagination, edits, Arabic/RTL shaping, annotations, signatures, and partial regeneration. A proof-of-concept should test that question before standardization.

### Bottom-line decisions

| Question | Decision |
| --- | --- |
| Is a genuinely new file format necessary? | **NO** as a new container or media stack; **HYBRID** as a narrow EPUB-compatible profile plus companion specifications. |
| EPUB relationship | Build on EPUB 3.3/OCF and remain EPUB-compatible where possible; do not fork OCF. |
| Canonical fixed representation | Tagged PDF 2.0; PDF/A-4 for archive conformance. Do not standardize restricted SVG pages in 0.1. |
| Determinism | Preserve and hash an already-generated fixed scene. Do not promise cross-engine byte-identical HTML/CSS rendering. |
| Semantic authority | Constrained XHTML plus native HTML semantics; JSON-LD only for relationships that HTML cannot express cleanly. |
| Annotations | Adopt the W3C Web Annotation Data Model with a small selector profile and stable-ID selector extension. |
| Stable identity | Random persistent IDs plus explicit lineage; never content hashes as identity. |
| Agent operations | Companion transactional API with preconditions, atomic change sets, validation, and immutable revision tokens. |
| Signatures | Reuse existing signature ecosystems; postpone a normative signature profile until expert interoperability testing. |
| Forms | Defer a full forms profile; 0.1 may preserve static HTML controls but must not promise portable calculations or workflow. |

## 2. Is a New Format Actually Necessary?

### Answer: HYBRID

A new *set of bytes with a novel extension* is not technically necessary. A new *conformance contract* is potentially useful.

The proposal overlaps heavily with three existing families:

- EPUB already supplies the web-native single-file publication and reflow model.
- PDF already supplies the reliable fixed-page, annotation, form, signature, and archival ecosystems.
- ODF already supplies a rich editable office-document model, package manifest, styles, change tracking, metadata, signatures, and forms.

No one of these makes all desired properties co-equal. EPUB does not define an authoritative-source/sealed-rendition lifecycle or a fine-grained mapping between semantic objects and a canonical PDF. PDF does not offer robust general-purpose semantic editing, even when well tagged. ODF is a mature editable office format but is not naturally a web document and does not guarantee fixed rendition identity.

The defensible innovation is therefore an integration profile:

> EPUB-compatible semantic publication + tagged PDF rendition + stable IDs + state binding + mapping + transactional API.

This could initially use `.epub` and `application/epub+zip` if it remains fully conformant. A new extension or media type should be considered only after interoperability trials show that ordinary EPUB readers mis-handle the profile or that distinguishing sealed semantics is operationally necessary. Prematurely assigning a new extension would reduce compatibility without solving a technical problem.

### Why this is not “just EPUB”

EPUB can contain reflowable and pre-paginated content, and the [multiple-rendition specification](https://www.w3.org/TR/epub-multi-rend-11/) provides rendition selection and a mapping document. But it does not establish:

- one rendition as the editable source of truth;
- a finalize/seal state machine;
- a cryptographic binding from a semantic revision to a canonical fixed rendition;
- persistent semantic identity rules across edits;
- page-level geometric mappings suitable for precise annotations and agents;
- transactional edit semantics.

Those are the candidate project contributions. Everything else should be reused.

### Why extending only Tagged PDF is insufficient

[WTPDF](https://pdfa.org/wtpdf) makes PDF 2.0 content much more reusable and accessible. PDF 2.0 structure namespaces, structure attributes, MathML integration, annotations, associated files, and structure destinations are material capabilities, not cosmetic tags. PDF can also embed a source file as an [Associated File](https://pdfa.org/resource/pdf-2-0-application-note-002-associated-files/).

However, a PDF structure tree remains coupled to a page-content object model optimized for presentation, not semantic authoring. Editing paragraphs, tables, citations, references, footnotes, and styles while preserving layout is still substantially harder than editing a schema-constrained semantic tree. Embedding HTML inside PDF would create a package-within-a-package and make the editable representation subordinate in most tooling. It is a viable distribution architecture, but not the best primary model for this project.

### Decision gate before standardization

Proceed only if a prototype proves all of the following:

1. The semantic-to-fixed map survives representative edits without widespread invalidation.
2. Arabic/RTL, Indic, CJK, emoji, variable fonts, and color fonts reproduce acceptably in the sealed rendition.
3. Agent tasks materially outperform WTPDF on correctness and corruption rate.
4. EPUB-compatible packaging does not create unacceptable reader behavior.
5. Maintaining semantic and fixed representations is operationally simpler than distributing source plus PDF as two ordinary files.

## 3. Existing Standards Landscape

| Layer | Mature basis | What it already provides | Remaining gap |
| --- | --- | --- | --- |
| Container | EPUB OCF / ODF ZIP profile / OPC | ZIP constraints, MIME identification, manifests, package paths, signatures conventions | State binding and project-specific capability declarations |
| Publication | EPUB 3.3 | Manifest, spine, navigation, metadata, resources, fallbacks, reflow/fixed layout | Authoritative rendition and seal lifecycle |
| Semantic content | HTML, MathML, SVG | Native document semantics and broad tooling | Academic/office constructs need a constrained authoring schema |
| Accessibility | HTML, WAI-ARIA, DPUB-ARIA, EPUB Accessibility, PDF/UA | Roles, names, relationships, discoverability, conformance | Profile-specific mapping validation |
| Semantic graph | JSON-LD/RDF | Identified nodes and extensible relationships | Avoiding duplicate or contradictory semantics |
| Fixed pages | PDF 2.0, WTPDF, PDF/A | Exact page scene, tagged structure, fonts, annotations, signatures, archival profiles | Binding to authoritative semantic revision |
| Alternative fixed pages | OpenXPS | FixedPage hierarchy, resources, print-oriented packaging | Weak cross-platform ecosystem compared with PDF |
| Annotation | W3C Web Annotation | Body/Target, motivations, selectors, states, collections | Stable-node selector and sealed-page anchoring profile |
| Integrity | SHA-2, JCS, XML Signature, JWS, COSE, CMS/CAdES, ASiC | Digests, signature envelopes, timestamps, multi-file signatures | A single interoperable profile and precise mutation policy |
| Preservation | PDF/A, BagIt, PREMIS, OAIS | Rendering constraints, checksums, preservation metadata and process concepts | A tested archive conformance profile |
| Agent editing | DOM/editor models, HTTP preconditions, revision tokens | Structured mutation concepts and optimistic concurrency patterns | Standard operation semantics and benchmark |

The [W3C Publication Manifest](https://www.w3.org/TR/pub-manifest/) is also relevant: it models a publication using schema.org-aligned JSON-LD metadata and exposes a normalized internal representation, but does not define an agent API or sealed rendition lifecycle.

## 4. PDF / WTPDF Analysis

### What modern PDF already solves

The project would underestimate PDF if it treated it as merely a bag of drawing commands. PDF 2.0 can provide:

- stable indirect object identity within a file revision;
- page trees and exact page geometry;
- logical structure trees with namespaces, attributes, marked-content references, and alternate text;
- annotations with page locations, appearances, replies, states, and rich subtypes;
- AcroForms with field hierarchies, widgets, values, calculations, and signature fields;
- embedded and associated files with semantic relationships;
- XMP metadata;
- incremental updates that preserve prior bytes;
- byte-range digital signatures, certification signatures, modification permissions, timestamps, and long-term validation profiles;
- archival restrictions through PDF/A;
- accessibility through PDF/UA.

[WTPDF](https://pdfa.org/wtpdf) is particularly important. It specifies Tagged PDF 2.0 for reuse and accessibility, aligns its accessibility conformance level with PDF/UA-2, and adds detailed requirements for structure types, attributes, annotations, MathML, artifacts, structure destinations, and associated files. The [Tagged PDF Q&A](https://pdfa.org/resource/tagged-pdf-q-a/) explains that WTPDF is specifically intended to make content reliably reusable, not only accessible.

PDF incremental updates are a mature answer to “change without rewriting everything.” New and changed objects are appended, preserving old bytes; signed PDFs depend on this property. The historical Adobe reference documents the mechanism and its signature relationship, while ISO 32000-2 is the current normative basis. This does not make PDF semantic editing easy, but it does solve revision preservation better than a naive ZIP rewrite.

### Limits relevant to this proposal

- A structure tree can describe reading order and semantics, but content streams remain presentation-centric and may contain fragmented or reused text operators.
- Indirect object numbers are not durable semantic identity across optimization, conversion, or full rewrite.
- Tagged PDF quality varies widely; the standard permits capability that real authoring tools may not produce.
- AcroForm behavior, appearances, and JavaScript support differ across readers.
- Incremental updates preserve historical bytes but also preserve superseded or hidden data, complicating privacy and redaction.
- PDF signatures are mature but complex; certification permissions and later annotations require careful policy and reader interoperability testing.
- Associated Files are useful but effectively a flat attachment model; they do not replace a structured authoring package.

### PDF profiles

- **PDF/UA-2 / WTPDF:** adopt as the accessibility/reuse target for fixed renditions.
- **PDF/A-4:** require for an archive profile. The [PDF standards index](https://pdfa.org/pdf-standards/) identifies PDF/A-4 as the PDF 2.0 archival profile. PDF/A requires key rendering resources such as fonts, images, and color profiles to be embedded, but archival policy still has to address external semantic links and embedded non-PDF resources.
- **PDF/A-4f:** use when the archival PDF itself embeds associated source or data files. The Library of Congress warns that arbitrary embedded files create separate preservation-policy obligations; inclusion does not magically make the attachment archival.
- **AcroForms:** export target and conceptual reference, not the 0.1 source forms model.

### Recommendation

Use PDF as the canonical fixed rendition, not as the authoritative editable source. Require WTPDF reuse conformance for sealed renditions where feasible; require PDF/UA-2 when accessibility is claimed; require PDF/A-4 for archive conformance. Do not invent a second digital-signature ecosystem if PDF signatures already cover the final fixed artifact.

## 5. EPUB Analysis

### Coverage

[EPUB 3.3](https://www.w3.org/TR/epub-33/) is already a single-file ZIP container for semantically enhanced web content. It defines:

- OCF ZIP and `mimetype` identification;
- one or more package documents;
- a resource manifest and spine;
- XHTML and SVG content documents;
- reflowable and pre-paginated/fixed-layout presentation;
- navigation documents;
- Dublin Core and refinable metadata;
- media overlays;
- core media types, foreign-resource fallbacks, and font embedding/obfuscation;
- scripting contexts and processing restrictions;
- optional XML signatures in `META-INF/signatures.xml`.

[EPUB Accessibility 1.1](https://www.w3.org/TR/epub-a11y-11/) is a W3C Recommendation tied to WCAG and accessibility-discovery metadata. EPUB Accessibility 1.2 was a Candidate Recommendation in July 2026; it should be monitored but not made normative in Format 0.1 until Recommendation status.

### Fixed layout and multiple renditions

EPUB fixed layout can be pixel precise, but it is not a promise of permanent page-identical rendering. Reading systems may override styles because of user preferences, and implementation differences remain. Fixed-layout XHTML/SVG works for many books and comics, but is not an archival scene contract.

The [EPUB Multiple-Rendition Publications 1.1](https://www.w3.org/TR/epub-multi-rend-11/) note is extremely close to this proposal. It allows multiple package documents, identifies reflowable versus pre-paginated renditions, and defines cross-rendition mapping points. However, the [EPUB Accessibility Techniques](https://www.w3.org/TR/epub-a11y-tech-11/) explicitly state that multiple-rendition support is not broadly implemented. This is a specification/implementation gap the project must not conceal.

### Scripting

EPUB permits scripting and defines container-constrained and spine-level contexts. The [reading-system requirements](https://www.w3.org/TR/epub-rs-33/) make support conditional in places and allow additional restrictions such as blocking networking. For this project, arbitrary JavaScript should be prohibited in the core and sealed profiles. Merely inheriting EPUB’s scripting rules would be inconsistent with deterministic rendering and an untrusted-document threat model.

### Signatures

EPUB OCF can sign any or all package files using XML Signature references. The specification itself warns that a signature does not prevent tampering if a reading system does not check it. The mechanism is reusable, but real-world validation and long-term-signature support are not comparable to mature PAdES deployments. A project signature profile should therefore be postponed until conformance tests exist.

### Four classification options

| Option | Assessment |
| --- | --- |
| EPUB profile | Best starting point. Maximum tooling and container reuse; requires strict restrictions and new state/mapping metadata. |
| EPUB extension | Necessary only for sealed-rendition declarations, mapping, and state binding; keep extension vocabulary narrow. |
| EPUB-derived format | Avoid. It inherits complexity but loses reader compatibility and the benefit of an established media type. |
| Independent format | Unjustified unless EPUB conformance prevents essential security or lifecycle rules. No such blocker has been verified. |

### Recommendation

Implement the 0.1 specification as a **strict EPUB 3.3 profile with a small extension vocabulary**. Preserve a valid EPUB navigation document and default semantic rendition so ordinary readers have useful fallback behavior. Treat EPUB 3.4 as informative work-in-progress only; as of this audit it is a Working Draft expected to become a Recommendation later.

## 6. OpenXPS Analysis

[ECMA-388 OpenXPS](https://ecma-international.org/publications-and-standards/standards/ecma-388/) defines a paginated document using XML, Unicode, ZIP, Open Packaging Conventions, fixed pages, resources, and package digital signatures. It is a serious precedent for a self-contained fixed-page scene.

Concepts worth reusing:

- explicit document-sequence, document, and page relationships;
- per-page resource dependencies;
- fixed coordinate systems and page dimensions;
- embedded/obfuscated font handling;
- separation between package relationships and rendered content;
- print-oriented resource completeness;
- a declarative fixed-page grammar rather than executable content.

Weaknesses for this project:

- it is fixed-layout-first, not semantic-source-first;
- its ecosystem and web support are far smaller than PDF’s;
- adopting it adds OPC and XML vocabularies beside EPUB/HTML without removing the need for PDF export;
- accessibility and semantic reuse are not as central or broadly deployed as WTPDF/PDF/UA;
- cross-platform renderer availability is limited.

Recommendation: reuse architectural ideas, not the format. OpenXPS is evidence against inventing a custom page scene: an open, standardized, packaged fixed-page language already exists and still did not displace PDF.

## 7. ODF Analysis

[ODF 1.4](https://docs.oasis-open.org/office/OpenDocument/v1.4/) is a mature editable-document family. Its package specification defines `META-INF/manifest.xml`, MIME types, encryption metadata, RDF package metadata, and XML digital signatures. Its schema covers styles, office text, tables, forms, metadata, tracked changes, and many document constructs that HTML does not model natively.

### Concepts preferable to the strawman

- **Named and automatic styles:** clearer authoring semantics than unrestricted CSS cascading for office editing.
- **Package manifest:** one authoritative inventory with media types instead of separate ambiguous `manifest.json` files.
- **Change tracking:** a standardized representation exists, although ODF 1.4 itself notes prior under-specification and interoperability variation.
- **Form model and values:** richer than raw HTML forms.
- **Metadata manifests:** explicit relationships among metadata and package files.
- **Foreign-element extensibility:** namespace rules are mature and preserve unknown content.
- **Formula language:** OpenFormula solves spreadsheet calculation; it should not be reinvented.

### Why not simply use ODF

ODF is optimized for office suites and XML processing, not browser-native display. Its style and layout model is large, its web rendering is not native, and fixed pagination still depends on an office layout engine. Adopting it would exchange HTML/CSS complexity for ODF/LibreOffice complexity and weaken the responsive-web proposition.

### Recommendation

Keep XHTML as the semantic serialization, but borrow ODF disciplines: a single normative package inventory, explicit style classes/tokens for authoring, extension preservation, and carefully specified change records. Do not copy ODF’s complete schema or forms model into 0.1.

## 8. Web Platform Analysis

### Strengths

HTML, CSS, SVG, MathML, Unicode, and web fonts provide unmatched rendering reach, accessibility integration, internationalization, and authoring tools. Native HTML semantics should remain the primary meaning layer. MathML should remain actual MathML. Vector figures should remain SVG where safe. Text should remain Unicode logical-order text in the semantic source.

### Pagination maturity

[CSS Paged Media Level 3](https://www.w3.org/TR/css-page-3/) defines page boxes, page size, orientation, margins, and margin content. [CSS Fragmentation](https://www.w3.org/TR/css-break-3/) defines breaks, widows, orphans, and fragmentation behavior. [Generated Content for Paged Media](https://www.w3.org/TR/css-gcpm-3/) addresses running heads, footnotes, and page-oriented generated content, but is still a Working Draft and contains unresolved algorithmic questions. The standards are sufficient for high-quality implementations, but not sufficient to guarantee that independent implementations paginate identically.

### Why HTML/CSS rendering is not permanently deterministic

Even with identical source bytes, output can vary with:

- browser engine and version;
- font bytes, font sanitizer, hinting, shaping engine, and fallback selection;
- Unicode and line-breaking data versions;
- device scale and rasterization;
- image decoding and color management;
- hyphenation dictionaries and language tagging;
- default style sheets and unsupported CSS;
- rounding and fragmentation algorithms;
- platform accessibility or user preference overrides.

Pinning a browser build and its complete environment can make a build reproducible in a controlled system. It does not create an engine-independent archival rendering rule.

### Semantics versus supplemental data

Use HTML for headings, sections, paragraphs, lists, tables, figures, captions, links, quotations, code, emphasis, forms, and language/direction. Use MathML for mathematics and SVG for vector graphics. Use ARIA only where native HTML cannot express the role or state. Use JSON-LD for cross-document entities, citations, provenance, datasets, and relationships that are not naturally hierarchical.

Duplicating a heading, table, or caption in `graph.jsonld` creates two truths and should be prohibited. Supplemental graph statements should point to HTML node IDs and must not redefine native text content.

### Recommendation

Profile HTML/CSS; do not freeze a browser engine in the format. Use a pinned renderer only as an implementation/reproducible-build technique. On finalization, preserve the generated fixed scene as PDF.

## 9. Semantic & Accessibility Standards

### Native-first rule

The precedence should be:

1. Native HTML semantics.
2. HTML attributes such as `lang`, `dir`, `headers`, `scope`, `alt`, and accessible names.
3. WAI-ARIA only to fill a real semantic gap.
4. [DPUB-ARIA 1.1](https://www.w3.org/TR/dpub-aria-1.1/) for publishing roles such as footnotes, endnotes, and bibliographic structures when native HTML lacks a role.
5. JSON-LD for non-tree relationships and external identities.

ARIA must not be used to repair invalid structure or override correct native semantics. Accessibility conformance must test keyboard navigation, name/role/value exposure, reading order, language/direction, alternative text, tables, equations, and fixed-rendition tagging.

### JSON-LD and RDF

[JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) is appropriate for a small relationship graph. Use absolute IRIs for external entities and stable document-local identifiers for package nodes. Avoid blank nodes for anything that must be annotated, revised, or externally referenced. Do not require a general RDF reasoner in a core reader.

### Schema.org

Use schema.org terms for publication metadata where their meaning is exact and interoperable. Do not use schema.org as a document-structure language. Dublin Core remains the EPUB package baseline.

### Accessibility profiles

The Accessible capability should require EPUB Accessibility conformance for the semantic rendition and PDF/UA-2/WTPDF accessibility conformance for a sealed fixed rendition. Passing one does not prove the other. The mapping validator must also test that every non-artifact fixed object is traceable to an accessible semantic node or explicitly justified.

## 10. Annotation Analysis

The [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/) should be adopted, not recreated. It already defines Annotation, Body, Target, motivations, agents, lifecycle metadata, collections, and selectors including FragmentSelector, TextQuoteSelector, TextPositionSelector, SVGSelector, and RangeSelector.

### Profile recommendation

Require every annotation to have:

- a stable annotation ID;
- at least one motivation;
- a body or a body purpose;
- a target with a source revision identifier;
- a creator/generator distinction where machine-generated;
- creation time and optional modification time;
- one robust selector and, where practical, one fallback selector.

Recommended selector order:

1. **StableNodeSelector** — a small extension naming a semantic node ID and optional logical text range.
2. **TextQuoteSelector** — exact text plus prefix/suffix for re-anchoring.
3. **TextPositionSelector** — useful but brittle after edits; define offsets over Unicode scalar values in a specified normalized text projection.
4. **FixedPageSelector** — page ID plus a list of quadrilaterals or paths in the canonical page coordinate space.
5. SVGSelector only for genuinely non-rectangular regions.

The extension is needed because Web Annotation has no normative concept of the project’s persistent semantic object identity or a sealed-rendition state hash. The existing model can carry these selectors cleanly; the overall annotation model does not need extension.

### Post-signature annotations

Annotations added after sealing must be stored as a new package revision or external annotation collection. They must not silently alter the signed fixed rendition. A signature policy may sign: (a) content only, (b) content plus existing annotations, or (c) a later annotation layer. The UI must distinguish these states.

## 11. Rendering and Pagination Analysis

### Define “deterministic” precisely

These are different requirements:

| Level | Definition | Reasonable target? |
| --- | --- | --- |
| D1: byte-identical renderer output | Same output bytes, object ordering, compression, metadata, and timestamps | Only in a pinned reproducible toolchain; not across independent renderers |
| D2: identical pagination | Same page count and break locations | Possible for a strict renderer/version profile; difficult across engines |
| D3: visually identical pages | Same perceived appearance | Testable by raster comparison with tolerances; not byte identity |
| D4: geometrically equivalent | Objects and glyphs fall within declared coordinate tolerances | Practical conformance target for independent fixed renderers |
| D5: preserved fixed scene | The already-generated page scene is stored and its bytes/digests are preserved | Strongest portable guarantee and the recommended meaning of “sealed” |

Format 0.1 should promise **D5** for a sealed document. It may define D3/D4 comparison metrics for renderer testing. It must not claim D1 or D2 for arbitrary HTML/CSS engines.

### Approach comparison

| Approach | Strength | Failure mode | Decision |
| --- | --- | --- | --- |
| A. Required reference browser | Reproducible within a pinned build | Engine is huge, evolves, and couples format lifetime to a binary | POSTPONE as build profile, not file semantics |
| B. Fully specified HTML/CSS subset | Interoperable in principle | Text layout, fonts, fragmentation, and rasterization remain large; subset becomes a new browser spec | REJECT as determinism strategy |
| C. Generate canonical fixed pages | Separates authoring from preservation | Two representations must stay synchronized | ADOPT |
| D. Store semantic plus fixed scene | Supports reflow, editing, exact pages, and verification | Package size and lifecycle complexity | ADOPT for sealed profile |
| E. PDF canonical rendition | Mature rendering, print, tagging, signatures, archival | PDF generation/tagging quality varies | ADOPT |
| F. SVG pages | Web-native and inspectable | Text and filter support vary; multi-page, printing, signatures, and archival ecosystem weaker | POSTPONE |
| G. OpenXPS-like pages | Declarative and print-oriented | Limited ecosystem and duplicates an existing standard | REJECT for 0.1 |
| H. Minimal custom scene | Could be precisely constrained | Creates a renderer, font model, accessibility mapping, and decades of compatibility burden | REJECT |

### Reproducible rendering profile

A future reproducible-build profile may record renderer name/version, operating-system-independent font set, shaping library/version, Unicode data version, hyphenation dictionaries, color-management configuration, input-resource hashes, environment variables that affect output, and a canonical invocation. This metadata is useful provenance, but readers should render the stored PDF without needing that historical toolchain.

### Pagination acceptance tests

Conformance tests should include nested fragmentation, tables spanning pages, floats, footnotes, running headers, named pages, widows/orphans, multi-column layouts, transforms, vertical writing, and mixed Arabic/Latin text. Browser print output, Paged.js, Vivliostyle, and WeasyPrint should be compared against the same fixtures; differences should be recorded, not averaged away.

## 12. Canonical Fixed Representation Analysis

### Candidate comparison

| Representation | Text fidelity | Search/accessibility | Ecosystem | Archival/signing | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Tagged PDF 2.0 | Excellent when fonts and glyph mapping are correct | Strong with WTPDF/PDF/UA | Dominant | Strongest | **Use** |
| Restricted SVG pages | Good but implementation-dependent | Searchable text possible; page semantics need external model | Broad display, weak document workflow | Weak/fragmented | Do not standardize in 0.1 |
| OpenXPS FixedPage | Strong | Structured but less deployed | Mostly Windows/print | Standardized but narrow | Reference only |
| Positioned HTML | Depends on browser/font environment | DOM accessible | Broad | Weak as permanent scene | Not canonical |
| Canvas/Skia display list | Renderer-efficient | Semantics generally absent | Implementation-internal | No stable interchange contract | Reject |
| Custom vector graph | Controllable | Must invent everything | None | None | Reject |

### Text representation choices

| Text strategy | Advantages | Costs/risks |
| --- | --- | --- |
| Embedded font + Unicode text | Small, searchable, copyable, accessible; reshaping possible | Viewer/font stack can choose subtly different glyphs unless fixed output stores glyph choices |
| Positioned glyph IDs + embedded font | Preserves advances and glyph choice; handles Arabic shaping and ligatures | Glyph IDs are font-file-specific; must retain logical Unicode mapping and cluster order |
| Glyph outlines + invisible Unicode text | Maximum visual stability | Large files, harder editing, weaker text fidelity, duplicated hidden text, accessibility risk |
| Fully vectorized text only | Stable appearance | Loses text semantics, search, copy/paste, and accessibility; very large | 

The recommended PDF rendition should store embedded/subset fonts, positioned glyph runs, and correct ToUnicode/ActualText mappings plus WTPDF structure. Outlining text should be forbidden for ordinary text in Accessible and Archive profiles except documented exceptional glyphs. Invisible replacement text must not be used to conceal a visually different content stream.

### Semantic-to-fixed mapping model

A single rectangle per node is inadequate. A paragraph can span pages and columns; a selection can consist of disjoint line fragments; a table row can split; a rotated label needs a transform; and a footnote has both a call and a body. The mapping should be a revision-bound set of **fragments**, not one bounding box.

Each mapping record should identify:

- semantic Document ID, Revision ID, and Node ID;
- fixed-rendition digest and stable page ID, not only a mutable page number;
- fragment kind: block, line, text range, glyph cluster, image, vector region, table cell, note call, note body, artifact, or link target;
- logical text start/end over the profile’s normalized Unicode text projection;
- page coordinate system, page box, units, origin, and applicable transform matrix;
- ordered quadrilaterals for normal multi-line text, or a closed path for irregular/curved geometry;
- clipping path when the visible region differs from the object geometry;
- fragment reading-order index and occurrence index;
- optional PDF structure-element/object reference for diagnostics, never as the sole persistent identity;
- confidence/evidence only for imported or inferred mappings.

Rules by content type:

- **Text:** map logical Unicode ranges to ordered line quadrilaterals and, where needed, glyph clusters. For bidi text, range order is logical while quadrilateral order carries visual placement. Never infer logical order from x-coordinates.
- **Tables:** give the table, row groups, rows, and every cell stable IDs and separate fragments. Spanning cells list all page fragments. Header relationships remain semantic, not geometric.
- **Figures/SVG:** map the figure/caption separately; map subregions only when they have semantic IDs. Preserve the composed transform and clip.
- **Footnotes/endnotes:** map the reference/call and note body as distinct related nodes; page placement does not change semantic parentage.
- **Multi-column flow:** fragment order records reading order independently from geometric left/right order, which is essential for RTL layouts.
- **Artifacts:** page numbers, running heads, crop marks, and decorative objects are explicitly classified so they are not mistaken for semantic duplicates.

Mappings are immutable for a sealed revision. Any semantic edit marks the mapping and fixed rendition stale; a finalize transaction regenerates both atomically. The validator should report node coverage, text-range coverage, overlapping/conflicting ranges, unmapped non-artifact PDF content, and semantic nodes with no visible or declared nonvisual representation.

### Arabic, bidi, and complex scripts

Arabic is a core conformance axis. The semantic source must keep Unicode in logical order, set `lang` and `dir` correctly, and follow the [Unicode Bidirectional Algorithm](https://www.unicode.org/reports/tr9/) and [CSS Writing Modes](https://www.w3.org/TR/css-writing-modes-3/). The fixed rendition must preserve:

- the exact embedded font bytes or archival-permitted subset;
- glyph IDs, positions, advances, offsets, and variation coordinates;
- character-to-glyph cluster mapping, including many-to-one ligatures and one-to-many marks;
- logical Unicode extraction order, not merely visual glyph order;
- bidi embedding/isolate boundaries and paragraph base direction;
- diacritic and kashida positioning;
- ToUnicode/ActualText sufficient for correct copy, search, and accessibility.

Tests must mix Arabic, Latin, European/Arabic-Indic digits, punctuation, URLs, equations, table cells, footnotes, and rotated labels. Similar tests are required for Indic clusters, CJK vertical text, emoji sequences, OpenType variations, and COLR color glyphs. The [SVG 2 text model](https://www.w3.org/TR/SVG2/text.html) itself notes that font and layout capabilities vary across software, which is another reason not to use generic SVG text as the archive guarantee.

### Recommendation

Use tagged PDF 2.0 as the canonical fixed representation. Define a generation conformance report that records font embedding, text extraction checks, structure validation, and semantic-map coverage. Archive conformance upgrades the PDF to PDF/A-4 and adds preservation metadata.

## 13. Stable Identity and Editing Model

### Identity model

Use three scopes:

- **Document ID:** a UUID identifying this document lineage.
- **Revision ID:** an immutable digest or UUID for one semantic state.
- **Node ID:** a persistent, document-local identifier for an addressable logical object.

Random UUIDv4 or time-sortable [UUIDv7](https://www.rfc-editor.org/rfc/rfc9562/) values are suitable. For HTML ergonomics, serialize node IDs as an ASCII, CSS-safe form such as `n_` plus lower-case base32 UUID bytes. Do not derive IDs from text, DOM paths, order, page number, or content hashes: all of those change during normal editing.

### What “same logical object” means

Sameness is the editor’s assertion that an object continues the same authorial role through a revision. It is not string equality. Changing all words in a paragraph may retain identity; copying the paragraph creates a distinct identity.

Format-level rules:

- IDs are unique within the document lineage and immutable for a continuing node.
- Deleted IDs are tombstoned and never reused.
- Copied/imported nodes receive new IDs unless a deliberate document merge preserves a declared lineage.
- A clone of the whole document receives a new Document ID and may record `derivedFrom`; it must not create two live documents claiming the same lineage.
- Cross-document references use a document identifier plus node identifier, not a bare HTML fragment.
- A revision records parent revision(s), enabling branch/merge provenance without requiring a full editor history.

Editor-behavior recommendations, not Format 0.1 mandates:

- On split, one result retains the original ID according to the user’s edit focus or a deterministic editor policy; other results get new IDs and declare `splitFrom`.
- On merge, one surviving node retains an ID; retired IDs declare `mergedInto`.
- Copy/paste always mints IDs at the destination and may retain `copiedFrom` provenance.
- Import/export preserves IDs only when the target format can carry them losslessly and the export is declared identity-preserving.

### HTML sufficiency

HTML is sufficient for ordinary narrative structure, tables, figures, equations, code, links, quotations, lists, and basic forms. It becomes awkward for:

- page master semantics, running headers/footers, and intentional page-break objects;
- sophisticated footnote/endnote placement;
- tracked changes spanning arbitrary tree ranges;
- citation databases and reference-resolution state;
- generated cross-references and numbering;
- repeated content, fields, and conditional content;
- complex office layouts and section-specific page styles.

The answer is not to replace HTML with arbitrary JSON. Define a constrained **authoring schema over XHTML** with explicit elements/attributes or referenced data for footnotes, citations, cross-references, page intentions, and change marks. The normalized editor model can be a ProseMirror-style typed tree, but XHTML remains the interchange serialization.

### Competing editable models

| Model | Strength | Weakness | Role |
| --- | --- | --- | --- |
| DOM/HTML | Native rendering, accessibility, interchange | Mutation permissive; invalid states easy | Canonical serialization |
| ProseMirror document model | Schema-constrained transactions and collaboration | Not a standardized file format; custom nodes needed | Recommended editor model |
| ODF XML | Rich office semantics and styles | Large, web-hostile, pagination engine dependent | Source of concepts/import target |
| DOCX WordprocessingML | Extremely rich and deployed | Huge, compatibility-driven, complex licensing/spec surface | Import/export only |
| Markdown AST | Simple and agent-friendly | Loses layout, tables, notes, change tracking, rich semantics | Authoring input only |
| Custom JSON tree | Easy API integration | Reinvents HTML serialization and accessibility mapping | Reject as second source of truth |

## 14. AI-Agent Architecture Analysis

### When the central hypothesis is true

The semantic-first format is substantially easier and safer than PDF when:

- nodes have valid roles and persistent identities;
- tables use real row/cell structure and explicit headers;
- references, citations, notes, figures, and captions are explicit relationships;
- the agent edits through validated typed operations;
- revision tokens prevent lost updates;
- rendering and validation occur after every transaction;
- converters distinguish asserted from inferred semantics.

### When the advantage shrinks

- A WTPDF document may already expose reliable headings, lists, tables, math, artifacts, links, and reading order.
- A source document with malformed HTML, CSS-generated content, duplicated JSON-LD, or editor-specific conventions can be harder than a well-tagged PDF.
- Visual edits such as moving a precisely positioned callout may be more natural in PDF/page coordinates.
- Scanned/image PDFs require OCR and inference regardless of packaging.

### Where the API belongs

Split responsibilities:

- **Format standard:** node identity, revision identity, validation invariants, package state, mapping, and provenance fields.
- **Companion Agent API:** query and mutation operations, error model, transactions, preconditions, diff/patch representation, and rendering jobs.
- **SDK bindings:** language-specific method names such as `getNode` or `replaceText`.

Embedding method names in the file format would freeze one programming model and confuse stored data with processor behavior.

### Required transaction semantics

An agent change set should contain:

- base document/revision ID;
- one or more typed operations;
- node-level expected hashes or versions where useful;
- declared intent and agent identity;
- atomic commit semantics;
- schema, link, accessibility, and security validation;
- a resulting immutable revision ID;
- a machine-readable conflict report on failure.

Hashes/version tokens should be mandatory at the transaction or revision level and supported at node level. A node hash is a concurrency precondition, not its identity. Multi-node changes such as “update a table cell and all references” must commit atomically.

### Provenance

Minimal provenance belongs in the package only for committed revisions: who/what generated a revision, time, parent revision, tool identity/version, and optional human approval. Prompt transcripts, model chain-of-thought, and proprietary service logs do not belong in the portable format. Detailed audit trails may be external or an optional signed provenance extension.

### Measurable claim

Success is not “the model understood the document.” It is a statistically significant improvement over tagged and untagged PDF baselines in task accuracy, unrelated-content corruption, accessibility preservation, layout preservation, and human repair time. Section 25 specifies the benchmark.

## 15. Forms

### Standards comparison

| Model | Strengths | Problems for this project |
| --- | --- | --- |
| HTML forms | Native semantics, accessibility, broad widgets, basic constraint validation | Submission/network assumptions; calculations and repeating groups need script |
| PDF AcroForms | Mature fixed-page fields, widgets, values, signatures | Appearance and JavaScript interoperability vary; semantic data model is limited |
| XForms | Declarative data/model/view split, constraints, calculations, relevance, repeats | Limited browser deployment; XML/XPath stack is heavy |
| ODF forms | Office integration and richer controls | Coupled to ODF and suite behavior |
| JSON Schema 2020-12 | Strong portable data validation vocabulary | No standard UI/layout, calculation, or workflow semantics |
| JSON Forms and similar projects | Schema-driven UI patterns | Not one mature cross-document standard; implementation-specific |

[HTML constraint validation](https://html.spec.whatwg.org/multipage/form-control-infrastructure.html) handles required fields, types, patterns, ranges, and custom validity APIs. [XForms](https://www.w3.org/TR/xforms20/) demonstrates a much richer declarative design with separate instance data, constraints, calculations, conditional relevance, and repeating structures. [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) is the best reusable value-schema layer, but it is not a forms UI standard.

### Recommendation

Defer a normative Forms capability to 0.2+. In 0.1:

- preserve safe static HTML form controls and labels if present;
- allow a clearly separated template state and filled-value dataset;
- prohibit automatic submission and network access;
- do not standardize calculations, conditional visibility, repeats, or workflows;
- export to AcroForms only as a potentially lossy conversion with a conformance report.

A later profile should use HTML for presentation, JSON Schema for values, and a very small declarative expression language selected only after evaluating XForms and existing safe-expression standards. It must define whether signatures cover the template, values, appearances, or all three.

## 16. Integrity and Digital Signatures

### Separate four concepts

1. **Content digest:** detects changed bytes.
2. **State binding:** proves that fixed rendition F was generated from semantic revision S.
3. **Digital signature:** authenticates a digest/state using a key.
4. **Long-term validation:** preserves certificates, revocation evidence, policy, and trusted timestamps.

Conflating them will produce signature confusion.

### Technology comparison

| Technology | Strength | Weakness | Fit |
| --- | --- | --- | --- |
| EPUB/ODF XML Signature | Already defined for OCF packages; partial file signatures | XML canonicalization/transforms are complex; reader verification is uncommon | Reuse candidate, interoperability test required |
| JWS (RFC 7515) | Web/JSON tooling, detached payloads, multiple JSON signatures | Does not canonicalize arbitrary JSON; X.509/LTV needs a profile | Good simple signature envelope |
| COSE (RFC 9052) | Compact, algorithm-agile, embedded/WASM friendly | CBOR toolchain less natural for XHTML/JSON package; certificate/LTV conventions still need profiling | No automatic advantage |
| XML Signature | Rich reference/transform model and existing OCF usage | Signature wrapping, transform, and canonicalization complexity | Do not design new uses beyond a strict profile |
| CMS/CAdES | Mature certificate, timestamp, and long-term ecosystem | ASN.1 complexity; browser APIs weaker | Best long-term-signature foundation |
| PDF/PAdES | Mature for the fixed artifact, incremental co-signing and timestamps | Covers PDF, not automatically the outer semantic package | Adopt for sealed PDF signatures |
| ASiC | ZIP container supporting CAdES/XAdES signatures and later signatures/timestamps | Nesting ASiC and EPUB may be awkward; profile complexity | Study for package signature profile |

[RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html) can canonicalize I-JSON, but it should be used only for a small state descriptor, not HTML, CSS, SVG, or the whole ZIP. Hash the exact bytes of every package entry. A canonical state descriptor then lists normalized paths, media types, byte lengths, and SHA-256 digests. Its own JCS bytes can be signed.

### Proposed non-signature integrity model for 0.1

- One authoritative package inventory.
- SHA-256 over the exact uncompressed bytes of every normative entry.
- A canonical semantic revision digest derived from that inventory’s semantic subset.
- A fixed-rendition digest and map digest.
- A state assertion binding semantic revision, renderer provenance, fixed rendition, and mapping.
- Unknown/unlisted normative files are an error; explicitly non-normative caches and signatures are excluded by rule.

This resembles the checksum discipline of [BagIt RFC 8493](https://www.rfc-editor.org/rfc/rfc8493.html) without turning the document into a BagIt bag.

### Mutation and co-signing policy

- Editing semantic content after sealing creates a new unsealed revision; the old fixed rendition remains historical or is removed by an explicit compaction operation.
- Adding a signature must not alter the bytes covered by earlier signatures.
- Adding an annotation after content signing creates a separately signed annotation layer or a new document revision.
- Verifiers must display *what* was signed: semantic state, fixed rendition, annotations, form values, or package metadata.
- Offline validation requires the signer certificate chain and applicable validation material; long-term profiles require RFC 3161-compatible timestamps and archival evidence.

### Recommendation

Define digest/state binding in 0.1. Keep PDF signatures available for the fixed rendition. **Postpone a normative outer-package signature profile** until prototypes compare strict EPUB XML Signature, detached JWS, CMS/CAdES, and ASiC for co-signing, certificate support, timestamps, and browser/WASM validation. COSE should not be chosen merely because it is modern.

## 17. Archival Architecture

An archive claim must cover more than “the ZIP has hashes.” [PDF/A-4](https://pdfa.org/pdf-standards/) is the correct fixed-rendition basis. [BagIt](https://www.rfc-editor.org/rfc/rfc8493.html) contributes complete inventories and checksums. [PREMIS](https://www.loc.gov/standards/premis/) provides implementable preservation metadata for objects, events, rights, and agents. [OAIS ISO 14721:2025](https://www.iso.org/standard/87471.html) is a repository/reference model, not a file format to embed wholesale. WARC is relevant only when preserving fetched web transactions; it is not a general document container.

### Credible future Archive profile

Require:

- sealed tagged PDF/A-4 rendition;
- all fonts required by both semantic preview and PDF embedded with clear licensing rights;
- ICC color profiles and no uncontrolled device-dependent color where PDF/A disallows it;
- no executable content, encryption, or external rendering dependencies;
- complete exact-byte inventory with approved digests;
- self-contained Unicode, language, direction, and accessibility metadata;
- format/version identifiers for every asset;
- preservation event metadata for finalization, validation, migration, and signature renewal;
- documented renderer and shaping provenance;
- validation reports from at least two independent validators where available;
- optional BagIt wrapper at repository ingest rather than inside every end-user document.

Archive 0.1 should be a research profile, not a marketing promise. Long-term preservation also depends on repositories, migration policy, fixity checking, and designated-community requirements.

## 18. Security Threat Model

Assume every package and nested resource is hostile.

### Package and parser threats

| Threat | Required default |
| --- | --- |
| ZIP bomb / extreme compression ratio | Limit total expanded bytes, per-entry bytes, entry count, ratio, CPU time, and nesting |
| Path traversal / ambiguous paths | Reject absolute paths, drive prefixes, `..`, backslashes, NULs, duplicate normalized names, and Unicode-normalization collisions |
| Duplicate ZIP entries | Reject; never use “first wins” or “last wins” ambiguity |
| Malformed central/local headers | Require consistency and fail closed |
| XML entity expansion / XXE | Disable DTDs and external entities; cap depth and attributes |
| Huge DOM / deep nesting | Enforce node, depth, text, CSS rule, selector, and table-size limits |
| Parser differentials | Canonical path/media rules; differential fuzzing across implementations |

### Active-content threats

- Prohibit JavaScript, event-handler attributes, plugins, iframes, service workers, custom elements requiring script, and active SVG.
- Prohibit SVG scripts, animation in sealed/archive profiles, external references, `foreignObject`, and network-fetching paint servers.
- Ignore or reject CSS `url()` outside the package; prohibit `@import` external URLs; restrict expensive selectors, filters, counters, and pathological layout.
- Disable network access by default. Hyperlinks may be exposed only as explicit user-activated navigation with scheme allowlists and warnings.
- Sanitize metadata and filenames before UI display; never interpret them as HTML.
- Decode images, media, and fonts in sandboxed processes with resource limits.
- Reject hidden interactive content, zero-opacity overlays, or off-page content where it creates signature or accessibility deception; validators should report non-rendered semantic text.
- Treat font parsing and shaping as high-risk native-code surfaces. Subset accepted font formats and use maintained sanitizers.

### Signature threats

- Verify the exact manifest and reject references outside the package.
- Prevent signature wrapping by binding one expected state-descriptor path and type.
- Reject unknown critical algorithms and deprecated hashes.
- Present certificate trust separately from byte integrity.
- Prevent “valid signature” UI when only an attachment or old revision was signed.
- Define rollback and duplicate-revision detection.

### Security posture

No arbitrary JavaScript is necessary but not sufficient. The safe reader architecture is a brokered package parser, isolated renderer, no ambient filesystem/network authority, strict quotas, and explicit capability escalation for links or media.

## 19. Open-Source Implementation Landscape

No reviewed project implements most of the complete proposal. The closest rendering pipeline is Vivliostyle or Paged.js (HTML/CSS to pages/PDF); the closest package/reader ecosystem is Readium; the closest fixed-document engine is MuPDF; and the closest structured editing core is ProseMirror/Tiptap. None provides the proposed identity, sealing, semantic-to-fixed mapping, transactional agent API, and archive/signature policy as one system.

| Project | Architecture/maturity relevant here | Applicability |
| --- | --- | --- |
| Chromium/Blink | Full web engine, multi-process sandbox, broad HTML/CSS/SVG/MathML and print support | Viewer/preview and renderer baseline; too large to make normative |
| Firefox/Gecko | Independent full web engine with strong standards/accessibility implementation | Critical differential-rendering target; embedding is difficult |
| WebKit | Embeddable web-content engine used across Apple platforms | Differential target and possible native viewer engine |
| Paged.js | Browser polyfill for paged-media features and PDF generation | Fast prototype and authoring preview; depends on browser/Puppeteer |
| Vivliostyle | HTML/CSS typesetting, EPUB/Web publication viewer and CLI | Closest open architecture to semantic publication plus pagination |
| WeasyPrint | Purpose-built Python HTML/CSS paged renderer, not a full browser | Server-side deterministic-ish renderer candidate; support differs from browsers |
| Prince | Proprietary high-quality HTML/CSS-to-PDF engine | Benchmark and conceptual reference; not an open reference implementation |
| epub.js | Browser EPUB renderer with persistence, pagination, and hooks | Lightweight compatibility viewer; scripted content is disabled by default |
| Readium | Cross-platform EPUB/Web Publication building blocks | Best reader/package ecosystem foundation |
| Calibre | Mature e-book view/edit/convert suite | Conversion oracle and stress corpus; unsuitable as a small embedded core |
| MuPDF | Lightweight PDF/XPS/EPUB/SVG rendering and document APIs | Strong fixed-rendition renderer/validator candidate; license implications |
| PDF.js | Web PDF parser/renderer | Browser fixed-rendition viewing; validation and editing are not its focus |
| LibreOffice filters | Broad ODF/DOCX import/export and PDF export | Conversion bridge; headless process isolation preferable |
| Pandoc | Broad markup AST and conversion ecosystem | Import/export scaffolding; semantics are necessarily lossy for rich layouts |
| ProseMirror | Typed schema, transactions, collaborative editing | Best editor-core fit |
| Tiptap | Productive ProseMirror-based headless framework | UI/editor acceleration; paid extensions must be separated from open core |
| Lexical | Extensible editor framework | Strong alternative, especially React; less directly schema-centric |
| Slate | Highly customizable React editor, currently described as beta | Flexible but more application-defined invariants |
| zip-rs | Rust ZIP library with WASM support | Candidate package primitive only after secure-profile hardening |
| wasm-bindgen | Rust/JavaScript/WASM bindings | Suitable for validator/parser exposure to web apps |
| lopdf | Rust PDF manipulation library | Useful low-level export/inspection; not a full PDF 2.0/WTPDF solution |

### Maturity caveats

- A project being able to render a standard does not mean it validates every conformance rule.
- Conversion tools should be treated as evidence-generating adapters, not semantic authorities.
- Paged rendering engines implement overlapping but non-identical CSS feature sets.
- PDF generation must be tested for WTPDF/PDF/UA tagging, ToUnicode, annotations, and PDF/A, not merely visual output.
- Browser-engine embedding dramatically increases update and security-maintenance obligations.

## 20. Licensing Analysis

This is an architectural licensing review, not legal advice. Verify the exact versions and dependency trees before distribution.

| Project | Verified license | Permissive reference implementation implications | Server/WASM/commercial implications |
| --- | --- | --- | --- |
| Chromium/Blink | BSD-style top-level plus many third-party licenses ([source license](https://chromium.googlesource.com/chromium/src.git/+/main/LICENSE)) | Embeddable, but compliance inventory is large | Commercial use possible; ship notices and continuously audit dependencies |
| Firefox/Gecko | MPL 2.0 for Mozilla source, with third-party components | File-level copyleft permits larger proprietary/permissive works with conditions | Modified MPL files must remain MPL; embedding and updates are operationally heavy |
| WebKit | Mix of LGPL and BSD ([project license](https://webkit.org/licensing-webkit/)) | Usable, but LGPL linking/source obligations matter | Commercial embedding possible with LGPL compliance; WASM is not the normal integration path |
| Paged.js | MIT ([repository](https://github.com/pagedjs/pagedjs)) | Easy to embed in a permissive viewer | Server/browser/commercial use straightforward with notice |
| Vivliostyle Core/Viewer/CLI | AGPL-3.0 ([license FAQ](https://github.com/vivliostyle/vivliostyle.org/blob/master/faq.md)) | Do not combine into a permissive reference binary without accepting AGPL obligations | Modified/network-deployed combined works may trigger source obligations; separate-process use reduces coupling but needs counsel |
| WeasyPrint | BSD-3-Clause ([repository](https://github.com/Kozea/WeasyPrint)) | Permissive and suitable for a reference server tool | Commercial/server use straightforward; audit native/Python dependencies |
| Prince | Proprietary | Cannot be the open reference implementation | Commercial license required; useful as external test oracle |
| epub.js | FreeBSD/BSD-2-Clause style ([repository](https://github.com/futurepress/epub.js)) | Permissive browser embedding | Commercial use straightforward; sanitize hostile EPUB content |
| Readium | BSD-3-Clause ([project goals](https://readium.org/about/project_goals.html)) | Strong permissive foundation | Suitable for commercial apps and services with notices |
| EPUBCheck | MIT ([W3C project page](https://www.w3.org/publishing/epubcheck/)) | Easy integration, but Java footprint | Server use straightforward; browser/WASM port is nontrivial |
| Calibre | GPL-3.0 ([repository](https://github.com/kovidgoyal/calibre)) | Prefer separate-process converter/test tool for a permissive project | Distribution of combined derivative work invokes GPL; ordinary server use is not AGPL, but distribution still matters |
| MuPDF/MuPDF.js | AGPL-3.0 or commercial ([repository](https://github.com/ArtifexSoftware/mupdf)) | Cannot simply embed in a permissive/proprietary reference app under AGPL without compatible release | MuPDF.js states network-service use is subject to AGPL; commercial license for closed/SaaS use |
| PDF.js | Apache-2.0 ([repository](https://github.com/mozilla/pdf.js)) | Excellent permissive browser viewer | Patent grant and notices; commercial/server/browser use allowed |
| LibreOffice | MPL 2.0 source ([official licenses](https://www.libreoffice.org/licenses/)) | Prefer process boundary for filters and to isolate complexity | Headless server use possible; distribute modifications to MPL files under MPL |
| Pandoc | GPL-2.0-or-later ([repository](https://github.com/jgm/pandoc)) | Use as separate CLI/service unless the reference implementation is GPL-compatible | Server execution generally does not trigger source distribution; shipped combined/library use needs GPL compliance |
| ProseMirror | MIT ([repository](https://github.com/ProseMirror/prosemirror)) | Excellent permissive editor core | Browser/server/commercial use straightforward |
| Tiptap open core | MIT ([repository](https://github.com/ueberdosis/tiptap)) | Permissive, but Pro/paid extensions have separate terms | Keep paid collaboration/AI features outside the open reference baseline |
| Lexical | MIT ([license](https://github.com/facebook/lexical/blob/main/LICENSE)) | Permissive alternative | Commercial/browser use straightforward |
| Slate | MIT ([repository](https://github.com/ianstormtaylor/slate)) | Permissive, but beta status increases maintenance risk | Commercial/browser use straightforward |
| zip-rs | MIT ([repository](https://github.com/zip-rs/zip2)) | Permissive core primitive | Supports WASM with feature selection; disable unnecessary codecs/crypto |
| wasm-bindgen | MIT or Apache-2.0 ([repository](https://github.com/rustwasm/wasm-bindgen)) | Permissive Rust/WASM bridge | Strong commercial/browser fit |
| lopdf | MIT ([repository](https://github.com/J-F-Liu/lopdf)) | Permissive low-level PDF library | Commercial/server/WASM possible, but capability/maturity must be validated |

Copyleft projects should remain in the evaluation matrix. They may be used as separate validation/rendering services, development tools, or the basis of an openly licensed implementation. The choice is architectural and legal, not a quality judgment.

## 21. Decision Matrix

The recommendation vocabulary is intentionally exclusive: **ADOPT**, **PROFILE**, **EXTEND**, **DESIGN NEW**, **POSTPONE**, or **REJECT**.

| Capability | Existing Standard/Project | Coverage | Recommendation | Rationale |
| --- | --- | --- | --- | --- |
| ZIP container | EPUB OCF / ISO ZIP profile | High | PROFILE | Reuse OCF paths, `mimetype`, and ZIP constraints; add security quotas |
| Package inventory | EPUB package document / ODF manifest | High | PROFILE | One normative inventory; do not maintain competing manifests |
| Reading order | EPUB spine | High | ADOPT | Mature and interoperable |
| Navigation | EPUB navigation document | High | ADOPT | Human- and machine-readable HTML navigation |
| Publication metadata | EPUB/Dublin Core | High | ADOPT | Add only profile/state metadata |
| Resource fallback | EPUB | High | ADOPT | Existing foreign-resource behavior |
| Reflowable content | XHTML/CSS | High | PROFILE | Constrain active and non-deterministic features |
| Native semantics | HTML | High | PROFILE | Require valid structured subset and addressable IDs |
| Mathematics | MathML | High | ADOPT | Do not invent equation syntax |
| Vector graphics | SVG | High | PROFILE | Static safe subset; no script/external resources |
| Fonts | OpenType/WOFF2 | High | PROFILE | Embed, license, limit formats/features, test shaping |
| Unicode text | Unicode | High | ADOPT | Logical-order source text |
| Arabic/RTL | UAX #9, HTML `dir`, CSS Writing Modes | High in specs | PROFILE | Make conformance fixtures mandatory |
| Responsive rendering | Web platform | High | PROFILE | Ordinary view, not archival determinism |
| Paged authoring CSS | CSS Paged Media/Fragmentation/GCPM | Medium | PROFILE | Useful subset; implementation differences remain |
| Reference browser requirement | Chromium/Gecko/WebKit | Medium | POSTPONE | Build-profile option, not format semantics |
| Fixed-layout EPUB as canonical | EPUB FXL | Medium | REJECT | Pixel layout does not guarantee permanent identical rendering |
| Canonical fixed rendition | PDF 2.0 | High | PROFILE | Use tagged PDF with strict resource/text rules |
| Fixed accessibility | WTPDF / PDF/UA-2 | High | PROFILE | Existing reuse/accessibility rules |
| Fixed archival rendition | PDF/A-4 | High | PROFILE | Existing archival standard |
| Restricted SVG pages | SVG | Medium | POSTPONE | Prototype only if PDF mapping proves inadequate |
| OpenXPS pages | ECMA-388 | High for fixed pages | REJECT | Adds a weaker ecosystem without removing PDF needs |
| Custom page-scene language | None | Low | REJECT | Unnecessary renderer and standards burden |
| Canvas/Skia display list | Internal APIs | Low as interchange | REJECT | No stable semantic archival interchange contract |
| Semantic-to-fixed mapping | EPUB rendition map / Web Annotation | Partial | DESIGN NEW | Need fine-grained fragments, page geometry, state hashes, and logical text ranges |
| Stable HTML element IDs | HTML `id` | Partial | EXTEND | Define persistent random identity and lineage rules |
| Cross-document identity | UUID/IRI | Medium | PROFILE | Document ID + node ID; avoid bare fragments |
| Supplemental relationship graph | JSON-LD | High | PROFILE | Only non-tree relationships; no duplicate text semantics |
| Annotations | W3C Web Annotation | High | EXTEND | Adopt model; add stable-node and sealed-page selector profile |
| Comments/replies | Web Annotation | High | ADOPT | Existing motivations, bodies, agents, lifecycle |
| Declarative basic forms | HTML + JSON Schema | Medium | POSTPONE | Preserve only in 0.1; full behavior needs a later profile |
| Calculations/repeating forms | XForms concepts | Medium | POSTPONE | Requires expression/security/interoperability work |
| PDF form export | AcroForms | High | PROFILE | Export target with loss report, not source model |
| Exact-byte fixity | SHA-256 / BagIt concepts | High | PROFILE | Hash exact entries, not parsed/canonicalized documents |
| JSON canonicalization | RFC 8785 JCS | High for I-JSON | ADOPT | Limit use to small state descriptors |
| Semantic/fixed state binding | None complete | Low | DESIGN NEW | Central integration requirement |
| Outer-package signatures | EPUB XMLDSig / JWS / CAdES / ASiC | Medium | POSTPONE | Choose only after interoperability and LTV tests |
| Fixed-rendition signatures | PDF/PAdES | High | ADOPT | Mature and already tied to fixed artifact |
| Timestamping | RFC 3161 / ETSI AdES | High | ADOPT | Do not invent timestamps |
| Co-signing | PDF/AdES/ASiC | High | PROFILE | Mutation policy must state signed scope |
| Merkle tree | General technique | Unnecessary in 0.1 | POSTPONE | Flat manifests are simpler at expected package sizes |
| Incremental ZIP updates | ZIP append patterns | Weak/ambiguous | REJECT | Rewrite package atomically; revisions are logical, not ambiguous duplicate entries |
| PDF incremental updates | PDF 2.0 | High | ADOPT | Use inside signed fixed artifact where appropriate |
| Revision graph | PROV/PREMIS concepts | Partial | EXTEND | Minimal parents/tool/time model only |
| Full edit history in package | ODF/editor logs | Mixed | POSTPONE | Privacy, size, and merge complexity |
| Agent query/mutation methods | Editor APIs | Partial | DESIGN NEW | Companion specification, not serialization |
| Optimistic concurrency | Revision tokens/hashes | High conceptually | ADOPT | Mandatory transaction precondition |
| AI provenance transcripts | Proprietary logs | Low portability | REJECT | Store minimal committed-event metadata only |
| Accessibility discovery | EPUB Accessibility | High | ADOPT | Existing metadata and conformance framework |
| Archive metadata | PREMIS | High | PROFILE | Minimal preservation events; do not embed all OAIS concepts |
| Transfer packaging | BagIt | High | ADOPT externally | Repository wrapper, not document’s inner container |
| WARC capture | WARC | Low relevance | REJECT | Only relevant to preserved web transactions |
| Arbitrary JavaScript | HTML/EPUB | Technically available | REJECT | Security, determinism, and archival risk |
| External network resources | Web platform | Technically available | REJECT | Core files must be offline and self-contained |
| Vendor extensions | Namespaced vocabularies | High | PROFILE | Declared optional/required behavior and preservation rules |
| Capability profiles | EPUB `conformsTo` + project registry | Partial | EXTEND | Small composable capability set, no profile explosion |

## 22. Architectural Alternatives

Scores are 1 (poor) to 10 (excellent). They assess the architecture, not a particular implementation team.

### Architecture A — Independent new format

Custom ZIP profile containing HTML/CSS plus a chosen fixed representation and new manifests.

**Benefits:** maximum control, clean namespace, security rules can be normative from the beginning, and the lifecycle can be designed without compatibility compromises.

**Weaknesses:** recreates OCF/package behavior, requires new media type and reader adoption, duplicates validation/signature work, and risks a large specification. Implementation effort and ecosystem complexity are highest. Fixed reliability depends entirely on the chosen fixed layer. Accessibility and archival credibility must be earned from scratch.

| Criterion | Score | Explanation |
| --- | ---: | --- |
| Technical soundness | 6 | Coherent in theory, but unnecessary custom integration surfaces add failure modes |
| Novelty | 8 | Most visibly new, though many components are reused |
| Implementation feasibility | 4 | Parser, validator, tooling, media registration, and adoption all start at zero |
| Standards reuse | 6 | Uses web standards but discards mature package conventions |
| AI-agent suitability | 8 | Can make identity and transactions first-class |
| Editing suitability | 8 | Semantic source can be designed cleanly |
| Fixed-layout reliability | 8 | Good if PDF/fixed scene is stored |
| Accessibility | 7 | HTML basis helps, but profile/tooling is new |
| Security | 5 | Small subset helps; new parser ecosystem hurts |
| Archival suitability | 6 | Possible, but lacks institutional track record |
| Adoption potential | 3 | New extension and tooling face a severe cold-start problem |

### Architecture B — EPUB profile/extension

Strict EPUB 3.3 with semantic XHTML, EPUB FXL/multiple renditions, stable-ID rules, and project metadata.

**Benefits:** maximum package, reader, accessibility, navigation, and validator reuse. Ordinary readers can present the semantic rendition. Editing and AI access remain strong.

**Weaknesses:** EPUB FXL does not provide an archive-grade canonical scene, multiple-rendition support is not broad, and EPUB’s allowed scripting/web surface must be narrowed. Security improves through profiling but legacy readers will not enforce all restrictions.

| Criterion | Score | Explanation |
| --- | ---: | --- |
| Technical soundness | 8 | Strong fit except for canonical fixed rendering |
| Novelty | 4 | Mostly a conformance profile |
| Implementation feasibility | 8 | Existing OCF, EPUBCheck, readers, and web tooling |
| Standards reuse | 10 | Reuses nearly every base layer |
| AI-agent suitability | 8 | XHTML plus stable IDs is strong |
| Editing suitability | 9 | Web editor ecosystem is broad |
| Fixed-layout reliability | 6 | EPUB FXL is fixed, not archival-deterministic |
| Accessibility | 9 | Mature EPUB/web accessibility basis |
| Security | 7 | Profile can reject active content; legacy behavior remains |
| Archival suitability | 6 | Self-contained but no canonical archive page guarantee |
| Adoption potential | 7 | EPUB compatibility helps; profile awareness still required |

### Architecture C — Semantic document + PDF canonical rendition

EPUB 3.3-compatible OCF outer package; authoritative XHTML rendition; tagged PDF 2.0 sealed rendition; custom state binding and semantic-to-page map.

**Benefits:** best standards reuse and clearest separation of concerns. EPUB/web handles semantics, reflow, editing, and accessibility; PDF handles exact pages, print, signatures, and archival. It supports ordinary EPUB fallback and ordinary PDF export. Agent operations target the semantic tree.

**Weaknesses:** synchronization and package size; two accessibility representations must be validated; ordinary EPUB readers will not automatically expose the PDF as canonical; finalization must be precise.

| Criterion | Score | Explanation |
| --- | ---: | --- |
| Technical soundness | 9 | Each representation does what it is best at; state binding is explicit |
| Novelty | 5 | Novel integration, not novel primitives |
| Implementation feasibility | 8 | Major components exist; mapping remains difficult |
| Standards reuse | 10 | EPUB, web, WTPDF, PDF/A, Web Annotation |
| AI-agent suitability | 9 | Stable semantic source and transactional companion API |
| Editing suitability | 9 | XHTML/editor model is authoritative until finalization |
| Fixed-layout reliability | 10 | Preserved PDF scene |
| Accessibility | 9 | Strong dual conformance, with validation cost |
| Security | 8 | Active content can be prohibited; parsers can be isolated |
| Archival suitability | 9 | PDF/A-4 plus fixity/provenance is credible |
| Adoption potential | 8 | Familiar component formats and useful fallbacks |

### Architecture D — Semantic document + new restricted page scene

HTML semantics plus a newly standardized, non-PDF vector/glyph scene.

**Benefits:** exact control, streamable page data, potentially simple sandboxed renderer, direct semantic IDs on scene primitives, and clean geometric mapping.

**Weaknesses:** the project must specify text shaping outputs, fonts, color, transparency, images, printing, accessibility, selection, copy/paste, annotations, signatures, and archival behavior. It is effectively a new PDF/OpenXPS. Long-term maintainability and adoption are poor.

| Criterion | Score | Explanation |
| --- | ---: | --- |
| Technical soundness | 7 | Can be precise but duplicates mature fixed-document work |
| Novelty | 8 | New scene and mapping could be distinctive |
| Implementation feasibility | 4 | Multiple independent renderers and validators required |
| Standards reuse | 6 | Reuses text/font standards but replaces PDF |
| AI-agent suitability | 9 | Direct scene/semantic linkage possible |
| Editing suitability | 9 | Same semantic source advantages |
| Fixed-layout reliability | 10 | Scene preservation can be exact |
| Accessibility | 7 | Must build and test a new mapping layer |
| Security | 8 | A small declarative scene could be sandbox-friendly |
| Archival suitability | 7 | Simple grammar helps; ecosystem longevity does not |
| Adoption potential | 4 | Requires every consumer to add a new renderer |

### Architecture E — PDF outer document + associated semantic source

Tagged PDF 2.0/PDF/A-4f is the distributed file; XHTML/EPUB source, mapping, and data are Associated Files.

**Benefits:** immediate opening in ubiquitous PDF viewers, excellent fixed reliability, signatures and archival maturity, and no new outer container. PDF 2.0 can machine-associate source/data files.

**Weaknesses:** most tools treat attachments as secondary; editing requires extraction/repackaging; Associated Files are not a rich hierarchical package; source authority is counterintuitive; an unrecognized editor may save or strip attachments. Agent suitability is good only through a special SDK.

| Criterion | Score | Explanation |
| --- | ---: | --- |
| Technical soundness | 8 | Standards-compliant and simple for distribution |
| Novelty | 3 | Existing associated-file pattern |
| Implementation feasibility | 8 | PDF tooling exists; robust embedded-package updates are harder |
| Standards reuse | 10 | PDF 2.0, WTPDF, PDF/A, Associated Files |
| AI-agent suitability | 7 | Strong if source attachment is present and trusted |
| Editing suitability | 6 | PDF-first tooling obscures semantic authority |
| Fixed-layout reliability | 10 | PDF is primary |
| Accessibility | 9 | WTPDF/PDF/UA mature |
| Security | 7 | Attachments add nested-parser and signature-scope risk |
| Archival suitability | 10 | PDF/A-4f is designed for this class of package |
| Adoption potential | 9 | PDF opens everywhere, but advanced behavior is invisible |

### Recommended architecture

Choose **Architecture C**. It is the smallest architecture that honors semantic authority while refusing to recreate PDF. Architecture B is the fallback if the sealed fixed rendition is dropped. Architecture E is a useful export/distribution profile for organizations that require a PDF-first artifact.

## 23. Novelty Analysis

### Already solved

- ZIP/OCF packaging, manifests, spines, navigation, metadata, and resource fallback.
- Semantic web content, responsive rendering, SVG, MathML, Unicode, and web fonts.
- Accessibility vocabularies and conformance frameworks.
- Fixed page scenes, printing, annotations, forms, signatures, incremental updates, and archival PDF.
- Annotation bodies/targets/selectors and lifecycle metadata.
- Checksums, signatures, timestamps, certificate validation, and preservation metadata.
- Typed collaborative editor transactions in application frameworks.

### Partially solved

- EPUB multiple renditions and cross-rendition mapping.
- Tagged PDF reuse and deriving HTML from well-tagged PDF.
- Stable IDs within HTML/DOM and document editors.
- Source files associated with fixed PDF objects.
- Declarative safe forms without JavaScript.
- Reproducible browser-based pagination.

### Integration opportunity

- Make one semantic rendition explicitly authoritative.
- Define finalization as a state transition rather than an export convention.
- Bind a semantic revision, mapping, and PDF rendition by digest.
- Validate semantic and fixed accessibility together.
- Give annotations dual robust targets across semantic and fixed views.
- Expose the same typed document model to humans, converters, and agents.

### Actually novel

The potentially novel combination is:

> authoritative semantic XHTML + persistent logical object identity + transactional agent edits + canonical tagged-PDF snapshot + fine-grained bidirectional mapping + explicit sealed-state binding.

Individual ingredients exist. No reviewed standard or project was verified to make all six a single interoperable lifecycle. This is an integration novelty, not a new media primitive.

### Probably unnecessary

- New ZIP profile, compression, markup, vector graphics, font format, or cryptography.
- A mandatory “AI document” sidecar duplicating the semantic source.
- Custom fixed-page scene in 0.1.
- Merkle trees for ordinary document package sizes.
- Full prompt/model transcripts in document provenance.
- Byte-identical HTML renderer output as a portable conformance promise.

## 24. Risk Register

| Risk | Severity | Probability | Why it matters | Mitigation |
| --- | --- | --- | --- | --- |
| Trying to replace PDF directly | Critical | Medium | Requires recreating a massive ecosystem and loses adoption | Use PDF as fixed rendition/export; market semantic editing, not replacement |
| Insufficient differentiation from EPUB | High | High | Project becomes a private EPUB dialect | Limit novelty claim to lifecycle, IDs, mapping, and API; remain conformant |
| HTML/CSS complexity | High | High | Large attack and interoperability surface | Strict safe subset, schema, quotas, and conformance fixtures |
| Deterministic rendering failure | Critical | High if defined as re-render identity | Undermines signing and archival claims | Define sealed determinism as preserved fixed scene |
| Browser-engine dependence | High | High | Version changes alter pagination | Renderer provenance plus stored PDF; differential tests |
| Font availability/licensing | Critical | High | Layout and archival fail without exact fonts | Require embeddable fonts, validate licenses/embedding flags, fallback policy |
| Arabic/RTL rendering defects | Critical | Medium | Corrupts first-class languages and agent selection | Mandatory mixed-script corpus, logical extraction and cluster checks |
| Digital-signature complexity | Critical | High | Misleading trust UI is worse than no signature | Defer outer signature profile; reuse PAdES/AdES and expert review |
| Premature archival promises | High | High | Institutions may rely on unsupported longevity claims | Experimental Archive profile until repository pilots and dual validators |
| Editor complexity | High | High | Typed tables, notes, references, changes, and layout are hard | Limit 0.1 schema; ProseMirror model; defer tracked changes/forms |
| Legacy PDF conversion | High | High | Semantics are often inferred and lossy | Preserve original, confidence/evidence metadata, never label inference authoritative by default |
| Standards fragmentation | High | Medium | Yet another dialect damages interoperability | Contribute extensions upstream; use registered IRIs and EPUB mechanisms |
| Security vulnerabilities | Critical | High | Documents are hostile multi-parser bundles | Sandboxing, no script/network, quotas, fuzzing, minimal codecs |
| Weak adoption | High | High | Format value depends on readers/editors | EPUB/PDF fallbacks, open validator, measurable agent benefit |
| Specification creep | Critical | High | Recreates PDF/ODF complexity | Capability registry, strict 0.1, separate companion specs, kill features |
| Multiple representations | Critical | High | Size, validation, and update complexity | Fixed rendition only in sealed profile; immutable revision binding |
| Semantic/fixed desynchronization | Critical | High | Wrong page shown or signed relative to source | Digest binding, coverage metrics, stale-state hard errors |
| Mapping invalidation after edits | High | High | Annotations and page targets break | Mapping belongs to a revision; regenerate atomically on finalize |
| Divergent accessibility trees | Critical | Medium | Semantic view may say something different from PDF | Cross-view validation and content-equivalence tests |
| Hidden-content/signature confusion | Critical | Medium | User signs unseen or stale data | Signed-scope UI, no hidden normative content, explicit revision IDs |
| ID misuse or collisions | High | Low | References and agent edits target wrong object | UUID-derived IDs, uniqueness validation, tombstones, clone rules |
| Privacy leakage in history | High | Medium | Deleted/sensitive content remains recoverable | Minimal provenance, explicit history compaction, redaction tests |
| Copyleft architecture surprise | Medium | Medium | Product distribution/service obligations change | License boundaries planned early; retain strong projects as services/tools |
| Validation monoculture | High | Medium | One validator’s bug becomes the de facto standard | Independent implementations, published corpus, differential fuzzing |

## 25. Proposed AI-vs-PDF Benchmark

### Purpose and baselines

Measure whether the proposed structured architecture produces safer, cheaper, and more correct document operations than:

1. untagged PDF;
2. tagged PDF of ordinary quality;
3. WTPDF/PDF/UA-2 quality PDF;
4. source DOCX/ODT where available, as a non-PDF upper baseline;
5. the proposed semantic package without stable IDs, as an ablation.

Each intellectual document should be rendered into all available baselines from the same source. Include born-digital, scanned/OCR, academic, financial, legal, multilingual, form-like, and graphic-heavy documents. At least 25% of fixtures should contain Arabic/RTL; smaller sets should target CJK vertical text, Indic shaping, emoji, equations, and accessibility edge cases.

### Tasks

1. Find a named table cell and change its value.
2. Update every semantic reference to that value, excluding unrelated identical strings.
3. Replace a figure while preserving caption, alt text, number, and inbound references.
4. Move a section and repair outline, numbering, notes, and references.
5. Insert a citation and bibliography entry using a supplied source record.
6. Extract every table with header relationships and reading order.
7. Extract the logical outline and section extents.
8. Translate one section while leaving equations, citations, IDs, and other sections untouched.
9. Change one style token without changing semantic content.
10. Render and verify that unrelated regions are unchanged.
11. Re-anchor annotations after a paragraph split and table-row insertion.
12. Update a mixed Arabic/English value and verify visual order, copy/paste, and accessibility.

### Experimental controls

- Use identical agent models, temperature, tool budgets, and machine resources.
- Randomize format order and blind human judges to the format.
- Run each task/document pair multiple times.
- Distinguish extraction-only, edit-only, and render-validation phases.
- Record tool errors separately from agent reasoning errors.
- Test both API-mediated and raw-file access.
- Include adversarial malformed but valid documents and stale revision conflicts.

### Metrics

| Metric | Definition |
| --- | --- |
| Task accuracy | Exact and graded semantic correctness against a gold result |
| Edit success rate | Valid committed result satisfying all task assertions |
| Unrelated-content corruption | Semantic nodes or fixed pixels changed outside allowed regions |
| Reference integrity | Percentage of links/citations/notes still resolved |
| Token consumption | Input/output tokens to successful completion |
| Execution steps | Tool/API calls and retries |
| Wall/CPU time | End-to-end and per-phase latency |
| Semantic correctness | Schema, table, outline, relation, and language/direction validity |
| Layout preservation | Page count/break changes and perceptual/geometric diff outside allowed regions |
| Accessibility preservation | Automated plus human AT checks before/after |
| File-size change | Absolute and percentage package growth |
| Conflict safety | Percentage of stale edits correctly rejected without mutation |
| Human repair time | Minutes for an expert to accept the result |
| Mapping coverage | Percentage of required semantic nodes correctly located in fixed pages |

### Success threshold

Before creating a new branded format, the structured system should improve complex edit success by at least 25 percentage points over WTPDF, cut unrelated corruption by at least half, and not regress accessibility or Arabic/RTL correctness. Thresholds should be finalized prospectively before running the benchmark.

## 26. Recommended Format 0.1 Scope

### Capability model

Replace the proposed independent `Core / Paged / Accessible / Archive / Signed / Forms` labels with composable capabilities plus explicit dependencies:

| Capability | Depends on | Minimum meaning |
| --- | --- | --- |
| Base | — | Safe EPUB-compatible package with semantic rendition, IDs, navigation, inventory, and validation |
| Fixed | Base | Tagged PDF 2.0 rendition plus complete revision-bound mapping |
| Sealed | Fixed | Immutable state descriptor binds semantic revision, fixed PDF, mapping, and resources |
| Accessible | Base; and Fixed if present | EPUB Accessibility for semantics; PDF/UA-2/WTPDF for fixed PDF; cross-view checks |
| Archive | Sealed + Accessible | PDF/A-4, embedded dependencies, preservation metadata, no active/external content |
| Signed | Sealed | Approved signature profile and explicit signed scope |
| Forms | Base | Future declarative form/data/validation model |

Capabilities are composable, but not all combinations are meaningful. `Archive` is hierarchical because it depends on Sealed and Accessible. `Signed` is independent of Archive but depends on a stable Sealed state. `Forms` is orthogonal and deferred.

### MUST HAVE IN 0.1

- EPUB 3.3-compatible OCF ZIP and package document.
- One default authoritative semantic rendition in valid XHTML, split across spine items if needed.
- Valid EPUB navigation document and metadata.
- Safe core profile: no scripting, no automatic networking, static SVG restrictions, XML hardening, package quotas, and normalized path rules.
- HTML-native semantics, MathML, language and direction metadata, and WCAG-oriented validation rules.
- Persistent Document ID, Revision ID, and stable IDs on all addressable block objects, table structures, figures, notes, citations, form controls that are preserved, and referenced inline ranges.
- One normative resource inventory with exact byte length, media type, and SHA-256 digest.
- Explicit distinction among authoritative, generated, inferred, cached, and non-normative resources.
- Minimal revision metadata: parent revision, time, generator, and conformance capabilities.
- Validation result categories and a standard machine-readable conformance report.
- Import provenance fields that distinguish asserted source semantics from converter/AI inference.

### SHOULD HAVE IN 0.1

- Fixed capability using tagged PDF 2.0.
- Sealed state descriptor binding semantic revision, PDF, mapping, fonts/assets, and renderer provenance.
- Semantic-to-fixed mapping with page IDs, fragment lists, quadrilaterals/paths, logical text ranges, and coordinate-system declarations.
- Web Annotation profile using stable-node, quote, position, and fixed-page selectors.
- EPUB Accessibility 1.1 conformance for Accessible documents.
- WTPDF/PDF/UA-2 validation for accessible fixed renditions.
- ProseMirror-compatible normalized document-model guidance, explicitly non-normative.
- Companion Agent API 0.1 with read operations, atomic mutations, revision preconditions, validation, and render/finalize jobs.

### MAY HAVE IN 0.1

- JSON-LD graph for external entities and non-tree relationships.
- Static, non-submittable HTML form controls preserved as content.
- Minimal committed-revision provenance.
- PDF-first export using PDF/A-4f Associated Files.
- Reproducible-render build metadata.
- Media overlays inherited unchanged from EPUB, if they comply with the security profile.

### DEFER TO 0.2+

- Outer-package digital-signature and long-term-validation profile.
- Declarative forms, calculations, repeats, conditional relevance, and data export.
- Tracked changes and collaborative history serialization.
- Fine-grained partial/Merkle signatures.
- Encrypted packages and DRM.
- Audio/video interactivity beyond safe inherited EPUB media.
- A normative pinned-renderer/reproducible-build profile.
- Advanced semantic graph vocabularies.
- Lossless DOCX/ODF round-trip claims.
- Distributed cross-document references with network resolution.

### OUT OF SCOPE

- New compression, cryptography, markup, font, accessibility, vector, or page-scene language.
- Arbitrary JavaScript, plugins, macros, active SVG, or automatic network access.
- Browser-engine standardization.
- Pixel editing of the semantic source as a universal operation.
- Guaranteed semantic recovery from arbitrary PDF.
- Full office-suite compatibility.
- Blockchain/distributed-ledger integrity.
- Prompt or chain-of-thought archival.

### Versioning and extensibility

- Use `major.minor` format-profile versions. Major changes may break processors; minor versions are additive and must preserve old required semantics.
- Identify the base profile and capabilities with stable IRIs in package metadata.
- Every extension declares an IRI, version, whether it is required, and affected resources.
- Unknown **required** extensions make the relevant capability unsupported; the reader may still expose safe fallback content.
- Unknown **optional** extensions must be preserved by editors and ignored without changing normative meaning.
- Vendor extensions use vendor-owned IRIs and cannot redefine core elements, algorithms, or security behavior.
- Capability declarations must be testable; avoid marketing-only labels.
- Keep schemas and registries separate from the core narrative specification so new optional vocabularies do not expand the base reader.
- Add features only with two interoperable implementations, test fixtures, and a documented threat analysis.

### Import/export strategy

| Direction | Expected fidelity | Required declaration |
| --- | --- | --- |
| Format → PDF | High visual; high semantic only if WTPDF generation succeeds | Validation report and mapping coverage |
| Format → HTML | High semantics; paged intentions may be lost | List unsupported page/form/signature features |
| Format → EPUB | Near-lossless Base profile; sealed lifecycle/mapping may be ignored | Preserve extension resources or report their removal |
| Format → plain text | Intentionally lossy | Reading order, language, and omitted-object report |
| HTML/Markdown → Format | High for represented constructs | Source-asserted vs converter-created IDs |
| EPUB → Format | High when source is semantic and safe | Report scripting, DRM, unsupported rendition behavior |
| ODT/DOCX → Format | Medium to high for narratives; variable for complex layout | Per-feature loss and inferred semantics |
| PDF → Format | Low to medium; high only for excellent WTPDF | Original PDF preserved; every inferred node carries method/confidence/evidence |

Converters must never upgrade inferred semantics to authoritative silently. A PDF-imported table, heading, or reading order is `inferred` until a human or trusted policy accepts it. The original source object and extraction evidence should remain addressable. Confidence values are informative, not proof.

## 27. Recommended Reference Implementation Architecture

No implementation should begin until the mapping and benchmark prototype is approved. If it proceeds, use the following separation.

### Core parser/package/validator

**Recommendation: Rust core, with TypeScript bindings.**

Rust is preferable for hostile ZIP/XML/HTML package handling, typed invariants, predictable memory management, command-line validation, and WASM reuse. A minimal dependency set should parse OCF, enforce quotas and paths, compute fixity, validate schemas, and expose a normalized read-only model. `zip-rs` is a candidate primitive, not a security policy; wrap it with strict limits and fuzzing.

TypeScript remains the best browser/editor integration language. It should consume generated bindings and implement UI-level models, not duplicate package validation. A pure TypeScript prototype is acceptable for early experimentation but should not become the only hostile-input parser.

### Browser viewer

- Use a sandboxed browser rendering surface for the authoritative XHTML view.
- Use PDF.js for the fixed PDF view in browsers.
- Never place package content in the application’s own origin; use opaque origins and restrictive CSP.
- Broker all asset reads through validated package URLs with no network fallback.
- Overlay mapping and annotations in a separate trusted UI layer.
- Test Chromium, Gecko, and WebKit rendering; do not define any as the standard renderer.

### Editor

Use ProseMirror as the default editor engine because typed schemas and transactions align closely with the required document and Agent API model. Tiptap can accelerate UI development, but the portable schema and transactions must not depend on proprietary extensions. Lexical is a strong alternative for React-first teams; Slate’s flexibility places more invariant burden on the application.

The editor’s normalized model should include first-class nodes for sections, figures, tables, equations, notes, citations, references, intentional page breaks, and change-safe anchors. It must serialize deterministically to constrained XHTML without storing a second canonical JSON tree.

### Renderer

Prototype at least three paths against the same corpus:

1. Chromium print plus Paged.js.
2. Vivliostyle CLI/Core.
3. WeasyPrint.

Measure page breaks, Arabic/RTL, font embedding, SVG/MathML, footnotes, tables, PDF tagging, and performance. Vivliostyle’s AGPL license affects embedding; it remains an excellent external engine or open-reference choice. WeasyPrint’s BSD license is permissive and its dedicated pagination architecture is attractive. Chromium has broad web fidelity but weaker control over reproducible versioning and tagged-PDF quality.

Do not build a custom renderer. If no existing engine can generate conforming tagged PDF, improve or wrap an existing open engine, or use a separate post-processing/tagging stage with transparent validation.

### PDF export

Evaluate PDF generation by conformance, not appearance:

- correct glyph embedding and ToUnicode/ActualText;
- WTPDF structure and annotation rules;
- PDF/UA-2 and PDF/A-4 validation;
- page destinations and links;
- stable mapping targets;
- Arabic/RTL extraction and accessibility;
- deterministic metadata/compression options where required.

PDF.js is a viewer, not the exporter. MuPDF is strong for rendering/inspection but AGPL/commercial licensing affects embedding. `lopdf` may support low-level manipulation but is not, by itself, evidence of complete PDF 2.0/WTPDF/PDF/A conformance. LibreOffice and Pandoc are conversion tools, not normative renderers. Proprietary Prince may serve as a high-quality comparison oracle.

### WASM

Use WASM for package validation, hashes, normalized-model queries, mapping checks, and possibly safe SVG/font inspection. `wasm-bindgen` is a mature permissive bridge. Do not force full pagination or PDF rendering into WASM unless profiling proves it necessary: large font, image, and rendering stacks can increase binary size, startup cost, and attack surface.

### Verification pipeline

Every finalize operation should run:

1. package/security validation;
2. semantic schema and link validation;
3. accessibility checks;
4. render to tagged PDF;
5. PDF structural, text-extraction, font, WTPDF/PDF-UA/PDF-A checks as applicable;
6. semantic-to-fixed mapping coverage and geometry validation;
7. Arabic/RTL and complex-script regression tests where those scripts occur;
8. digest/state binding;
9. atomic package rewrite to a new file;
10. independent reopen and verification.

## 28. Biggest Technical Unknowns

Ranked in prototype order:

1. **Semantic/fixed synchronization:** Can the system prove that the PDF and source express the same content and that the mapping is complete?
2. **Mapping granularity:** Can node/range-to-page fragments support text selection, tables, transforms, notes, multi-column flow, and annotations without becoming another layout model?
3. **Tagged PDF generation:** Can an open renderer reliably emit WTPDF/PDF/UA-2, PDF/A-4, links, annotations, and correct complex-script extraction?
4. **Arabic/RTL fidelity:** Do rendering, mapping, search, copy/paste, and accessibility agree on logical text and clusters?
5. **EPUB compatibility:** Will ordinary EPUB readers safely present the semantic rendition and ignore the sealed extension without confusing users?
6. **Agent advantage:** Are stable IDs and typed transactions measurably better than WTPDF plus a good PDF API?
7. **Signature lifecycle:** Can outer-package co-signing and post-signature annotations work across independent implementations without misleading trust states?
8. **Identity under structural edits:** Are split/merge/copy rules intuitive enough for multiple editors to produce interoperable histories?
9. **Font rights and permanence:** Can real-world documents legally embed all fonts needed for semantic preview and archival PDF?
10. **Validation independence:** Can two parsers/render validators agree, avoiding a monoculture?

### First prototype

Build no editor or generalized viewer. Create a research harness around 50 representative semantic documents and existing renderers. Generate tagged PDFs and proposed mappings, then test content equivalence, mapping coverage, re-anchoring, and Arabic/RTL. Compare with EPUB multiple-rendition mapping and WTPDF extraction. This prototype should be disposable and should not establish a de facto file layout.

## 29. Kill Criteria

Abandon the new profile or radically change direction if any of these occur:

- EPUB 3.3 plus its existing extension mechanisms already expresses the lifecycle/mapping with no meaningful new conformance rules.
- WTPDF plus Associated Files and a companion API matches agent benchmark results within the predeclared margin.
- Semantic-to-fixed synchronization cannot be validated automatically above an agreed coverage threshold.
- Complex-script mapping requires duplicating the entire glyph/layout engine in the interchange specification.
- Maintaining source, PDF, mapping, and accessibility equivalence causes unacceptable authoring latency or package growth.
- No open renderer can produce sufficiently conforming tagged PDF and the project cannot sustain improvements upstream.
- The structured format fails to improve agent edit success by the benchmark’s minimum threshold.
- Ordinary EPUB readers expose confusing, unsafe, or misleading behavior that cannot be fixed while retaining compatibility.
- Signature requirements force a custom trust ecosystem or cannot express safe post-signature annotation policy.
- Archive claims depend on unavailable font rights or an unreproducible proprietary renderer.
- The 0.1 specification grows beyond the Base/Fixed/Sealed integration and begins duplicating forms, office layout, or cryptography.
- Fewer than two independent implementations can pass the core conformance suite.

A successful kill decision is not failure. The likely fallback products—a transactional semantic document API, a WTPDF sidecar/mapping convention, or an EPUB authoring profile—could still be valuable without a branded format.

## 30. Final Recommendation

## Recommended Direction

Pursue a **hybrid EPUB 3.3-compatible profile** whose default rendition is constrained semantic XHTML and whose optional sealed rendition is tagged PDF 2.0. Use PDF/A-4 for archive conformance. Bind semantic revision, PDF, mapping, and resources with exact-byte digests. Define agent edits in a separate transactional API.

Do not register a new extension or media type for 0.1. Prove the profile using ordinary `.epub` packaging first. Revisit branding only after reader and distribution tests.

## What We Should Reuse

- EPUB 3.3 OCF, package document, spine, navigation, metadata, resource fallback, and accessibility framework.
- HTML, CSS, MathML, SVG, Unicode, UAX #9, OpenType/WOFF2, and web accessibility APIs.
- WAI-ARIA and DPUB-ARIA with native-HTML-first authoring.
- JSON-LD for supplemental relationships only.
- W3C Web Annotation for annotations.
- PDF 2.0, WTPDF, PDF/UA-2, PDF/A-4, and PAdES for fixed artifacts.
- SHA-256, RFC 8785 JCS for a small state descriptor, RFC 3161 timestamps, and established certificate ecosystems.
- PREMIS concepts and BagIt at repository boundaries.

## What We Should Profile

- OCF/ZIP paths, codecs, sizes, and hostile-input processing.
- XHTML/CSS/SVG/fonts to a safe, offline, authoring-oriented subset.
- Persistent IDs and cross-document references.
- EPUB package metadata for authority, capabilities, and revisions.
- Tagged PDF requirements for fonts, text extraction, accessibility, links, and archive conformance.
- Web Annotation selectors and revision anchoring.
- Extension/capability declarations and conformance reports.

## What We Actually Need to Design

1. Stable semantic identity and minimal lineage rules.
2. The semantic-revision/fixed-rendition state binding.
3. A fine-grained semantic-to-fixed mapping profile.
4. A companion transactional Agent API and benchmark.

This is intentionally the shortest design list.

## What We Should Not Build

- A new container, compression method, markup language, CSS engine, font format, vector language, page-scene format, accessibility vocabulary, cryptographic algorithm, timestamp system, or archive repository model.
- A custom browser or PDF renderer.
- Arbitrary scripting or network-enabled documents.
- A general office suite, lossless universal converter, or full forms/workflow engine in 0.1.
- A separate AI-readable duplicate of the document.

## Format 0.1 Scope

Ship only the Base profile specification, a research-quality Fixed/Sealed profile, conformance fixtures, and companion Agent API draft. Forms, outer signatures, tracked changes, encryption, and full archive certification wait for later versions. Accessible semantics are not optional quality polish; any public conformance claim should state whether the Accessible capability is met.

## Biggest Technical Unknown

Whether a complete, stable, bidirectional semantic-to-PDF mapping and content-equivalence check can be generated across complex pagination—especially Arabic/RTL—without duplicating a layout engine or producing intolerable synchronization cost.

## Kill Criteria

Kill or radically narrow the project if WTPDF/EPUB already match the benchmark, if mapping/equivalence cannot be validated, if dual-representation maintenance dominates editor complexity, or if the agent advantage is not measurable. In that case, standardize only the transactional Agent API and stable-ID convention over existing EPUB/WTPDF documents.

---

### Research status note

The core conclusions are supported by current public specifications and authoritative project sources as of the audit date. For exact interoperability of EPUB multiple renditions across commercial reading systems, outer-package signature validation rates, and the ability of specific renderer versions to emit full WTPDF/PDF/UA-2:

> Not verified.

Those questions require executable interoperability testing and are intentionally treated as prototype questions rather than facts.
