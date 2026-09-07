# Conformance corpus EPUBCheck results

**Tool:** EPUBCheck 5.3.0 (repository-pinned Phase 1B copy)

**Scope:** every package classified as Base-valid: all packages under `tests/valid/` and `tests/edge/`.

| Class | Fixture | Result |
|---|---|---|
| valid | accessible | PASS |
| valid | annotations | PASS |
| valid | arabic | PASS |
| valid | figure-svg | PASS |
| valid | fixed-without-mapping | PASS |
| valid | lineage-scoped-annotation | PASS |
| valid | mapped | PASS |
| valid | mapping-with-current-fixed | PASS |
| valid | mathml | PASS |
| valid | minimal-base | PASS |
| valid | mixed-bidi | PASS |
| valid | multi-spine | PASS |
| valid | revision-scoped-annotation | PASS |
| valid | same-semantic-different-revision-id | PASS |
| valid | sealed | PASS |
| valid | semantic-change-new-revision | PASS |
| valid | semantic-only-sealed | PASS |
| valid | table | PASS |
| edge | cjk-vertical | PASS |
| edge | combining-character-range | PASS |
| edge | css-change-stales-fixed | PASS |
| edge | deep-lists | PASS |
| edge | emoji-range | PASS |
| edge | empty-section | PASS |
| edge | font-change-stales-fixed | PASS |
| edge | node-not-visible | PASS |
| edge | partial-mapping | PASS |
| edge | rtl-range | PASS |
| edge | table-spanning-pages | PASS |
| edge | unsupported-mapping | PASS |
| edge | very-long-paragraph | PASS |

Final result: **31/31 PASS** (18 valid fixtures and 13 Base-valid edge fixtures).

EPUBCheck covers inherited EPUB/OCF rules. The repository conformance checks separately cover JSON Schema validation, descriptor discovery, complete inventory coverage and hashes, digest projections, state/fixed/mapping bindings, capability dependencies, and expected corpus classifications.
