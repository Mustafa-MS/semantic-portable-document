# EPUB Reader Interoperability

- **epub.js 0.3.93** (Chromium via Playwright): opened 12/12 packages.
- **Foliate JS git:78914aef4466eb960965702401634c2cb348e9b1** (Chromium via Playwright): opened 12/12 packages.
- **calibre E-book viewer 9.14** (Qt WebEngine): opened 5/5 packages.

**OBSERVED IN IMPLEMENTATIONS.** Tests cover opening, navigation, XHTML, Arabic metadata/text,
images, MathML, links, unknown experimental manifest resources, and embedded-PDF non-activation.
epub.js, Foliate JS, and Calibre showed the semantic spine without surfacing the sealed state or fixed PDF, which is safe
fallback behavior but creates user-experience ambiguity: an ordinary reader cannot communicate
that a bound fixed rendition exists. Screenshots are under `reports/screenshots/`.

Technical validity, fallback behavior, security, and user-experience ambiguity are separate axes.
