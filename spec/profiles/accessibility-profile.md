# Format 0.1 accessibility profile

Base accessibility authority is the authoritative semantic XHTML, not an optional fixed rendition. This profile separates machine-detectable structure from human quality.

## Automated structural checks

- EPUB package/navigation and XHTML syntax validity.
- Root language metadata and direction declarations in deterministic cases.
- Unique IDs, valid references, heading/list/table element structure, form labels where controls are preserved, and alternative-text attribute presence where applicable.
- Native-semantics-first anti-patterns, invalid/conflicting ARIA, broken ID references, inaccessible required remote dependencies, and focusable active content prohibited by Base.
- MathML/SVG accessibility hooks and figure-caption relationships where mechanically determinable.

## Partially automated checks

- Logical heading hierarchy, meaningful link purpose, correct table header relationships, reading order, sufficient language changes, appropriate ARIA/DPUB-ARIA, and whether hidden content improperly carries meaning.
- WCAG contrast and reflow checks can be assisted but require context and sampling.

## Human judgment required

- Whether alternative text, captions, labels, link text, headings, reading order, and mathematical descriptions are meaningful and equivalent.
- Whether cognitive/interaction requirements and the claimed WCAG level are met across the publication.

## Conformance basis

SPD Accessible 0.1 is exactly EPUB Accessibility 1.1 plus WCAG 2.2 Level AA. A claiming document records `epubAccessibility: 1.1` and `wcag: 2.2-AA`. Other claims may be added but do not redefine SPD Accessible. Native HTML semantics are used first, WAI-ARIA 1.2 only when necessary, and DPUB-ARIA 1.1 where applicable. Automated success is never described as full accessibility certification; applicable human evaluation remains required.

An independently distributed PDF or other fixed export claiming accessibility must independently meet its own profile (for example PDF/UA) and human-quality requirements. Accessible XHTML cannot confer accessibility on that export. PDF accessibility and PDF/A are not Base requirements.

The edition pins are EPUB Accessibility 1.1 REC 17 October 2024 and WCAG 2.2 REC 12 December 2024, AA. Accessible capability meaning and human evaluation are unchanged. Passive controls/media must preserve accessible labels, values and alternatives; the passive profile alone never establishes Accessible conformance.
