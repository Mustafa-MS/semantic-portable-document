# Whole-publication EPUBCheck results

Official EPUBCheck 5.3.0 executed on all **107/107** final package byte sequences for each validator. A: {'PASS': 86, 'FAIL': 21}. B: {'PASS': 86, 'FAIL': 21}. All **48/48 Base-PASS** fixtures have EPUBCheck PASS; no unresolved EPUB error is accepted. Warnings alone are not failures.

S29 (missing OPF title) fails exactly SPD-BASE-002. Native-invalid packages retain native IDs plus BASE-002 when EPUB also fails. S27 malformed ZIP retains operational MALFORMED_INPUT and independently established EPUB failure; S28 retains RESOURCE_LIMIT with no invented native conformance failure.

Raw per-package outputs, diagnostic codes, exit status, executed flag, exact source and JAR hashes are retained in the final validator reports. Interrupted or unavailable tool evidence is never counted as document failure. Operational attempt records: operational-attempt-a.json, operational-attempt-b.json. Where present, these preserve transient parallel-run probe failures; only affected fixtures were re-evaluated at lower concurrency with unchanged sources/package bytes and the same tool/time limits.

S25 was completed after the initial batch when byte inspection found that only its symlink flag was present. The final package includes both symlink and device modes. Direct EPUBCheck and both validators re-evaluated those final bytes; the initial package and its digest are retained in s25-mode-review.json and s25-initial-symlink-only.epub. Reused results for all other fixtures are checked against their exact final package hashes and unchanged implementation sources.

The dated-standard/tool relationship and observed escaped-import limitation are documented in UPSTREAM_PINNING.md. EPUBCheck PASS is required but does not by itself prove the SPD passive profile, human semantic completeness or reader conformance.
