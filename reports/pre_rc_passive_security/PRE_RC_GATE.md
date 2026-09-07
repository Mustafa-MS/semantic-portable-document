# Pre-RC passive security gate

No RC1 is created. This authorizes only the next editorial/identifier preparation stage; existing production-identifier migration remains separate.

| Question | Answer |
|---|---|
| A | YES — conforming EPUB 3.3 publication/package profile retained. |
| B | YES — Recommendation 13 January 2026 pinned. |
| C | YES — explicit roles and maintenance policy; living sources are not falsely described as immutable snapshots. |
| D | YES — document-originated executable behavior prohibited. |
| E | YES — automatic publication-originated network authority prohibited. |
| F | YES — optional/decorative resources included. |
| G | YES — supported XHTML/CSS/SVG/MathML resource paths are inspected transitively; unresolved locality is NOT_TESTED. |
| H | YES — namespace-aware XML and standards-aware CSS tokens; regex is not authoritative content-security parsing. |
| I | YES — every completed EPUB publication error prevents Base PASS. |
| J | YES — semantic display is distinct from verified SEALED/current fixed presentation. |
| K | YES — hash integrity is distinct from authentication; no signatures added. |
| L | NO — no new MIME type or mandatory extension. |
| M | YES — semantic/revision/mapping architecture and canonical schemas unchanged. |
| N | 118 requirements: 113 baseline + 5, with 11 modified and 102 unchanged. |
| O | 107 corpus fixtures: 70 retained + 37 targeted additions. |
| P | 8 reader-security scenarios; processor conformance, all NOT_TESTED. |
| Q | YES — 48/48 Base-PASS fixtures pass EPUBCheck 5.3.0. |
| R | YES — 107/107 A/B agreement. |
| S | YES — both 107/107 against the independent oracle. |
| T | NO — zero open specification blockers. |

All required build/lint/unit/property/schema/coverage/native/full-corpus/external gates pass. Reader behavior and complete static semantic meaning are honestly unevaluated, as required for this pre-reader task. Bounded corpus agreement is not a claim of exploit-proof implementations or universal EPUB reader compatibility.

READY FOR FORMAT 0.1 RC1 EDITORIAL AND IDENTIFIER PREPARATION
