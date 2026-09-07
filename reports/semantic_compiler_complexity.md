# Semantic compiler complexity

## Implemented custom PDF knowledge

- PDF 2.0 structure elements, namespace, MCRs, parent tree, artifacts, language, IDs and XMP;
- semantic mapping from XHTML roles and attributes;
- renderer MCID ownership adapter and marked-content `/ActualText` experiments;
- structure-destination repair for outlines;
- byte/pixel/operator preservation evidence.

## Explicitly not implemented

- glyph shaping, bidi layout, line breaking, pagination, font selection/rasterization;
- image/vector re-rendering;
- a second page scene or PDF text-layout engine.

## Assessment

**SEMANTIC COMPILATION**, with one architectural warning: interoperable logical text repair is renderer/consumer-sensitive. The map remains small, but wrapping correct semantic ranges requires a renderer-MCID association adapter. If a future implementation must infer or rebuild glyph shaping to make T09 work, it crosses the kill criterion into reimplementing a PDF renderer.
