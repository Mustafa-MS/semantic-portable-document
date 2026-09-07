# Format 0.1 CSS profile

CSS is presentation, not authoritative text or structure. EPUB 3.3 CSS requirements continue to apply.

| Class | Features | Rule |
|---|---|---|
| ALLOWED | selectors, cascade, box model, typography, flex/grid, tables, writing modes, bidi properties, transforms, counters used for labels, multi-column, ordinary paged-media rules | Allowed when they do not hide required meaning or introduce external dependencies. |
| RESTRICTED | `url()`, `@font-face`, generated content, `display:none`, visibility/opacity, transforms, filters, counters, multi-column, page floats | URLs resolve to packaged resources; generated content cannot carry primary meaning; hidden content must have a semantic reason; mapping geometry reflects the final visual result. |
| PROHIBITED | remote `@import`, any automatically consumed remote URL, `javascript:`/executable URL, behavior bindings, CSS used to reverse source into visual reading order | Base violation. Local `@import` is allowed when inventoried and acyclic. |
| EXPERIMENTAL | animations, transitions, time-dependent presentation, complex filters, interactive state-dependent primary presentation | May be preserved but cannot be required for Base meaning or a sealed deterministic fixed appearance. A fixed renderer samples a declared stable state. |

## Specific rules

- Remote fonts, images, stylesheets, cursor assets, masks, filters, and all other automatic resources, including optional/decorative resources are prohibited.
- `@import` MUST resolve locally, be inventoried, and terminate without a cycle. Remote `@import` is prohibited.
- `content` on pseudo-elements MAY add decorative marks or generated numbering. It MUST NOT supply primary text, alternative text, headings, table data, or other authoritative meaning.
- Content hidden with `display:none`, `visibility:hidden`, clipping, zero opacity, off-page transforms, or equivalent MUST NOT be the sole source of required authoritative meaning. `NOT_VISIBLE` mapping is valid only when non-visibility is intentional and semantics remain available.
- Transforms, filters, columns, counters, and paged media are not prohibited merely because they complicate mapping. A Mapping claim must still provide final page-local geometry or an honest partial/unsupported status.
- CSS animations/transitions MUST be disabled or resolved to a declared stable snapshot when producing a sealed fixed rendition.


## Passive resource and static presentation obligations

Every resource-consuming `url()` and string URL (including `@import`, font `src()` and image-set image strings) MUST use the passive package resolver. Package-local resources and valid fragments are allowed; network, executable, file, UNC, data/blob and package-escape resources are prohibited. This includes inline style elements/attributes, nested rules, imports, fonts, cursors, masks, filters and optional decorations. Font `local()` MUST NOT substitute an unbound authoritative font; package font resources instead.

Custom properties remain allowed. A token containing a resource reference remains subject to the resource policy, including when stored in a custom property or used through substitution. String-only values that do not consume a resource are inert. Dynamic string-to-URL consumers whose package locality cannot be established MUST be reported NOT_TESTED, never silently accepted. Validators inspect grammar tokens, decoded escapes and nested functions; comments and escaping cannot bypass checks.

Complex selectors, transforms and static filters are allowed. CSS-generated text MAY provide decoration/numbering but MUST NOT be the only source of primary semantic content, alternative text or table data. Animation, transitions and time-dependent declarations MAY remain only with a complete meaningful static state; their execution SHALL be suppressed in Base. Semantic completeness is PARTIALLY_AUTOMATED and requires human review, including for generated/hidden content. Existing stable-snapshot requirements for SEALED fixed rendering are unchanged.
