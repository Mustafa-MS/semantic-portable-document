# Format 0.1 RC1 standards traceability

| Standard | Version/status used | Feature reused/profiled | Adoption | SPD requirements |
|---|---|---|---|---|
| EPUB | 3.3 W3C Recommendation, 13 January 2026 | OCF ZIP, exactly one SPD rootfile, `container.xml` processing links, package document, manifest, spine, navigation, resource URLs | Profiled with offline/security/inventory/discovery restrictions | SPD-BASE-001–006, SPD-DISC-001–003, SPD-RES-001–006 |
| HTML | Living Standard baseline reviewed 3 September 2026, only as incorporated by pinned EPUB 3.3 | XHTML serialization and native semantics | Profiled | SPD-SEM-001–013 |
| XML | 1.0 Fifth Edition | Well-formed XHTML/XML IDs | Unchanged | SPD-SEM-002, SPD-ID-005–010 |
| CSS | Dated module set in UPSTREAM_DEPENDENCY_BASELINE_0.1.md, otherwise only as incorporated by pinned EPUB 3.3 | Author styling and paged media | Profiled | SPD-SEC-005, SPD-I18N-002 |
| MathML | MathML 3 Second Edition, 10 April 2014, as incorporated by pinned EPUB 3.3 | Semantic mathematics | Profiled | SPD-SEM-009 |
| SVG | SVG 1.1 Second Edition (16 August 2011) and SVG 2 CR (4 October 2018), as incorporated by pinned EPUB 3.3 | Static vector graphics | Security-profiled | SPD-SEC-007 |
| Unicode | Unicode 17.0.0; UAX #15 rev. 57; UAX #9 rev. 51 | Scalar values and character encoding | Profiled; UAX #9 logical order is normative behavior | SPD-I18N-001–006, SPD-MAP-008–009 |
| UAX #9 | Unicode Bidirectional Algorithm | Logical storage versus visual display | Adopted | SPD-I18N-001–005 |
| WAI-ARIA | 1.2 | Supplemental accessibility semantics | Profiled; native semantics first | SPD-SEM-004–006, SPD-ACC-001 |
| DPUB-ARIA | 1.1 | Digital-publishing roles where applicable | Profiled | SPD-SEM-004–006, SPD-ACC-001 |
| EPUB Accessibility | 1.1 Recommendation | Publication accessibility evaluation/discoverability | Normative Accessible 0.1 dependency | SPD-ACC-001, SPD-ACC-004 |
| WCAG | 2.2 Recommendation | Level AA accessibility success criteria | Normative Accessible 0.1 dependency | SPD-ACC-001, SPD-ACC-004 |
| Web Annotation Data Model | 2017 Recommendation | Annotation/body/target/selector model | Adopted with one selector extension | SPD-ANN-001 |
| EPUB Annotations | 1.0 Working Draft (2026) | JSON-LD annotation set/profile and packaging direction | Informative monitored dependency only | SPD-ANN-001 |
| JSON Schema | Draft 2020-12 | Structural schemas | Adopted | SPD-ID-001–005, SPD-RES-002, SPD-MAP-002/005/007, SPD-STATE-002 |
| SHA-256 | FIPS 180-4 / RFC 6234 | Resource and state digests | Adopted; exact resource-byte profile added | SPD-INT-001–003, SPD-RES-004 |
| UUID | RFC 9562 | Document and Revision UUID textual syntax/opacity | Profiled to canonical lowercase UUID URNs | SPD-ID-001–002 |
| JSON Canonicalization Scheme | RFC 8785 | Lifecycle descriptor canonical bytes with self-digest omitted | Adopted only for the closed I-JSON state descriptor | SPD-INT-006 |
| PDF | 2.0 (ISO 32000-2) | Reference fixed rendition | Experimental/informative | SPD-FIX-001–003 |
| PDF/UA | PDF/UA-2 where claimed | Accessible standalone PDF | Independent optional fixed-export profile | SPD-ACC-002–003 |
| PDF/A | PDF/A-4 | Reference archival fixed rendition | Archive-Experimental only | SPD-FIX-003 |

The OCF profile references EPUB requirements instead of copying them. Draft EPUB 3.4 and EPUB Annotations work may inform future revisions but is not a Base 0.1 normative dependency.

## RC1 dated inheritance and passive profile

The normative edition/update policy is [UPSTREAM_DEPENDENCY_BASELINE_0.1.md](UPSTREAM_DEPENDENCY_BASELINE_0.1.md): EPUB 3.3 REC 2026-01-13; explicitly relied-on Reading Systems 3.3 REC 2024-10-17; EPUB Accessibility 1.1 REC 2024-10-17; WCAG 2.2 REC 2024-12-12, AA unchanged. Living HTML/URL and transitive CSS/SVG/MathML references are governed by explicit maintenance review, never silent future adoption. EPUB 3.4 remains monitored future work only.

SEC-001–008 and PASS-001–003 restrict capabilities of EPUB XHTML, CSS, SVG and MathML without replacing their languages. See the normative profiles and shared passive resource-reference contract. RS-001–002 add processor authority/verification obligations; document validation does not certify them. Passive restrictions do not prove Accessible conformance; equivalent labels, values and semantic alternatives require the existing human evaluation.

## RC1 identifier and artifact traceability

Stable public identifiers are listed in [IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md](IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md). The RC1 registry retains 118 requirement IDs. The RC1 corpus retains all 107 reviewed expected outcomes and changes only identifier-bearing bytes and their deterministic integrity bindings. No future upstream edition or erratum changes Format 0.1 without an explicit maintenance revision.
