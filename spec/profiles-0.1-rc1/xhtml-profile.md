# Format 0.1 semantic XHTML profile

The authoritative rendition is one or more well-formed EPUB XHTML content documents in spine order. EPUB 3.3 content-document requirements apply.

## Core semantic structures

The profile supports ordinary native structures including `article`, `section`, `nav`, `h1`–`h6`, `p`, `ol`, `ul`, `li`, `dl`, `figure`, `figcaption`, `table`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td`, `blockquote`, `cite`, `code`, `pre`, `aside`, links, embedded static images/SVG, and MathML. This is not an exhaustive allow-list.

## Required rules

- XHTML MUST be XML-well-formed and valid for the applicable EPUB XHTML profile.
- The package spine MUST identify the full primary reading order and exactly one authoritative rendition.
- Root `lang` and `xml:lang` MUST both be present, valid BCP 47 language tags, and language-equivalent.
- Root `dir` MUST be explicitly `ltr` or `rtl`; `auto` is prohibited on the root. A nested semantic element MUST declare direction when its intended base direction differs from inherited direction. Nested/user-generated content MAY use `dir="auto"` where appropriate.
- Independently addressable sections, headings, paragraphs, list items, figures/captions, tables/rows/cells, equations, notes, citations, references, and preserved controls MUST have Node IDs.
- All XML/HTML IDs are unique in the package; Node IDs are additionally unique across the document lineage to the extent history is available.
- Text remains in DOM logical Unicode order. CSS layout or bidi display does not rewrite source order.
- Tables use native table elements; applicable `th`/`scope`/`headers` relationships are expressed semantically.
- Native semantics take precedence over ARIA. Roles that conflict with or needlessly replace equivalent native semantics are errors or warnings according to determinacy.

## Normative passive restrictions (SEC-001–008; PASS-001–003)

Prohibited: every `script` including data blocks; event-handler attributes; executable URLs; `iframe` including `srcdoc`; `object`; `embed`; plugins; service-worker dependencies; `form`; authoritative interactive `canvas`; meta refresh; automatic redirects/navigation; `base` and `xml:base` resolution overrides; external embedded browsing contexts. A host's own rendering frame is outside document content.

`input` MAY preserve an inert semantic value only when disabled, accessibly labeled, with its value available, no password/file capture, form association, submission attributes or activation behavior. `button` MAY be preserved only disabled, labeled and without form submission/association, command, popover or activation behavior. Functional forms and interactive drawing are deferred; no new capability is defined here. Label correctness and completeness require human evaluation.

Packaged `audio`, `video`, `poster` and `track` resources MAY be used where EPUB permits. Autoplay is prohibited. Playback requires explicit user action; meaning necessary to understand the document MUST be accessibly available without relying solely on playback. All sources, posters, tracks, srcset candidates, styles and nested dependencies obey the [passive resolver](passive-resource-profile.md).

Explicit HTTP/HTTPS hyperlinks MAY be activated through host mediation. Validators MUST NOT visit them. Ping, prefetch, DNS prefetch/preconnect and remote preload declarations are prohibited. Namespace/vocabulary IRIs are identifiers, not fetch instructions. Inline SVG, MathML and annotation-xml content inherit the same passive restrictions.

## Unsupported is not prohibited

Harmless HTML supported by EPUB 3.3 is not invalid merely because an initial reader lacks UI support. A reader reports unsupported optional features without misrepresenting the Base semantic content.

## Text-value algorithm for mapping

For a mapped Node, take descendant XML text nodes in DOM order, excluding comments, processing instructions, `head`, `script`, `style`, and CSS generated content. Preserve the code points and whitespace as serialized after XML character-reference expansion. Count Unicode scalar values; use half-open ranges. No NFC/NFKC, whitespace collapse, shaping, or bidi reordering is performed.
