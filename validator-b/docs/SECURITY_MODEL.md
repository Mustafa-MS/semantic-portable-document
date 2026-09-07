# Security Model

Validator B treats every package byte as hostile.

- ZIP resources are streamed from the archive and never extracted.
- Entry names reject absolute paths, drive paths, backslashes, dot segments, control characters, duplicate names, and NFC collisions.
- Stored and Deflate are the only accepted SPD methods; encrypted entries are rejected.
- Configurable limits bound compressed package size, entry count, single-entry expansion, total expansion, compression ratio, XML/JSON input size, and JSON depth.
- XML disables DTD loading, entities, network access, recovery, and huge-tree mode. Explicit DTD/entity declarations are rejected.
- JSON is strict UTF-8, rejects duplicate member names, NaN/Infinity, excessive depth, and lone surrogates.
- URI resolution uses parsed, normalized package-local references. External required resources are identified but never fetched.
- CSS is tokenized, SVG/XHTML are parsed, and active content/event handlers/remote required resources are checked without executing content.
- EPUBCheck is a separate bounded subprocess. Validation never downloads tools.
- Operational limits and missing tools are kept separate from document failures.

The validator does not implement repair, rendering, PDF text inspection, macro execution, browser execution, or network retrieval.

