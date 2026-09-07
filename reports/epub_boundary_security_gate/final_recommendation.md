# Final architecture recommendation

**Keep EPUB 3.3 as Format 0.1's normative packaging/publication profile. Confidence: HIGH in the architecture choice.** Proceed to targeted passive-profile clarification and verification before RC preparation is completed. This audit is not an RC release authorization and makes no implementation or normative-file changes.

No current frozen SPD requirement has been shown to need behavior that a strict EPUB subset cannot provide. EPUB scripting and remote-resource facilities are optional. A file-format inheritance requirement is different from granting publication content browser/application privileges. With the identical passive policy, B supplies no demonstrated exclusive security benefit. It does supply real identity and future-divergence freedom, but no Format 0.1 need currently outweighs the extra conformance, accessibility and implementation burden.

## Explicit answers Q1–Q15

**Q1 — What is Format 0.1 fundamentally?** Its architecture is a distinct semantic document model; its current serialization is an EPUB specialization with normative inherited constraints. Both statements matter. It is accurate to say that the model uses an EPUB-compatible packaging profile; inaccurate to imply the 0.1 package is already independent of EPUB publication conformance. The Draft's OCF-compatible/SHOULD-compatibility wording should be made explicit if A is adopted.

**Q2 — Can it remain fully EPUB 3.3 conforming while prohibiting scripting, automatic network, remote required resources and active capabilities?** Yes. EPUB §6.3.2.1 permits scripting and §3.6 permits certain remote resources; neither requires their presence. Removing optional content choices does not conflict with the package/resource/nav obligations in §2. SPD's reader can deny document network/execution authority separately. It must still preserve the other inherited content and publication constraints. [EPUB 3.3, 2026-01-13](https://www.w3.org/TR/2026/REC-epub-33-20260113/), [Reading Systems 3.3, 2024-10-17](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/).

**Q3 — Does B provide meaningful security unavailable under A?** None demonstrated. ZIP containment/limits, passive content, no network, decoder isolation and host-mediated links are achievable under A. Different dispatch/associations can improve UX but do not reduce the common XHTML/CSS/SVG/MathML/font/image attack surface by themselves.

**Q4 — What unavoidable constraints does EPUB impose?** The internal EPUB marker; OCF ZIP/path/reserved-file rules; OPF, manifest, spine and navigation; applicable resource/fallback and content-integration requirements; and maintenance of the inherited standards boundary. A cannot use another internal marker, non-OCF archive or incompatible publication structure while making the same conformance claim. Nor can it make ordinary EPUB readers verify SPD state.

**Q5 — What concrete interoperability benefits exist?** Reuse of a complete publication contract, whole-EPUB validation, existing parsing/navigation/metadata workflows and bounded observed semantic fallback. Historical tests opened 12/12 packages in epub.js, 12/12 in Foliate JS and 5/5 in calibre. These are 29 observations over historical packages, not 29 readers or a 70-fixture reader certification. Thorium and other Readium applications have no SPD-specific results in the reviewed repository. [Reader evidence](../epub_reader_interop.md).

**Q6 — What must B specify or maintain?** A complete incorporation/exception contract for 24 enumerated responsibility groups: ZIP/profile identity, discovery, OPF/manifest/resource/fallback rules, reading order/nav, URL/XML/content integration, metadata/accessibility, processor behavior and validation/versioning. Reusing OPF is reasonable; merely calling it “OPF-like” is insufficient. Six groups can be directly referenced, sixteen need an SPD-specific application profile, one identity group needs replacement, and one unused optional-feature group can be omitted.

**Q7 — Can EPUB Accessibility 1.1 be reused cleanly under B?** Its substance and metadata syntax can be reused, particularly if OPF remains. An unqualified conformance claim for a non-EPUB publication is not a clean direct adoption; B needs a publication-scope/applicability/reporting mapping while keeping WCAG 2.2 AA. ACC-004 and the meaning of the EPUB-named accessibilityTarget field require explicit attention. [Accessibility impact](accessibility_impact.md).

**Q8 — Is generic fallback unacceptable for SEALED documents?** It is unacceptable **as evidence of verified SEALED/current fixed presentation**, especially in sensitive workflows. It is still useful as semantic reading. Preserve authoritative semantic XHTML; do not relabel it non-authoritative simply because F8 exists. Require truthful state-aware UI and managed-viewer or labeled-export policies where verified representation matters. A new marker alone does not enforce that policy. [SEALED analysis](sealed_fallback_analysis.md).

**Q9 — Does 0.1 need its own MIME type now?** No demonstrated requirement. Retain the EPUB internal marker under A. Replacing that marker leaves unchanged OCF conformance; registering an external specialized type over EPUB-conforming bytes is a separate possible design, not automatically forbidden by A and not decided here. [MIME analysis](mime_identity_analysis.md).

**Q10 — Does it need its own extension now?** No. A distinct suffix can route to SPD-aware software without changing internal EPUB bytes, but reader acceptance is untested and no security boundary follows from it. Leave the extension unassigned in this audit and retain the current corpus convention.

**Q11 — Separate semantic model from packaging?** Yes, conceptually and in the input contracts: document model, passive content profile, packaging profile. Use the name “SPD EPUB-Compatible Packaging Profile 0.1” if adopted in later editing. Keep one 0.1 conformance bundle; independent wire-level version negotiation is unnecessary now. Names alone do not eliminate discovery/path/inventory coupling.

**Q12 — Define a normative Passive Content Profile regardless of packaging?** Yes. Align existing profiles and weak “not required” wording; specify file prohibitions, reader authority denial and operational hardening separately. Preserve ordinary CSS/static SVG/MathML and inert semantics instead of inventing new languages. The five candidate groups P1–P5 are proposed, not enacted. [Passive profile](passive_content_profile.md).

**Q13 — Which current requirements change under B?** In B-min: BASE-001/002/005/006, SEM-002/003, ACC-004, CAP-003, DISC-001/002: **10 of 113**. The partition is **103 unchanged, 1 wording-only, 6 dependency changes, 3 native restatements, 0 removed**. Eight new grouped obligations are enumerated. With the identical shared passive clarification included, **19 existing rows change, 94 remain unchanged and 13 new groups are proposed**. [Every-row matrix](requirement_impact_matrix.md).

**Q14 — How much 70-fixture evidence survives B?** All 70 historical results remain valid historical observations and all 70 semantic test intents remain useful. If B retains current bytes, no fixture byte changes are forced merely by dropping inheritance. Under B-min's new internal marker, **70/70 envelopes and integrity bindings change**, while the marker's affects array is empty in all 70, preserving semantic/rendition projections for that change alone. **All 70 new inputs require rerun**; no old full-file result certifies a converted file. Direct EPUBCheck-source authority is lost, component/export checking survives. [Corpus impact](corpus_impact.md).

**Q15 — Which is easiest for independent third parties?** A. It gives readers, validators and editors a complete existing publication contract plus the SPD overlay, with mature libraries and conformance tools. B preserves useful components but adds integration/exception checking. C forces new publication machinery. This preference remains after discounting the cost already invested in the current corpus.

## Smallest proposed pre-RC package

This is a plan for a later authorized change, **not changes made by this audit**.

| Topic | Proposed action | Affected location / validation |
| --- | --- | --- |
| Conceptual model | State the three-layer architecture and honest semantic-versus-serialization identity | Draft §§1, 4–6; no schema field required |
| Packaging profile | Explicitly require complete EPUB publication conformance and retain current OPF/nav/discovery | BASE-001/002; Draft §§4–6; OCF/XHTML profiles |
| Exact pin | Propose EPUB 3.3 Recommendation 2026-01-13, RS 3.3 2024-10-17 and dated accessibility/CSS/SVG/MathML references; freeze living-reference policy | Dependency ledger; reconcile EPUBCheck 5.3.0 rule support before asserting the pin is fully validated |
| Passive profile | Align SEC-001–008; introduce P1–P3 with no application execution, no automatic requests, inert controls and complete static meaning | Draft §7 and XHTML/CSS/SVG profiles; 30 targeted package cases enumerated |
| Reader security | Adopt P4 and separately publish sandbox/budget guidance; do not standardize arbitrary numeric ceilings | 8 runtime scenarios R1–R8; cannot be proved by validators alone |
| SEALED fallback | Clarify BASE-004 and P5: generic semantic reading is unverified, no implied current fixed/seal/authentication claim | State-aware UI/distribution policy; no automatic rewriting of existing SEALED packages |
| MIME/extension | Keep internal EPUB marker, describe detection and defer new names | No registration, renaming or corpus identity migration in this package |

The explicit A proposal touches **11 existing requirement rows**, adds **5 grouped obligations**, and plans to retain the **70 existing fixture byte sequences**, adding **30 package cases** plus **8 separate reader scenarios**. Exact future diagnostic outputs require rerun. This plan excludes the separately required production-identifier migration under DISC-004; that existing gate must still be satisfied before RC.

## Additional validation work required before an unconditional RC gate

The baseline's zero reported blockers and 70/70 convergence remain true historical evidence. This architecture audit identifies further **coverage/contract questions** that the old corpus does not settle:

1. Ensure all applicable inherited EPUB errors prevent an unconditional Base PASS, including errors outside the seven guarded attribution mappings. The inspected corpus has no Base-PASS/EPUBCheck-FAIL case, but both adapters have an unmapped-error acceptance route.
2. Complete grammar/context-aware passive validation. A's regex-based security function and B's incomplete inline/nested-resource coverage must not be described as an exhaustive security boundary.
3. Verify decoded-name collisions, symlink/device handling, ZIP overlap/header consistency and actual expansion budgets; separate format errors from operational limits. Test the static presentation, link mediation and truthful SEALED UI in an actual reader.

These findings apply to A and B. They justify targeted pre-RC work, not an independent container. The original freeze is not rewritten or invalidated by this report; new claims require new evidence. No arbitrary code, corpus or specification fix was made here.

## RC impact of alternatives

**A:** proceed now into that focused clarification/verification work; preserve architecture and semantic evidence. Validator A's security component needs substantial work (HIGH in that component), while B's common passive work is MEDIUM. Both retain their semantic algorithms.

**B:** first settle the incorporation contract and accessibility interpretation; migrate the ten packaging-sensitive rows and eight new groups, replace source-level inherited validation authority, convert/rebind all 70 B-min packages, extend the corpus, and establish a new independent convergence freeze. Both validators have HIGH integration burden. Marker-only packaging requires no structural schema rewrite; the accessibilityTarget contract remains a real review item.

**C:** reject. Package/publication architecture and validation adapters restart; the frozen semantic model need not. Ten registry rows are known affected and four more ZIP-related rows conditional, leaving 99 with no identified packaging-text change. New requirement count and allocation of the 70 converted/replaced envelopes cannot be exact without inventing C. Twelve work groups and 42 test planning cases identify a floor, not a finished design.

## Confidence and strongest counterarguments

**Confidence: HIGH in choosing A; MEDIUM in future implementation effort estimates.** Unspecified alternative design choices are disclosed rather than assigned invented precision.

Three strongest supporting pieces of evidence:

1. The standards' optional scripting/remote provisions establish that the intended passive subset is conforming; no compulsory active behavior conflicts with SPD.
2. Existing profiles already express local-resource/passive restrictions, and independent A/B/oracle results agree on 70 cases with all 140 EPUBCheck executions recorded. That demonstrates a workable semantic model on the reused structures, within the measured coverage.
3. Historical reader observations show a real semantic access path, and direct EPUB publication/accessibility tooling reduces the burden on an independent implementer.

Three strongest arguments against A:

1. It cannot force generic readers to verify SEALED/current fixed state; sensitive-document distribution needs an explicit policy and trusted viewer.
2. The mandatory internal identity and publication structure impose genuine limits if a future SPD requirement needs another envelope, no EPUB navigation or no EPUB identity.
3. EPUB's broad/transitive standards and current validator coverage gaps mean inheritance is not effortless: a dated dependency ledger, complete conformance gating and stronger passive checks remain necessary.

The weighted matrix (A **198/230**, B **144/230**, C **100/230**) makes those tradeoffs visible but does not replace the requirement gate. No present requirement passes the test for departing from A. No further packaging-choice experiment is needed to establish that conclusion; targeted tests are needed to substantiate the ensuing security/RC claims.

A — KEEP EPUB 3.3 AS THE FORMAT 0.1 NORMATIVE PACKAGING PROFILE
