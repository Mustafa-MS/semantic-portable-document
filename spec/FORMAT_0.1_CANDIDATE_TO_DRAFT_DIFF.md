# Format 0.1 Candidate-to-Draft normative diff

The Candidate remains unchanged. This register records every normative Draft clarification. No entry has `MATERIAL` architecture impact.

| Candidate section | Draft section | Decision | Old meaning | New meaning | Architecture impact |
|---|---|---|---|---|---|
| 1, 4, 68 | 4, 75 | A-001 | Standards-reuse/project directives looked document-normative. | Governance is informative and cannot fail a document; the RC identifier gate remains explicit. | NONE |
| 11–14 | 11–14 | A-002 | ID syntax was absent; prior schema imposed an arbitrary eight-character token minimum. | Document/Revision use lowercase RFC 9562 UUID URNs; Node/Fixed/Page use 1–128-character lowercase opaque tokens and 130-character total maximum. | CLARIFICATION |
| 12, 29 | 12, 29, 70 | A-003 | Revision identity versus digest was unspecified. | Revision ID is opaque; semanticStateDigest is separate; identical semantics may have distinct revision IDs. | CLARIFICATION |
| 13–15 | 14–15 | A-004 | “Unique within lineage” was presented as fully package-testable. | Current-revision uniqueness is document conformance; editor lineage preservation/non-reuse is history-dependent and becomes NOT_TESTED without history. | CLARIFICATION |
| 16 | 16 | A-005 | Language/direction were required only “where necessary.” | Root lang/xml:lang and explicit ltr/rtl direction are mandatory; nested direction changes are explicit. | CLARIFICATION |
| 28 | 28 | A-006 | Inventory coverage of caches/control files was ambiguous. | Every ZIP entry is inventoried except the inventory itself and lifecycle descriptor; caches are listed, never silently omitted. | CLARIFICATION |
| 28–29 | 29, 70–72 | A-007 | One underspecified integrity concept covered semantic and presentation state. | Exact decompressed resource bytes feed explicit semanticStateDigest and renditionInputDigest projections. | CLARIFICATION |
| 27 | 27 | A-008 | Candidate allowed optional fixed in a seal but earlier ADR prose implied fixed was required. | Semantic-only SEALED is explicitly valid; fixed, if present in SEALED, is current. | CLARIFICATION |
| 26 | 26, 31, 71 | A-009 | current/stale/absent lacked a complete machine test. | current requires matching Revision ID, renditionInputDigest, and fixed resource digest; mismatch is stale. | CLARIFICATION |
| 17, 40 | 40 | A-010 | Logical range unit/text extraction were unspecified. | Zero-based half-open Unicode scalar offsets over a precise DOM-logical text value; no generated content or whitespace collapse. | CLARIFICATION |
| 36–37 | 36 | A-011 | Geometry omitted units/origin/point order and prior schema required precision. | Page-local CSS px, top-left/+x right/+y down, TL/TR/BR/BL, finite in-page values, optional affine transform, no precision field. | CLARIFICATION |
| 38 | 38 | A-012 | Status names lacked fragment/reason cardinalities. | Exact MAPPED/PARTIALLY/NOT_VISIBLE/UNMAPPABLE/UNSUPPORTED meanings and cardinalities are normative. | CLARIFICATION |
| 54–59 | 54, 56, 58–59 | A-013 | Documents carried capability status and Mapping depended on a Fixed-Experimental claim. | Documents declare only ID/version; specification controls status; Mapping needs current fixed but no Fixed claim. | CLARIFICATION |
| 42–43, 58 | 42, 58 | A-014 | Accessible target version/level was open. | Accessible 0.1 is exactly EPUB Accessibility 1.1 plus WCAG 2.2 AA with applicable human evaluation. | CLARIFICATION |
| 22–24 | 23, 73 | A-015 | Web Annotation reuse was approved but EPUB Annotations status/namespace were open. | Web Annotation remains normative; EPUB Annotations draft is monitored/informative; stable SPD selector IRI is an RC blocker. | NONE |
| 16–17 | 17, 74 | A-016 | Logical order was mandatory without admitting general detection limits. | General prose assessment is partially automated; validators cannot overclaim inference. | CLARIFICATION |
| 8–9, 20 | 42, 74 | A-017 | Native-semantics applicability appeared fully decidable. | Known anti-patterns are automated; intent-dependent judgment remains human. | CLARIFICATION |
| none | 69 | A-018 | Processors had no normative descriptor discovery algorithm. | Exact OCF container links discover document-state, inventory, and lifecycle state; scanning/guessing is prohibited. | CLARIFICATION |
| 5, 8 | 5 | A-019 | EPUB allowed multiple rootfiles and SPD did not narrow them. | SPD Base has exactly one rootfile; its spine is authoritative; fixed output is not another rootfile. | CLARIFICATION |
| 54 | 54 | A-020 | Schema let documents declare normative/experimental status. | Status field is removed; schema allows only capability ID/version. | CLARIFICATION |
| 27, 56 | 27, 56 | A-021 | State schema made every current fixed rendition require Mapping. | Current fixed without Mapping is valid; Mapping claim cross-requires current fixed plus mapping. | CLARIFICATION |
| 28–29 | 72 | A-022 | Control-descriptor digest dependencies and exclusions were incomplete. | Exact cycle-free graph: resources→inventory→state; state self-digest uses RFC 8785 JCS with field omitted. | CLARIFICATION |
| 22, 27 | 73 | A-023 | Annotation edits after sealing were unspecified. | Annotation edit does not create semantic revision; packaged edit invalidates bound seal; external collections evolve independently. | CLARIFICATION |

## Release Candidate placeholders

The Draft deliberately retains `https://example.invalid/spd/` identifiers for schemas, capability discovery, OCF relationships, and annotation vocabulary. Replacing them with stable project-controlled identifiers is a normative Release Candidate gate, not a Draft processing ambiguity.
