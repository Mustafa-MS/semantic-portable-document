# Architecture decision implemented

Option A is retained: SPD 0.1 uses a conforming EPUB 3.3 publication/package profile, pinned to Recommendation 13 January 2026. SPD is a distinct semantic document model with a passive content profile and EPUB-compatible packaging layer. The decision was not reopened.

No new internal marker, MIME type, mandatory extension, container manifest, Forms/Interactive capability, signature, reader, editor or renderer was introduced. Semantic XHTML remains authoritative for SEALED documents. Generic reading is distinct from verified state/fixed presentation. Fixed-Experimental and Archive-Experimental remain experimental. No RC1 was created.

Document/revision/node identity, both digest algorithms, lifecycle, Mapping, annotations, transactional editing and Accessible 0.1 meaning are unchanged. Baseline preservation and final integrity checks identify exact bytes. Changes are approved clarifications, stricter subset rules, processor obligations, upstream pins and validation-closure fixes; they are not all editorial.
