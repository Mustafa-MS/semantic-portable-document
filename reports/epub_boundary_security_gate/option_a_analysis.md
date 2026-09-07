# Option A — EPUB-compatible packaging

**Recommended for Format 0.1, with targeted pre-RC clarifications and verification.** Strict EPUB publication conformance can coexist with the intended passive model. It is not necessary to run any document script, fetch a remote resource, or grant document-originated device/storage authority to create or read this subset. See the exact [conformance argument and source editions](standards_reuse_analysis.md).

## What A actually promises

The SPD semantic model adds authority, persistent identity, lifecycle and correspondence beyond EPUB. Its 0.1 serialization is nevertheless an EPUB specialization: a conforming package must also satisfy the pinned EPUB publication rules. Calling EPUB merely an incidental source of technology would be inaccurate. The technically honest description is: **a semantic portable-document format whose 0.1 packaging profile is a strict conforming subset of a dated EPUB 3.3 baseline**.

The current [Draft §§5–7](../../spec/FORMAT_0.1_DRAFT.md) does not express that boundary as cleanly as the task premise: §5 says OCF-compatible; §6 says EPUB usability SHOULD be retained where practical. The [OCF](../../spec/profiles/ocf-profile.md), [XHTML](../../spec/profiles/xhtml-profile.md), and [CSS](../../spec/profiles/css-profile.md) profiles supply broader normative inheritance. A should make whole-publication conformance explicit, rather than silently upgrading a SHOULD in this audit. Similarly, several SEC registry entries say “does not require”; the stronger no-active/no-automatic-fetch proposal is partly clarification and partly a genuine restriction.

## Concrete advantages

Existing ZIP/XML/content libraries and whole-publication EPUB validation remain useful. Independent implementers can combine existing publication handling with SPD checks rather than reconstruct publication rules from an exception list. Navigation, resource relationship conventions and accessibility applicability have established meanings. The 70-case convergence remains evidence about the same serialization. Older reader tests provide bounded evidence of semantic fallback, described below.

**EPUBCheck remains the project's external validation dependency, not the definition of conformance.** No registry row names a particular executable as the only legitimate way to conform. The frozen validators operationally require EPUBCheck to establish complete Base results; the normative dependency is EPUB's requirements. A future independent validator may implement those requirements another way. Current integration also needs a completeness review: unmatched EPUBCheck errors remain metadata rather than automatically preventing Base PASS. [Validator impact](validator_impact.md) identifies the exact code paths and attribution set.

## Concrete costs and constraints

| Constraint | Cost to SPD | Can a profile remove it while retaining A? |
| --- | --- | --- |
| Mandatory internal EPUB MIME marker and ZIP/OCF rules | A distinct internal SPD marker, different compression method, or a non-ZIP envelope is unavailable in profile 0.1 | No; future packaging change would leave A |
| OPF, manifest, spine and EPUB navigation | Requires publication metadata and navigation even for short forms or certificates | No removal of mandatory inherited structure; simple instances can minimize overhead |
| Core/foreign resource and fallback rules | New authoritative content media may need an EPUB-compatible route/fallback | No blanket exemption; current XHTML authority and auxiliary fixed resources fit |
| META-INF and resource placement | SPD controls must retain permitted extension placement and cannot become ordinary referenced publication resources there | Must respect placement; descriptors already use container links |
| EPUB's HTML/MathML/SVG constraints | A future non-EPUB host integration may not fit | Existing SPD requirements show no such contradiction |
| Generic reader expectations | A reader may reflow, override fonts, ignore SPD state, or offer editing/conversion | Cannot make generic readers implement SPD semantics |
| SEALED fallback | A reader can display semantic content without verifying R8/F8/state bindings | Policy and trusted reader UI can manage distribution; cannot force ordinary readers to verify |
| Dependency maintenance | Dated core plus transitive living references require deliberate tracking | Cannot remove; B also retains most of it |
| Conceptual complexity | Implementers must distinguish “EPUB-valid,” “SPD-valid,” and “verified current fixed rendition” | Clear layering and status language reduce confusion |
| Format identity | Generic file associations say EPUB; people may infer SPD is just an ebook convention | Explain the model and packaging honestly; branding alone is not a packaging requirement |

These are real constraints, not zero-cost reuse. None currently prevents the frozen document model or identical passive security policy.

## Reader evidence, with limits

| Reader/system | Existing repository observation | What is not established |
| --- | --- | --- |
| epub.js 0.3.93, Chromium/Playwright | 12/12 historical T01–T12 packages opened; semantic/navigation/resource observations recorded | No 70-fixture trial, comprehensive accessibility audit, or SPD lifecycle support |
| Foliate **JS**, commit `78914aef4466eb960965702401634c2cb348e9b1`, Chromium/Playwright | 12/12 historical packages opened | Not evidence for every Foliate desktop release or engine |
| calibre E-book viewer 9.14, Qt WebEngine | 5/5 historical packages T04/T05/T08/T09/T12 opened; figures, MathML, Arabic/mixed bidi and supplemental-resource behavior observed | Not general current-version certification or verified SEALED behavior |
| Thorium | No SPD-specific execution evidence found in the reviewed repository | Do not claim tested compatibility |
| Other Readium-based systems | No SPD-specific execution evidence found | Toolkit adoption alone does not prove an application's behavior |

Sources: [reader report](../epub_reader_interop.md), [epub.js results](../epubjs_reader_results.json), [Foliate JS results](../foliate_reader_results.json), [calibre results](../calibre_reader_results.json). The earlier [compatibility report](../epub_compatibility.md) explicitly records NOT RUN at an earlier stage; it is not the current convergence evidence. No readers were executed during this audit. The old report's description of fallback as “safe” is too broad for integrity-sensitive use: it only establishes the observed non-activation/readability behavior, not authenticity or canonical fixed display.

## Future evolution, import and export

Additional collaboration metadata, annotations, signature artifacts and new fixed media can plausibly remain supplementary resources with SPD capability semantics. A already separates fixed output from the authoritative spine. Stronger **SPD-aware** sealing does not conflict with that. Requiring every generic EPUB reader to enforce a seal, eliminating all semantic fallback, changing the archive algorithm, removing the XHTML/nav spine, or replacing the mandatory internal marker would conflict. No such mandatory Format 0.1 requirement is established.

For A → ordinary EPUB, structural conversion is **zero** for an already conforming passive package. An intentionally simplified export may remove SPD controls/metadata and unneeded fixed/mapping resources, preserve valid manifest/nav relations, and omit any claim that the result retains the SPD seal. Removing arbitrary extensions without updating references is not safe. Export is a new artifact; do not rewrite the source SEALED file.

For EPUB → A, retain an already compatible container/OPF/nav where possible, normalize unsafe package arrangements through an explicit conversion, remove or replace active/remote dependencies, and preserve meaning. Independently create or map Document/Revision/Node identities, inventory/effects/digests, state and capability claims. Ordinary EPUB validity does not supply these SPD facts. Lossless import of arbitrary interactive EPUB is not promised.

## RC consequence

Proceed into the small clarification/verification work package in [final recommendation](final_recommendation.md), **not directly to RC1**. Packaging-only A changes 0 of 113 requirements and 0 of 70 fixture files. The explicit proposed clarification package touches 11 existing requirements and proposes 5 grouped additions, with 30 new package fixtures and 8 reader test scenarios. Counts are enumerated, not predicted implementation effort. Current conformance/security completeness gaps and the existing stable-identifier release gate must be closed before a new freeze.
