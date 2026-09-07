# EPUB boundary and passive security architecture gate

Research performed 2026-09-03; report completion 2026-09-04 (Asia/Baghdad). **Recommendation: Option A. Confidence: HIGH.** Keep EPUB 3.3 as Format 0.1's normative packaging/publication profile and proceed to targeted passive-profile clarification and verification. Do not create RC1 yet.

EPUB permits scripting and selected remote resources; it does not require them. The same no-execution/no-automatic-network policy works in A and B. A new marker or suffix does not remove ZIP, XML, CSS, SVG, MathML, font, image or rendering vulnerabilities. B offers identity and future structural freedom, but no significant current requirement was found that needs that freedom enough to offset the implementation, validation and accessibility costs. C fails its stronger necessity gate.

The principal disadvantage of A is **generic SEALED fallback**. An ordinary reader can display authoritative semantic XHTML while saying nothing about state verification or the bound current fixed rendition. That is useful reading access, but insufficient for a verified-record claim. Preserve semantic authority and adopt truthful state-aware UI/distribution policies; do not redefine SEALED as requiring PDF or treat hashes as authentication.

## What was verified and what was found

| Item | Audit finding |
| --- | --- |
| Frozen versions | Validator A 0.1.0-draft.2; Validator B 0.1.1; shared contract/corpus 0.1.1 |
| Registry | All 113 unique requirements reviewed; all represented in the impact matrix |
| Corpus | 70 fixtures: 18 valid, 39 invalid, 13 edge; all 70 package hashes and 70 expected-file hashes match the manifest |
| Convergence | Frozen normalized A/B arrays agree exactly on all 70; comparison with the reviewed oracle found zero differences across the seven audited normative/experimental fields |
| EPUBCheck | 70 executions each, 140 total; 62 PASS and 8 FAIL per validator; all 40 Base-PASS fixtures have EPUBCheck PASS |
| External attribution | Seven guarded mappings add six possible SPD requirement IDs; unmatched errors remain raw evidence |
| Reader evidence | Historical epub.js 12/12, Foliate JS 12/12, calibre 5/5; no new reader runs or universal compatibility claim |
| New gate concern | Source review shows unmapped EPUBCheck FAIL alone need not prevent Base PASS; not exposed as a false-positive fixture in the current corpus |
| Security coverage | Existing profile prose is broader than the tested/implemented URL/context coverage; A uses regex-based security checks, B has remaining inline/nested-resource gaps |
| Pinning | Current published EPUB 3.3 is Recommendation 2026-01-13; EPUB 3.4 is CR Draft 2026-08-03. A bare “3.3” does not freeze living transitive references. |

The prior “zero blockers / ready for RC preparation” result remains a historical conclusion about the frozen gate. The additional architecture/security questions above must be resolved before making stronger release/security claims. No code or adversarial proof-of-concept was created, and no validators or readers were run during this audit.

## Quantified options

Counts below use the explicit B-min scenario: retained ZIP/OPF/nav/content with a different internal identity marker. New-rule counts are enumerated proposed groups, not guesses about the eventual number of atomic normative clauses.

| Measure | A boundary only | A with proposed pre-RC package | B-min with same passive package | Fully independent C |
| --- | --- | --- | --- | --- |
| Current requirements unchanged | 113 | 102 | 94 | 99 packaging-only; 90 with shared clarification |
| Current requirements modified | 0 | 11 | 19 | 10 known + 4 conditional packaging-only; 19 known + 4 conditional with shared clarification |
| Current requirements removed | 0 | 0 | 0 | 0 proven; design not specified |
| New proposed groups | 0 | 5 | 13 = 8 B + 5 common | Final count undefined; 12 packaging work groups plus 5 common identified |
| Existing fixture bytes | 70 unchanged | 70 retained in plan | 70 envelopes/bindings modified; 0 test intents replaced | 70 conversion/replacement allocations unresolved |
| New proposed package fixtures | 0 | 30 | 38 | 42 named planning cases; final suite open |
| Separate reader tests | Existing evidence only | 8 scenarios | Same 8 scenarios | Same 8 plus new adapter coverage as designed |
| Schema | No impact | No impact | No container-only structural impact; accessibilityTarget meaning requires explicit review | No semantic redesign assumed; packaging and accessibility mapping unresolved |
| Validator work | NONE | A security component HIGH; B MEDIUM | A HIGH; B HIGH, semantic algorithms retained | Package/publication layer REWRITE; semantic algorithms retained |

B's **packaging-only** registry matrix is 103 unchanged and 10 affected (1 wording, 6 dependency, 3 native restatements). Dropping EPUB inheritance while retaining original bytes forces zero byte changes; the 70-envelope change applies to the separately stated new-marker scenario. An independent architecture is not sufficiently specified to produce a truthful exact final C requirement or modified-versus-replaced fixture count. Those unknowns are explicitly partitioned.

## Smallest next work package

Clarify the document-model/passive-profile/packaging-profile layers; explicitly state whole-publication EPUB conformance; adopt a dated reference/dependency policy; align SEC-001–008 with a uniform passive policy; separate reader authority from hardening limits; document unverified SEALED fallback; retain the internal EPUB marker and defer extension/MIME assignment. Close the external-error and parser/package coverage gaps with the enumerated targeted tests. The existing production-identifier RC gate remains separate and unchanged.

## Report map

| Decision/evidence | Reports |
| --- | --- |
| Final answers and choice | [Final recommendation, Q1–Q15](final_recommendation.md), [scored decision matrix](decision_matrix.md) |
| Options | [A](option_a_analysis.md), [B](option_b_analysis.md), [C](option_c_analysis.md) |
| Security | [Candidate passive profile](passive_content_profile.md), [threat model / ZIP attribution / renderer risks](threat_model.md), [reader security](reader_security_model.md) |
| Exact impacts | [113-row requirement matrix](requirement_impact_matrix.md), [validators](validator_impact.md), [70-row corpus matrix and new test list](corpus_impact.md), [accessibility/schema](accessibility_impact.md) |
| Boundary tradeoffs | [SEALED fallback](sealed_fallback_analysis.md), [MIME/extension identity](mime_identity_analysis.md), [standards versions, reuse and pinning](standards_reuse_analysis.md) |

Only audit reports/evidence are produced. The specification, registry, canonical schemas, validators, fixtures, format name and RC status are not changed. Final checks confirmed all 113 registry IDs appear exactly once in the impact matrix, all 70 fixture rows are present, all local report links resolve, and **265 tracked input files** have identical pre/post SHA-256 values. [Machine-readable audit evidence](audit_evidence.json) records the counts, scenario definitions and preservation hashes.

A — KEEP EPUB 3.3 AS THE FORMAT 0.1 NORMATIVE PACKAGING PROFILE
