# Format 0.1 static SVG profile

Ordinary static SVG geometry, paint, text, gradients, clipping, masks, symbols, and local fragment references are supported subject to EPUB 3.3 and this security profile.

## Prohibited

- `script`, event-handler attributes, `javascript:` URLs, and executable bindings.
- `foreignObject` in Base 0.1 because it can embed active HTML and create a second content-processing context.
- External/network resource references from `href`, `xlink:href`, paint servers, filters, images, fonts, styles, or other URL-bearing attributes.
- Plugin/object execution and automatic navigation.
- SMIL or CSS animation required to convey authoritative meaning or determine a sealed fixed scene.

## Restricted

- Links MAY target local package content or external user-activated destinations. External links are never fetched automatically.
- Filters are permitted when self-contained and bounded; processors may report resource-limit failure for pathological filter regions.
- Embedded font data must be packaged, inventoried, and licensed for embedding; remote fonts are prohibited.
- SVG text that is authoritative content must be represented or referenced semantically in XHTML. SVG MUST NOT become an independently editable duplicate source of primary prose.
- Local fragment references must resolve within the package and must not form unbounded reference cycles.

Static SVG unsupported by a particular reference renderer remains format-valid if it satisfies the profile; the renderer reports `UNSUPPORTED` rather than inventing geometry.


## Uniform embedding and resolution

These normative rules apply to namespace-aware standalone SVG, inline SVG, SVG used as images, nested/referenced SVG and SVG embedded in other supported content, including fonts. Scripts (even data blocks), events, foreignObject, executable URLs, automatic remote dependencies and active document behavior are prohibited in every context. All href/xlink:href, paint, style, mask/filter, image and font references obey the transitive passive resolver. Safe terminating cross-file package references are allowed; valid local fragments must exist. Geometry, shapes, text, gradients, clipping, masks, transforms and symbols are retained.

Optional animation declarations require complete static meaning and suppressed Base execution (PASS-003). This profile reuses SVG processing concepts but does not claim exact SVG Secure Static mode conformance, since its mediated hyperlinks and package-local cross-file references have an explicitly bounded policy.
