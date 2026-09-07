# EPUB Compatibility

**Evidence:** internal OCF/ZIP/XML profile checks are VERIFIED BY TEST; EPUB conformance and
reader compatibility are NOT VERIFIED.

| Document | Internal profile | Errors | EPUBCheck |
| --- | --- | ---: | --- |
| T01 | True | 0 | NOT RUN |
| T02 | True | 0 | NOT RUN |
| T03 | True | 0 | NOT RUN |
| T04 | True | 0 | NOT RUN |
| T05 | True | 0 | NOT RUN |
| T06 | True | 0 | NOT RUN |
| T07 | True | 0 | NOT RUN |
| T08 | True | 0 | NOT RUN |
| T09 | True | 0 | NOT RUN |
| T10 | True | 0 | NOT RUN |
| T11 | True | 0 | NOT RUN |
| T12 | True | 0 | NOT RUN |

Each package has an uncompressed first `mimetype` entry, `META-INF/container.xml`, package
document, manifest, spine, navigation document, XHTML, CSS, local assets, and experimental JSON/PDF
resources. EPUBCheck and two independent reader trials were unavailable, so the harness does not
claim the packages are EPUB-conformant or that unknown resources are harmless in readers.
