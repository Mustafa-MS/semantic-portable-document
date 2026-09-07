# Cross-spine duplicate Node ID

Corpus 0.1.1 negative revision-wide identity regression. Both authoritative XHTML documents have locally unique XML IDs, but chapter1.xhtml:4 and chapter2.xhtml:4 each contain article id=n_article01 in the same current semantic revision. Expected Base FAIL includes SPD-ID-006. EPUBCheck is expected to pass: the defect is the stronger SPD revision-wide identity rule, not per-document XML ID uniqueness.

The package preserves the historical multi-spine bytes. All inventory/state bindings are internally consistent. The repaired positive case remains tests/valid/multi-spine.
