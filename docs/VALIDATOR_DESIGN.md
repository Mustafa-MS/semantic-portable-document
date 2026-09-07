# Format 0.1 validator design preview

This document describes a future validator architecture. The repository intentionally does not implement the production validator in this phase.

## Result contract

The validator emits the shape in `schemas/conformance-result.schema.json`. It reports Base independently from optional capabilities. Experimental presence is not certification:

```json
{
  "base": "PASS",
  "capabilities": {
    "Mapping": "PASS",
    "Fixed-Experimental": "PRESENT_EXPERIMENTAL",
    "Accessible": "NOT_CLAIMED"
  },
  "violations": []
}
```

Each finding carries a stable requirement ID, severity, resource, Node ID/revision/capability where relevant, and evidence. A tool limitation produces `NOT_TESTED`; it does not silently become PASS.

## Processing pipeline

```text
bounded input stream
  → safe ZIP directory scan (no extraction)
  → OCF/EPUB profile and normalized-name checks
  → EPUBCheck
  → resolve exactly one rootfile and OCF-linked SPD descriptors
  → parse package, capabilities, document/revision/state descriptors
  → inventory coverage and exact resource-byte hashes
  → XML/XHTML, identity, semantics, Unicode/bidi source checks
  → CSS/SVG/URL active-content and offline checks
  → sealed/current/stale binding checks
  → mapping schema and procedural correspondence checks
  → accessibility automation and manual-test inventory
  → capability-separated report
```

## 1. Safe package opening

Read the central directory under configurable limits before extracting. Reject duplicate names, unsupported/encrypted methods, traversal/absolute/backslash names, unsafe entry types, overlapping entries, and NFC-normalized collisions. Resolve each extraction path and prove it remains under a dedicated temporary directory. Treat resource exhaustion separately from conformance failure.

## 2. OCF and EPUB profile

Invoke EPUBCheck for inherited EPUB 3.3 rules instead of recreating it. Add only SPD restrictions: exact authoritative rendition declaration, local required resources, inventory coverage, capability metadata, and stricter active-content rules. Preserve raw EPUBCheck evidence with a mapping to SPD-BASE-001/002/005; do not translate unrelated warnings into SPD errors.

## 3. Metadata and schema validation

Resolve the three exact provisional SPD relationship tokens from `container.xml`; never scan filenames. Apply the Draft 2020-12 schemas to document state, inventory, lifecycle state, annotations, and mapping. Then perform cross-document checks schemas cannot express: equal Document/Revision IDs, unique inventory paths, discovery/descriptor agreement, exact OPF-versus-descriptor capability claims, capability dependency closure, and referenced-resource existence.

## 4. Resource inventory and integrity

Stream every listed ZIP entry through SHA-256 after decompression; compare exact byte count and digest. Only the inventory itself and lifecycle descriptor are unlisted exceptions. Do not normalize XML, JSON, CSS, line endings, or Unicode. Recompute both UTF-8 byte-sorted inventory projections, the RFC 8785 JCS state descriptor digest, inventory binding, mapping digest, and fixed digest. A recomputed self-digest detects accidental change, not malicious recomputation or signer identity.

## 5. Semantic XHTML and IDs

Use a hardened XML parser with external entities and network resolution disabled. Validate EPUB XHTML, language/direction metadata, native semantic structures, references, XML IDs, required Node IDs, and package-wide uniqueness. History-dependent persistence/copy rules are checked only when lineage history is supplied; otherwise report `NOT_TESTED`, not PASS.

Logical-order checks combine deterministic corpus/source-oracle tests, suspicious bidi-control diagnostics, and manual review. No general validator can infer the intended order of arbitrary prose with certainty.

## 6. CSS, SVG, and security

Use real tokenizing parsers, not regular expressions, for CSS URLs/imports and SVG/XML. Build a resource-reference graph, classify user-activated hyperlinks separately from automatic fetches, detect cycles, and verify every required edge resolves locally and is inventoried. Unsupported harmless layout is not a security failure.

## 7. Capabilities and lifecycle

Read discovery metadata from the OPF and authoritative ID/version declarations from document-state JSON; reject any claim-set disagreement or document-controlled status. Enforce dependency closure. Determine fixed state from explicit status plus Revision ID, renditionInputDigest, and resource digest:

- `absent`: no current fixed presentation;
- `stale`: may be retained in EDITABLE but never exposed as current;
- `current`: matching revision and verified bytes;
- inconsistent declaration: failure.

A sealed semantic-only state is permitted. Current fixed output does not imply Mapping. Mapping requires a current fixed rendition and mapping artifact but does not require a Fixed-Experimental claim.

## 8. Mapping

After schema validation:

1. match Document/Revision/Fixed IDs and fixed digest;
2. index page IDs and dimensions;
3. resolve every Node ID in authoritative XHTML;
4. calculate the node semantic text value and scalar length;
5. verify half-open range bounds/order;
6. reject NaN/infinite or out-of-page geometry and invalid point order;
7. enforce status/fragment rules and honest reasons;
8. report forward-layout versus recovery/inferred provenance;
9. ensure no page-description/font/glyph instructions have entered the correspondence artifact.

Geometry comparison with an independently extracted PDF is optional evidence, not the required generation method.

## 9. Accessibility

Use EPUBCheck and mature HTML/ARIA accessibility engines where applicable. Retain tool/version output. Automated checks cover structural invariants; the final report enumerates required human checks for alternative-text meaning, reading order, table semantics, link purpose, and the declared WCAG target. A fixed export claim runs its own external profile tooling (for example veraPDF for a PDF profile) and never inherits PASS from XHTML.

## 10. Tool boundaries

Prefer existing maintained tools:

- EPUBCheck for EPUB/OCF/content-document requirements;
- a secure XML parser and HTML/ARIA conformance tooling;
- a standards-aware CSS parser;
- platform cryptographic SHA-256;
- JSON Schema Draft 2020-12 implementation;
- Unicode libraries with a declared Unicode version;
- fixed-format validators only for separately claimed experimental profiles.

The validator must pin tool/profile versions in reports. It must not fetch schemas, contexts, fonts, or referenced resources from the network while validating an untrusted package.

## 11. Test architecture

Corpus packages are immutable inputs. Parameterized tests run each package through applicable stages and compare the normalized result against `expected.json`. Mutation tests start from `valid/sealed`, alter exactly one covered resource without rebinding, and require SPD-INT-003/STATE failures. Schema tests are supplemented with procedural assertions because JSON Schema cannot validate ZIP paths, digest bytes, DOM identities, range lengths, or cross-resource bindings.

## 12. Exit criteria for implementation

The clarified Draft resolves identity grammar, inventory coverage, both digest projections, range/text-value algorithm, geometry, capability serialization, dependencies, and the Accessible target. Production validator work may begin against the Draft. Stable project-controlled schema/capability/discovery/annotation identifiers remain a Release Candidate blocker but do not make Draft algorithms ambiguous.
