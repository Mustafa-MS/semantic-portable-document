# Candidate SPD Passive Content Profile

**Proposal only; not an amendment to the frozen Draft.** The same profile is used for Options A and B. Its purpose is to make document-originated authority explicit while retaining useful declarative content. Conformance of a file does not prove safety of a reader.

## Candidate normative model

The following are five proposed grouped additions, labeled P1–P5 only for this report. They are not allocated registry IDs.

1. **P1 — Passive data.** SPD content SHALL be treated as untrusted document data. A Base document SHALL NOT supply executable application behavior, and a Base processor SHALL NOT execute document-supplied code. Host/editor application code is outside the document and has a separate trust boundary.
2. **P2 — Inert content controls.** Base SHALL NOT contain form submission, embedded browsing contexts, plugin/object execution, automatic navigation, base-URL overrides, or document-originated permission mechanisms. Preserved controls SHALL be inert, labeled representations whose values/meaning remain semantically available. Interactive Forms/Interactive behavior requires a future capability; this proposal does not design it.
3. **P3 — Stable passive presentation.** Base meaning SHALL be available in a static state without autoplay, animation or interactive state changes. A Base presentation SHALL suppress document-driven animation/transition/autoplay and preserve a complete static presentation. Optional time-dependent declarations MAY be retained only with a complete static state; they SHALL NOT run in Base. SEALED fixed output retains the existing stable-snapshot rule.
4. **P4 — Reader authority.** An SPD reader SHALL deny publication-originated network, filesystem, device-permission, shared-cookie and persistent-Web-storage authority. Resource resolution SHALL use only verified package entries. External hyperlinks MAY be activated only by an intentional user action through host mediation, without automatic tracking requests or document access to the destination context. Host-owned imports, exports and user preferences are separate operations.
5. **P5 — Verification representation.** A processor SHALL distinguish displayed semantic content, declared SEALED state, verified current state, and any verified current fixed rendition. A generic or unverified view SHALL NOT be represented by an SPD processor as a verified sealed/fixed view. No hash-only seal SHALL be represented as signer authentication.

The eight existing SEC rows would be aligned with these principles: SEC-001/002 prohibit occurrence/execution rather than merely dependence; SEC-003 prohibits automatic requests; SEC-004/005/006 apply to decorative as well as required fetched resources; SEC-007 covers every SVG embedding context and static operation; SEC-008 defines transitive package-local resource resolution across all rendered content. BASE-001/002 state complete dated EPUB inheritance; BASE-004 states the fallback contract. These are the **11 proposed modified rows**, not eleven changes already made.

## Capability policy

Each row supplies the requested primary classification. Where a file prohibition also needs runtime enforcement, both enforcement layers are identified. “SAFE TO ALLOW” means within this profile and implementation limits, not that a decoder cannot have bugs.

| Technology/Capability | Base policy | Reason | Format rule or reader rule |
| --- | --- | --- | --- |
| JavaScript and executable macros | PROHIBIT IN BASE | No document application code | File: no script/executable content; reader: execution disabled |
| Inline event handlers, executable URLs | PROHIBIT IN BASE | Alternate routes to execution | File, after namespace-aware parsing and URL interpretation; reader backstop |
| HTML script data blocks | PROHIBIT IN BASE | Simpler existing script-element prohibition; use existing JSON resource mechanisms | File; data blocks are not executable in HTML/EPUB, so this is a profile simplicity choice |
| iframe, including srcdoc | PROHIBIT IN BASE | Adds a document-created browsing context even if ostensibly local | File; reader creates no document-directed frames |
| object/embed and plugins | PROHIBIT IN BASE | Type-dispatch and embedded-handler surface; static alternatives already exist | File; no renderer/plugin delegation from content |
| Service workers | PROHIBIT IN BASE | Persistent executable request interception | File dependencies prohibited; reader registration disabled |
| Automatic network access | PROHIBIT IN BASE | Privacy, nondeterminism and undeclared external dependencies | File: no fetch-triggering remote references; reader: deny requests |
| Remote required resources | PROHIBIT IN BASE | Meaning/rendering must be available offline | File, including transitive dependencies |
| Remote stylesheets | PROHIBIT IN BASE | CSS may fetch further assets or change presentation | File plus reader request denial |
| Remote fonts | PROHIBIT IN BASE | Font fetching and nondeterministic fallback | File plus reader request denial |
| Automatic external image loading | PROHIBIT IN BASE | Tracking/decode surface, even for a decorative pixel | File plus reader request denial |
| Packaged fonts/images | SAFE TO ALLOW | Necessary declarative resources | File inventory/local resolution; reader sandbox/limits |
| SVG scripts/events/active execution | PROHIBIT IN BASE | Same execution risk as HTML | File in standalone, inline, referenced and nested contexts; reader backstop |
| SVG foreignObject | PROHIBIT IN BASE | Extra host-language context; static alternatives suffice for 0.1 | File; already prohibited by local SVG profile |
| SVG cross-document packaged references | SAFE TO ALLOW, constrained | Enables reusable symbols/images/fonts without network | File: local safe targets, inventory and terminating references; reader local resolver |
| SVG remote references | PROHIBIT IN BASE | Package containment must propagate through SVG | File and reader |
| CSS automatic external fetching | PROHIBIT IN BASE | Script-free CSS can issue requests | File and reader, including imports, fonts, masks, cursors and filters |
| Form submission | DEFER TO FUTURE CAPABILITY | Submission/edits need explicit transactional and privacy semantics | No form/submission behavior in Base; future Forms capability |
| Inert preserved input/button values | SAFE TO ALLOW, constrained | Keeps native labels/values useful without enabling interaction | File: disabled controls, no form owner/action or activation bindings; reader inert |
| Automatic navigation/redirect | PROHIBIT IN BASE | Can escape the intended document view without user intent | File: no refresh/automatic redirect; reader blocks navigation |
| User-activated external hyperlink | ALLOW ONLY WITH EXPLICIT USER ACTION | A chosen destination differs from automatic document fetching | File: permitted hyperlink role; reader host mediation |
| Link ping, prefetch, preload of remote data, DNS preconnect | PROHIBIT IN BASE | Can contact a host without following a link | File declarations prohibited; reader network backstop |
| Local audio/video playback | ALLOW ONLY WITH EXPLICIT USER ACTION | Declarative local media can supplement passive meaning | File: packaged source/poster/tracks, no autoplay, equivalent semantics; reader controls |
| Media autoplay | PROHIBIT IN BASE | Unsolicited output/time-dependent presentation | File attribute/behavior prohibition and reader suppression |
| CSS/SVG animation and transitions | DEFER TO FUTURE CAPABILITY for execution | Primarily determinism/performance/accessibility concerns | Optional inert declarations may remain; reader suppresses; complete static meaning required |
| Document-originated permission requests | IMPLEMENTATION SANDBOX REQUIREMENT | APIs are runtime authority, not reliably detectable from a file | Reader exposes no permission-grant path to the document |
| Local filesystem access | IMPLEMENTATION SANDBOX REQUIREMENT | Package-local references must not become OS paths | Reader denies file/UNC/drive access; host mediates explicit import/export |
| Camera | IMPLEMENTATION SANDBOX REQUIREMENT | Not needed for passive reading | Reader denies document access |
| Microphone | IMPLEMENTATION SANDBOX REQUIREMENT | Not needed for passive reading | Reader denies document access |
| Location | IMPLEMENTATION SANDBOX REQUIREMENT | Not needed for passive reading | Reader denies document access |
| Persistent Web storage | IMPLEMENTATION SANDBOX REQUIREMENT | Prevent tracking, cross-document state and persistent application behavior | Reader disables document storage; host may save reading position separately |
| Cookies | IMPLEMENTATION SANDBOX REQUIREMENT | Prevent ambient credentials/tracking | Reader has no shared cookie jar and no publication cookies |
| Host reading preferences, temporary cache | SAFE TO ALLOW | Useful application data controlled by the host | Reader-private bounded storage, separate from document-originated Web APIs |

## XHTML decisions

The current [XHTML profile](../../spec/profiles/xhtml-profile.md) is an open set of harmless EPUB HTML, not a narrow element allow-list. Preserve that approach.

| Construct | Placement | Candidate treatment and rationale |
| --- | --- | --- |
| script | Always prohibited in the passive profile | Includes inert data blocks for an unambiguous file rule; this does not claim all script elements execute |
| iframe | Always prohibited in the passive profile | Including nested local documents and srcdoc; host-owned renderer frames are different |
| object, embed | Always prohibited in the passive profile | Even a nominally static object can dispatch another handler; use img/SVG or separately mediated resource viewing |
| form | Future Forms capability | Prohibit form containers in Base, including nominally non-submitting forms; EPUB labels form-containing XHTML scripted even without JavaScript |
| input | Base only as inert preserved control; functional input deferred to Forms | Require disabled state, accessible label/value, no file/password capture, no form association/submit attributes; do not silently discard represented values |
| button | Base only as inert preserved control; active behavior deferred | Disabled, no form association or declarative command/popover behavior; ordinary links serve navigation |
| audio, video | Base with explicit user playback | Packaged media/poster/tracks; no autoplay; meaning available without playback; host-accessible playback UI |
| canvas | Future Interactive capability | Base should not use a canvas element as an authoritative drawing surface; use static image/SVG plus semantics. Preserving arbitrary executable canvas behavior is out of scope. |
| Event-handler attributes | Always prohibited in the passive profile | Apply across namespaces and embedded languages |
| meta refresh | Always prohibited in the passive profile | Timed navigation needs no script |
| base and xml:base overrides | Prohibit in Base | Keep a single package-resolution model; harmless relative references still work |
| External embedded browsing contexts | Always prohibited in the passive profile | Hyperlinks open through the host, not inside an active document-created context |

“Always” here means the passive profile, not a promise about a hypothetical future interactive SPD profile. HTML supplies the element semantics; these choices are SPD policy. [HTML metadata](https://html.spec.whatwg.org/multipage/semantics.html), [embedded contexts](https://html.spec.whatwg.org/multipage/iframe-embed-object.html), [forms](https://html.spec.whatwg.org/multipage/forms.html), [media](https://html.spec.whatwg.org/multipage/media.html).

## CSS: precision without a new styling language

The existing [CSS profile](../../spec/profiles/css-profile.md) is a good basis but “required remote URL” is too narrow for a no-network policy. Validation must cover external and inline styles, style attributes, escapes/comments, nested rules and deferred values; a regex looking for literal `http` is insufficient. Keep the runtime network denial even after validation. [CSS Syntax 3](https://www.w3.org/TR/2021/CRD-css-syntax-3-20211224/), [Variables 1](https://www.w3.org/TR/2022/CR-css-variables-1-20220616/).

| CSS feature | Security | Determinism | Performance | Decision |
| --- | --- | --- | --- | --- |
| @import | Remote import is a request vector | Missing/changing remote style changes layout | Chains/cycles amplify work | Allow local inventoried acyclic imports; prohibit remote imports |
| url(), including escaped forms and nested functions | Resolve at every actual resource consumer; no external authority | Same resolved packaged bytes | May invoke decoders/filters | Allow package-local references and valid local fragments, prohibit executable/file/network references |
| @font-face | Network and font parser surface | Authoritative fonts must be packaged; local() cannot substitute an unbound authoritative font | Font tables and shaping | Allow bounded packaged fonts; ordinary fallback preferences remain reader UI |
| External stylesheet | “External” can mean a separate local file | A packaged CSS file is deterministic input | Normal CSS parsing | Allow local linked stylesheet; prohibit remote linked stylesheet |
| Remote image/mask/filter/cursor | Request vector even when decorative | Remote bytes mutable | Potential decode/paint load | Prohibit remote fetching, including optional styling |
| Generated content | Can hide or replace represented meaning; URLs also fetch | Counters can vary with layout | Usually ordinary layout | Allow decoration/numbering; no primary text, alt text or table data solely in generated content |
| Custom properties | Values can later reach a URL consumer | Cascade-dependent | Expansion cycles/pathological values | Allow; inspect substituted resource use and enforce resolver policy |
| Complex selectors | Not inherently executable | Usually stable for fixed DOM/state | Expensive matching or restyling | Allow with implementation budgets |
| Filters and transforms | Local references still invoke complex rendering | Output may vary between engines | Large filter regions and GPU cost | Allow self-contained bounded cases; report resource/unsupported results honestly |
| Animation/transition | Not inherently arbitrary code; may activate resource consumers | Time-dependent | Continuous layout/paint | Retain only with complete static state; suppress in Base; future execution deferred |

No universal selector-depth, filter-pixel or CSS-byte ceiling is proposed as a format maximum. These are operational budgets. Nor does disabling animation guarantee pixel-identical cross-engine rendering: fonts, viewport, CSS implementations and shaping still matter.

## SVG: reuse graphics, constrain capabilities

Keep paths, basic shapes, text, gradients, clipping, masks, transforms, symbols and safe local references. Prohibit scripts, events, foreignObject, executable URLs and network resources consistently for standalone and inline SVG. Do not allow a namespace or embedding-mode switch to escape the same policy. Optional animation declarations may be retained inert only with complete static meaning.

[SVG 2 processing modes](https://www.w3.org/TR/SVG2/conform.html) provide useful vocabulary: secure static mode excludes script, animation, interactivity and external references. It is a **processing mode**, not a syntax validator or proof that SVG Tiny/Basic is passive. A verbatim secure-static requirement would also disable cross-file packaged references and SVG links, which the existing SPD profile permits. Therefore reuse its no-execution/no-animation principles, with an explicitly bounded package resolver and host-mediated hyperlink exception where needed; do not claim exact secure-static conformance for that broader mode. SVG used as an image may retain the narrower native secure-static behavior and require self-contained content.

This is a short capability restriction over SVG, not a new geometric language. A universal graphics-element allow-list would needlessly duplicate the mature standard. Clipping/masks/filters can still exhaust resources, and embedded font SVG must inherit the same no-active/no-network policy. Unsupported static SVG is not automatically invalid.

## MathML

Reuse the MathML authoring model inherited by EPUB: Presentation MathML, with permitted semantic annotations/Content MathML placement. Do not replace it silently with MathML Core or claim arbitrary unprofiled MathML is already allowed. MathML introduces no necessary script interpreter, but it is **not completely behavior-free**: MathML 3 includes href links, mglyph image resources and maction behavior; annotation-xml can contain other markup. [MathML presentation](https://www.w3.org/TR/MathML3/chapter3.html), [mixed markup](https://www.w3.org/TR/MathML3/chapter5.html), [EPUB embedded MathML](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-xhtml-mathml).

Apply the same URL/local-resource and nested-content rules. Keep mathematical structure and semantic annotations, but treat embedded annotations as data and do not instantiate arbitrary active HTML. A maction requiring input or state changes to reveal primary meaning is deferred; a static presentation with its semantic information available remains appropriate. Mathematical depth, tables, stretchy glyphs, bidi and shaping remain resource/renderer issues, not an argument for a custom SPD mathematics subset.

## Hyperlinks and URI boundaries

Permit explicit user activation of http/https anchors through the host. Do not follow links while validating, generating previews or opening the document. Do not send ping, referrer containing package data, prefetch, speculative DNS, cookies, or background link-check requests. Show the interpreted destination in trusted UI; isolate it from the document context. Schemes that launch applications require an explicit future host policy; Base need not automatically support mailto or custom protocols. Executable/file/UNC and package-escape targets are not permitted navigation shortcuts.

Namespace identifiers, vocabulary IRIs and annotation identifiers are strings, not instructions to fetch. Reader-owned in-memory blob URLs are implementation plumbing, not permission for author-supplied blob/file/data documents to create unvalidated contexts. The minimal proposal disallows author-supplied data/blob resource URLs and uses inventoried resources instead; this is an inventory/processing simplification, not the false claim that data URLs are network requests. Local fragments and packaged relative links remain allowed. [HTML links](https://html.spec.whatwg.org/multipage/links.html).

The frozen semantic/digest model is preserved: parse for validation without rewriting bytes; do not sanitize a SEALED source in place and then present it as still verified.
