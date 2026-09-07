# Option C — Fully independent package/publication model

**Reject Option C.** Its gate is conjunctive: A must fail a demonstrated SPD requirement, and B must remain harmfully constrained. Neither has been established. A permits the intended passive profile; B already permits explicit departures from OCF and OPF if needed. There is no evidence requiring a substantially new container, manifest, reading order or resource model.

The same XHTML/CSS/SVG/MathML/font/image rendering surface remains unless content technologies also change, which is outside this audit. A custom container does not by itself sandbox a renderer. It adds a new parser and publication-processing contract to review.

## What restarts, and what survives

Container identification, entry addressing, manifest rules, metadata, reading order, navigation integration, resource discovery, URL bases and error processing require architecture work. EPUB export would require an explicit mapping for those structures. Whole-package EPUBCheck and generic EPUB opening cease to be direct evidence for C inputs. Accessibility still needs a publication-scope adaptation.

The frozen semantic source of truth, identity/revision rules, effects/digest algorithms, SEALED currentness, mapping, annotation selectors and transactional semantics do not restart. Their input adapters and package bindings do. A new binary layout does not justify a new Node ID or digest design.

## Exact known impact versus unavailable precision

The registry review identifies **10 existing requirements affected even by B-min**. C also makes **4 more rows conditional** on whether ZIP entry semantics survive: SPD-BASE-003 and SPD-RES-003/004/006. Thus **99/113 have no identified architecture-text change, 10/113 have a known packaging/dependency restatement, and 4/113 are unresolved**. No current row is proven removable. This is an exact partition of the reviewed registry, not a prediction that C changes only fourteen checks. If C retains ordinary ZIP, those four can remain unchanged; if it does not, their ZIP references need replacement. Shared passive-profile changes are accounted for separately.

A final number of new C requirements cannot honestly be derived from a registry for an architecture that has not been designed. The audit can enumerate **12 proposed work groups**: B's eight explicit incorporation/validation groups plus container model, manifest model, reading-order model and resource-addressing model. Some may replace rather than add registry clauses once designed. These are a lower-bound planning list, not a fabricated exact specification delta.

All **70 test intents** remain useful. No existing full package can be certified as conforming to an undefined C serialization. For a distinct C serialization, all **70 need conversion or replacement**; allocation between those two categories is unresolved. Zero fixture mutations are performed here. **42 candidate new package tests** are enumerated in [corpus impact](corpus_impact.md), but the final C suite is open. All 70 historical full-package claims would require rerun against a C implementation.

Both validators have **REWRITE at the packaging/publication layer**, not a whole-validator rewrite: Validator A's package/discovery/OPF/EPUBCheck route and Validator B's package/epub/discovery adapters must be replaced. Semantic algorithms and strict JSON/schema infrastructure remain useful. See [validator impact](validator_impact.md).

A C RC is an architecture and implementation restart for the package/publication boundary, followed by independent validation and corpus convergence. It is not a justified pre-RC detour. The final recommendation's letter **C** means “insufficient evidence; run experiments”; that decision label is distinct from this fully independent architectural **Option C**, whose final-choice label would be **D**.
