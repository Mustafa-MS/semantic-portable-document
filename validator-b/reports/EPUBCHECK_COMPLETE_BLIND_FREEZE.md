# EPUBCheck-Complete Blind Freeze

Status: **EPUBCHECK-COMPLETE BLIND VALIDATOR B FROZEN**

Freeze date: 2026-09-03 (Asia/Baghdad).

## Validator and frozen inputs

- Validator B version: **0.1.0**, with two documented external-adapter-only fixes.
- Original `blind-results.json` SHA-256: `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c`.
- New `blind-results-with-epubcheck.json` SHA-256: `af68e0e02182cf6a212c437ba19f6faa8a2d08409b65c3d77aa848e895cc2ed4`.
- Format Draft SHA-256: `fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849`.
- Requirements registry SHA-256: `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`.
- Canonical schema record: `SCHEMA_INPUT_MANIFEST.json` (unchanged; six canonical schemas).
- Validator-B non-normative schema-set digest: `8baf64736240b33c043ecf10fbb75a2dd07cf4db90a421dc0a937d16b3f42a45`.

The original `blind-results.json` and `BLIND_FREEZE_EVIDENCE.md` were neither modified nor overwritten. The original evidence-file SHA-256 remains `30b898063dea5ab007e3c704f7fdcda87f81e819d16fe03f1f2810ab74db70d7`.

## Independently obtained external dependency

- Official source: [W3C EPUBCheck v5.3.0 release](https://github.com/w3c/epubcheck/releases/tag/v5.3.0).
- Release ZIP SHA-256: `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5` (verified before extraction).
- JAR: `validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar` (workspace-relative).
- JAR SHA-256: `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`.
- Version output: `EPUBCheck v5.3.0`.
- Availability: **AVAILABLE**.
- Java executable: `C:\Program Files\Common Files\Oracle\Java\javapath\java.EXE`.
- Java version: `java version "22.0.1" 2024-04-16`; Java(TM) SE Runtime Environment build `22.0.1+8-16`; Java HotSpot(TM) 64-Bit Server VM build `22.0.1+8-16, mixed mode, sharing`.

Tool installation was a separate, explicitly authorized bootstrap operation. Validation itself still performs no downloads.

## Execution and regression gate

- Corpus packages: **69/69** executed through Validator B with EPUBCheck 5.3.0.
- EPUBCheck corpus validation invocations: **69** (plus separate version probes and an integration-test invocation).
- EPUBCheck results: **61 PASS / 8 FAIL / 0 ERROR**.
- Validator operational results: **69 COMPLETE**.
- Internal errors: **0**.
- Requirement coverage: **113/113 represented; 74/74 automated routes**, unchanged.
- All original unit/security/schema/property tests and new integration tests: **43 passed, 0 failures, 0 errors, 0 skipped**.
- SPEC blockers: **0**, unchanged.
- External-adapter defect fixes: **2** — distinguish release ZIP/JAR pins; parse the official version prefix.
- Other adapter changes: metadata-only capture of execution diagnostics; no normalized semantic change.

Exact source diff: `epubcheck-adapter-only.diff`. Fix rationale and regression evidence: `VALIDATOR_B_EXTERNAL_ADAPTER_FIX.md`. Full test output: `epubcheck-regression-tests.xml`.

## B-only before/after evidence

- Unavailable-tool regression reproduces the original blind-results file byte-for-byte: SHA-256 `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c`.
- All **69/69 detailed SPD-native finding sets are identical** before/after.
- All **69** normalized changes are `EPUBCHECK_NOW_EVALUATED`.
- `UNEXPECTED_NON_EPUB_DIFFERENCE`: **0**.
- Base results: **39 PASS / 30 FAIL**.
- Mapping: **9 PASS / 15 FAIL / 45 NOT_CLAIMED**.
- Accessible: **1 NOT_TESTED / 68 NOT_CLAIMED**; human evaluation remains unresolved.

Per-fixture evidence: `epubcheck-fixture-execution.json` and `epubcheck-before-after.json`. Summary: `EPUBCHECK_B_BEFORE_AFTER.md`.

## Unicode environment

- Python: **3.13.3**.
- Unicode data: **15.1.0**.
- Status: **NO_OBSERVED_CORPUS_IMPACT**, retained from the original freeze; native code, corpus bytes, and detailed native findings are unchanged in this stage.

## Continued independence

No Validator A source, tests, executable, adapter implementation, golden oracle, or summary was accessed. No individual corpus expected-result file was read. No A-vs-B comparison was performed. No SPD-native package, descriptor, digest, XHTML, identity, state, capability, mapping, annotation, accessibility, or normalized roll-up logic was changed.

This EPUBCheck-complete independent result is frozen. Differential comparison remains a separate, not-yet-started stage.
