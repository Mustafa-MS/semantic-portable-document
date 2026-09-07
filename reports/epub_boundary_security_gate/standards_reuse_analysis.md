# Standards reuse and the EPUB boundary

Research date: 2026-09-03; report completion: 2026-09-04 (Asia/Baghdad). Research and recommendations only. The Draft, registry, schemas, validators, fixtures, working name, and release status remain unchanged. References below are the editions inspected, not an automatic update of SPD dependencies.

## Standards inspected

| Source | Exact edition/status inspected | Relevant material |
| --- | --- | --- |
| [EPUB 3.3](https://www.w3.org/TR/2026/REC-epub-33-20260113/) | W3C Recommendation, 2026-01-13 | §§1.3, 2, 3, 4, 5, 6, 7, 10–11, I.2: publication conformance, inherited technologies, resources, OCF, OPF, content, navigation, security, media identification |
| EPUB 3.3 OCF | §4 of the preceding Recommendation; not a separate current EPUB 3.3 specification | Abstract container, paths, reserved files, ZIP, font obfuscation |
| [EPUB Reading Systems 3.3](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/) | Recommendation, 2024-10-17 | Publication processing, scripting support, origins, rendering and security |
| [EPUB Accessibility 1.1](https://www.w3.org/TR/2024/REC-epub-a11y-11-20241017/) | Recommendation, 2024-10-17 | Scope, discoverability, publication-wide WCAG application, reporting |
| [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) | Recommendation, 2024-12-12 | AA success criteria and conformance |
| [EPUB 3.4](https://www.w3.org/TR/2026/CRD-epub-34-20260803/) | Candidate Recommendation Draft, 2026-08-03 | Status and forward-evolution risk only; not an SPD dependency |
| [HTML metadata](https://html.spec.whatwg.org/multipage/semantics.html), [embedded contexts](https://html.spec.whatwg.org/multipage/iframe-embed-object.html), [links](https://html.spec.whatwg.org/multipage/links.html), [forms](https://html.spec.whatwg.org/multipage/forms.html), [media](https://html.spec.whatwg.org/multipage/media.html) | WHATWG Living Standard, displayed update 2026-09-03; inspected that date | Base URLs, links/resource loading, refresh, browsing contexts, submission, playback. These dated observations are not immutable HTML version identifiers. |
| [CSS Syntax 3](https://www.w3.org/TR/2021/CRD-css-syntax-3-20211224/) | Candidate Recommendation Draft, 2021-12-24 | Tokenization, escapes, parsing |
| [CSS Cascade 5](https://www.w3.org/TR/2022/CR-css-cascade-5-20220113/) | Candidate Recommendation Snapshot, 2022-01-13 | Imports and cascade |
| [CSS Values 4](https://www.w3.org/TR/2024/WD-css-values-4-20240312/) | Working Draft, 2024-03-12 | URL values and resolution |
| [CSS Variables 1](https://www.w3.org/TR/2022/CR-css-variables-1-20220616/) | Candidate Recommendation Snapshot, 2022-06-16 | Deferred substitution and cycles |
| [CSS Fonts 4](https://www.w3.org/TR/2026/WD-css-fonts-4-20260831/) | Working Draft, 2026-08-31 | Font sources; consulted for resource-fetch surface, not adopted wholesale |
| [CSS Animations 1](https://www.w3.org/TR/2023/WD-css-animations-1-20230302/), [CSS Transitions 1](https://www.w3.org/TR/2026/WD-css-transitions-1-20260108/) | Working Drafts, 2023-03-02 and 2026-01-08 | Time-dependent presentation |
| [SVG 2](https://www.w3.org/TR/2018/CR-SVG2-20181004/), especially [processing modes](https://www.w3.org/TR/SVG2/conform.html) | Candidate Recommendation, 2018-10-04 | Secure static versus static/animated/interactive modes |
| [SVG 1.1 second edition](https://www.w3.org/TR/2011/REC-SVG11-20110816/) | Recommendation, 2011-08-16 | Mature graphics baseline; not a passive-content profile by itself |
| [MathML 3 second edition](https://www.w3.org/TR/2014/REC-MathML3-20140410/), [presentation](https://www.w3.org/TR/MathML3/chapter3.html), [mixed markup](https://www.w3.org/TR/MathML3/chapter5.html) | Recommendation, 2014-04-10 | Presentation mathematics, resource/link attributes, actions, annotations |
| [MathML Core](https://www.w3.org/TR/2025/CR-mathml-core-20250624/) | Candidate Recommendation Snapshot, 2025-06-24 | Browser rendering subset; not a replacement for EPUB's MathML 3 authoring contract |
| [Unicode 17.0](https://www.unicode.org/versions/Unicode17.0.0/), [release confirmation](https://www.unicode.org/L2/L2025/25234-rmg-report-utc185.pdf) | Released 2025-09-09; release report dated 2025-10-22 | Character-version context. The landing page returned a stale preliminary-status notice; the release report resolves that ambiguity. |
| [UAX #15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html) | Unicode 17.0.0, 2025-07-30 | NFC and normalization stability |
| [UAX #9 revision 51](https://www.unicode.org/reports/tr9/tr9-51.html) | Unicode 17.0.0, 2025-08-13 | Bidi display versus logical storage |
| [RFC 6838](https://www.rfc-editor.org/rfc/rfc6838.html) | BCP 13, January 2013 | Media-type registration; registration and internal package identification are separate questions |
| [EPUBCheck CLI](https://www.w3.org/publishing/epubcheck/docs/cli/) | Unversioned documentation inspected 2026-09-03; project executable frozen at 5.3.0 | Whole-publication and partial file checking |
| [Ace by DAISY](https://daisy.github.io/ace/) | Unversioned project documentation inspected 2026-09-03 | EPUB accessibility tooling, with manual assessment still necessary |

## Decisive conformance reasoning

EPUB 3.3 §2 requires the package, resources, navigation, and container to conform. §6.3.2.1 **permits** scripting; it does not require a publication to contain it. Likewise §3.6 permits specified remote resources; it does not require any. Therefore excluding both is a restriction of the allowed publication set, not a contradiction. SPD can prohibit scripts, event handlers, forms and executable contexts and still satisfy EPUB. Forbidding network authority in an SPD reader is a separate processing requirement. EPUB Reading Systems scripting recommendations are not a requirement that every publication execute scripts. An SPD reader need not claim support for every optional EPUB feature. [EPUB 3.3](https://www.w3.org/TR/2026/REC-epub-33-20260113/), [Reading Systems 3.3](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/).

A strict subset must still meet the other EPUB rules. “Passive” does not excuse a missing navigation document, malformed OPF, incorrect manifest properties, or an unsupported foreign resource lacking an applicable fallback. JSON descriptors and generated fixed output must retain their correctly located extension/resource roles. Reusing an HTML element does not authorize arbitrary browser behavior.

## Pinning is more than a version number

The local [technology table](../../spec/STANDARDS_TRACEABILITY.md) names EPUB 3.3 but not a dated edition. Its HTML reference is living, and its CSS reference set is inherited. EPUB §1.3 itself warns of evolving dependencies. Thus “exactly EPUB 3.3” prevents automatic adoption of 3.4, but alone does **not** freeze all transitive grammar and processing changes.

Proposed pre-RC action: record the **2026-01-13 EPUB 3.3 edition**, the **2024-10-17 reading-system edition**, the accessibility/WCAG editions above, and a reviewed dependency snapshot policy. Reconcile this proposed pin against EPUBCheck 5.3.0's supported rules before calling it settled. Record immutable upstream snapshots/commits for living references in the eventual dependency ledger; do not pretend the inspection date is such a commit. Accept later errata only through an explicit SPD maintenance decision and regression review. Label the claim as conformance to SPD's dated EPUB baseline, not to any future meaning of “latest EPUB.” Future upstream contradictions require review, not silent acceptance or silent relaxation.

This is manageable maintenance under A. B must still pin OPF, HTML, CSS, SVG, MathML, URL and Unicode if it reuses them. Removing the EPUB publication claim does not remove those dependencies. EPUB 3.4 is currently a CR Draft, not a Recommendation; this audit proposes no automatic migration.

## Option B accounting scenario

To make counts reproducible, **B-min** means: retain ZIP Stored/Deflate, paths, container.xml link discovery, OPF grammar/namespaces, XHTML spine, EPUB navigation syntax and existing content restrictions; replace the mandatory EPUB package identity marker and whole-publication inheritance with an explicit SPD incorporation table. No new marker spelling or extension is selected. Accessibility requires an explicit applicability mapping. No semantic/identity/digest/mapping algorithms change.

This is a conditional cost model within Option B, not a fourth architecture or a proposal to implement B. A B package retaining the original marker and all current bytes could still happen to be EPUB-conforming; dropping a requirement alone forces **zero** byte changes. Conversely a new internal marker forces all 70 envelopes to change. Both cases are quantified in [corpus impact](corpus_impact.md).

## Responsibilities that lose umbrella inheritance under B

These are **24 responsibility groups**, not 24 newly invented languages or an estimate of specification pages. There are 6 direct-reference groups, 16 SPD-profile groups, 1 rewrite group and 1 omission group. The eight candidate B registry additions in [requirement impact](requirement_impact_matrix.md) group these responsibilities; existing requirements also cover parts of them.

| # | Behavior | B treatment | Work and source of reuse |
| --- | --- | --- | --- |
| 1 | ZIP binary syntax | Can reference existing standard directly | Retain the ZIP specification referenced by EPUB; no new compression format |
| 2 | ZIP allowed methods, flags, ordering | Needs SPD-specific profile | Carry forward the OCF restrictions and explicit exceptions |
| 3 | Package identity/detection | Must be rewritten | Define a truthful non-EPUB marker if chosen, recognition and mismatch behavior |
| 4 | Path grammar/collisions | Needs SPD-specific profile | Carry forward current SPD path rules and selected OCF constraints |
| 5 | Container discovery | Needs SPD-specific profile | Retain rootfile/link syntax, define which context it addresses outside EPUB |
| 6 | Reserved files/directories | Needs SPD-specific profile | State META-INF rules and classification of SPD descriptors |
| 7 | OPF grammar and namespaces | Can reference existing standard directly | Incorporate the dated Package Document section and its transitive dependencies |
| 8 | Manifest membership/completeness | Needs SPD-specific profile | Define publication versus control versus supplementary resources |
| 9 | Media-type support and fallbacks | Needs SPD-specific profile | Select EPUB rules or explicitly replace them; no silent gaps |
| 10 | Reading order | Needs SPD-specific profile | State spine, linear/nonlinear handling, reachability and SPD authority |
| 11 | Navigation | Needs SPD-specific profile | Incorporate EPUB nav syntax, then bind it to the SPD manifest/spine |
| 12 | Resource discovery | Needs SPD-specific profile | Retain authoritative descriptor relationships and no filename guessing |
| 13 | URL syntax/parsing | Can reference existing standard directly | Reuse URL semantics; do not substitute ad hoc concatenation |
| 14 | URL base, decoding and package lookup | Needs SPD-specific profile | Bind URI processing to the new container and current safe-path contract |
| 15 | XML and namespaces | Can reference existing standard directly | Reuse XML/Namespaces; retained entity/XInclude restrictions remain explicit |
| 16 | XHTML/SVG/MathML integration | Needs SPD-specific profile | Carry forward EPUB host-language constraints and the same passive rules |
| 17 | CSS grammar/cascade | Can reference existing standard directly | Reuse CSS modules; URL capability policy belongs to SPD |
| 18 | Unicode normalization and bidi | Can reference existing standard directly | Keep SPD scalar ranges and exact-byte hashes; do not normalize prose |
| 19 | Publication metadata | Needs SPD-specific profile | Incorporate required metadata, property vocabularies and version behavior |
| 20 | Accessibility scope and metadata | Needs SPD-specific profile | Explicit non-EPUB applicability/reporting mapping; preserve WCAG 2.2 AA |
| 21 | Reader processing/unsupported features | Needs SPD-specific profile | Bind passive behavior and capability reporting to the new package |
| 22 | Conformance checking/errors | Needs SPD-specific profile | Replace whole-package EPUBCheck authority and define imported-rule attribution |
| 23 | Extension handling | Needs SPD-specific profile | Relate retained SPD required/optional extension rules to imported OPF rules |
| 24 | DRM and unused EPUB optional features | Can be omitted | Do not import processing obligations for features outside the chosen Base profile |

## OPF, OCF, navigation: reuse rather than redesign

OPF can be incorporated directly without asserting that the enclosing file is an EPUB publication. This preserves XML parsers, schemas, authoring familiarity and some diagnostic tools. It is clear reuse when SPD states the exact incorporated clauses, their dependencies, and the meaning of publication-related terms in SPD. Merely saying “OPF-like” leaves standards ambiguity. Changing OPF element meanings while keeping its namespace creates a compatibility hazard; that should be avoided.

The same is true of the spine and navigation document. They can remain the structures, but SPD owns their **application**: primary reading order, references, nonlinear resources, required nav, and fallback behavior. In B-min, this requires binding four groups above (8–11), not inventing a new nav language. A standalone OPF/nav checker cannot establish the validity of the complete independent package.

“OCF except for these replacements” is workable constrained reuse. With a replaced mandatory marker, however, the result is **OCF-derived**, not an unqualified conforming OCF container. Maintain an exception table, upstream errata tracking, cross-reference closure, import tests and export tests. The cost is ongoing comparison work even when the binary ZIP implementation is unchanged. Renaming the manifest would increase that cost without a demonstrated requirement.

## Layering recommendation

Adopt the conceptual layers **SPD document model → SPD Passive Content Profile → SPD EPUB-Compatible Packaging Profile 0.1**. Give each layer a clear responsibility and reference boundary. Keep a single 0.1 conformance bundle now; adding a new independently negotiable version field is unnecessary and would touch schemas without a current need.

The name alone does not decouple implementations: discovery, path identity, inventory membership and metadata still bind the model to packaging. A documented mapping from package facts to document-model inputs is the useful separation. A later packaging profile can preserve those contracts with explicit migration. It cannot make previously serialized 0.1 documents independent of EPUB retroactively.
