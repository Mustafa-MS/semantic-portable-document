# Corpus 0.1.2 changes

70 historical packages retain their original bytes. Historical 0.1.1 manifest/expected files/oracles are not overwritten; new expectations live under tests/corpus-0.1.2/historical. The new version has **107 fixtures**: 70 retained plus **37 additions**.

S01–S30 implement the audit's enumerated Option-A plan. S31–S37 isolate seven explicitly required families: standalone SVG script, SVG event handler, bare iframe, authoritative canvas, ordinary hyperlink, nested CSS rule resource and annotation-xml active content. Existing script/event/remote font/stylesheet/image fixtures are retained. The count is 37 rather than 30 for these targeted reasons, not arbitrary bulk coverage.

The final local MathML glyph fixture uses a token-element child permitted by MathML. An exploratory misplacement was corrected before oracle finalization; no policy was weakened. S29 removes only the required OPF title and rebinds existing inventory/state; it produces BASE-002 without a more-specific native attribution. S27 tests local/central header mismatch; unit/scanner logic also rejects overlapping intervals. S28 is a small bounded ratio-limit fixture, not a universal format maximum.

Native expectations were authored from the profile before validator comparison. Direct EPUBCheck findings are reviewed through the shared attribution contract. Full A/B outputs are evidence, not the oracle. Human/processor NOT_TESTED portions are explicit. Every manifest row records package and expected-result SHA-256; manifest-sha256.txt pins the final manifest.

| Audit label | Fixture | Base | Native failed predicates | Direct EPUBCheck |
|---|---|---|---|---|
| S01 | security/optional-remote-image | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-008 | FAIL |
| S02 | security/escaped-remote-import | FAIL | SPD-SEC-003, SPD-SEC-005, SPD-SEC-008 | FAIL |
| S03 | security/inline-remote-style | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-008 | FAIL |
| S04 | security/custom-property-resource | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-008 | FAIL |
| S05 | security/nested-svg-remote | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-007, SPD-SEC-008 | PASS |
| S06 | security/inline-foreignobject | FAIL | SPD-PASS-002, SPD-SEC-007 | PASS |
| S07 | security/prefixed-svg-script | FAIL | SPD-SEC-001, SPD-SEC-007 | PASS |
| S08 | security/encoded-executable-link | FAIL | SPD-SEC-001, SPD-SEC-008 | FAIL |
| S09 | security/iframe-srcdoc | FAIL | SPD-PASS-002, SPD-SEC-002 | FAIL |
| S10 | security/object-embed | FAIL | SPD-PASS-002, SPD-SEC-002 | FAIL |
| S11 | security/active-form | FAIL | SPD-PASS-002 | PASS |
| S12 | security/meta-refresh | FAIL | SPD-PASS-002, SPD-SEC-003 | PASS |
| S13 | security/base-overrides | FAIL | SPD-PASS-002 | PASS |
| S14 | security/network-hints | FAIL | SPD-SEC-003, SPD-SEC-008 | PASS |
| S15 | security/local-css-font-image | PASS | no native failure | PASS |
| S16 | security/local-import-cycle | FAIL | SPD-SEC-008 | PASS |
| S17 | security/static-svg-local | PASS | no native failure | PASS |
| S18 | security/inert-controls | PASS | no native failure | PASS |
| S19 | security/local-media | PASS | no native failure | PASS |
| S20 | security/media-autoplay | FAIL | SPD-PASS-003 | PASS |
| S21 | security/static-animation-declaration | PASS | no native failure | PASS |
| S22 | security/mathml-local-glyph | PASS | no native failure | PASS |
| S23 | security/mathml-remote-glyph | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-008 | PASS |
| S24 | security/inert-hostile-metadata | PASS | no native failure | PASS |
| S25 | security/zip-special-modes | FAIL | SPD-BASE-002 | PASS |
| S26 | security/decoded-path-collision | FAIL | SPD-BASE-002, SPD-RES-002 | PASS |
| S27 | security/zip-header-mismatch | FAIL | no native failure | FAIL |
| S28 | security/bounded-expansion | NOT_TESTED | no native failure | PASS |
| S29 | security/unmapped-epub-title | FAIL | no native failure | FAIL |
| S30 | security/script-data-block | FAIL | SPD-SEC-001 | PASS |
| S31 | security/standalone-svg-script | FAIL | SPD-SEC-001, SPD-SEC-007 | FAIL |
| S32 | security/svg-event-handler | FAIL | SPD-SEC-001, SPD-SEC-007 | FAIL |
| S33 | security/plain-iframe | FAIL | SPD-PASS-002, SPD-SEC-002 | FAIL |
| S34 | security/authoritative-canvas | FAIL | SPD-PASS-002 | PASS |
| S35 | security/ordinary-hyperlink | PASS | no native failure | PASS |
| S36 | security/nested-rule-remote | FAIL | SPD-SEC-003, SPD-SEC-006, SPD-SEC-008 | FAIL |
| S37 | security/annotation-xml-active | FAIL | SPD-SEC-001 | PASS |
