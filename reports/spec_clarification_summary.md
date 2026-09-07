# Format 0.1 specification clarification summary

## Outcome

The Candidate has been preserved as historical input. The Draft incorporates decisions A-001 through A-023 without a material architecture change. Its normative algorithms, schemas, requirement registry, conformance matrix, terminology, traceability, validator design, and generated test corpus now agree.

The resulting model contains 113 requirements and 69 fixtures: 18 valid, 38 invalid, and 13 edge. All 21 repository tests pass. EPUBCheck 5.3.0 passes all 31 packages classified as Base-valid.

## Were all known ambiguities resolved?

**Yes, for Draft conformance behavior.** Every ambiguity in the task has a normative disposition and an independently reproducible validation rule. Provisional public identifiers remain an explicit Release Candidate publication blocker, not an unresolved algorithmic ambiguity.

## Did any clarification require an architecture change?

**No.** Every applied decision is classified as `NONE` or `CLARIFICATION` in the Candidate-to-Draft diff. No change is classified as `MATERIAL`.

## Is descriptor discovery deterministic?

**Yes.** `META-INF/container.xml` must contain exactly one processing link for each required SPD descriptor, with these exact provisional relationships and `application/json` media type:

- `https://example.invalid/spd/rel/document-state`
- `https://example.invalid/spd/rel/resource-inventory`
- `https://example.invalid/spd/rel/lifecycle-state`

Processors do not scan or guess filenames. A missing, duplicate, or conflicting link fails conformance. Format 0.1 Base also requires exactly one OCF rootfile.

## Is the semantic-state versus rendition-input digest distinction deterministic?

**Yes.** The inventory declares an explicit `affects` set for every listed resource. `semanticStateDigest` projects resources marked `semantic`; `renditionInputDigest` projects resources marked `semantic` or `rendering`. Both use the same precisely specified byte record, normalized-path rules, UTF-8 bytewise sort, and SHA-256 procedure.

## Can presentation-only changes stale a fixed rendition without changing semantic Revision ID?

**Yes.** A CSS or font-only change leaves `semanticStateDigest` unchanged, changes `renditionInputDigest`, and therefore makes a fixed rendition bound to the former rendition-input digest stale. Revision IDs remain opaque semantic-revision identities; no presentation revision ID was introduced.

## Is the digest graph cycle-free?

**Yes.** Every ZIP entry is inventoried except the inventory descriptor itself and the lifecycle state descriptor. Resource bytes feed inventory records; inventory bytes are bound by the state descriptor; and the state descriptor self-digest is SHA-256 over its RFC 8785 canonical JSON form with `descriptorDigest` omitted. No node depends on its own final digest.

## Can a current fixed rendition exist without Mapping?

**Yes.** A fixed rendition may be `current` without a Mapping capability claim or mapping descriptor. It must still bind the current Revision ID and `renditionInputDigest`, and its resource digest must verify.

## Are Mapping dependency rules deterministic?

**Yes.** Claiming Mapping requires Base, a verified current fixed rendition, and a mapping descriptor bound to that rendition. A document does not need to claim `Fixed-Experimental`. A current fixed rendition alone does not imply Mapping.

## Is Accessible 0.1 exactly EPUB Accessibility 1.1 + WCAG 2.2 AA?

**Yes.** A document claiming SPD Accessible 0.1 must satisfy EPUB Accessibility 1.1 and WCAG 2.2 Level AA. Additional accessibility claims do not redefine that target, and criteria that cannot be reliably automated remain subject to human evaluation.

## Are Unicode scalar ranges interoperable across all existing internationalization fixtures?

**Yes.** Ranges are zero-based, half-open Unicode scalar-value offsets over the defined semantic text value. No whitespace collapsing, CSS-generated content, byte counting, UTF-16 indexing, or grapheme counting enters the algorithm. The Arabic/RTL, emoji, combining/Indic-sequence, CJK vertical-writing, and mixed-bidi fixtures exercise those rules and pass the repository checks.

## Does the revised mapping schema remain a small correspondence layer?

**Yes.** It contains rendition-local pages, scalar text ranges, page-local quadrilateral fragments, status, and reasons where required. The former required global `precision` field was removed; numeric comparison tolerance is validator policy rather than document state.

## Does the revised package remain EPUBCheck-valid?

**Yes.** EPUBCheck 5.3.0 reports **31/31 PASS** across all 18 valid fixtures and all 13 Base-valid edge fixtures. See `reports/conformance_epubcheck_results.md` for the fixture-level record.

## Are any normative placeholders still unresolved?

**Yes, deliberately and explicitly.** Draft schema IDs, capability IDs, descriptor relationship identifiers, and the StableNodeSelector/annotation namespace use provisional `https://example.invalid/...` identifiers. They must be replaced with stable project-controlled identifiers before Release Candidate. The Draft does not invent a production domain, and this publication task does not change validation semantics.

## Is Format 0.1 Draft ready for production validator implementation?

**Yes.** Two independent validator implementations now have deterministic discovery, serialization, hashing, state, dependency, mapping, identity, Unicode, and lifecycle rules, with corresponding registry entries and fixtures. Stable public identifiers block Release Candidate publication, but do not block implementation against the Draft identifiers.

READY FOR VALIDATOR IMPLEMENTATION
