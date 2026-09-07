# Phase 1 Experiment Design

## Goal and falsification posture

The harness tests whether semantic XHTML, persistent identity, atomic edits, a generated fixed PDF,
partial semantic/fixed mapping, and integrity binding form a coherent architecture. It does not try
to prove superiority. Unsupported checks and failures are first-class results.

## Independent variables

- Document structure: T01-T12 in `corpus/expected/corpus_manifest.json`.
- Renderer: Chromium, WeasyPrint, and a Vivliostyle/Paged.js-class adapter. Only installed engines run.
- Revision: original corpus state R1 versus the targeted T10 R2 update.
- Directionality: English LTR, Arabic RTL, and mixed Arabic/English bidi.

## Dependent measures

- Render success, time, page count, and PDF/package/mapping sizes.
- PDF text, link, image, font-resource, structure-tree, marked-content, and language observations.
- Semantic node mapping coverage and validation failures.
- Normalized semantic/PDF text similarity and exact Arabic logical-order phrase matches.
- Transaction atomicity, unrelated changed nodes, stale-revision rejection, and node-hash rejection.
- Integrity detection after semantic, fixed, and mapping tampering.

## Corpus design

T01-T12 directly correspond to the required baseline, multipage paragraph, complex table, figure,
MathML, notes, columns, Arabic, mixed bidi, academic, legal, and accessibility stress cases. Each
addressable semantic object receives a random opaque ID persisted in `identities.json`. IDs are not
computed from text, position, page, numbering, DOM path, or hashes.

## Renderer procedure

Chromium runs headlessly with local-file access, network background activity disabled, and tagged
PDF export requested. Each successful PDF is inspected using `pypdf` and `pdfplumber`. A structure
tree or marked-content flag is an observation, not a conformance determination. Missing renderer
executables generate structured `RENDERING` records.

## Mapping algorithm 0.1

1. Parse each `data-node-id` element and obtain its logical Unicode text.
2. Extract ordered PDF words and geometry from each page.
3. Normalize tokens with Unicode NFKC and case folding, preserving decimal values.
4. Find an exact contiguous logical token sequence.
5. Group matched words by page and emit logical source ranges plus quadrilaterals.
6. For raster figures, associate a caption page with an extracted image region where possible.
7. Retain every unmatched node and reason. Large nested ancestors are intentionally not forced
   through the exact-sequence matcher.

This is deliberately smaller than a glyph scene. It will fail where extraction changes token order,
where vector content has no image object, or where MathML visual text differs from source text.

## Validation and negative controls

Mapping validation checks revision, fixed hash, node/page targets, duplicates, quad bounds, and text
ranges. Unit tests inject wrong revisions/hashes, unknown nodes, duplicates, invalid quads, and
range mismatches. T10 R1 mapping is also checked against R2 and must be rejected.

The T10 transaction changes the FROC cell and its exact discussion paragraph together. The commit
must preserve the two Node IDs, change revision and node hashes, change no unrelated semantic node,
and reject stale revision and wrong node hash attempts without changing source bytes.

## Packaging and integrity

Each EPUB-compatible ZIP stores the mimetype first and uncompressed, then container XML, package
document, navigation, source, CSS, local assets, mapping, state, and PDF. Internal ZIP/XML checks do
not replace EPUBCheck or reader trials. A sealed descriptor hashes the source, mapping, and fixed
PDF; temp copies are modified one at a time to verify detection.

## Evidence levels

- `VERIFIED BY TEST`: directly asserted by an executed harness check.
- `OBSERVED IN ONE IMPLEMENTATION`: Chromium/PDF-library behavior.
- `SUPPORTED BY STANDARD`: only used with cited primary standards evidence.
- `HYPOTHESIS`: proposed explanation or future comparison.
- `NOT VERIFIED`: missing tool, validator, reader, clipboard, human review, or comparative baseline.

## Stop conditions

The summary must recommend narrowing/stopping if broader trials show that mapping recreates a
renderer, equivalence is not useful, Arabic mapping is fundamentally unreliable, existing renderers
require enormous custom work, OCF compatibility fails, identity/transactions show no advantage, or
dual-representation complexity exceeds distributing source plus PDF.

