# Format 0.1 conformance corpus

Each fixture directory contains `document.epub`, `expected.json`, and a short `README.md`. `expected.json` follows `schemas/conformance-result.schema.json` and names exact requirement IDs.

- `valid/`: representative conforming Base/capability packages.
- `invalid/`: one primary targeted failure per package, including security, identity, integrity, mapping, RTL, stale-state, and mutation failures.
- `edge/`: valid but difficult cases that define boundaries without implying invalidity.

Regenerate deterministically with `python scripts/build_conformance_corpus.py`. Verify schemas, inventory hashes, package invariants, expected-result references, and intentional schema failures with `pwsh scripts/verify_conformance_model.ps1`.

The corpus scripts are test-data tooling, not a production validator.

## Corpus category semantics

A fixture under `tests/valid/` means that no evaluated normative document
requirement is expected to `FAIL` and that Base may conform. It does not mean
that every claimed capability containing `PARTIALLY_AUTOMATED` or `MANUAL`
requirements must be reported `PASS` by an automated validator. In particular,
`Base: PASS` with `Accessible: NOT_TESTED` is valid when no accessibility failure
is established but required human WCAG evaluation remains unresolved.
