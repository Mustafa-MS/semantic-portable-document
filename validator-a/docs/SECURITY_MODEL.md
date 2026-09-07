# Security model

Inputs are hostile. The ZIP gate rejects non-UTF-8/absolute/traversal/backslash/
dot-segment names, duplicate names, NFC collisions, symlinks, and compression
outside Stored/Deflate. Configurable ceilings cover package size, entry count,
entry size, aggregate expansion, compression ratio, XML/JSON bytes, and mapping
records. A ceiling produces `RESOURCE_LIMIT`, not an SPD violation.

Descriptors are strict UTF-8 JSON with duplicate-member rejection and embedded
Draft schemas; no URI is fetched. XML and CSS/XHTML checks operate only on bounded
package bytes. Validation never extracts or mutates the document and performs no
network access. No `unsafe` Rust is used. EPUBCheck is never downloaded at
runtime and receives a path as one process argument without shell interpolation.
