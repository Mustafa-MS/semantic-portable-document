# Dependency Decisions

The versions below are the independently selected blind-development environment on Python 3.13.3. Runtime ranges are constrained in `pyproject.toml`.

| Package | Version | Purpose | License | Why selected | Alternatives considered |
|---|---:|---|---|---|---|
| Python standard library | 3.13.3 | ZIP, SHA-256, URI/path handling, Unicode NFC, subprocess isolation | PSF-2.0 | Mature built-ins avoid extraction helpers and keep exact-byte hashing explicit | libarchive, pyzipper |
| jsonschema | 4.26.0 | JSON Schema Draft 2020-12 plus format checks | MIT | Mature, specification-oriented Python implementation with local-schema operation | fastjsonschema, custom validator |
| lxml | 6.1.3 | Hardened XML/XHTML/OPF/SVG parsing and XPath | BSD-3-Clause | Mature libxml2 binding with explicit entity/network/DTD controls | defusedxml + ElementTree, Saxon |
| tinycss2 | 1.5.1 | CSS syntax tokenization and URL/import inspection | BSD-3-Clause | Standards-oriented tokenization avoids regex-only CSS interpretation | cssutils, custom tokenizer |
| rfc8785 | 0.1.4 | RFC 8785 JCS serialization | Apache-2.0 | Small dedicated implementation, independently testable against RFC vectors | canonicaljson, custom JCS implementation |
| PyYAML | 6.0.3 | Frozen requirements registry and coverage generation | MIT | Mature safe YAML loader | ruamel.yaml, bespoke flow-map parser |
| pytest | 9.1.1 | Unit/security/corpus tests | MIT | Mature Python test runner | unittest |
| Hypothesis | 6.167.1 | Property tests for paths, digests, and Unicode boundaries | MPL-2.0 | Generates adversarial cases beyond hand-authored vectors | custom random loops |
| EPUBCheck | unavailable; target 5.3.0 | Inherited EPUB 3.3 validation | BSD-3-Clause | Frozen acceptance tool required by experiment | no substitute accepted |

No dependency was chosen from Validator A implementation information. EPUBCheck remains external and is never auto-downloaded during validation.

