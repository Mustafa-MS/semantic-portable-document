# Format 0.1 RC1 validation report

## Result

- Requirements: **118**; IDs and conformance predicates preserved.
- Corpus: **107** fixtures; Base results PASS 48, FAIL 58, NOT_TESTED 1.
- Validator A ↔ Validator B: **107/107** exact agreement.
- Validator A ↔ reviewed oracle: **107/107**.
- Validator B ↔ reviewed oracle: **107/107**.
- Official EPUBCheck 5.3.0 executed on **107/107** package byte sequences for each validator.
- All Base-PASS fixtures pass EPUBCheck: **48/48** for A and **48/48** for B.
- Final operational statuses: 105 COMPLETE, one MALFORMED_INPUT, one RESOURCE_LIMIT; no INTERNAL_ERROR or SPEC_BLOCKER.
- New specification blockers: **0**.
- Normative semantic changes: **NONE**.

## Identifier and mechanical migration

Every RC1 package is a versioned copy. Stable UUID URNs replace Draft schema, relationship, capability, and annotation-extension placeholders. Valid byte/digest bindings were regenerated deterministically; deliberately invalid bindings and malformed/special ZIP predicates were retained. RC1 expected results differ from Corpus 0.1.2 only in `corpusVersion`. No RC1 package contains `https://example.invalid/spd/`.

The RC1 corpus manifest SHA-256 is `3caf773edb46edd2cbf051735eb115292794bbefbda2dd74452db12b830dcf0a`. The official EPUBCheck 5.3.0 JAR SHA-256 is `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`. Exact package, expected-result, source-package, schema, validator-output, and publication-artifact hashes are recorded in the versioned manifests.

## Preservation and scope

The converged Draft specification, Draft registry, Corpus 0.1.2 packages and expectations, reviewed oracle, validator convergence freezes, and pre-RC evidence remain unchanged. Fixed-Experimental and Archive-Experimental remain experimental. No reference reader was started or evaluated. Reader behavior, manual accessibility evaluation, signatures, encryption/DRM, functional forms, interactive/scripting capability, collaboration/tracked changes, and a final agent API remain outside this RC1 validation claim.

FORMAT 0.1 RC1 READY FOR EXTERNAL REVIEW
