# Semantic Portable Document (SPD)

> **Format 0.1 RC1 — experimental / open for external review**

[Read the Format 0.1 RC1 specification](spec/FORMAT_0.1_RC1.md) · [Open the RC1 release](https://github.com/Mustafa-MS/semantic-portable-document/releases/tag/v0.1.0-rc1) · [Browse the conformance corpus](tests/corpus-0.1-rc1/) · [Review the RC1 validation report](reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md) · [See the Draft-to-RC1 changelog](spec/FORMAT_0.1_DRAFT_TO_RC1_CHANGELOG.md)

SPD is a semantic portable-document format designed so humans and software or AI agents can safely address, edit, and reason about persistent document objects. Format 0.1 is a release candidate for experimentation and independent review, not a finalized standard.

## Why EPUB

Format 0.1 deliberately reuses the pinned EPUB 3.3 publication and package model. It does not invent another container, replace HTML, or define a new layout stack. An SPD 0.1 package remains an EPUB-compatible package with stricter, versioned semantics layered on top.

## What SPD adds

- persistent document, revision, and node identity;
- transaction-safe editing semantics and explicit revision lineage;
- integrity bindings and document lifecycle state;
- optional semantic-to-fixed-rendition mapping;
- revision-aware annotations; and
- a passive-content security profile with bounded processing expectations.

These mechanisms are intended to make document state and changes inspectable. They do not make every package or implementation universally secure.

## Architecture

```text
EPUB 3.3 package and publication model
  + semantic XHTML with persistent node identities
  + document, revision, inventory, and lifecycle descriptors
  + transaction and integrity rules
  + optional fixed rendition and semantic mapping
  + annotations and passive-content restrictions
  = SPD Format 0.1 package
```

The semantic representation is authoritative. Fixed renditions and mappings are explicit, integrity-bound capabilities rather than a second canonical document model.

## Repository structure

| Path | Contents |
| --- | --- |
| [`spec/`](spec/) | RC1 specification, profiles, requirements registry, traceability, and changelog |
| [`schemas/rc1/`](schemas/rc1/) | Versioned JSON Schema bundle for RC1 |
| [`tests/corpus-0.1-rc1/`](tests/corpus-0.1-rc1/) | 107 reviewed conformance fixtures and expected results |
| [`validator-a/`](validator-a/) | Rust reference conformance validator |
| [`validator-b/`](validator-b/) | Independently implemented Python validator |
| [`validation/`](validation/) | Validator-neutral contracts and attribution data |
| [`reports/format-0.1-rc1/`](reports/format-0.1-rc1/) | RC1 validation summary and artifact manifest |
| [`docs/`](docs/) and [`reports/`](reports/) | Architecture decisions and preserved research evidence |

## Validation

The qualifying RC1 run covers **118 requirements** and **107 fixtures**:

- Validator A ↔ Validator B: **107/107** exact agreement;
- Validator A ↔ reviewed oracle: **107/107**;
- Validator B ↔ reviewed oracle: **107/107**;
- official EPUBCheck 5.3.0 executed for all **107/107** package byte sequences in each validator; and
- all **48/48** Base-PASS fixtures pass EPUBCheck in both validators.

The run reported zero new specification blockers and no normative semantic changes from the converged pre-RC Draft. See the [human-readable report](reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md), [machine-readable summary](reports/format-0.1-rc1/RC1_VALIDATION_REPORT.json), and [artifact manifest](reports/format-0.1-rc1/RC1_ARTIFACT_MANIFEST.json).

To run the fast repository tests from PowerShell:

```powershell
./scripts/test.ps1
```

Validator-specific build and usage instructions are in [Validator A](validator-a/README.md) and [Validator B](validator-b/README.md). EPUBCheck is an explicit external dependency and is not downloaded by either validator at runtime.

## Status and limitations

SPD Format 0.1 RC1 is experimental and open for external review. It is not a W3C standard, a finalized standard, or a PDF replacement. The passive-content profile reduces and makes explicit parts of the attack surface, but it is not a claim of universal security.

Fixed-Experimental and Archive-Experimental remain experimental. Reader behavior, manual accessibility evaluation, digital signatures, encryption/DRM, functional forms, interactive or scripting capabilities, collaboration and tracked changes, and a final agent API are outside the RC1 validation claim. No reference reader is included in this release.

## Roadmap

The immediate goal is to gather independent implementation and interoperability feedback, resolve genuine specification ambiguities without destabilizing established semantics, and define the evidence needed for a later Format 0.1 release. Deferred capabilities will be considered separately rather than folded into RC1.

## Contributing and external review

External review is the purpose of this release. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open a focused issue for specification ambiguity, validator behavior, security, accessibility, EPUB interoperability, or identity/mapping concerns. Report suspected vulnerabilities through the process in [SECURITY.md](SECURITY.md), not a public issue.

## License

Software and code are licensed under Apache License 2.0. The specification and documentation are licensed under Creative Commons Attribution 4.0 International. The exact scope of the split is defined in [LICENSE](LICENSE).
