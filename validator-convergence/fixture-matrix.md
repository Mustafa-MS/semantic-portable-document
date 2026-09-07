# Corpus 0.1.1 fixture matrix

Every value below is equal in A, B and the independently reviewed oracle. All operational statuses are COMPLETE. Missing/conflicting descriptor fixtures carry UNKNOWN authority and capabilities; all others have KNOWN authority. Full values, digests, pairwise fields and old Stage 2 outcomes are in `differential-results.json`. Experimental equality is measured separately.

| Fixture | Base | Accessible | Mapping | Failed IDs | NOT_TESTED IDs | Three-way exact | Experimental exact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| edge/cjk-vertical | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/combining-character-range | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/css-change-stales-fixed | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/deep-lists | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/emoji-range | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/empty-section | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/font-change-stales-fixed | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/node-not-visible | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/partial-mapping | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/rtl-range | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/table-spanning-pages | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| edge/unsupported-mapping | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| edge/very-long-paragraph | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| invalid/bad-resource-hash | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-INT-003, SPD-INT-004, SPD-INT-005, SPD-RES-004 | SPD-ID-013 | YES | YES |
| invalid/capability-status-not-user-controlled | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-CAP-002 | SPD-ID-013 | YES | YES |
| invalid/cross-spine-duplicate-node-id | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ID-006 | SPD-ID-013 | YES | YES |
| invalid/descriptor-discovery-conflict | FAIL | UNKNOWN | UNKNOWN | SPD-DISC-002 | SPD-CAP-002, SPD-CAP-003, SPD-ID-002, SPD-ID-013, SPD-INT-004, SPD-INT-005, SPD-INT-006, SPD-STATE-002, SPD-STATE-003, SPD-STATE-006, SPD-STATE-007 | YES | YES |
| invalid/descriptor-discovery-missing | FAIL | UNKNOWN | UNKNOWN | SPD-DISC-001 | SPD-CAP-002, SPD-CAP-003, SPD-ID-002, SPD-ID-013, SPD-INT-003, SPD-INT-004, SPD-INT-005, SPD-INT-006, SPD-RES-001, SPD-RES-002, SPD-RES-003, SPD-RES-004, SPD-RES-005, SPD-RES-006, SPD-STATE-002, SPD-STATE-003, SPD-STATE-006, SPD-STATE-007 | YES | YES |
| invalid/duplicate-node-id | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ID-006 | SPD-ID-013 | YES | YES |
| invalid/duplicate-normalized-path | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-BASE-002, SPD-RES-002 | SPD-ID-013 | YES | YES |
| invalid/event-handler | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ID-006, SPD-SEC-001 | SPD-ID-013 | YES | YES |
| invalid/external-required-css | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEC-005 | SPD-ID-013 | YES | YES |
| invalid/external-required-font | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEC-004 | SPD-ID-013 | YES | YES |
| invalid/external-required-image | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEC-006 | SPD-ID-013 | YES | YES |
| invalid/invalid-table-semantics | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEM-013 | SPD-ID-013 | YES | YES |
| invalid/invalid-xhtml | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEM-002 | SPD-ID-006, SPD-ID-013 | YES | YES |
| invalid/javascript | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-SEC-001 | SPD-ID-013 | YES | YES |
| invalid/mapping-invalid-geometry | PASS | NOT_CLAIMED | FAIL | SPD-MAP-011, SPD-MAP-012 | SPD-ID-013 | YES | YES |
| invalid/mapping-invalid-page | PASS | NOT_CLAIMED | FAIL | SPD-MAP-011 | SPD-ID-013 | YES | YES |
| invalid/mapping-invalid-range | PASS | NOT_CLAIMED | FAIL | SPD-MAP-008 | SPD-ID-013 | YES | YES |
| invalid/mapping-with-stale-fixed | PASS | NOT_CLAIMED | FAIL | SPD-STATE-007 | SPD-ID-013 | YES | YES |
| invalid/mapping-wrong-rendition | PASS | NOT_CLAIMED | FAIL | SPD-MAP-002 | SPD-ID-013 | YES | YES |
| invalid/mapping-wrong-revision | PASS | NOT_CLAIMED | FAIL | SPD-MAP-002 | SPD-ID-013 | YES | YES |
| invalid/missing-document-id | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ID-001 | SPD-ID-013 | YES | YES |
| invalid/missing-revision-id | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ID-002 | SPD-ID-013 | YES | YES |
| invalid/missing-root-direction | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-I18N-004 | SPD-ID-013 | YES | YES |
| invalid/missing-root-language | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-I18N-003 | SPD-ID-013 | YES | YES |
| invalid/multiple-rootfiles | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-BASE-006 | SPD-ID-013 | YES | YES |
| invalid/mutation-asset | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004, SPD-STATE-003 | SPD-ID-013 | YES | YES |
| invalid/mutation-css | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004 | SPD-ID-013 | YES | YES |
| invalid/mutation-fixed | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007 | SPD-ID-013 | YES | YES |
| invalid/mutation-mapping | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004, SPD-STATE-002 | SPD-ID-013 | YES | YES |
| invalid/mutation-semantic | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004, SPD-STATE-003 | SPD-ID-013 | YES | YES |
| invalid/not-visible-reason | PASS | NOT_CLAIMED | FAIL | SPD-MAP-005 | SPD-ID-013 | YES | YES |
| invalid/partial-mapping-reason | PASS | NOT_CLAIMED | FAIL | SPD-MAP-005 | SPD-ID-013 | YES | YES |
| invalid/path-traversal | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-BASE-002, SPD-RES-002 | SPD-ID-013 | YES | YES |
| invalid/sealed-after-annotation-modification | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-ANN-004, SPD-INT-003, SPD-RES-004 | SPD-ID-013 | YES | YES |
| invalid/sealed-after-semantic-modification | FAIL | NOT_CLAIMED | FAIL | SPD-INT-003, SPD-RES-004, SPD-STATE-003 | SPD-ID-013 | YES | YES |
| invalid/stale-fixed-rendition | PASS | NOT_CLAIMED | FAIL | SPD-STATE-007 | SPD-ID-013 | YES | YES |
| invalid/unlisted-non-normative-resource | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-RES-003, SPD-RES-006 | SPD-ID-013 | YES | YES |
| invalid/unlisted-normative-resource | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-RES-003, SPD-RES-006 | SPD-ID-013 | YES | YES |
| invalid/visual-order-arabic-source | FAIL | NOT_CLAIMED | NOT_CLAIMED | SPD-I18N-001 | SPD-ID-013 | YES | YES |
| valid/accessible | PASS | NOT_TESTED | NOT_CLAIMED | — | SPD-ACC-001, SPD-ACC-004, SPD-ID-013 | YES | YES |
| valid/annotations | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/arabic | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/figure-svg | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/fixed-without-mapping | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/lineage-scoped-annotation | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/mapped | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| valid/mapping-with-current-fixed | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| valid/mathml | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/minimal-base | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/mixed-bidi | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/multi-spine | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/revision-scoped-annotation | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/same-semantic-different-revision-id | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/sealed | PASS | NOT_CLAIMED | PASS | — | SPD-ID-013 | YES | YES |
| valid/semantic-change-new-revision | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/semantic-only-sealed | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
| valid/table | PASS | NOT_CLAIMED | NOT_CLAIMED | — | SPD-ID-013 | YES | YES |
