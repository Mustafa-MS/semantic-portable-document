# Verification scope notes

The required A fuzz/smoke check was executed as the deterministic `bounded_fuzz_smoke` test: 128 hostile byte inputs under small ZIP/resource ceilings, included in the 17 passing A tests. The existing libFuzzer target remains unchanged. `cargo fuzz --version` reported that cargo-fuzz is not installed, so no long-running libFuzzer campaign was performed or claimed. The task's bounded smoke alternative was used.

B's 57 passing tests include Hypothesis property checks, strict JSON/ZIP/XML protections, Unicode behavior, and six external-adapter tests (including real official-tool invocation, digest/version verification, unavailable-tool and timeout handling). The full final corpus evaluation is additional evidence, not a substitute for those tests.

The final corpus runs contain 140 completed EPUBCheck fixture evaluations (70 per validator), in addition to adapter test invocations and preliminary diagnostic runs. An EPUBCheck exit of 1 on an intentionally invalid fixture is a completed evaluation, not an operational failure. Both runs have 62 exit-0 and eight exit-1 fixtures.

The versioned files under `freezes/` are the immutable validator outputs. `candidate-*` and the unversioned initial detailed reports are preliminary evidence and must not be used as release freezes. `finish.py --verify-existing` rechecks the gates and existing freeze contents without overwriting those files; it may refresh derived reports and their checksum manifest.

Historical scenario labels in the corpus manifest are not authoritative capability declarations. The reviewed expected reports and both validators determine explicit claims from the successfully discovered authoritative document descriptor. In particular, physical fixed-rendition presence and a Mapping dependency do not manufacture a Fixed-Experimental declaration.
