# Option B — Independent packaging derived from EPUB/OCF

**Not recommended for 0.1.** B is technically viable, but no requirement has been demonstrated that both needs B now and outweighs its conformance/tooling/applicability cost. Compare B with **A using the identical passive profile**, not with unrestricted EPUB.

The technically honest description would be: **a semantic portable-document format using an OCF-derived container and constrained Web publication technologies**. It may still reuse OPF and EPUB navigation directly. It need not invent a new manifest.

## Security benefit test

| Claimed B advantage | Classification | Finding |
| --- | --- | --- |
| Disable JavaScript/event handlers/plugins | REAL BUT ALSO ACHIEVABLE UNDER A | Publication scripting is optional; SPD can prohibit its inclusion and execution |
| Disable automatic network and remote dependencies | REAL BUT ALSO ACHIEVABLE UNDER A | Package-local content and reader request denial do not violate EPUB |
| Harden ZIP names, duplicates and expansion | REAL BUT ALSO ACHIEVABLE UNDER A | These restrictions are already profiled or can be implemented independently of identity |
| Isolate XML/CSS/SVG/font/image parsers | NO MATERIAL DIFFERENCE | The same hostile parsers and renderers remain |
| Smaller validator without EPUBCheck | THEORETICAL | Removing a subprocess can reduce that component surface, but A can implement inherited checks independently; B needs replacement validation |
| Avoid opening in an EPUB application by default | IDENTITY/UX BENEFIT, NOT SECURITY | Association routing can reduce accidental fallback; it is neither a sandbox nor an access-control boundary |
| Guarantee no generic EPUB fallback | THEORETICAL | A non-EPUB marker discourages opening but cannot prevent sniffing, renaming, extraction or conversion |
| Own passive processing requirements | REAL BUT ALSO ACHIEVABLE UNDER A | File inheritance and SPD reader requirements are separate |
| Eliminate HTML/SVG/image/font vulnerabilities | NO MATERIAL DIFFERENCE | B-min uses the same content languages and decoders |
| Security advantage unavailable under A | REAL AND UNAVAILABLE UNDER A: **none demonstrated** | No inherited mandatory active behavior was found |

**B does not materially reduce attack surface with the same passive profile and implementation boundaries.** Reducing the implementation to the actually supported passive features is valuable under either option.

## Sovereignty benefit test

| Benefit | Reality | Worth abandoning strict EPUB conformance in 0.1? |
| --- | --- | --- |
| Different internal marker | Real exclusive freedom relative to unmodified OCF identification | No current requirement; external type registration is a separate issue |
| Own default application association | Useful UX | Not enough; A can use an alternate extension and explicit application routing |
| Own processing model | Useful | Mostly already achievable in SPD-aware A readers |
| No implied generic-reader validity | Real clarity of distribution contract | Valuable for sensitive records, but does not enforce safe handling; managed distribution also works under A |
| Remove mandatory OPF/nav/publication metadata | Real freedom if B elects to remove them | No demonstrated burden sufficient to justify replacements; B-min retains them |
| Different archive rules and future binary resource handling | Real freedom | Hypothetical future packaging need, not a 0.1 blocker |
| Independent evolution | Real ability to diverge | OPF/Web/Unicode dependencies remain; independence moves maintenance responsibility to SPD |

## Quantified consequences under B-min

The exact model is defined in [standards reuse](standards_reuse_analysis.md). It substitutes the internal marker while retaining the package structures and frozen semantic model.

| Area | Derived consequence |
| --- | --- |
| Existing requirements | 103 unchanged; 10 affected = 1 wording + 6 dependency + 3 SPD-native restatements; 0 removed; see all 113 rows |
| New requirements | 8 enumerated candidate incorporation/validation groups, not a claim that standards contain only eight obligations |
| Shared passive clarification | With that separate work included: 94 unchanged, 19 modified, 0 removed, 13 proposed new groups |
| Fixtures | All 70 envelopes modified, 0 test intents replaced; preserve deliberate negative mutations; all 70 rerun |
| New package fixtures | 38 proposed = 30 shared passive/boundary tests + 8 independent-package tests |
| Schemas | 0 structural changes forced by marker/OPF reuse; 1 accessibility field contract needs explicit review; see [accessibility impact](accessibility_impact.md) |
| Validator A | HIGH for package/publication validation and external-result authority; semantic algorithms retained |
| Validator B | HIGH for the same replacement responsibility; existing modular OPF adapter can be reused |
| EPUBCheck | Partial diagnostics, compatibility projection and EPUB export checking; not conformance authority for the independent input |
| Reader evidence | Historical EPUB readability still true for historical bytes; application acceptance of new B files untested |
| Specification burden | 24 responsibility groups need explicit disposition; 16 need an SPD profile and 1 new identity rule |

Numbers are conditional on B-min, not an invented universal cost of every possible B. Merely removing an EPUB requirement without changing bytes yields 70 unchanged fixture files and does not erase their EPUB behavior. B-min is used to make the requested independent-identity migration concrete without selecting a MIME name.

## Evidence retention and migration sequence if B were selected later

The 70 historical A/B/oracle results remain valid historical observations. Every underlying identity, digest, lifecycle, mapping and annotation algorithm remains reusable. But none of those results alone certifies a newly repackaged B file. A compatibility projection can recover an EPUB-checkable artifact; it must not be mislabeled a check of the independent source.

Before a B RC: agree an incorporation/exception table; revise Draft §§4–6, 8, 54–55, 58, 69 and affected profiles/traceability; settle the ten affected registry rows and eight addition groups; resolve the accessibilityTarget interpretation; replace complete-publication validation responsibility; regenerate all 70 packages while preserving negative mutations and rebind inventories/state; rerun independent validators and review the oracle; add B identification/OPF/nav/accessibility tests; and separately test reader/export acceptance. Shared passive security work remains required. This is a conditional work sequence, not an implementation authorization.

## Import/export burden

For B-min → EPUB: retain ZIP, OPF, nav, XHTML and resource paths; restore the EPUB marker, validate the imported publication clauses, and create a derivative artifact whose SPD integrity/seal claims are either recomputed through an authorized conversion or removed. **One marker substitution plus archive/inventory/state rebinding** is the minimal structural conversion; **zero manifest/nav/semantic-language conversions** are required by B-min itself. These counts increase if B uses its freedom to depart from those structures.

EPUB → B adds that envelope conversion to exactly the same passive-content adaptation and creation of SPD identities/revisions/integrity required by A. Creating a new filename is not a substitute for creating the SPD document state. Content that depends on scripts or network may need human-assisted semantic conversion in both cases.

B becomes attractive if a concrete future requirement conflicts with mandatory EPUB structure—such as a non-ZIP package or a distribution contract that expressly forbids EPUB identity—and the measured benefit exceeds this work. It does not pass that test today.
