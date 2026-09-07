# Baseline identity clarification

The preserved BASELINE_FREEZE.md recorded the literal `HEAD` output from the original Git probe. It is not a commit identifier. `git rev-parse --verify HEAD` fails because this repository has no resolvable HEAD revision. The freeze file remains unchanged as historical evidence.

The authoritative baseline identity is the SHA-256 inventory in baseline-sha256.json together with pre-clarification-inputs.zip. Final implementation identities are the per-file SHA-256 inventories in the new validator evidence, plus the built artifact digests. No commit identity is claimed.
