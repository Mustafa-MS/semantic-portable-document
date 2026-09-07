# Architecture

`validate_path`/`validate_reader` first performs a bounded central-directory ZIP
gate. One in-memory package fact set is then consumed by discovery, strict JSON
and local schema parsing, inventory/integrity, semantic/security, lifecycle,
capability, mapping, annotation/accessibility, and deterministic roll-up stages.
Rules consume shared facts; they do not reopen the package.

Foundational failures stop dependent checks. Package traversal/collision failures
stop descriptor processing; discovery failures stop guessed-filename access;
descriptor parse failures stop dependent state and capability assertions; a
broken state-to-inventory binding prevents invented projection diagnostics.

Production findings carry requirement, outcome, severity, capability, stage,
resource/node/revision context, structured evidence, and source. Fixture tests
compare a normalized surface. External EPUBCheck execution uses an argument-safe
`Command`, null stdin, bounded wait, and explicit operator-supplied path.
