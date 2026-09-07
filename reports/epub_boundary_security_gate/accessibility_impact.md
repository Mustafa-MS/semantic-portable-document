# Accessibility and schema impact

**A preserves the cleanest accessibility contract. B can reuse the substance, but cannot silently claim that an independent non-EPUB publication satisfies an EPUB-scoped specification without an applicability mapping.** This is a direct packaging-boundary consequence, not a reopening of SPD's accessible semantic authority.

## Current contract and standards scope

[SPD-ACC-004](../../spec/requirements.yaml) requires EPUB Accessibility 1.1 **and WCAG 2.2 AA**, with applicable human evaluation. [The profile](../../spec/profiles/accessibility-profile.md) evaluates the authoritative XHTML, not the optional fixed rendition. Fixed exports need their own accessible-format conformance. Those distinctions survive all three options.

[EPUB Accessibility 1.1, 2024-10-17](https://www.w3.org/TR/2024/REC-epub-a11y-11-20241017/) applies across EPUB versions/profiles and says broader Open Web publication applicability is outside its scope. Its publication-wide WCAG application, OPF discovery metadata, page navigation and conformance reporting assume an EPUB publication. Therefore being independent of EPUB does not make its accessibility techniques unusable; it makes **unqualified whole-specification conformance** problematic. Merely retaining XHTML does not solve the publication-level issue.

## Five required answers for B

| Question | Answer |
| --- | --- |
| Can SPD normatively incorporate EPUB Accessibility 1.1? | Yes, selected requirements and an explicit applicability mapping can be incorporated by reference. It must identify the SPD publication unit and how EPUB-specific terms/locations apply. |
| Does it assume EPUB in ways that block direct adoption? | Yes, for an unqualified claim that an independent non-EPUB package itself conforms. If a particular B file also happens to conform to EPUB, that particular file can retain an EPUB accessibility claim after full assessment. |
| Must metadata/requirements be restated? | Applicability and claim semantics must be specified. With OPF retained, metadata syntax can be reused rather than rewritten. A new manifest would need a location/serialization mapping as well. |
| Does WCAG remain usable? | Yes. WCAG 2.2 AA remains the content accessibility target. Define the complete SPD publication assessment scope, navigation, alternatives, supported technologies and full processes; do not assume isolated XHTML pages passing checks proves package conformance. |
| What tooling is lost? | Direct EPUB input acceptance and whole-publication workflows may be lost. Reusable HTML checks, manual evaluation, ARIA and semantic structure remain. Ace and EPUB metadata/nav tools may work on an EPUB projection or adapted OPF, but that result does not certify the independent source automatically. |

These are architecture consequences and proposed mappings, not legal compliance advice. [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) remains the criterion source; [Ace](https://daisy.github.io/ace/) is an EPUB-oriented tool and cannot replace required human assessment.

## Exact affected registry surface

For B-min, **SPD-ACC-004 is classified MUST BE RESTATED AS SPD-NATIVE** because the EPUB publication-level applicability/claim must change. ACC-001/002/003 remain unchanged. SEM-004/005/006/009/012/013 and I18N language/direction obligations remain unchanged: native semantics and meaningful accessibility do not depend on an EPUB filename. BASE-005, SEM-002/003 and discovery rows also need explicit inheritance bindings as documented in the 113-row matrix.

Do not erase metadata such as access modes, accessibility features/hazards, sufficient access modes where applicable, summaries, and conformance reporting merely because B has its own identity. Do not upgrade Base to a full accessibility certification: the current corpus's `valid/accessible` result remains **NOT_TESTED**, not a completed manual AA evaluation. Reuse all applicable discovery and content requirements through the mapping.

## Schema audit

The relevant [document-state schema](../../schemas/document-state.schema.json) has a closed `accessibilityTarget` object requiring `epubAccessibility: "1.1"` and `wcag: "2.2-AA"` when Accessible is claimed. This is a real EPUB-named field and must not be overlooked.

| Scope | Structural schema delta | Semantic consequence |
| --- | --- | --- |
| A, including proposed conceptual layering | **NO SCHEMA IMPACT** | No new profile-version field or semantic model change required |
| B marker/container-only, retained OPF and frozen SPD data | **NO SCHEMA IMPACT** | MIME strings in inventory/fixed resources are generic; changing a resource changes values/bindings, not their schema grammar |
| Complete B accessibility migration | **1 schema contract requiring review**, 0 structural edits inherently forced | The meaning of `epubAccessibility` must be resolved alongside ACC-004; do not relabel a non-EPUB claim invisibly |
| C | 0 proven forced semantic-schema rewrites; packaging adapters and the same accessibility contract unresolved | Do not invent schema replacements until a serialization is specified |

B-min can preserve the JSON structure **if** an explicit revised specification defines the existing field as the version of the incorporated accessibility basis and clearly distinguishes the resulting SPD claim from EPUB Accessibility conformance. That is a semantic contract change, not “nothing changed.” If instead the field continues to mean actual unqualified EPUB Accessibility conformance, a B file that does not conform to EPUB cannot honestly satisfy it; revising that field/schema or preserving a conforming EPUB representation becomes necessary. This conditional choice is why the audit does not make a blanket “no schema impact” claim for all of B.

The inventory, lifecycle state, mapping, annotation selector and transaction structures have no identified packaging-only redesign need. Schema IDs remain provisional under the pre-existing release gate; choosing production identifiers is outside this audit. No schema was edited.

## Pre-RC recommendation

Keep the current Accessible target under A. Pin its inspected editions in the dependency ledger, preserve human-evaluation status, and ensure the passive restrictions do not strip native labels, alternative content, math semantics, keyboard reading/navigation or user playback controls. A visible fallback notice should be understandable by assistive technology and should not obscure the authoritative semantic content.
