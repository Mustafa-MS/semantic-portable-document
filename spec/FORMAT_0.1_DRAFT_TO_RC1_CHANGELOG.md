# Format 0.1 Draft to RC1 change log

This change log compares the converged pre-RC Draft baseline with Format 0.1 Release Candidate 1. The Draft specification, Draft requirement registry, Draft schemas, Corpus 0.1.2, reviewed oracle, and prior validator freezes remain preserved.

## Identifier/namespace finalization

- Replaced every normative `https://example.invalid/spd/` schema `$id`, OCF discovery relationship, and capability discovery IRI with a permanent project-assigned UUID URN.
- Assigned permanent IRIs to `StableNodeSelector` and its compact extension terms; annotation documents carry the mappings inline and require no remote context fetch.
- Added the normative identifier/namespace registry and a no-reassignment policy.
- Retained the EPUB `application/epub+zip` container marker and existing JSON media types. No SPD-specific media type or mandatory filename extension was invented or registered.

## Editorial clarification

- Identified SPD consistently as a semantic portable-document format, with the layering: SPD document model → SPD passive content profile → EPUB-compatible packaging profile 0.1.
- Removed pre-RC and provisional wording from RC1 artifacts while keeping historical wording in frozen Draft artifacts.
- Kept `Fixed-Experimental` and `Archive-Experimental` experimental. PDF/PDF-A remain reference experimental renditions, not canonical or Base representations.
- Kept digital signatures, encryption/DRM, functional forms, interactive/scripting capability, collaboration/tracked changes, and the final agent API specification deferred.
- Preserved all 118 requirement IDs, levels, capability scopes, testability classifications, and conformance predicates. Three process/identifier descriptions were updated only to name the finalized identifiers.

## Normative-reference pinning

- Confirmed EPUB 3.3 Recommendation 13 January 2026, EPUB Reading Systems 3.3 Recommendation 17 October 2024, EPUB Accessibility 1.1 Recommendation 17 October 2024, and WCAG 2.2 Recommendation 12 December 2024.
- Replaced ambiguous traceability labels for Unicode, SVG, MathML, CSS, and HTML with the dated or governed baselines already selected in `UPSTREAM_DEPENDENCY_BASELINE_0.1.md`.
- Restated that future editions, errata, and living-standard changes do not silently redefine Format 0.1.

## Mechanical fixture/schema updates

- Created a new 107-fixture RC1 corpus. Draft/Corpus 0.1.2 packages remain untouched.
- Updated only identifier-bearing package resources and their deterministically derived byte lengths, SHA-256 bindings, semantic/rendering projections, inventory bindings, and RFC 8785 descriptor digests when the corresponding Draft binding was valid.
- Preserved deliberately invalid bindings, malformed ZIP behavior, special entry modes, expected Base/capability results, failed requirement IDs, NOT_TESTED sets, and operational statuses.
- Created a versioned RC1 canonical schema bundle. Schema structure is unchanged except for `$id` replacement and the finalized selector type IRI.

## Normative semantic changes

NONE
