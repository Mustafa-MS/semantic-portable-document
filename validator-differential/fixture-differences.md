# Fixture differences

All 25 differing fixtures; A_ONLY is empty in every row. A = COMMON; B = COMMON plus B_ONLY. Capability and NOT_TESTED fields remain equal; full values are in raw-diff.json. “ESTABLISHED” means a testable failed predicate, not proof that every frozen ID is the best attribution. Secondary classifications do not inflate counts.

| Fixture | A | B | Difference | Classification | RC Severity | Correct Interpretation | Recommended Target |
|---|---|---|---|---|---|---|---|
| invalid/bad-resource-hash | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-INT-004, SPD-INT-005, SPD-RES-004, SPD-STATE-002 | B_ONLY: SPD-INT-004, SPD-INT-005, SPD-RES-004, SPD-STATE-002 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | Byte/hash and both declared-inventory projection mismatches are directly measurable. STATE-002 is a sealed-state rule but lifecycle is EDITABLE (Draft §§27–29,70,72). | Validator B; Differential contract |
| invalid/descriptor-discovery-conflict | FAIL; SPD-DISC-002 | FAIL; SPD-ARCH-001, SPD-BASE-005, SPD-CAP-002, SPD-CAP-003, SPD-DISC-002, SPD-ID-002 | B_ONLY: SPD-ARCH-001, SPD-BASE-005, SPD-CAP-002, SPD-CAP-003, SPD-ID-002 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | Document-state and lifecycle links both target state.json. That candidate fails document-state schema, but its fields cannot establish authoritative capability equality or architecture (§69). | Validator B; Differential contract |
| invalid/descriptor-discovery-missing | FAIL; SPD-DISC-001 | FAIL; SPD-ARCH-001, SPD-CAP-002, SPD-CAP-003, SPD-DISC-001 | B_ONLY: SPD-ARCH-001, SPD-CAP-002, SPD-CAP-003 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | No descriptor links exist. OPF and spine are independently discoverable; descriptor claims are unknown, not an empty set. No filename fallback is permitted (§69). | Validator B; Differential contract |
| invalid/duplicate-node-id | FAIL; SPD-ID-006 | FAIL; SPD-BASE-002, SPD-ID-006 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:6,7 repeats n_paragraph01; EPUBCheck RSC-005. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/duplicate-normalized-path | FAIL; SPD-BASE-002 | FAIL; SPD-BASE-002, SPD-RES-002 | B_ONLY: SPD-RES-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/cafe\u0301.txt and EPUB/caf\u00e9.txt: One inventory path is decomposed, not NFC, and the ZIP has a normalized collision. Package rejection does not prevent inspecting the inventory string (§§5,28,70). | Differential contract; Validator A reporting |
| invalid/event-handler | FAIL; SPD-SEC-001 | FAIL; SPD-BASE-002, SPD-ID-006, SPD-SEC-001 | B_ONLY: SPD-BASE-002, SPD-ID-006 | VALIDATOR_A_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:4 has two h1 elements with n_heading01, one with onclick; EPUBCheck OPF-014 and RSC-005. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Validator A; Differential contract |
| invalid/external-required-css | FAIL; SPD-SEC-005 | FAIL; SPD-BASE-002, SPD-SEC-005 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:3 links https://example.org/x.css; EPUBCheck RSC-006. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/external-required-font | FAIL; SPD-SEC-004 | FAIL; SPD-BASE-002, SPD-SEC-004 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | style.css:2 has remote x.woff2 without manifest declaration; EPUBCheck OPF-014 and RSC-008. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/external-required-image | FAIL; SPD-SEC-006 | FAIL; SPD-BASE-002, SPD-SEC-006 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:7 has remote x.png; OPF omits remote-resources; EPUBCheck OPF-014 and RSC-006. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/invalid-xhtml | FAIL; SPD-SEM-002 | FAIL; SPD-BASE-002, SPD-SEM-002 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:1 has an unclosed p and missing head; EPUBCheck RSC-005 and RSC-016. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/javascript | FAIL; SPD-SEC-001 | FAIL; SPD-BASE-002, SPD-SEC-001 | B_ONLY: SPD-BASE-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | content.xhtml:7 contains script; OPF c1 omits scripted; EPUBCheck OPF-014. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization. | Differential contract; A oracle-generation workflow |
| invalid/mapping-invalid-geometry | PASS; SPD-MAP-011 | PASS; SPD-MAP-011, SPD-MAP-012 | B_ONLY: SPD-MAP-012 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | Page p_1 is 816×1056; quad [-1,0,900,0,900,1200,-1,1200] is finite, structurally valid and TL-TR-BR-BL ordered, but out of bounds. §§36 and 56 both prohibit it. | Differential contract; Validator A reporting |
| invalid/mapping-with-stale-fixed | PASS; SPD-STATE-007 | PASS; SPD-STATE-001, SPD-STATE-007 | B_ONLY: SPD-STATE-001 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | EDITABLE explicitly says stale and fixed input digest differs from current. Mapping must fail STATE-007; a Mapping claim alone does not establish reader mispresentation under STATE-001 (§§26,56,71). | Validator B |
| invalid/mutation-asset | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-003 | B_ONLY: SPD-RES-004, SPD-STATE-003 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/figure.svg: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71). | Differential contract; Validator A reporting |
| invalid/mutation-css | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-003 | B_ONLY: SPD-RES-004, SPD-STATE-003 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/style.css: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71). | Validator B; Differential contract |
| invalid/mutation-fixed | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-001, SPD-STATE-003, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007 | B_ONLY: SPD-RES-004, SPD-STATE-001, SPD-STATE-003, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/fixed.pdf: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71). | Validator B; Differential contract |
| invalid/mutation-mapping | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-002, SPD-STATE-003 | B_ONLY: SPD-RES-004, SPD-STATE-002, SPD-STATE-003 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | META-INF/spd/mapping.json: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71). | Validator B; Differential contract |
| invalid/mutation-semantic | FAIL; SPD-INT-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-003 | B_ONLY: SPD-RES-004, SPD-STATE-003 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/content.xhtml: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71). | Differential contract; Validator A reporting |
| invalid/path-traversal | FAIL; SPD-BASE-002 | FAIL; SPD-BASE-002, SPD-RES-002 | B_ONLY: SPD-RES-002 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | ../escape.txt: The inventory explicitly contains a prohibited parent component; the path schema independently rejects it. Package rejection does not prevent inspecting the inventory string (§§5,28,70). | Differential contract; Validator A reporting |
| invalid/sealed-after-annotation-modification | FAIL; SPD-ANN-004 | FAIL; SPD-ANN-004, SPD-INT-003, SPD-RES-004, SPD-STATE-003 | B_ONLY: SPD-INT-003, SPD-RES-004, SPD-STATE-003 | VALIDATOR_B_BUG | RC_DIAGNOSTIC_CONVERGENCE | annotations.json changed from 465 to 466 bytes in SEALED. Seal invalidity and ANN-004 are clear, but annotation bytes have affects=[] and are not semantic content (§§27,73). | Validator B; Differential contract |
| invalid/sealed-after-semantic-modification | FAIL; SPD-STATE-003 | FAIL; SPD-INT-003, SPD-RES-004, SPD-STATE-003 | B_ONLY: SPD-INT-003, SPD-RES-004 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | SEALED authoritative content.xhtml differs in exact bytes; resource hash and seal invalidity are separately established (§§27–29). | Differential contract; Validator A reporting |
| invalid/stale-fixed-rendition | PASS; SPD-STATE-001 | PASS; SPD-STATE-001, SPD-STATE-007 | B_ONLY: SPD-STATE-007 | VALIDATOR_A_BUG | RC_DIAGNOSTIC_CONVERGENCE | EDITABLE explicitly says stale although its numerical bindings match. Mapping requires current, not merely equal hashes. B adds the correct STATE-007; both sides share unsupported processor-level STATE-001 attribution (§§26,56). | Validator A; Validator B; Corpus |
| invalid/unlisted-non-normative-resource | FAIL; SPD-RES-006 | FAIL; SPD-RES-003, SPD-RES-006 | B_ONLY: SPD-RES-003 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/cache.bin exists outside inventory and is neither self-reference exception. Both RES-003 and RES-006 apply; the former explicitly includes caches (§28). | Differential contract; Validator A reporting |
| invalid/unlisted-normative-resource | FAIL; SPD-RES-003 | FAIL; SPD-RES-003, SPD-RES-006 | B_ONLY: SPD-RES-006 | NORMALIZATION_CONTRACT_BUG | RC_DIAGNOSTIC_CONVERGENCE | EPUB/extra.css exists outside inventory and is neither self-reference exception. Both RES-003 and RES-006 apply; the former explicitly includes caches (§28). | Differential contract; Validator A reporting |
| valid/multi-spine | PASS; no violations | FAIL; SPD-ID-006 | B_ONLY: SPD-ID-006 | CORPUS_ORACLE_BUG | RC_BLOCKER | Invalid: n_article01 is repeated across two authoritative spine resources in one revision (Draft §§8,14; SPD-ID-006). | Corpus; Validator A |

## invalid/bad-resource-hash

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:19b4199d7708e10074cb2fa51059340eef257a41ecc82be4f3c8377693162d70`. Evidence paths are ZIP-entry paths inside `tests/invalid/bad-resource-hash/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-INT-004, SPD-INT-005, SPD-RES-004, SPD-STATE-002.

Byte/hash and both declared-inventory projection mismatches are directly measurable. STATE-002 is a sealed-state rule but lifecycle is EDITABLE (Draft §§27–29,70,72).

- `SPD-RES-004`: ESTABLISHED: content.xhtml is 516 bytes; declared hash is all zero, actual is 51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935.
- `SPD-INT-004`: ESTABLISHED: declared-inventory projection d774ef728e31b285e4f10985af261ed70550723d3401f6ad65f722587dd13aa3 differs from descriptor 36f4e697ebaa31e51e1b1789afe3b611aa5ee284785c4117c9929bdcef5ba0d6.
- `SPD-INT-005`: ESTABLISHED: declared-inventory projection f2d76f12b5ef7cda3db25403375d4a7419dedcf1b176e7d41968b2b5940594ec differs from descriptor 6c4b44d7572730c76f1ca20a7b0b079df75beed8a4e9f7875040d779cb72f5d7.
- `SPD-STATE-002`: WRONG REQUIREMENT/APPLICABILITY: exact inventory binding does mismatch, but this is EDITABLE, not SEALED. General integrity failure is established; a sealed-state failure is not.

Measured resource mismatches:

- `EPUB/content.xhtml`: 516 → 516 bytes; affects=['semantic', 'rendering']; `sha256:0000000000000000000000000000000000000000000000000000000000000000` → `sha256:51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935`.

## invalid/descriptor-discovery-conflict

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:964fabfad3c5db0fa9a7a79692493fd0b25d124c0f2cc82376c1225ad54fd438`. Evidence paths are ZIP-entry paths inside `tests/invalid/descriptor-discovery-conflict/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-DISC-002. B_ONLY: SPD-ARCH-001, SPD-BASE-005, SPD-CAP-002, SPD-CAP-003, SPD-ID-002.

Document-state and lifecycle links both target state.json. That candidate fails document-state schema, but its fields cannot establish authoritative capability equality or architecture (§69).

- `SPD-ARCH-001`: NOT ESTABLISHED: no Base claim in the wrong-type candidate does not establish absence of the authoritative semantic rendition.
- `SPD-BASE-005`: ESTABLISHED AT CANDIDATE/STRUCTURAL LEVEL: the explicitly linked document-state candidate fails required descriptor shape. It does not show a missing OPF spine.
- `SPD-CAP-002`: CANDIDATE FAILURE ONLY: state.json lacks required capabilities. Reporting a candidate-schema failure is defensible; authoritative claims remain unavailable.
- `SPD-CAP-003`: BLOCKED: invalid/conflicting descriptor authority does not supply a valid known-empty capability set to compare with OPF.
- `SPD-ID-002`: CANDIDATE FAILURE ONLY: state.json has flat revisionId, not required document-state /revision/revisionId. This is not proof the semantic state has no Revision ID.

## invalid/descriptor-discovery-missing

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:5302054ce8cee31ffa2d4af7a523182580d7d464753eceb8499b5d2dc7da859b`. Evidence paths are ZIP-entry paths inside `tests/invalid/descriptor-discovery-missing/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-DISC-001. B_ONLY: SPD-ARCH-001, SPD-CAP-002, SPD-CAP-003.

No descriptor links exist. OPF and spine are independently discoverable; descriptor claims are unknown, not an empty set. No filename fallback is permitted (§69).

- `SPD-ARCH-001`: NOT ESTABLISHED: missing Base declaration is not evidence of zero/multiple authoritative semantic representations; OPF has one spine.
- `SPD-CAP-002`: BLOCKED: authoritative capability array unavailable; do not treat unavailable as known empty.
- `SPD-CAP-003`: BLOCKED: OPF claim Base is known, authoritative descriptor claim set is not. Equality cannot be tested.

## invalid/duplicate-node-id

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:83d7242dc155c8915b50e54a4d85a0bbe662d51ae96dded6047c5df92a4fdb0d`. Evidence paths are ZIP-entry paths inside `tests/invalid/duplicate-node-id/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-ID-006. B_ONLY: SPD-BASE-002.

content.xhtml:6,7 repeats n_paragraph01; EPUBCheck RSC-005. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:6,7 repeats n_paragraph01; EPUBCheck RSC-005. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/duplicate-normalized-path

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:3a32c886b7920e089a8c1624d0df95c03307a842a5cdd4b8c70bf0abd4996d89`. Evidence paths are ZIP-entry paths inside `tests/invalid/duplicate-normalized-path/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-BASE-002. B_ONLY: SPD-RES-002.

EPUB/cafe\u0301.txt and EPUB/caf\u00e9.txt: One inventory path is decomposed, not NFC, and the ZIP has a normalized collision. Package rejection does not prevent inspecting the inventory string (§§5,28,70).

- `SPD-RES-002`: ESTABLISHED: One inventory path is decomposed, not NFC, and the ZIP has a normalized collision.

## invalid/event-handler

Primary: VALIDATOR_A_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:93d1fe2dbf19a687df1441c8e5be5e1fd26b7d1bcffbe8a94c90b958148f4c68`. Evidence paths are ZIP-entry paths inside `tests/invalid/event-handler/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEC-001. B_ONLY: SPD-BASE-002, SPD-ID-006.

content.xhtml:4 has two h1 elements with n_heading01, one with onclick; EPUBCheck OPF-014 and RSC-005. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:4 has two h1 elements with n_heading01, one with onclick; EPUBCheck OPF-014 and RSC-005. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- `SPD-ID-006`: ESTABLISHED: duplicate n_heading01 occurs twice in a well-formed authoritative XHTML DOM at line 4. The onclick attribute does not exempt either ID.

## invalid/external-required-css

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:736becb1a57b763114188c5d5f92f54d7efab7502da4057c660d0e1fe16bb21a`. Evidence paths are ZIP-entry paths inside `tests/invalid/external-required-css/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEC-005. B_ONLY: SPD-BASE-002.

content.xhtml:3 links https://example.org/x.css; EPUBCheck RSC-006. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:3 links https://example.org/x.css; EPUBCheck RSC-006. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/external-required-font

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:35b7f76b10f6059f001492b44b1016725e0c694ba7727d4047642b8e03acfa2a`. Evidence paths are ZIP-entry paths inside `tests/invalid/external-required-font/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEC-004. B_ONLY: SPD-BASE-002.

style.css:2 has remote x.woff2 without manifest declaration; EPUBCheck OPF-014 and RSC-008. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: style.css:2 has remote x.woff2 without manifest declaration; EPUBCheck OPF-014 and RSC-008. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/external-required-image

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:f66558fb085027113665e5962af229555b53372b676cd49a61c93b73e4df53fb`. Evidence paths are ZIP-entry paths inside `tests/invalid/external-required-image/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEC-006. B_ONLY: SPD-BASE-002.

content.xhtml:7 has remote x.png; OPF omits remote-resources; EPUBCheck OPF-014 and RSC-006. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:7 has remote x.png; OPF omits remote-resources; EPUBCheck OPF-014 and RSC-006. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/invalid-xhtml

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:6019a48c745987fef21b8e8895b7f340750cd6c8edb71b9337238b6543f321dc`. Evidence paths are ZIP-entry paths inside `tests/invalid/invalid-xhtml/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEM-002. B_ONLY: SPD-BASE-002.

content.xhtml:1 has an unclosed p and missing head; EPUBCheck RSC-005 and RSC-016. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:1 has an unclosed p and missing head; EPUBCheck RSC-005 and RSC-016. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/javascript

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:eea5d55ec2e73d2372fdf6ce2489ac4cad0270866e9d84c5b518fea6c0beb597`. Evidence paths are ZIP-entry paths inside `tests/invalid/javascript/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-SEC-001. B_ONLY: SPD-BASE-002.

content.xhtml:7 contains script; OPF c1 omits scripted; EPUBCheck OPF-014. Native invalidity is clear (Draft §§5,7,14). External failure is measurable independently; ID multiplicity and external scope need normalization.

- `SPD-BASE-002`: INDEPENDENT EXTERNAL FAILURE: content.xhtml:7 contains script; OPF c1 omits scripted; EPUBCheck OPF-014. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## invalid/mapping-invalid-geometry

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:1918ea0ece62c0726514453fb7dee19d8d49b9571f1d3f62e45304f953ee09f3`. Evidence paths are ZIP-entry paths inside `tests/invalid/mapping-invalid-geometry/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-MAP-011. B_ONLY: SPD-MAP-012.

Page p_1 is 816×1056; quad [-1,0,900,0,900,1200,-1,1200] is finite, structurally valid and TL-TR-BR-BL ordered, but out of bounds. §§36 and 56 both prohibit it.

- `SPD-MAP-012`: ESTABLISHED under its linked §36 geometry rule, which explicitly requires visible bounds. Registry shorthand emphasizes coordinates/dimensions; MAP-011 explicitly names page bounds. This is overlapping rule attribution, not a parser cascade or undefined geometry.

## invalid/mapping-with-stale-fixed

Primary: VALIDATOR_B_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:f0eb7197d18cba56d24d17b63c912aa7c34d9772c244a536aacf04e05fbf1b21`. Evidence paths are ZIP-entry paths inside `tests/invalid/mapping-with-stale-fixed/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-STATE-007. B_ONLY: SPD-STATE-001.

EDITABLE explicitly says stale and fixed input digest differs from current. Mapping must fail STATE-007; a Mapping claim alone does not establish reader mispresentation under STATE-001 (§§26,56,71).

- `SPD-STATE-001`: NOT ESTABLISHED: declared stale is not declared current, and this fixture supplies no reader behavior evidence.

## invalid/mutation-asset

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:0f4383f670617e41ec93ce214b7282ef6a541c58de79b1aa94b019b47daa8955`. Evidence paths are ZIP-entry paths inside `tests/invalid/mutation-asset/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-RES-004, SPD-STATE-003.

EPUB/figure.svg: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).

- `SPD-RES-004`: ESTABLISHED: exact bytes and length for EPUB/figure.svg disagree with its inventory entry.
- `SPD-STATE-003`: ESTABLISHED as integrity coverage of a semantic-affecting resource: SEALED and affects includes semantic; the committed exact bytes changed. This does not prove visible text changed.

Measured resource mismatches:

- `EPUB/figure.svg`: 41 → 55 bytes; affects=['semantic', 'rendering']; `sha256:900fbe934249ad120004bd24adf66aad8817d89586273c0cc50e187bddebb601` → `sha256:57b5c8eee4abd1da0516049e648646d8623501366a45d0d01a78c6d5cb3e8b28`.

## invalid/mutation-css

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:fbe020b4ea4eba00842cf899bb1469787b7a78c374f796567889377959470c90`. Evidence paths are ZIP-entry paths inside `tests/invalid/mutation-css/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-RES-004, SPD-STATE-003.

EPUB/style.css: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).

- `SPD-RES-004`: ESTABLISHED: exact bytes and length for EPUB/style.css disagree with its inventory entry.
- `SPD-STATE-003`: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.

Measured resource mismatches:

- `EPUB/style.css`: 95 → 107 bytes; affects=['rendering']; `sha256:b68ee1ec263cff1ff6d3768be4598dfab0946fa8a44fd1f055614e30632552e2` → `sha256:08ab11eb73557b588cc2dd00a46ff5f12e90f9c8fd04560602155062ce02c239`.

## invalid/mutation-fixed

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:c263a520a223bd2bdc8bf40ad93367a267d5747b72e311cb92dd5b1f4a29af1d`. Evidence paths are ZIP-entry paths inside `tests/invalid/mutation-fixed/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-RES-004, SPD-STATE-001, SPD-STATE-003, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007.

EPUB/fixed.pdf: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).

- `SPD-RES-004`: ESTABLISHED: exact bytes and length for EPUB/fixed.pdf disagree with its inventory entry.
- `SPD-STATE-003`: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.
- `SPD-STATE-001`: PROCESSOR CLAIM NOT ESTABLISHED: false current token is established and covered by STATE-005, but no reader execution proves the processor exposed it as current.
- `SPD-STATE-005`: ESTABLISHED: status=current but fixed resource hash c9bd22e9… differs from actual df6cb8ce…; currentness is disproved directly.
- `SPD-STATE-006`: ESTABLISHED: SEALED has fixed output whose exact digest does not verify, so it cannot be current.
- `SPD-STATE-007`: ESTABLISHED: Mapping is explicitly claimed and required current fixed output is disproved by its own hash mismatch.

Measured resource mismatches:

- `EPUB/fixed.pdf`: 434 → 442 bytes; affects=[]; `sha256:c9bd22e957e95665fc31183ed692bbbd3b06b40d6fdb4a64ae3c0a80ff8f6419` → `sha256:df6cb8ce89dd17bff5cc3ec48fc595ddea600c1ff6f6c7c782cacb58cdc11185`.

## invalid/mutation-mapping

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:615d3ac2c3531f65047456367877f28e5bacfd2b1ee65e667ec3c702d5dd7000`. Evidence paths are ZIP-entry paths inside `tests/invalid/mutation-mapping/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-RES-004, SPD-STATE-002, SPD-STATE-003.

META-INF/spd/mapping.json: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).

- `SPD-RES-004`: ESTABLISHED: exact bytes and length for META-INF/spd/mapping.json disagree with its inventory entry.
- `SPD-STATE-003`: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.
- `SPD-STATE-002`: ESTABLISHED: SEALED mapping binding hash 54a9175f… differs from exact mapping hash 3104fb6a…; a trailing byte still matters under exact-byte hashing.

Measured resource mismatches:

- `META-INF/spd/mapping.json`: 1424 → 1425 bytes; affects=[]; `sha256:54a9175fe9082bb90b14e335329cf3876aa2fedff1d25ae0f8a2689c78872de6` → `sha256:3104fb6ac4be7854fe24f7dc44ee92761aef8b9664eb0c39fbf087e534f05e80`.

## invalid/mutation-semantic

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:a77e1f70411328b50932144eb770e8d962979c2d451ade02c8bccf9e58453147`. Evidence paths are ZIP-entry paths inside `tests/invalid/mutation-semantic/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-INT-003. B_ONLY: SPD-RES-004, SPD-STATE-003.

EPUB/content.xhtml: exact-byte failure invalidates SEALED; distinguish actual resource effects from generic seal invalidity (§§27–29,71).

- `SPD-RES-004`: ESTABLISHED: exact bytes and length for EPUB/content.xhtml disagree with its inventory entry.
- `SPD-STATE-003`: ESTABLISHED as integrity coverage of a semantic-affecting resource: SEALED and affects includes semantic; the committed exact bytes changed. This does not prove visible text changed.

Measured resource mismatches:

- `EPUB/content.xhtml`: 516 → 530 bytes; affects=['semantic', 'rendering']; `sha256:51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935` → `sha256:da05ce846c0732d29beb24aed77a5c5a5b1ddd5a1e896a26ad7db79d0107dd5b`.

## invalid/path-traversal

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:81cb41c70df476f6094c4a789e69784e790163c6afc02e5dbff0630f03ce9750`. Evidence paths are ZIP-entry paths inside `tests/invalid/path-traversal/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-BASE-002. B_ONLY: SPD-RES-002.

../escape.txt: The inventory explicitly contains a prohibited parent component; the path schema independently rejects it. Package rejection does not prevent inspecting the inventory string (§§5,28,70).

- `SPD-RES-002`: ESTABLISHED: The inventory explicitly contains a prohibited parent component; the path schema independently rejects it.

## invalid/sealed-after-annotation-modification

Primary: VALIDATOR_B_BUG. Secondary: NORMALIZATION_CONTRACT_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:49c5b2bee4a49a15544c6d7a077bee420fad709e06ab7e22921977e7c9d0b66e`. Evidence paths are ZIP-entry paths inside `tests/invalid/sealed-after-annotation-modification/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-ANN-004. B_ONLY: SPD-INT-003, SPD-RES-004, SPD-STATE-003.

annotations.json changed from 465 to 466 bytes in SEALED. Seal invalidity and ANN-004 are clear, but annotation bytes have affects=[] and are not semantic content (§§27,73).

- `SPD-INT-003`: ESTABLISHED: packaged annotation modification breaks covered integrity.
- `SPD-RES-004`: ESTABLISHED: exact annotation bytes/hash differ, even if the extra byte is whitespace.
- `SPD-STATE-003`: WRONG REQUIREMENT ATTRIBUTION: non-semantic annotation mutation invalidates the seal, not the semantic-content-specific predicate.

Measured resource mismatches:

- `EPUB/annotations.json`: 465 → 466 bytes; affects=[]; `sha256:9f9dc38dcb45a50f1ef7f926eacd7e2bbb286a44bdeeaac77569346e6c3c0adc` → `sha256:584850018abcfc8e59400ef1146d4ecb0b39c0fe8ae3310e347d4a8477e27715`.

## invalid/sealed-after-semantic-modification

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:ceaef7fe4a81eb72012b347583c6b774850c59e54af2b021cc9a265f4197c81a`. Evidence paths are ZIP-entry paths inside `tests/invalid/sealed-after-semantic-modification/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-STATE-003. B_ONLY: SPD-INT-003, SPD-RES-004.

SEALED authoritative content.xhtml differs in exact bytes; resource hash and seal invalidity are separately established (§§27–29).

- `SPD-INT-003`: ESTABLISHED: covered authoritative bytes changed without rebinding.
- `SPD-RES-004`: ESTABLISHED: content.xhtml declared 516 bytes, actual 525, and SHA-256 differs.

Measured resource mismatches:

- `EPUB/content.xhtml`: 516 → 525 bytes; affects=['semantic', 'rendering']; `sha256:51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935` → `sha256:8ca1c25ccf2e8b81fbded88233caadc527f9ef705f9596389fdff4a3597533f7`.

## invalid/stale-fixed-rendition

Primary: VALIDATOR_A_BUG. Secondary: VALIDATOR_B_BUG, CORPUS_ORACLE_BUG. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:f4f78e5c3bd011051884dbffb4dd637cbfa2dc0ae880c567e99ebfbcad36e422`. Evidence paths are ZIP-entry paths inside `tests/invalid/stale-fixed-rendition/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-STATE-001. B_ONLY: SPD-STATE-007.

EDITABLE explicitly says stale although its numerical bindings match. Mapping requires current, not merely equal hashes. B adds the correct STATE-007; both sides share unsupported processor-level STATE-001 attribution (§§26,56).

- `SPD-STATE-007`: ESTABLISHED: Mapping is claimed but fixed is explicitly stale. A incorrectly routes this Mapping failure to the processor rule STATE-001.

## invalid/unlisted-non-normative-resource

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:ae6b28b7cf9f783b9425290cdbb3207edc2da81844252cede8f5509a7d542f78`. Evidence paths are ZIP-entry paths inside `tests/invalid/unlisted-non-normative-resource/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-RES-006. B_ONLY: SPD-RES-003.

EPUB/cache.bin exists outside inventory and is neither self-reference exception. Both RES-003 and RES-006 apply; the former explicitly includes caches (§28).

- `SPD-RES-003`: ESTABLISHED: all package entries, including non-normative caches, must be inventoried; role/manifest membership does not partition these two requirements.

## invalid/unlisted-normative-resource

Primary: NORMALIZATION_CONTRACT_BUG. Secondary: none. Severity: RC_DIAGNOSTIC_CONVERGENCE.

Package SHA-256: `sha256:d94313f1ea3c8b1dee3f16138c1e2445c5071dd4be9d2f6a07ccd4c9f922d3de`. Evidence paths are ZIP-entry paths inside `tests/invalid/unlisted-normative-resource/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: SPD-RES-003. B_ONLY: SPD-RES-006.

EPUB/extra.css exists outside inventory and is neither self-reference exception. Both RES-003 and RES-006 apply; the former explicitly includes caches (§28).

- `SPD-RES-006`: ESTABLISHED: all package entries, including non-normative caches, must be inventoried; role/manifest membership does not partition these two requirements.

## valid/multi-spine

Primary: CORPUS_ORACLE_BUG. Secondary: VALIDATOR_A_BUG. Severity: RC_BLOCKER.

Package SHA-256: `sha256:7e38a98b2c52e2552613cd5ef22046f1ee39c9ffc273a06470b1b0d712e0a5d3`. Evidence paths are ZIP-entry paths inside `tests/valid/multi-spine/document.epub`; machine-readable measurements are in fixture-byte-evidence.json.

A_ONLY: none. COMMON: none. B_ONLY: SPD-ID-006.

Invalid: n_article01 is repeated across two authoritative spine resources in one revision (Draft §§8,14; SPD-ID-006).

- `SPD-ID-006`: ESTABLISHED: chapter1.xhtml:4 and chapter2.xhtml:4 both identify html/body/article as n_article01; unrelated non-spine IDs are excluded.
