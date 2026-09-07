# Controlled external evaluation

Both validators invoked official EPUBCheck 5.3.0 for all 70 fixtures, including native failures: 140 completed evaluations, zero skips and zero operational failures. Every record has fixture SHA-256, version, executed flag, skip reason, exit code, diagnostic codes, attributed SPD IDs and raw stdout/stderr. Exit, codes and attribution agree for all 70. Raw line endings/messages are not normative equality fields.

The exact per-fixture records are in each versioned freeze and full native reports are in `final-0.1.1-detailed-a.json` / `final-0.1.1-detailed-b.json`. Environment/source/schema hashes and aligned common limits are in each freeze and `environment.json`. Both use a 120-second evaluation timeout. A retains bounded output capture; B retains its prior subprocess containment. No parser or ZIP safety check was relaxed.

Official JAR SHA-256: `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`. Its previously verified release ZIP SHA-256 is `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5`.

## Attribution

The shared Contract 0.1.1 code-plus-message policy distinguishes ZIP/OCF, content XML, identity and offline resource predicates. OPF-014, OPF-074 and other unmatched diagnostics remain raw; they are not automatically BASE-002. No post-run primary-error filter is applied.

## Historical evidence correction

Stage 2 correctly identified only 31 retained A external records versus 69 B records. Inspection of the old A freezer shows it actually invoked A with EPUBCheck for every fixture, then retained detailed logs only for valid/edge fixtures and removed BASE-002 whenever another failed ID existed. Thus 31 is a retained-evidence count, not proof of only 31 invocations. The historical script, freezes and Stage 2 reports remain unchanged. This new workflow records every invocation and never filters failed IDs.

A second metadata correction: unicode-normalization 0.1.25 exports Unicode 17.0.0, not the historical hardcoded Unicode 16 label. A now reports the crate constant. B uses Unicode 15.1.0. These are controlled same-corpus/tool/policy runs, not bit-identical environments; no observed fixture outcome differs because of Unicode.

## Every fixture

Both executed=true and skipReason=null throughout. Package digests appear beside these records in the machine-readable freezes.

| Fixture | A exit | B exit | Diagnostic codes | Guarded SPD attribution |
| --- | --- | --- | --- | --- |
| edge/cjk-vertical | 0 | 0 | — | — |
| edge/combining-character-range | 0 | 0 | — | — |
| edge/css-change-stales-fixed | 0 | 0 | — | — |
| edge/deep-lists | 0 | 0 | — | — |
| edge/emoji-range | 0 | 0 | — | — |
| edge/empty-section | 0 | 0 | — | — |
| edge/font-change-stales-fixed | 0 | 0 | — | — |
| edge/node-not-visible | 0 | 0 | — | — |
| edge/partial-mapping | 0 | 0 | — | — |
| edge/rtl-range | 0 | 0 | — | — |
| edge/table-spanning-pages | 0 | 0 | — | — |
| edge/unsupported-mapping | 0 | 0 | — | — |
| edge/very-long-paragraph | 0 | 0 | — | — |
| invalid/bad-resource-hash | 0 | 0 | — | — |
| invalid/capability-status-not-user-controlled | 0 | 0 | — | — |
| invalid/cross-spine-duplicate-node-id | 0 | 0 | — | — |
| invalid/descriptor-discovery-conflict | 0 | 0 | — | — |
| invalid/descriptor-discovery-missing | 0 | 0 | — | — |
| invalid/duplicate-node-id | 1 | 1 | RSC-005 | SPD-ID-006 |
| invalid/duplicate-normalized-path | 1 | 1 | OPF-060, OPF-074 | SPD-BASE-002 |
| invalid/event-handler | 1 | 1 | OPF-014, RSC-005 | SPD-ID-006 |
| invalid/external-required-css | 1 | 1 | RSC-006 | SPD-SEC-005 |
| invalid/external-required-font | 1 | 1 | OPF-014, RSC-008 | SPD-SEC-004 |
| invalid/external-required-image | 1 | 1 | OPF-014, RSC-006 | SPD-SEC-006 |
| invalid/invalid-table-semantics | 0 | 0 | — | — |
| invalid/invalid-xhtml | 1 | 1 | RSC-005, RSC-016 | SPD-SEM-002 |
| invalid/javascript | 1 | 1 | OPF-014 | — |
| invalid/mapping-invalid-geometry | 0 | 0 | — | — |
| invalid/mapping-invalid-page | 0 | 0 | — | — |
| invalid/mapping-invalid-range | 0 | 0 | — | — |
| invalid/mapping-with-stale-fixed | 0 | 0 | — | — |
| invalid/mapping-wrong-rendition | 0 | 0 | — | — |
| invalid/mapping-wrong-revision | 0 | 0 | — | — |
| invalid/missing-document-id | 0 | 0 | — | — |
| invalid/missing-revision-id | 0 | 0 | — | — |
| invalid/missing-root-direction | 0 | 0 | — | — |
| invalid/missing-root-language | 0 | 0 | — | — |
| invalid/multiple-rootfiles | 0 | 0 | RSC-017, RSC-019 | — |
| invalid/mutation-asset | 0 | 0 | — | — |
| invalid/mutation-css | 0 | 0 | — | — |
| invalid/mutation-fixed | 0 | 0 | — | — |
| invalid/mutation-mapping | 0 | 0 | — | — |
| invalid/mutation-semantic | 0 | 0 | — | — |
| invalid/not-visible-reason | 0 | 0 | — | — |
| invalid/partial-mapping-reason | 0 | 0 | — | — |
| invalid/path-traversal | 0 | 0 | — | — |
| invalid/sealed-after-annotation-modification | 0 | 0 | — | — |
| invalid/sealed-after-semantic-modification | 0 | 0 | — | — |
| invalid/stale-fixed-rendition | 0 | 0 | — | — |
| invalid/unlisted-non-normative-resource | 0 | 0 | — | — |
| invalid/unlisted-normative-resource | 0 | 0 | — | — |
| invalid/visual-order-arabic-source | 0 | 0 | — | — |
| valid/accessible | 0 | 0 | — | — |
| valid/annotations | 0 | 0 | — | — |
| valid/arabic | 0 | 0 | — | — |
| valid/figure-svg | 0 | 0 | — | — |
| valid/fixed-without-mapping | 0 | 0 | — | — |
| valid/lineage-scoped-annotation | 0 | 0 | — | — |
| valid/mapped | 0 | 0 | — | — |
| valid/mapping-with-current-fixed | 0 | 0 | — | — |
| valid/mathml | 0 | 0 | — | — |
| valid/minimal-base | 0 | 0 | — | — |
| valid/mixed-bidi | 0 | 0 | — | — |
| valid/multi-spine | 0 | 0 | — | — |
| valid/revision-scoped-annotation | 0 | 0 | — | — |
| valid/same-semantic-different-revision-id | 0 | 0 | — | — |
| valid/sealed | 0 | 0 | — | — |
| valid/semantic-change-new-revision | 0 | 0 | — | — |
| valid/semantic-only-sealed | 0 | 0 | — | — |
| valid/table | 0 | 0 | — | — |
