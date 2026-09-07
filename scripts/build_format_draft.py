"""Build FORMAT_0.1_DRAFT.md from the preserved Candidate plus approved decisions."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "spec" / "FORMAT_0.1_CANDIDATE.md"
DRAFT = ROOT / "spec" / "FORMAT_0.1_DRAFT.md"


def replace_section(text: str, number: int, title: str, body: str) -> str:
    pattern = rf"(?ms)^# {number}\. .*?(?=^# {number + 1}\. |\Z)"
    replacement = f"# {number}. {title}\n\n{body.strip()}\n\n---\n\n"
    updated, count = re.subn(pattern, replacement, text)
    if count != 1:
        raise ValueError(f"Expected one section {number}, replaced {count}")
    return updated


def main() -> None:
    text = CANDIDATE.read_text(encoding="utf-8")
    text = re.sub(r"\\(?=[#*+_.-])", "", text)
    text = text.replace("## Candidate Specification", "## Draft Specification")
    text = text.replace("**Status:** Candidate specification", "**Status:** Draft specification — clarified and frozen for validator implementation")

    sections = {
        4: ("Normative Technology Baseline", """
The normative baseline is EPUB 3.3 OCF-compatible packaging, XHTML, CSS, MathML, SVG, Unicode including UAX #9, W3C Web Annotation, native HTML semantics, WAI-ARIA/DPUB-ARIA where applicable, EPUB Accessibility 1.1, WCAG 2.2, SHA-256, RFC 9562 UUID URNs, RFC 8785 JCS, and JSON Schema Draft 2020-12 as profiled here.

EPUB 3.4 and EPUB Annotations 1.0 drafts MAY inform implementations but are not normative dependencies. Specification-development preferences are informative and appear in section 75; they do not create document conformance failures.
"""),
        5: ("Package and Authoritative Package Document", """
A Format 0.1 document MUST be an EPUB 3.3 OCF-compatible ZIP package and MUST satisfy the inherited OCF rules plus the stricter OCF profile.

`META-INF/container.xml` MUST contain exactly one `rootfile` package document. The spine of that package document defines the authoritative semantic reading order. Multiple EPUB rootfiles MUST NOT be used for fixed renditions. Fixed renditions are generated resources bound through SPD state and mapping.

All entry paths MUST be relative, forward-slash-separated, Unicode NFC paths without dot segments, traversal, ambiguous normalized duplicates, or duplicate ZIP names. Stored and Deflate are the only compression methods. Section 69 defines deterministic SPD descriptor discovery.
"""),
        11: ("Document Identity", """
Every document MUST have a persistent Document ID identifying one lineage. It MUST be a lowercase UUID URN using RFC 9562 textual UUID syntax:

```text
urn:uuid:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Alphabetic hexadecimal digits MUST be lowercase. UUIDv4 or UUIDv7 are RECOMMENDED generation choices, but processors MUST treat UUID values as opaque and MUST NOT rely on generation-time or version semantics.
"""),
        12: ("Revision Identity", """
Each committed semantic state MUST have a Revision ID using the Document-ID grammar. A Revision ID is opaque identity and MUST NOT encode semantic-state identity or be a content digest.

Semantic modification MUST create a new Revision ID. A change confined to a resource with `affects: []` MUST NOT by itself create a new semantic revision. Two independently committed, semantically identical states MAY have different Revision IDs and the same `semanticStateDigest`.
"""),
        13: ("Node Identity and Syntax", """
Independently addressable semantic objects MUST carry persistent Node IDs, including sections, headings, paragraphs, list items, figures, captions, tables, rows, cells, equations, notes, citations, references, and preserved controls.

A Node ID has the grammar `n_<opaque-token>`. The token contains 1–128 lowercase ASCII characters from `[a-z0-9._-]`; the complete ID therefore has maximum length 130. The form is XML-ID compatible because it begins with `n_`. Additional inline structures MAY receive IDs.
"""),
        14: ("Node ID Document Conformance", """
Node IDs MUST be unique in the current authoritative semantic revision. They MUST NOT depend on page position, DOM path, visible numbering, text content, or content hash. A logically persistent object MAY retain its Node ID when moved, restyled, renamed, or edited.

Current-revision uniqueness is fully automated document conformance. Historical persistence is governed separately by section 15.
"""),
        15: ("Node Lineage Conformance", """
A conforming editor supplied with lineage history MUST preserve Node identity according to the copy, split, merge, and deletion rules and MUST NOT knowingly reuse a retired Node ID in that history. A copied logical object normally receives a new Node ID. Split/merge retention policy may be user-interface-specific but lineage provenance SHOULD be preserved.

When lineage history is unavailable, a standalone validator MUST report historical persistence and non-reuse checks as `NOT_TESTED`. Missing history MUST NOT make an otherwise conforming standalone package fail Base.
"""),
        16: ("Logical Text, Language, and Direction", """
Semantic text MUST be stored in logical Unicode order. Visual placement MUST NOT determine semantic ordering.

The root `<html>` of every authoritative XHTML document MUST contain valid, equivalent `lang` and `xml:lang` values and MUST explicitly declare `dir="ltr"` or `dir="rtl"`. Root `dir="auto"` is prohibited. A nested semantic element MUST declare direction when its intended base direction differs from the inherited direction. `dir="auto"` MAY be used for appropriate nested or user-generated content.
"""),
        17: ("Arabic, Bidirectional Text, and Detection Limits", """
Arabic and bidirectional behavior are normative conformance cases. Mapping and editing APIs MUST operate on logical text ranges and MUST NOT equate visual left-to-right position with logical order.

General natural-language intended order is `PARTIALLY_AUTOMATED`. Validators MUST use deterministic corpus/oracle checks and MAY report suspicious bidi controls or patterns, but MUST NOT claim they can always infer the intended logical order of arbitrary prose.
"""),
        23: ("StableNodeSelector", """
Format 0.1 defines a minimal W3C Web Annotation selector extension.

`scope: "lineage"` MUST contain Document ID and Node ID and MUST omit Revision ID. It follows the logical node across revisions while that Node ID survives.

`scope: "revision"` MUST contain Document ID, Revision ID, and Node ID and anchors the exact historical state.

The Draft provisional type name is `StableNodeSelector`. A stable public IRI/context is REQUIRED before Release Candidate (section 75).
"""),
        26: ("Editable State and Fixed Status", """
In `EDITABLE`, semantic content is authoritative and may be committed as a new revision. Fixed status is `absent`, `current`, or `stale`.

`current` is valid only when the fixed Revision ID equals the current Revision ID, the fixed `renditionInputDigest` equals the current value, and the fixed resource digest verifies. A mismatch MUST be treated as stale regardless of the declared token. A reader MUST NOT expose stale fixed content as current.
"""),
        27: ("Sealed State", """
A `SEALED` state finalizes one semantic revision and binds its Revision ID, semantic/rendition digests, inventory, and any present fixed/mapping artifacts.

A semantic-only revision MAY be SEALED. If a fixed rendition is present in SEALED, its status MUST be current. A fixed rendition MAY exist without Mapping. If Mapping is claimed, a current fixed rendition and mapping artifact are REQUIRED.

Changing any inventoried packaged resource invalidates the sealed state unless inventory and descriptor bindings are recomputed as a new internally consistent state. This is integrity, not signer authentication.
"""),
        28: ("Resource Inventory and Effects", """
Exactly one normative inventory MUST be discovered through section 69. It MUST list every ZIP entry, including `mimetype`, `META-INF/container.xml`, controls, caches, annotations, fixed output, and mapping, except the inventory itself and lifecycle state descriptor.

Every entry MUST include normalized NFC `path`, `mediaType`, exact decompressed `byteLength`, lowercase SHA-256, `role`, and `affects`. `affects` is a unique subset of `semantic` and `rendering`; an empty array means neither input scope. Role describes authority/provenance and MUST NOT be used to infer effects.

Unknown or unlisted ZIP entries outside the two explicit self-reference exceptions MUST fail Base. Non-normative caches remain listed with role `non-normative` and normally `affects: []`.
"""),
        29: ("Integrity", """
Resource SHA-256 covers exact decompressed ZIP-entry bytes without XML, JSON, Unicode, encoding, whitespace, or line-ending normalization. Compression method and ZIP timestamps do not affect resource digest identity.

Format 0.1 separately defines `semanticStateDigest`, `renditionInputDigest`, inventory digest, and `descriptorDigest` in sections 70–72. Integrity MUST detect covered semantic, style, font, asset, annotation, mapping, fixed, inventory, and state changes. Integrity is distinct from digital signature.
"""),
        31: ("Fixed Rendition Concept", """
A fixed rendition is an optional generated page appearance. It MUST identify an opaque `f_<token>` Fixed Rendition ID, source Revision ID, source `renditionInputDigest`, exact resource digest, path, and media type. Its token uses the Node-token grammar.

Presentation-only input changes do not introduce a Presentation Revision ID: they change `renditionInputDigest` and make the old fixed rendition stale.
"""),
        34: ("Semantic-to-Fixed Mapping", """
When Mapping is claimed, the renderer MUST emit a mapping artifact during fixed rendering. The mapping MUST bind Document ID, Revision ID, Fixed Rendition ID, and fixed resource digest.

Mapping requires Base, a current fixed rendition, and a mapping artifact. It does not require a separate `Fixed-Experimental` capability claim.
"""),
        36: ("Mapping and Geometry Model", """
A mapping is correspondence, not page description. It MAY contain Node ID, logical range, rendition-local Page ID, quad, optional affine transform, status, and provenance. It MUST NOT contain glyph rendering, font recreation, drawing operations, line breaking, or layout algorithms.

Geometry uses page-local CSS reference pixels, top-left origin, +x right, +y down. Each page MUST declare `p_<token>` ID, positive width, and positive height. Page IDs are unique only within that fixed rendition. Quad order is TL, TR, BR, BL. Values MUST be finite and visible fragments MUST be bounded by page space. A six-value affine transform MAY map to native fixed-medium coordinates. No precision field is defined; tolerance is validator/test policy.
"""),
        38: ("Mapping Status", """
Mapping records use exactly one status:

- `MAPPED`: all required visible correspondence represented; at least one fragment.
- `PARTIALLY_MAPPED`: some represented and known required visible correspondence missing; at least one fragment and a reason.
- `NOT_VISIBLE`: intentionally no visible representation; zero fragments and a reason.
- `UNMAPPABLE`: supported feature class but reliable instance correspondence cannot be established; zero fragments and a reason.
- `UNSUPPORTED`: implementation does not support mapping this feature class; zero fragments and a reason.

`NOT_VISIBLE` MUST NOT mean algorithm failure. Geometry MUST NOT be fabricated to claim coverage.
"""),
        40: ("Logical Range Model", """
Mapping and annotation text ranges are zero-based, half-open `[start,end)` Unicode scalar-value offsets over the semantic text value. They are not UTF-8 bytes, UTF-16 code units, or grapheme counts.

For the selected Node, the semantic text value concatenates descendant XML text nodes in DOM logical order after character-reference expansion, excluding comments, processing instructions, `head`, `script`, `style`, and CSS-generated content. Source characters and whitespace are preserved; no whitespace collapse, Unicode normalization, shaping, or bidi reordering occurs.

`0 <= start <= end <= scalarLength`. Endpoints need not coincide with extended grapheme-cluster boundaries. Human-facing editors and annotation tools SHOULD avoid splitting extended grapheme clusters unless sub-grapheme addressing is intended.
"""),
        42: ("Accessibility Authority", """
Base accessibility is evaluated against the authoritative semantic XHTML. Native-semantics applicability and qualitative accessibility remain partially automated; validators MAY detect known anti-patterns but MUST retain human evaluation where intent or quality cannot be inferred.
"""),
        54: ("Conformance Capabilities and Declaration", """
The authoritative document-state descriptor declares only capability `id` and `version`. A document MUST NOT declare whether a capability is normative or experimental; this specification controls that status.

The capability claim set in EPUB `dcterms:conformsTo` discovery metadata MUST equal the authoritative descriptor set. Disagreement fails Base.

Format 0.1 defines Base (normative), Mapping (normative when claimed), Accessible (normative when claimed), Fixed-Experimental (experimental), and Archive-Experimental (experimental).
"""),
        56: ("Mapping Capability", """
Mapping requires Base, a current fixed rendition, a bound forward-emitted mapping artifact, valid page IDs/dimensions/geometry, status, provenance, and scalar logical ranges where used. A document need not claim Fixed-Experimental merely because Mapping targets a fixed rendition.
"""),
        58: ("Accessible Capability", """
SPD Accessible 0.1 is exactly EPUB Accessibility 1.1 plus WCAG 2.2 Level AA. A claiming document MUST declare that fixed target and satisfy it, including human evaluation for criteria that cannot be reliably automated. Additional claims MAY be present but do not redefine SPD Accessible 0.1.

Accessible requires Base. A standalone fixed export claiming accessibility independently satisfies its fixed-format accessibility profile.
"""),
        59: ("Archive-Experimental Capability", """
Archive remains experimental and requires at least Base, SEALED lifecycle, and a current archive-appropriate fixed rendition. Accessibility is separately claimable and is not implied by Archive. PDF/A-4 remains the reference archival fixed target, not a Base requirement.
"""),
    }

    for number in sorted(sections):
        title, body = sections[number]
        text = replace_section(text, number, title, body)

    appendix = r'''
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
'''
    text = text.rstrip() + "\n\n---\n\n" + appendix.strip() + "\n"
    DRAFT.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
