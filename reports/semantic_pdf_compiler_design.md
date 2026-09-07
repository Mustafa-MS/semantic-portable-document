# Semantic PDF Compiler design

## Boundary

The disposable compiler consumes authoritative XHTML, the revision/rendition-bound Phase 1B forward map, and the Paged.js/Chromium visual PDF. It does not paginate, shape glyphs, choose fonts, redraw images, or recreate any visual object.

The compiler changes only the PDF header/version, metadata, logical structure and parent trees, marked-content properties, structure destinations, and artifact classification. Existing text-showing, image, path, graphics-state, and positioning operators remain unchanged. Across the six compiled fixtures, drawing-operator preservation was **True**.

## Semantic mapping table

| XHTML | PDF 2.0 role | Important attributes |
|---|---|---|
| `main`, `article`, `section`, `nav` | `Sect` | language, external XHTML node ID |
| `h1`–`h6` | `H1`–`H6` | logical text, language |
| `p` | `P` | logical text, language |
| `ul`, `ol` | `L` | `ListNumbering` |
| `li` | `LI` | `Lbl` + `LBody`; links are inside `LBody` |
| `table`, `tr`, `th`, `td` | `Table`, `TR`, `TH`, `TD` | `Scope`, `RowSpan`, `ColSpan` |
| `caption`, `figcaption` | `Caption` | logical text |
| `figure` | `Figure` | `Alt` from the meaningful image alternative |
| footnote `aside` | `FENote` | language and node ID |
| `a` | `Link` | annotation association remains a residual area |
| MathML `math` | `Formula` | logical equation text; native MathML association remains future work |

PDF object numbers are not identity. The XHTML `data-node-id` is copied to structure `/ID` for this experiment and the authoritative association is also emitted as companion JSON.

## Association method

Chromium's existing tags are treated only as disposable MCID ownership hints. Authoritative roles, hierarchy, language, alternate text, table attributes, and logical order come from XHTML. Existing MCID groups are matched in semantic role order and checked against the already-complete forward map. Unowned content is explicitly marked as artifact. The rebuilt parent tree binds every retained MCID to the new XHTML-derived structure element.

## Complexity boundary

This is semantic compilation, not rendering: no glyph IDs, shaping state, line-breaking model, scene graph, or rasterizer is stored in the mapping. The renderer-specific dependency is the ability to associate existing marked-content groups with semantic nodes. That dependency is why the proposed profile is restricted rather than renderer-independent.
