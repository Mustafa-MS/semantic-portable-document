# Validator B Architecture

Validator B uses an evidence pipeline designed independently for Python rather than a shared fact model.

1. `package.py` opens ZIP entries in place and establishes safe names, collision freedom, supported compression, encryption status, and resource limits.
2. `epub.py` parses `container.xml`, enforces the single OPF rootfile, discovers descriptors only through exact OCF relationships, and derives the XHTML spine/capability metadata from OPF.
3. `strictjson.py` and `schemas.py` parse descriptors without duplicate-key or non-I-JSON loss and apply the canonical Draft 2020-12 schemas locally.
4. `integrity.py` verifies complete inventory coverage, exact decompressed bytes, projection digests, state bindings, JCS descriptor digest, SEALED consistency, and fixed currentness.
5. `semantics.py` parses authoritative XHTML as hardened XML, builds Node identity/text views, checks language/direction/table rules, and tokenizes CSS/SVG/resource references without dereferencing them.
6. `mapping.py` cross-binds mapping identity and fixed state, then validates Node/page/range/status/geometry constraints without rendering or reading PDF semantics.
7. `annotations.py` locates packaged annotation resources through the OPF manifest and validates StableNodeSelector scope, identity, and scalar range bindings.
8. `epubcheck.py` invokes pinned EPUBCheck independently when configured and otherwise reports operationally honest `TOOL_UNAVAILABLE`/`NOT_TESTED` results.
9. `validator.py` orchestrates checks and rolls findings onto the normalized differential surface. Detailed diagnostics are Validator-B-specific; only the normalized surface is intended for later comparison.

All source bytes remain untouched. Parsed or normalized views are transient and never replace package resources.

