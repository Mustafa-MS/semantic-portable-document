# Architecture Decisions 0.1

## Next-Generation Semantic Portable Document Project

**Status:** Approved architectural baseline for experimental validation
**Version:** ADR 0.1
**Purpose:** Freeze the architectural principles that may be relied upon by prototype work while clearly separating confirmed decisions from unresolved research questions.

---

# 1. Project Objective

The project investigates whether a portable document can combine:

* semantic-first editable content;
* responsive/reflowable presentation;
* fixed page presentation;
* stable semantic object identity;
* safe structured editing;
* AI-agent access;
* offline portability;
* accessibility;
* integrity;
* long-term fixed-document preservation.

The project is **not currently defined as a PDF replacement**.

The initial objective is to determine whether this architecture provides a measurable advantage over:

* conventional PDF;
* Tagged PDF;
* WTPDF/PDF-UA;
* existing EPUB-based documents;
* and conventional editable source formats.

No claim of superiority shall be made before benchmarking.

---

# 2. Core Architectural Model

The document architecture SHALL follow a semantic-first model.

```text id="5e7pym"
                    DOCUMENT
                       │
                       ▼
              Semantic Source
                  XHTML
                       │
                stable IDs
                       │
                 Revision R
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼

   Responsive View            Fixed Rendition
                                    │
                                    ▼
                             Rendition Profile
                                    │
                          reference implementation:
                               Tagged PDF 2.0
```

The semantic source is authoritative.

The fixed rendition is generated from the semantic source.

The fixed rendition SHALL NOT become an independently editable second source of truth.

---

# 3. Decision AD-001 — Semantic Source Is Authoritative

**Decision:** ACCEPTED

The authoritative editable representation SHALL be semantic XHTML based on established web standards.

Primary document meaning shall be represented using:

* XHTML/HTML semantics;
* MathML;
* SVG where appropriate;
* Unicode;
* language metadata;
* direction metadata;
* ARIA only when native semantics are insufficient.

The format SHALL NOT maintain an independently editable JSON representation containing duplicate document content.

Example:

```text id="7r7rq1"
XHTML:
"The proposed system achieved 0.906 FROC"

JSON:
"The proposed system achieved 0.901 FROC"
```

This state MUST never be possible as two competing authoritative representations.

Supplemental structured data may contain relationships, provenance and external entities, but shall refer to semantic nodes rather than duplicate them.

---

# 4. Decision AD-002 — Reuse EPUB OCF Packaging

**Decision:** ACCEPTED FOR PROTOTYPE

The project SHALL reuse EPUB 3.x OCF packaging concepts rather than invent a ZIP-based container.

Prototype implementations shall reuse where practical:

* OCF ZIP structure;
* package document;
* manifest/resource inventory;
* spine;
* navigation document;
* metadata conventions;
* MIME declarations;
* resource fallback concepts.

The project SHALL NOT create:

* a new compression format;
* a new ZIP dialect;
* a new generic resource manifest model;
* a new navigation language.

---

# 5. Decision AD-003 — EPUB Compatibility Is Desired, Not Yet Normative Identity

**Decision:** OPEN / EXPERIMENTAL

The first prototype MAY use:

```text id="1y4gtc"
.epub
application/epub+zip
```

for interoperability testing.

However, the project does NOT yet decide that the final document format:

* must use the `.epub` extension;
* must identify itself exclusively as EPUB;
* or must expose every advanced capability to ordinary EPUB readers.

Prototype testing shall determine:

* how common EPUB readers display the semantic rendition;
* whether unknown extensions are safely ignored;
* whether sealed/fixed semantics become misleading;
* whether EPUB compatibility constrains security or lifecycle behavior.

A new extension or MIME type shall not be introduced until this question is experimentally answered.

---

# 6. Decision AD-004 — Persistent Object Identity Is Fundamental

**Decision:** ACCEPTED

The document model SHALL define three identity levels.

```text id="uvvi34"
Document ID
Revision ID
Node ID
```

## Document ID

Represents the lineage of a logical document.

## Revision ID

Identifies one immutable semantic state.

## Node ID

Identifies one persistent semantic object within the document lineage.

Examples:

```text id="75c2p8"
section
paragraph
figure
caption
table
row
cell
equation
citation
footnote
reference
```

Node identity SHALL NOT be derived from:

* page number;
* text content;
* document order;
* DOM path;
* heading number;
* position;
* content hash.

A node may move, be restyled or be renamed without losing identity.

---

# 7. Decision AD-005 — Content Hashes Are Not Identity

**Decision:** ACCEPTED

Hashes may be used for:

* integrity;
* revision verification;
* transaction preconditions;
* stale-write detection.

They SHALL NOT be used as semantic object identity.

Conceptually:

```text id="0g1dkp"
Node ID:
n_7f2a...

Current node hash:
sha256:7ab4...
```

Editing the paragraph changes the hash.

It does not change the Node ID.

---

# 8. Decision AD-006 — Agent Editing Is Transactional

**Decision:** ACCEPTED

Agents SHALL NOT normally modify raw package files directly.

A companion Agent API shall expose a normalized document model.

Conceptually:

```text id="ptx744"
Agent
   │
   ▼
Transactional Document API
   │
   ├── query
   ├── read
   ├── modify
   ├── validate
   ├── commit
   ├── render
   └── finalize
```

Multi-object changes SHALL support atomic transactions.

Example:

```text id="5sg9yj"
Transaction T

baseRevision = r105

operations:
    update table cell
    update paragraph reference
    update figure caption

commit
```

Either every required operation succeeds or none is committed.

---

# 9. Decision AD-007 — Optimistic Concurrency Is Required

**Decision:** ACCEPTED

Agent operations SHALL protect against stale writes.

Example:

```text id="o31hvt"
replaceText(
    node = "n_5837",
    expectedRevision = "r105",
    expectedNodeHash = "7ab4...",
    value = "new text"
)
```

If the document changed after the agent read it:

```text id="krcip2"
CONFLICT

expected revision:
r105

current revision:
r106
```

The system SHALL NOT silently overwrite the newer revision.

---

# 10. Decision AD-008 — Agent API Is a Companion Specification

**Decision:** ACCEPTED

The document file specification SHALL define:

* document identity;
* node identity;
* revision identity;
* validity;
* lifecycle state;
* mapping;
* integrity;
* provenance.

It SHALL NOT freeze programming-language-specific functions such as:

```text id="m0l4pc"
getNode()
replaceText()
render()
```

Those belong in:

```text id="juw6r5"
Agent API Specification
```

Individual SDKs may expose language-specific interfaces.

---

# 11. Decision AD-009 — Fixed Representation Is Generated

**Decision:** ACCEPTED

The fixed representation SHALL be derived from a specific semantic revision.

Conceptually:

```text id="y0j3km"
Semantic Revision R105
        │
        ▼
     Renderer
        │
        ▼
Fixed Rendition F105
```

A fixed rendition MUST identify the semantic revision from which it was produced.

Editing semantic Revision R105 creates a new revision:

```text id="7hz8iv"
R106
```

The previous fixed rendition:

```text id="24maxz"
F105
```

is no longer a valid rendition of the current semantic state.

---

# 12. Decision AD-010 — Fixed Rendition Is an Abstraction

**Decision:** ACCEPTED

The architecture shall define:

```text id="3l0z0k"
Canonical Fixed Rendition
```

as a capability and conformance contract.

It shall NOT permanently define:

```text id="jm1224"
Canonical Fixed Rendition = PDF
```

at the architectural level.

Instead:

```text id="o7aq7x"
Fixed Rendition Profile

    profile: pdf2
```

may be one implementation.

Future profiles may be possible if technically justified.

This prevents the semantic architecture from being permanently dependent on PDF.

---

# 13. Decision AD-011 — Tagged PDF 2.0 Is the Initial Reference Fixed Rendition

**Decision:** ACCEPTED FOR PROTOTYPE

The first prototype SHALL use Tagged PDF 2.0 as the fixed representation.

This choice is based on existing maturity in:

* fixed pages;
* printing;
* fonts;
* complex text;
* annotations;
* signatures;
* accessibility;
* archival workflows.

Where applicable, prototype testing shall evaluate:

* WTPDF;
* PDF/UA-2;
* PDF/A-4.

This decision does NOT mean the format is conceptually dependent on PDF forever.

---

# 14. Decision AD-012 — Do Not Design a New Page-Scene Format in 0.1

**Decision:** ACCEPTED

The project SHALL NOT initially create:

* a new PDF-like drawing language;
* a glyph scene language;
* a custom print graphics format;
* a custom vector document engine;
* a custom font layout model.

A new page-scene representation may only be reconsidered if experimental evidence demonstrates that existing fixed formats prevent an important architectural requirement.

---

# 15. Decision AD-013 — Semantic-to-Fixed Mapping Is a Core Research Contribution

**Decision:** ACCEPTED

Every sealed fixed rendition shall be capable of mapping visible fixed content back to semantic identity.

**Approved clarification (Phase 1B, incorporated 2026-08-31):**

> A fixed-rendition processor SHALL emit a revision- and rendition-bound semantic-to-fixed mapping as an output of rendering when the mapping profile is claimed. The generation mechanism is implementation-specific and non-normative. Reconstruction from the fixed rendition MAY be used for independent validation or recovery, but SHALL NOT be the required mapping-generation method.

**Evidence and decision history:** Phase 1's backward reconstruction experiment established a useful independent validation/recovery path, but reached only 62.6% macro mapping coverage. Phase 1B's renderer-emitted forward mapping reached 100% visible-node coverage, 100% logical-range coverage, and 3,094/3,094 valid fixed-page fragments; T08 and T09 each reached 100% mapping coverage. The emitted artifact remained a small correspondence layer rather than a second page-description or rendering model. These results approve forward emission as the required profile behavior while retaining reconstruction as an optional independent check.

Conceptually:

```text id="7s3t4q"
Semantic Node
n_123
      │
      ├── fixed fragment A
      │      page pg_12
      │
      └── fixed fragment B
             page pg_13
```

The mapping belongs to a specific semantic revision and fixed rendition pair.

It is NOT valid across arbitrary revisions.

---

# 16. Mapping 0.1 Minimum Model

The first experimental mapping model shall remain deliberately small.

It should support:

## Block mapping

```text id="3yw2r7"
Node ID
→ one or more page fragments
```

## Text mapping

```text id="ow4nn2"
Node ID
+
logical Unicode range
→ one or more geometric fragments
```

## Table mapping

```text id="o93edh"
Table ID
Row ID
Cell ID
→ page fragments
```

## Figure mapping

```text id="nmb2uj"
Figure ID
→ geometric region
```

The initial model SHOULD support:

* page ID;
* logical text range;
* quadrilateral;
* multiple fragments;
* transform where required.

The first implementation SHALL NOT attempt to standardize every possible glyph-level geometric case.

---

# 17. Decision AD-014 — Logical Text Order Is Canonical

**Decision:** ACCEPTED

Semantic text SHALL be stored in logical Unicode order.

Visual positioning SHALL NOT define semantic reading order.

This requirement is essential for:

* Arabic;
* bidirectional text;
* mixed Arabic/English;
* accessibility;
* search;
* copy/paste;
* AI processing.

The mapping layer may contain visual-order geometry while semantic text remains logical.

---

# 18. Decision AD-015 — Arabic/RTL Is a Core Conformance Requirement

**Decision:** ACCEPTED

Arabic and bidirectional text SHALL NOT be treated as later internationalization work.

All early prototypes must include:

* Arabic paragraphs;
* Arabic/English mixed text;
* Arabic-Indic and European numerals;
* URLs inside RTL text;
* punctuation;
* Arabic tables;
* footnotes;
* citations;
* equations near RTL text;
* Arabic captions;
* multi-column RTL layouts.

Validation shall test:

```text id="xwd1c2"
rendering
search
copy/paste
text extraction
logical order
mapping
accessibility
```

---

# 19. Decision AD-016 — Editable and Sealed States

**Decision:** ACCEPTED

The lifecycle shall distinguish:

```text id="pktd7l"
EDITABLE
```

and

```text id="17ylv7"
SEALED
```

## Editable

Semantic content is authoritative.

Fixed rendition may be absent or stale.

## Sealed

A fixed rendition has been generated and bound to a specific semantic revision.

Conceptually:

```text id="st50k4"
Semantic Revision
      +
Fixed Rendition
      +
Mapping
      +
Resource Inventory
      ↓
State Descriptor
      ↓
SEALED
```

---

# 20. Decision AD-017 — Sealing Uses Integrity Binding

**Decision:** ACCEPTED

Sealing SHALL bind at least:

* semantic revision;
* fixed rendition;
* mapping;
* required resources;
* relevant rendering provenance.

Cryptographic hashes SHALL be used to detect modification.

Digital identity/signature architecture is separate and may be added later.

Thus:

```text id="r4rthn"
integrity
≠
digital signature
```

The first prototype focuses on integrity.

---

# 21. Decision AD-018 — Arbitrary JavaScript Is Not Part of Core

**Decision:** ACCEPTED

Core documents SHALL NOT require or execute arbitrary JavaScript.

The safe profile shall prohibit or strongly restrict:

* JavaScript;
* event handlers;
* macros;
* plugins;
* executable SVG;
* automatic external resource loading;
* automatic network requests.

The document must remain usable offline.

Future interactivity should preferably use declarative behavior.

---

# 22. Decision AD-019 — Reuse Existing Annotation Standards

**Decision:** ACCEPTED

Annotations should reuse W3C Web Annotation concepts.

Annotations may target:

* Node ID;
* text range;
* page region;
* image region;
* table cell;
* figure;
* equation.

The project may define a small stable-node selector extension.

It SHALL NOT create a completely new annotation language.

---

# 23. Decision AD-020 — Accessibility Is Structural

**Decision:** ACCEPTED

Accessibility SHALL derive from the same semantic source used by agents and human editing.

Semantic structure must provide:

* headings;
* reading order;
* language;
* direction;
* lists;
* tables;
* captions;
* alt text;
* links;
* equations;
* footnotes;
* navigation.

Accessibility SHALL NOT be treated as metadata added after the document is visually complete.

---

# 24. Decision AD-021 — Rendering Engine Is Non-Normative

**Decision:** ACCEPTED

No specific browser or pagination engine shall define the document standard.

Prototype implementations shall compare multiple renderers.

Possible test implementations include:

* Chromium;
* Paged.js;
* Vivliostyle;
* WeasyPrint.

A particular engine/version may be recorded as provenance.

It shall not become the permanent definition of the document.

---

# 25. Decision AD-022 — Deterministic Means Preserving the Generated Fixed Scene

**Decision:** ACCEPTED

The initial meaning of deterministic fixed output is:

> Once finalized, the generated fixed rendition is preserved and verifiable.

The project does NOT currently promise that two independent HTML/CSS rendering engines will produce:

* byte-identical PDF;
* identical pagination;
* pixel-identical output.

Those are renderer research questions rather than Base-format promises.

---

# 26. Decision AD-023 — Import Confidence Must Be Explicit

**Decision:** ACCEPTED

Imported semantics SHALL distinguish:

```text id="ahhg4u"
ASSERTED
```

from:

```text id="p33j6p"
INFERRED
```

Example:

A native HTML `<table>` may be:

```text id="tkli65"
asserted semantic table
```

A table reconstructed from PDF coordinates may be:

```text id="gmclda"
inferred semantic table
```

AI-generated or heuristic semantics SHALL NOT silently become authoritative.

---

# 27. Decision AD-024 — PDF Is an Interoperability Target, Not an Enemy

**Decision:** ACCEPTED

The project shall support PDF because it is valuable for:

* printing;
* distribution;
* legal workflows;
* archival workflows;
* existing infrastructure.

Success does not require eliminating PDF.

A possible long-term outcome may be:

```text id="4np06d"
Semantic Document
      ↓
Edit / AI / responsive use
      ↓
PDF export when needed
```

This remains valuable even if PDF continues to dominate fixed-document distribution.

---

# 28. Deferred Features

The first experimental implementation SHALL NOT attempt to solve:

* full digital-signature architecture;
* outer-container long-term signatures;
* DRM;
* package encryption;
* full forms/workflow behavior;
* calculations;
* tracked changes;
* collaborative edit-history serialization;
* macros;
* arbitrary application scripting;
* universal DOCX round-trip;
* universal PDF reconstruction;
* full office-suite layout;
* real-time collaboration.

These may be reconsidered only after the core hypothesis is validated.

---

# 29. Core Experimental Hypotheses

The prototype shall test the following.

## H1 — Semantic Agent Advantage

Stable semantic structure and typed operations improve AI-agent document-edit correctness.

## H2 — Reduced Collateral Damage

Structured transactions reduce unrelated document corruption during agent edits.

## H3 — Stable Identity Advantage

Persistent IDs make references, annotations and agent targeting more reliable across edits.

## H4 — Dual Representation Viability

Semantic and fixed representations can coexist without unacceptable synchronization complexity.

## H5 — Mapping Viability

A semantic-to-fixed mapping can provide useful correspondence without becoming a second complete layout model.

## H6 — Arabic/RTL Viability

The architecture works correctly for Arabic and mixed bidirectional documents.

## H7 — EPUB Packaging Viability

EPUB OCF can serve as the underlying package without creating unacceptable compatibility or security problems.

## H8 — Existing Renderer Viability

Existing open rendering technologies can produce fixed output of sufficient quality without creating a custom renderer.

---

# 30. Primary Failure Conditions

The architecture must be reconsidered if testing demonstrates that:

1. semantic-to-fixed mapping becomes effectively another complete layout representation;
2. mapping cannot be validated reliably;
3. semantic and fixed content frequently diverge;
4. Arabic/RTL cannot be mapped reliably;
5. no open renderer can generate adequate tagged fixed output;
6. EPUB compatibility creates serious semantic or security confusion;
7. WTPDF plus a conventional API performs essentially as well for agent editing;
8. stable identity provides little measurable benefit;
9. maintaining both representations produces unacceptable complexity;
10. the project starts rebuilding PDF, EPUB, ODF or a browser engine.

---

# 31. Current Architecture Summary

The approved experimental architecture is:

```text id="bvb259"
EPUB-compatible OCF package
        │
        ▼
Authoritative semantic XHTML
        │
        ├── stable Document ID
        ├── stable Node IDs
        └── immutable Revision IDs
        │
        ▼
Transactional semantic operations
        │
        ▼
Renderer
        │
        ▼
Fixed Rendition
(reference implementation: Tagged PDF 2.0)
        │
        ▼
Semantic ↔ Fixed Mapping
        │
        ▼
Integrity State Descriptor
        │
        ▼
SEALED REVISION
```

The architecture intentionally reuses existing standards wherever possible.

The main experimental contributions are:

```text id="0wz9jx"
stable semantic identity
+
revision lifecycle
+
transaction-safe agent editing
+
semantic↔fixed mapping
+
sealed state binding
```

Everything else should be reused unless evidence demonstrates that it cannot satisfy the requirements.
