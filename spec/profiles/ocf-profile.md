# Format 0.1 OCF profile

This profile layers restrictions on EPUB 3.3 OCF; it does not restate OCF. EPUB 3.3 remains normative for ZIP structure, `mimetype`, `META-INF/container.xml`, package document, manifest, spine, navigation, URL processing, and the stored/Deflate compression methods.

## Adopted unchanged

- Only ZIP methods 0 (stored) and 8 (Deflate) are permitted.
- `mimetype` is first, stored, and exactly `application/epub+zip` for the 0.1 test corpus.
- ZIP names are UTF-8 and case-sensitive.
- OCF file-name and path length constraints apply.
- Split/spanned archives and ZIP encryption are prohibited by the inherited OCF rules.

## Additional Format 0.1 restrictions

- Each ZIP entry name MUST be a relative, forward-slash-separated path.
- Names MUST NOT contain a backslash, NUL/control character, empty segment, `.` segment, `..` segment, drive prefix, leading slash, or trailing slash for a file.
- Percent-decoding a referenced URL MUST NOT yield traversal or an absolute path.
- Every entry name MUST already be Unicode NFC. A package MUST NOT contain two entry names that are identical after percent-decoding each URL path segment and NFC normalization. This comparison does not make ordinary lookup case-insensitive.
- Duplicate ZIP entry names are prohibited even if their bytes match.
- Symlink/device entries and entries with data extending outside the archive are prohibited.
- All package-document manifest resources needed for the authoritative rendition MUST be local.
- Remote hyperlinks are permitted only when activation requires an explicit user action. Remote resources cannot be required for Base rendering or semantics.
- The inventory MUST list every ZIP entry, including `mimetype`, `META-INF/container.xml`, and non-normative caches, except the inventory itself and lifecycle state descriptor. No arbitrary cache exception exists.
- Every inventoried path resolves to exactly one ZIP entry with the same case-sensitive normalized path.

## Prohibited behavior

- Path traversal, absolute paths, backslashes, ambiguous normalized duplicates, duplicate central-directory names, encrypted entries, required network fetches, and active-content dependencies are conformance errors.
- Readers MUST NOT extract entries before validating their resolved destination remains inside the chosen extraction directory.

## Descriptor discovery and rootfile

- `META-INF/container.xml` MUST contain exactly one `rootfile`. Its package-document spine is the authoritative semantic reading order.
- It MUST contain exactly one `link` for each provisional relationship `https://example.invalid/spd/rel/document-state`, `https://example.invalid/spd/rel/resource-inventory`, and `https://example.invalid/spd/rel/lifecycle-state`.
- Each link uses media type `application/json` and a safe path-relative href resolving to exactly one resource.
- Processors MUST use these links and MUST NOT scan or guess descriptor filenames.
- The provisional identifiers MUST be replaced with stable project-controlled identifiers before Release Candidate.

## Security limits

Universal numeric size limits are not standardized in 0.1. A processor SHOULD enforce configurable limits for entry count, total expanded bytes, per-entry expanded bytes, compression ratio, XML depth, JSON depth, and processing time. Limit-triggered rejection is a resource-limit result, not proof that the document violates a universal Format 0.1 maximum.

## Normalization note

NFC is used only to reject ambiguous duplicate names. It does not rewrite stored paths, make lookup case-insensitive, or alter bytes used for hashing.

BASE-001/002 incorporate the complete EPUB 3.3 publication/container requirements from REC 13 January 2026, not only ZIP syntax. The internal application/epub+zip marker remains unchanged. Symlink/device entries, ambiguous decoded/NFC identities and inconsistent/overlapping ZIP entry bounds are rejected; malformed decoding is operational MALFORMED_INPUT, while proven profile defects fail BASE-002. Expansion ceilings are implementation RESOURCE_LIMIT, not universal format maxima.
