# Proposed Candidate Specification changes

These edits are proposals only. `FORMAT_0.1_CANDIDATE.md` is intentionally unchanged.

## Identity serialization (sections 11–14)

- **Current wording:** IDs are required but syntax is unspecified.
- **Problem:** No interoperable validation grammar.
- **Proposed wording:** “Document IDs and Revision IDs MUST be lowercase UUID URNs. Node IDs MUST match `n_[a-z0-9][a-z0-9._-]{7,127}` and be XML `ID` compatible. Fixed Rendition IDs MUST use the analogous `f_` grammar.”
- **Reason:** Deterministic interchange and schema validation.
- **Architecture impact:** CLARIFICATION.

## Revision identity (section 12)

- **Current wording:** A Revision ID identifies one immutable state.
- **Problem:** Digest relationship is unspecified.
- **Proposed wording:** “A Revision ID is opaque identity, not a content digest. Each revision descriptor MUST separately carry a SHA-256 semantic-state digest.”
- **Reason:** Separates identity from integrity without canonicalizing semantic content into an identifier.
- **Architecture impact:** CLARIFICATION.

## Inventory and hashing (sections 28–29)

- **Current wording:** Entries contain SHA-256 but covered bytes/resources are unspecified.
- **Problem:** Independent digest results can differ.
- **Proposed wording:** “Digest the exact decompressed ZIP-entry bytes, without text/XML normalization. Inventory all manifest resources and all resources affecting conformance or a claimed capability. `mimetype`, `META-INF/container.xml`, and explicitly non-normative caches may be omitted. The semantic-state digest is SHA-256 of UTF-8 records sorted by normalized path, each `path NUL byteLength NUL sha256 LF`, excluding generated fixed/mapping resources and the state descriptor itself.”
- **Reason:** Matches Phase 1 exact-resource-byte evidence and makes compression/timestamps irrelevant.
- **Architecture impact:** CLARIFICATION.

## Range model (sections 17 and 40)

- **Current wording:** Logical Unicode ranges are required.
- **Problem:** Unit and text extraction are undefined.
- **Proposed wording:** “Ranges are zero-based, half-open Unicode scalar-value offsets over the descendant text nodes of the identified node in DOM logical order. CSS generated content is excluded; source whitespace is not collapsed. `start <= end <= scalarLength`.”
- **Reason:** Cross-language deterministic behavior for Arabic, emoji, Indic, and combining marks.
- **Architecture impact:** CLARIFICATION.

## Geometry (sections 36–37)

- **Current wording:** Mapping may contain pages, quadrilaterals, and transforms.
- **Problem:** Coordinate conventions are absent.
- **Proposed wording:** “Geometry uses page-local CSS reference pixels, top-left origin, x right, y down. Quadrilateral points are TL, TR, BR, BL. Pages declare width/height and MAY declare a six-value affine transform to fixed-medium coordinates. Values MUST be finite and within page bounds after clipping.”
- **Reason:** Renderer-neutral forward geometry consistent with Phase 1B evidence.
- **Architecture impact:** CLARIFICATION.

## Statuses and provenance (sections 38–39)

- **Current wording:** Values are listed but not defined.
- **Problem:** Implementations can report the same failure differently.
- **Proposed wording:** Incorporate the definitions and record-level provenance rules from the mapping profile. Document-level provenance supplies defaults; every record repeats/overrides the evidence class.
- **Reason:** Deterministic reporting with minimal complexity.
- **Architecture impact:** CLARIFICATION.

## Fixed status (section 26)

- **Current wording:** A fixed rendition may be stale or absent.
- **Problem:** No machine representation.
- **Proposed wording:** “The state descriptor MUST declare `current`, `stale`, or `absent`. `current` is valid only when its Revision ID matches the current semantic revision and its digest verifies. A reader MUST treat mismatch as stale and MUST NOT present it as current.”
- **Reason:** Prevents silent stale presentation.
- **Architecture impact:** CLARIFICATION.

## Sealed state (section 27)

- **Current wording:** Fixed rendition is optional; earlier ADR wording implies it is required.
- **Problem:** Source conflict.
- **Proposed wording:** “A semantic-only revision MAY be sealed. If Fixed is present it MUST be current. If Mapping is claimed, both fixed rendition and mapping MUST be bound and current.”
- **Reason:** Honors the Candidate as primary normative source while resolving dependency behavior.
- **Architecture impact:** CLARIFICATION.

## Capabilities (sections 54–59)

- **Current wording:** Capability names and prose dependencies only.
- **Problem:** Claims are not discoverable/processable.
- **Proposed wording:** “Declare discovery links with EPUB package `dcterms:conformsTo`; declare the authoritative `{id,version,status}` set in document-state JSON. Mapping requires Base and Fixed-Experimental; Accessible requires Base; Archive-Experimental requires Base and Fixed-Experimental.”
- **Reason:** Reuses EPUB metadata while providing deterministic processing.
- **Architecture impact:** CLARIFICATION.

## Accessibility claim (sections 42–43, 58)

- **Current wording:** No target standard/version/level.
- **Problem:** Accessible PASS is underdefined.
- **Proposed wording:** “An Accessible claim MUST name its EPUB Accessibility and WCAG target. Format 0.1 recommends EPUB Accessibility 1.1 and WCAG 2.2 AA. Automated results do not replace required human evaluation.”
- **Reason:** Avoids false fully automated certification.
- **Architecture impact:** CLARIFICATION.

## Annotation dependency (sections 22–24)

- **Current wording:** Web Annotation is reused; a namespace is to be registered.
- **Problem:** EPUB Annotations 1.0 is currently a Working Draft.
- **Proposed wording:** “Web Annotation remains normative. `StableNodeSelector` uses a provisional project vocabulary until registered. EPUB Annotations 1.0 is a monitored informative dependency; compatibility SHOULD be maintained.”
- **Reason:** Avoids normatively freezing a draft while preserving convergence.
- **Architecture impact:** NONE.

## Governance clauses

- **Current wording:** Several uppercase clauses direct future specification work.
- **Problem:** They look like document conformance conditions.
- **Proposed wording:** Move them to a clearly marked “Specification governance” subsection and state they do not affect document conformance.
- **Reason:** Clean validator scope.
- **Architecture impact:** NONE.

No proposed change requires `MATERIAL CHANGE` or reopening the architecture.

