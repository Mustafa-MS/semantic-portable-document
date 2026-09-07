# SEALED fallback and ordinary EPUB reading

**Generic semantic fallback is useful, but it is not a verified SEALED/fixed presentation.** Unqualified reliance on it for integrity-sensitive records is unacceptable. This is a representation policy problem; it is not evidence that EPUB requires executable behavior or that a different extension enforces a seal.

## D / R8 / F8 example

Document D, Revision R8 is SEALED with current fixed rendition F8. An SPD processor verifies the inventory, semantic/rendering projections, state descriptor and F8 bindings; if Mapping is claimed, it checks those bindings too. A generic EPUB reader instead displays the XHTML spine. It may reflow text, change fonts, use another MathML renderer, ignore F8, and show no verification result.

The displayed XHTML remains the authoritative **semantic** representation under the frozen model. It must not be declared “non-canonical semantic content” merely because a fixed rendition exists. What is absent is verification of the claimed state and the promised fixed presentation. A semantic-only SEALED revision is also valid, so “SEALED means show a PDF” would directly contradict the frozen model.

| Risk | Finding |
| --- | --- |
| Semantic risk | Conditional: semantic reading is legitimate, but incomplete rendering, unsupported resources or hidden layout-dependent meaning may mislead. Valid markup does not prove faithful rendering. |
| Legal/representation risk | Real possibility of reliance on an unverified or differently presented record. No claim about legal enforceability is made here. |
| User-experience risk | Directly observed: historical readers displayed semantic content without surfacing SPD state or fixed PDF. |
| No meaningful risk | Reasonable only for low-stakes reading where no verified/fixed claim is implied. Not a universal conclusion. |

[Repository reader evidence](../epub_reader_interop.md) supports observed semantic display/non-activation, not a comprehensive sealed-record safety conclusion. The [frozen Draft §§26–30](../../spec/FORMAT_0.1_DRAFT.md) explicitly separates currentness, integrity and authentication.

## Fallback by document class

| Class | Value of generic fallback | Main condition/risk |
| --- | --- | --- |
| Books | Major benefit | Reflowable reading is usually the objective; no implied seal verification |
| Reports | Major benefit for reading; conditional for formal submission | Page references, charts and fixed layout may matter for the official version |
| Scientific documents | Major semantic access benefit, conditional fixed-fidelity benefit | Equations/figures/citations and page-based references need fidelity checks |
| Contracts | Potentially dangerous if presented as verified executed copy | Users may infer authentication, exact pagination or signatures absent from the generic view |
| Medical documents | Potentially dangerous for decisions relying on verified state or presentation | Missing context/layout or stale/unverified content may change interpretation |
| Official records | Potentially dangerous for authoritative-copy claims | Generic reading must not imply provenance/authentication/currentness |
| Certificates | Minor reading benefit; potentially dangerous verification confusion | Visual badge/seal can be mimicked; digest integrity is not issuer authentication |
| Forms | Minor for reading preserved values; dangerous for functional completion | Generic controls may appear editable without SPD transaction or submission semantics |

These are use-case judgments, not claims of legal or clinical sufficiency. No document-class taxonomy or new lifecycle state is proposed.

## Policy choices

| Policy | Advantages | Limitations/cost | Recommendation |
| --- | --- | --- | --- |
| Label semantic fallback as an **unverified reading view**, not a verified fixed view | Preserves semantic authority and honest status | Generic readers cannot be forced to show trusted UI | Adopt for SPD-aware processors and distribution claims |
| Embedded visible notice | Can appear in generic readers; accessible prose is portable | Author can spoof it; can be hidden/skipped; adding it changes document bytes/meaning and may require a revision | Consider for sensitive distribution, authored before sealing; never retrofit silently |
| Navigation notice/landmark | Discoverable, less intrusive | Users/readers may skip it; no proof of verification | Supplemental aid, not the enforcement mechanism |
| Prohibit generic-reader compatibility for a SEALED class | Clear managed-workflow instruction | A byte-valid EPUB cannot stop generic opening; breaking EPUB conformance solely for SEALED creates another packaging class | Do not add such a package split in 0.1 |
| Require SPD-aware viewer in a managed distribution workflow | Trusted state/fixed UI and capability handling | Viewer availability/deployment cost; cannot control extracted or forwarded copies | Appropriate where verified representation is required |
| Separate export-to-EPUB workflow | Makes derivative reading copy explicit, can omit misleading verification claims | Extra artifact, provenance/version management; export must preserve semantic meaning and remain accessible | Useful for high-stakes distribution, available under A and B |
| Independent B marker/extension | Reduces accidental default EPUB opening | Sniffing/extraction/conversion remain possible; does not validate the seal | Insufficient justification alone |

## Minimal policy to take into pre-RC work

Preserve the frozen semantic/fixed distinction. State that ordinary EPUB compatibility promises **semantic readability where supported**, not verification of SPD state, exact fixed rendering, identity authentication or editing safety. An SPD processor must expose verified status outside author content and must not assert it for a generic/unverified view. Sensitive workflows should require an SPD-aware viewer or distribute an explicitly labeled derivative EPUB reading copy.

Do not force an embedded notice into every existing SEALED package during clarification. The task's no-modification rule remains in force; adding notices would have the existing revision/inventory/seal consequences. Do not invent a digital-signature guarantee or call the fixed rendition the sole semantic authority.

A cannot guarantee that generic readers enforce this policy. B cannot guarantee that arbitrary applications refuse its content either. If a future requirement literally demands prevention of all unauthorized generic viewing, neither ZIP-based A nor B supplies that access control; it would be a different requirement and cannot be inferred from SEALED.
