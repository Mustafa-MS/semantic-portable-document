# Requirement differences

Only B_ONLY occurrences count below; no A_ONLY occurrences exist. COMMON findings are not automatically correct: STATE-001 in stale-fixed-rendition is an identified shared misattribution. See fixture details for every per-ID assessment.

## SPD-ARCH-001 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-ARCH-001, section: 3, level: SHALL, capability: [Base], subject: document, requirement: "A conforming document has exactly one authoritative semantic representation.", testability: AUTOMATED, testType: SEMANTIC}
```

- invalid/descriptor-discovery-conflict: NOT ESTABLISHED: no Base claim in the wrong-type candidate does not establish absence of the authoritative semantic rendition.
- invalid/descriptor-discovery-missing: NOT ESTABLISHED: missing Base declaration is not evidence of zero/multiple authoritative semantic representations; OPF has one spine.

## SPD-BASE-002 — 7 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-BASE-002, section: 5, level: SHALL, capability: [Base], subject: package, requirement: "Applicable EPUB 3.3 OCF requirements apply unless this profile further restricts them.", testability: AUTOMATED, testType: PACKAGE}
```

- invalid/duplicate-node-id: INDEPENDENT EXTERNAL FAILURE: content.xhtml:6,7 repeats n_paragraph01; EPUBCheck RSC-005. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/event-handler: INDEPENDENT EXTERNAL FAILURE: content.xhtml:4 has two h1 elements with n_heading01, one with onclick; EPUBCheck OPF-014 and RSC-005. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/external-required-css: INDEPENDENT EXTERNAL FAILURE: content.xhtml:3 links https://example.org/x.css; EPUBCheck RSC-006. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/external-required-font: INDEPENDENT EXTERNAL FAILURE: style.css:2 has remote x.woff2 without manifest declaration; EPUBCheck OPF-014 and RSC-008. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/external-required-image: INDEPENDENT EXTERNAL FAILURE: content.xhtml:7 has remote x.png; OPF omits remote-resources; EPUBCheck OPF-014 and RSC-006. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/invalid-xhtml: INDEPENDENT EXTERNAL FAILURE: content.xhtml:1 has an unclosed p and missing head; EPUBCheck RSC-005 and RSC-016. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.
- invalid/javascript: INDEPENDENT EXTERNAL FAILURE: content.xhtml:7 contains script; OPF c1 omits scripted; EPUBCheck OPF-014. Not a fabricated DOM cascade. Both adapters use this aggregate ID, but A frozen external evaluation scope omits this invalid fixture. The contract must specify scope and inherited-rule attribution.

## SPD-BASE-005 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-BASE-005, section: 55, level: SHALL, capability: [Base], subject: package, requirement: "A Base package includes navigation, an authoritative XHTML spine, identity metadata, inventory, offline required resources, semantic structure, logical text, and integrity digests.", testability: AUTOMATED, testType: PACKAGE}
```

- invalid/descriptor-discovery-conflict: ESTABLISHED AT CANDIDATE/STRUCTURAL LEVEL: the explicitly linked document-state candidate fails required descriptor shape. It does not show a missing OPF spine.

## SPD-CAP-002 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-CAP-002, section: 54, level: MUST, capability: [Base], subject: capability, requirement: "Documents declare only capability ID and version; normative or experimental status is specification-controlled.", testability: AUTOMATED, testType: SCHEMA, derivedFrom: A-020}
```

- invalid/descriptor-discovery-conflict: CANDIDATE FAILURE ONLY: state.json lacks required capabilities. Reporting a candidate-schema failure is defensible; authoritative claims remain unavailable.
- invalid/descriptor-discovery-missing: BLOCKED: authoritative capability array unavailable; do not treat unavailable as known empty.

## SPD-CAP-003 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-CAP-003, section: 54, level: MUST, capability: [Base], subject: discovery, requirement: "EPUB discovery metadata and the authoritative document-state capability declaration agree exactly.", testability: AUTOMATED, testType: PACKAGE, derivedFrom: A-013}
```

- invalid/descriptor-discovery-conflict: BLOCKED: invalid/conflicting descriptor authority does not supply a valid known-empty capability set to compare with OPF.
- invalid/descriptor-discovery-missing: BLOCKED: OPF claim Base is known, authoritative descriptor claim set is not. Equality cannot be tested.

## SPD-ID-002 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-ID-002, section: 12, level: MUST, capability: [Base], subject: revision, requirement: "Every committed semantic state has an opaque canonical lowercase RFC 9562 UUID URN Revision ID.", testability: AUTOMATED, testType: SCHEMA}
```

- invalid/descriptor-discovery-conflict: CANDIDATE FAILURE ONLY: state.json has flat revisionId, not required document-state /revision/revisionId. This is not proof the semantic state has no Revision ID.

## SPD-ID-006 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-ID-006, section: 14, level: MUST, capability: [Base], subject: node, requirement: "Node IDs are unique in the current authoritative semantic revision.", testability: AUTOMATED, testType: SEMANTIC}
```

- invalid/event-handler: ESTABLISHED: duplicate n_heading01 occurs twice in a well-formed authoritative XHTML DOM at line 4. The onclick attribute does not exempt either ID.
- valid/multi-spine: ESTABLISHED: chapter1.xhtml:4 and chapter2.xhtml:4 both identify html/body/article as n_article01; unrelated non-spine IDs are excluded.

## SPD-INT-003 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-INT-003, section: 29, level: SHALL, capability: [Base], subject: integrity, requirement: "Integrity detects modification of semantic content, normative styles/assets, mapping, fixed rendition, and state metadata when applicable.", testability: AUTOMATED, testType: INTEGRITY}
```

- invalid/sealed-after-annotation-modification: ESTABLISHED: packaged annotation modification breaks covered integrity.
- invalid/sealed-after-semantic-modification: ESTABLISHED: covered authoritative bytes changed without rebinding.

## SPD-INT-004 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-INT-004, section: 29, level: MUST, capability: [Base], subject: digest, requirement: "semanticStateDigest is computed by the normative UTF-8 inventory projection over resources whose affects contains semantic.", testability: AUTOMATED, testType: INTEGRITY, derivedFrom: A-007}
```

- invalid/bad-resource-hash: ESTABLISHED: declared-inventory projection d774ef728e31b285e4f10985af261ed70550723d3401f6ad65f722587dd13aa3 differs from descriptor 36f4e697ebaa31e51e1b1789afe3b611aa5ee284785c4117c9929bdcef5ba0d6.

## SPD-INT-005 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-INT-005, section: 29, level: MUST, capability: [Base], subject: digest, requirement: "renditionInputDigest is computed by the normative projection over resources affecting semantic or rendering; presentation-only change stales fixed without changing Revision ID.", testability: AUTOMATED, testType: INTEGRITY, derivedFrom: A-007}
```

- invalid/bad-resource-hash: ESTABLISHED: declared-inventory projection f2d76f12b5ef7cda3db25403375d4a7419dedcf1b176e7d41968b2b5940594ec differs from descriptor 6c4b44d7572730c76f1ca20a7b0b079df75beed8a4e9f7875040d779cb72f5d7.

## SPD-MAP-012 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-MAP-012, section: 36, level: MUST, capability: [Mapping], subject: geometry, requirement: "Mapping geometry uses finite page-local CSS reference pixels with top-left origin, x right, y down, TL-TR-BR-BL quads, and declared rendition-local page dimensions.", testability: AUTOMATED, testType: MAPPING, derivedFrom: A-011}
```

- invalid/mapping-invalid-geometry: ESTABLISHED under its linked §36 geometry rule, which explicitly requires visible bounds. Registry shorthand emphasizes coordinates/dimensions; MAP-011 explicitly names page bounds. This is overlapping rule attribution, not a parser cascade or undefined geometry.

## SPD-RES-002 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-RES-002, section: 28, level: MUST, capability: [Base], subject: resource, requirement: "Each inventory entry has a normalized NFC path, media type, byte length, SHA-256 digest, role, and explicit affects array.", testability: AUTOMATED, testType: SCHEMA}
```

- invalid/duplicate-normalized-path: ESTABLISHED: One inventory path is decomposed, not NFC, and the ZIP has a normalized collision.
- invalid/path-traversal: ESTABLISHED: The inventory explicitly contains a prohibited parent component; the path schema independently rejects it.

## SPD-RES-003 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-RES-003, section: 28, level: MUST, capability: [Base], subject: inventory, requirement: "The inventory lists every ZIP entry including non-normative caches except the inventory itself and lifecycle state descriptor.", testability: AUTOMATED, testType: INTEGRITY, ambiguity: A-006}
```

- invalid/unlisted-non-normative-resource: ESTABLISHED: all package entries, including non-normative caches, must be inventoried; role/manifest membership does not partition these two requirements.

## SPD-RES-004 — 8 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-RES-004, section: 28, level: SHALL, capability: [Base], subject: resource, requirement: "Inventory digests cover the exact decompressed bytes returned for the named ZIP entry.", testability: AUTOMATED, testType: INTEGRITY, ambiguity: A-007}
```

- invalid/bad-resource-hash: ESTABLISHED: content.xhtml is 516 bytes; declared hash is all zero, actual is 51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935.
- invalid/mutation-asset: ESTABLISHED: exact bytes and length for EPUB/figure.svg disagree with its inventory entry.
- invalid/mutation-css: ESTABLISHED: exact bytes and length for EPUB/style.css disagree with its inventory entry.
- invalid/mutation-fixed: ESTABLISHED: exact bytes and length for EPUB/fixed.pdf disagree with its inventory entry.
- invalid/mutation-mapping: ESTABLISHED: exact bytes and length for META-INF/spd/mapping.json disagree with its inventory entry.
- invalid/mutation-semantic: ESTABLISHED: exact bytes and length for EPUB/content.xhtml disagree with its inventory entry.
- invalid/sealed-after-annotation-modification: ESTABLISHED: exact annotation bytes/hash differ, even if the extra byte is whitespace.
- invalid/sealed-after-semantic-modification: ESTABLISHED: content.xhtml declared 516 bytes, actual 525, and SHA-256 differs.

## SPD-RES-006 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-RES-006, section: 28, level: MUST, capability: [Base], subject: package, requirement: "Any unlisted ZIP entry other than the two self-referential exceptions fails conformance.", testability: AUTOMATED, testType: INTEGRITY, derivedFrom: A-006}
```

- invalid/unlisted-normative-resource: ESTABLISHED: all package entries, including non-normative caches, must be inventoried; role/manifest membership does not partition these two requirements.

## SPD-STATE-001 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-001, section: 26, level: MUST_NOT, capability: [Fixed-Experimental], subject: processor, requirement: "A stale fixed rendition is not presented as the current authoritative fixed representation.", testability: AUTOMATED, testType: INTEGRITY}
```

- invalid/mapping-with-stale-fixed: NOT ESTABLISHED: declared stale is not declared current, and this fixture supplies no reader behavior evidence.
- invalid/mutation-fixed: PROCESSOR CLAIM NOT ESTABLISHED: false current token is established and covered by STATE-005, but no reader execution proves the processor exposed it as current.

## SPD-STATE-002 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-002, section: 27, level: SHALL, capability: [Base], subject: sealed-state, requirement: "A sealed state binds the semantic Revision ID, normative inventory, any claimed fixed rendition, and any applicable mapping artifact.", testability: AUTOMATED, testType: INTEGRITY}
```

- invalid/bad-resource-hash: WRONG REQUIREMENT/APPLICABILITY: exact inventory binding does mismatch, but this is EDITABLE, not SEALED. General integrity failure is established; a sealed-state failure is not.
- invalid/mutation-mapping: ESTABLISHED: SEALED mapping binding hash 54a9175f… differs from exact mapping hash 3104fb6a…; a trailing byte still matters under exact-byte hashing.

## SPD-STATE-003 — 6 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-003, section: 27, level: SHALL, capability: [Base], subject: sealed-state, requirement: "Changing normative semantic content invalidates the sealed state.", testability: AUTOMATED, testType: INTEGRITY}
```

- invalid/mutation-asset: ESTABLISHED as integrity coverage of a semantic-affecting resource: SEALED and affects includes semantic; the committed exact bytes changed. This does not prove visible text changed.
- invalid/mutation-css: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.
- invalid/mutation-fixed: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.
- invalid/mutation-mapping: WRONG REQUIREMENT ATTRIBUTION: the seal is invalid under §27, but the changed resource has no semantic effect. STATE-003 specifically names normative semantic content; use the general integrity/binding requirement.
- invalid/mutation-semantic: ESTABLISHED as integrity coverage of a semantic-affecting resource: SEALED and affects includes semantic; the committed exact bytes changed. This does not prove visible text changed.
- invalid/sealed-after-annotation-modification: WRONG REQUIREMENT ATTRIBUTION: non-semantic annotation mutation invalidates the seal, not the semantic-content-specific predicate.

## SPD-STATE-005 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-005, section: 26, level: MUST, capability: [Fixed-Experimental], subject: fixed-rendition, requirement: "A fixed rendition is current only when revision ID, renditionInputDigest, and resource digest match current verified state; otherwise it is stale.", testability: AUTOMATED, testType: INTEGRITY, derivedFrom: A-009}
```

- invalid/mutation-fixed: ESTABLISHED: status=current but fixed resource hash c9bd22e9… differs from actual df6cb8ce…; currentness is disproved directly.

## SPD-STATE-006 — 1 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-006, section: 27, level: MUST, capability: [Base], subject: sealed-state, requirement: "A semantic-only revision may be SEALED; if fixed is present in SEALED it is current.", testability: AUTOMATED, testType: SCHEMA, derivedFrom: A-008}
```

- invalid/mutation-fixed: ESTABLISHED: SEALED has fixed output whose exact digest does not verify, so it cannot be current.

## SPD-STATE-007 — 2 differing fixtures

Frozen registry entry:

```yaml
- {id: SPD-STATE-007, section: 56, level: MUST, capability: [Mapping], subject: capability, requirement: "A Mapping claim requires a current fixed rendition and a bound mapping artifact; current fixed without Mapping is permitted.", testability: AUTOMATED, testType: INTEGRITY, derivedFrom: A-021}
```

- invalid/mutation-fixed: ESTABLISHED: Mapping is explicitly claimed and required current fixed output is disproved by its own hash mismatch.
- invalid/stale-fixed-rendition: ESTABLISHED: Mapping is claimed but fixed is explicitly stale. A incorrectly routes this Mapping failure to the processor rule STATE-001.
