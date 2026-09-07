# Decision matrix

Scores are architecture judgments on **1–5**, with **5 favorable**. A/B/C are the three architectures, not the final decision-letter labels. Security uses the **identical candidate passive policy** for all options. Scores are not measured vulnerability probabilities or a substitute for the governing requirement test.

Independent third-party implementation, security and SEALED correctness receive high weight. Identity and preservation of existing work receive low weight so that the result is not determined by branding or sunk cost. Scores describe the architecture after its stated integration work, not a claim that the current validators already fully enforce the proposal.

| Criterion | Weight | A score and justification | B score and justification | C score and justification |
| --- | ---: | --- | --- | --- |
| Security | 5 | **4** — Same passive restrictions and sandbox can deny active/network authority. | **4** — Identical profile gives no exclusive security benefit. | **4** — Can impose the same policy; independent packaging alone adds no safety. |
| Determinism | 3 | **4** — Local inputs/stable presentation help; engine/font variation remains. | **4** — Same content and snapshots have the same remaining variation. | **4** — New container does not make Web layout deterministic. |
| Standards reuse | 4 | **5** — Retains a complete publication contract and its ecosystem. | **4** — Retains components but owns incorporation/applicability. | **2** — Keeps media standards but replaces publication structure. |
| Implementation simplicity | 4 | **4** — Package libraries/checkers exist; SPD overlay and hardening still needed. | **3** — Reuse remains, but explicit imported-rule integration expands. | **1** — New container/manifest/read-order implementations are required. |
| Interoperability | 4 | **5** — Conforming EPUB serialization plus bounded observed reader evidence. | **2** — No guaranteed direct EPUB acceptance; projections/exports required. | **1** — Only new-format implementations can rely on the package contract. |
| Accessibility | 4 | **5** — Current EPUB Accessibility plus WCAG contract fits directly. | **3** — Content reuse survives; publication scope/metadata claims need mapping. | **2** — Must bind accessibility to new manifest/navigation semantics. |
| Existing tooling | 3 | **5** — Whole-publication EPUBCheck and existing content tools remain. | **3** — Component tools and export checks remain; source check authority changes. | **1** — Most publication tools need new adapters. |
| Fallback readability | 2 | **5** — Historical generic EPUB semantic reading is observed, with limitations. | **2** — Possible after conversion or permissive sniffing, not promised for B sources. | **1** — No established reader path for a new serialization. |
| SEALED-document correctness | 5 | **3** — SPD-aware checks work; generic views cannot verify state/fixed representation. | **3** — Routing improves but no inherent verification or anti-fallback enforcement. | **3** — New identity also cannot prove semantics, authenticity or safe display. |
| Format identity | 1 | **2** — EPUB internal identity is mandatory and requires careful explanation. | **5** — Independent internal identity is available. | **5** — Independent identity is fully controlled. |
| Future evolution | 2 | **3** — Mandatory EPUB package/content rules constrain future incompatible changes. | **4** — Explicit exceptions permit divergence while reusing mature structures. | **5** — Maximum structural freedom, with implementation cost counted elsewhere. |
| Validator burden | 3 | **4** — Keep inherited checker; current passive/completeness gaps need repair. | **2** — Own imported publication checks and revise external-result authority. | **1** — New package/publication validator layer required. |
| Corpus migration cost | 1 | **5** — Retain all current package bytes for this clarification plan. | **2** — B-min changes all 70 envelopes/bindings, retaining test intents. | **1** — All 70 envelope adaptations unresolved pending design. |
| Third-party implementability | 5 | **5** — Clear existing publication standard, libraries, tests and checker reduce startup work. | **3** — Can reuse OPF but must implement SPD's exception/application contract. | **1** — Must learn and implement new publication rules with no mature package tooling. |

Total weight: **46**. Weighted totals: **A 198/230, B 144/230, C 100/230**. Weighted means: A 4.30, B 3.13, C 2.17. These totals are arithmetic over the table, not empirical precision.

## Tradeoffs that the total must not hide

A's weakest areas are media identity, long-term freedom to diverge and generic SEALED fallback. The semantic model can stay conceptually independent, but its 0.1 files remain EPUB-constrained. A trusted state-aware workflow is still needed for verification-sensitive use.

B's real advantages are internal identity and freedom to replace mandatory EPUB rules. It preserves more mature structure than C and would be the first independent packaging option to consider if a concrete EPUB conflict emerged. It does not score higher in security or SEALED correctness merely because a marker changes. The accessibility mapping and new inherited-rule checking are substantive costs.

C's freedom is real, but no demonstrated requirement needs it. It loses the most implementer/tooling leverage without eliminating the common Web renderer surface.

## Sensitivity and hard gate

Ignoring the low-weight corpus-migration criterion entirely does not change A's lead. Giving identity and future evolution much higher weights can narrow the result, but does not supply the **missing mandatory requirement** that A cannot satisfy. A new requirement that forbids EPUB internal identity or requires a non-ZIP container would change the hard-gate evidence; that should trigger a future review rather than an automatic score-based preference now.

The governing test decides this audit: **no significant current SPD requirement has been shown to require leaving a strict EPUB 3.3 profile**. B therefore fails the departure gate. C also fails because neither A's inadequacy nor B's harmful structural constraint has been established.

Evidence behind the judgments is in [A analysis](option_a_analysis.md), [B analysis](option_b_analysis.md), [C analysis](option_c_analysis.md), [threat model](threat_model.md), [accessibility impact](accessibility_impact.md), [validator impact](validator_impact.md), and [corpus impact](corpus_impact.md).

