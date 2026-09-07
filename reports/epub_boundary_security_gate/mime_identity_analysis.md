# MIME identity, extensions and public description

**Format 0.1 does not currently need a new MIME type or extension to satisfy its document model or security requirements.** Neither is selected or registered in this audit.

[EPUB 3.3 OCF §4.3.3](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-zip-container-mime) fixes the internal `mimetype` entry to `application/epub+zip` with its prescribed position/storage. The media registration's extension description identifies `.epub` as the usual extension; the host filename is not itself the internal ZIP conformance mechanism. Distinguish that marker from an HTTP Content-Type, a future registered subtype, an OS file association and a user-visible working name.

## Six required answers

| Question | Answer |
| --- | --- |
| 1. Can a package use a distinct OS extension while retaining the EPUB internal marker? | Yes. Renaming the outer file does not change its internal conformance. An SPD-specific association can be a routing convention under A. |
| 2. Would it still legitimately be EPUB? | Yes, if all EPUB publication/container/content requirements remain satisfied. An alternate suffix alone neither invalidates nor establishes that conformance. |
| 3. Would EPUB readers recognize/open it? | Not guaranteed. File dialogs, MIME dispatch, sniffing, imports and “open with” differ. The repository only tested historical EPUB packages, not a new suffix or media type. Renaming a copy may help some readers but is not a compatibility guarantee. |
| 4. Does application/epub+zip undermine SPD identity? | It expresses the serialization's EPUB identity. SPD's lifecycle/semantic model remains distinct. Saying the package is independent of EPUB would be misleading; saying SPD is only EPUB misses its additional conformance model. |
| 5. Is B required for a true SPD media type? | **For replacing OCF's mandatory internal marker, yes: that container would no longer satisfy unchanged OCF identification. For an externally registered specialized media type over EPUB-conforming bytes, not inherently.** A registration could describe a stricter format while retaining EPUB bytes, subject to review and ecosystem support. This audit does not assert that such a registration exists or will be approved. |
| 6. Is a new MIME type necessary now? | No demonstrated requirement. Detection can use existing SPD descriptor relationships/capabilities after safe ZIP identification. Keep the marker and defer any registration decision to a concrete distribution requirement. |

RFC 6838 sets the registration framework; it does not turn a chosen name into registered media identity or prescribe how every reader must dispatch it. The illustrative `application/spd+zip` in the task remains illustrative. [RFC 6838](https://www.rfc-editor.org/rfc/rfc6838.html).

## Extension strategy for 0.1

Continue the existing EPUB-compatible corpus convention while the Draft's extension remains unassigned. Document explicit SPD detection through existing discovery metadata, not an extension-only trust decision. An optional future SPD association may route users to a state-aware reader without changing container bytes; test that routing before promising compatibility. No security authority should depend on suffix, MIME or sniffing alone.

Under A, using EPUB's marker costs some default-application control and exposes users to generic-reader expectations. Under B, a new marker makes the independent contract clearer but requires package/tool/export changes. Under C, identity is unconstrained but still supplies no sandbox.

## Sustainable descriptions

| Option | Honest description | Main caveat |
| --- | --- | --- |
| A | A semantic portable-document format whose 0.1 EPUB-compatible packaging profile is a strict subset of a dated EPUB 3.3 baseline | EPUB is a normative publication/package parent, not merely a technology source |
| B | A semantic portable-document format with an OCF-derived package and explicitly incorporated Web publication technologies | Do not advertise automatic EPUB validity or generic-reader support |
| C | A semantic portable-document format with an independently specified container and publication model | Must actually specify and validate those new responsibilities |

Conceptual separation of document model and packaging is useful under A, but it does not justify denying the format's current serialization dependency. No rebranding is needed to express that accurately.
