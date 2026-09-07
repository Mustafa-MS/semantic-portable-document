# VALIDATOR_B_EXTERNAL_ADAPTER_FIX

Adapter-only defect count: **2**. Validator B remains version 0.1.0; this stage is an explicitly documented external-adapter correction, not a new SPD interpretation.

## Fix 1 — Release ZIP digest was incorrectly applied to the JAR

The frozen adapter compared the configured JAR bytes with SHA-256 `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5`. Independent official GitHub release metadata identifies this as the digest of `epubcheck-5.3.0.zip`, not `epubcheck.jar`.

The official ZIP was independently downloaded from W3C's [EPUBCheck v5.3.0 release](https://github.com/w3c/epubcheck/releases/tag/v5.3.0) and verified against that exact pinned digest before extraction. The contained JAR has SHA-256 `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`.

The adapter now retains both clearly named digest constants and applies the JAR digest to a configured JAR. No download functionality was added to validation.

## Fix 2 — Version parser rejected the official `v` prefix

The official command emits `EPUBCheck v5.3.0` and exits 0. The old regex required a word boundary immediately before the first digit; there is no such boundary between `v` and `5`. It therefore reported an unknown version despite successful invocation.

The adapter now matches the EPUBCheck name and an optional `v` prefix before the version, while continuing to require exactly 5.3.0. Version mismatch diagnostics additionally retain the exit code and tool output.

## Observability only

Per-invocation metadata now includes exit code, PASS/FAIL/ERROR, diagnostic codes, stdout, and stderr. This evidence is excluded from the normalized differential surface. The adapter's existing document-failure and operational roll-up behavior is unchanged.

## Regression and preservation

- All 37 original tests and 6 new adapter/integration tests pass: **43 passed**.
- The new tests independently verify official artifact hashes, the real version command and fixture invocation, missing-tool behavior, ZIP-versus-JAR distinction, timeout behavior, and diagnostic capture.
- `epubcheck-completion-baseline.json` records pre-fix hashes of every original Validator B Python file, original tests, project metadata, original freeze artifacts, normative inputs, canonical schemas, and all 69 corpus packages.
- The completion runner permits changes to only `spd_validator_b/epubcheck.py` among those baseline files.
- `epubcheck-adapter-only.diff` records the exact source diff.
- The completion runner reconstructs the unavailable-tool blind output and requires its SHA-256 to equal the original `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c` before writing the completed result.
- It also compares detailed native findings before/after for every fixture, not only normalized requirement-ID sets.

No Validator A source, tests, adapter, executable, golden oracle, or summary was accessed. No SPD-native validation or normalized roll-up code was modified.
