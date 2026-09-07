# SPD Validator B

Validator B 0.1.3rc1 is an independent Python 3.12+ conformance validator for SPD Format 0.1 RC1. It was implemented from the versioned specification, 118-requirement registry, canonical schemas, conformance matrix, standards traceability, 107-fixture corpus, and validator-neutral differential contract. It does not call or reuse Validator A.

Validation is read-only, performs no network access, never extracts a package, and never repairs source content.

## Install and use

From the repository root:

```powershell
python -m venv validator-b\.venv
validator-b\.venv\Scripts\python.exe -m pip install -e ".\validator-b[test]"
validator-b\.venv\Scripts\python.exe -m spd_validator_b validate tests\corpus-0.1-rc1\valid\minimal-base\document.epub
validator-b\.venv\Scripts\python.exe -m spd_validator_b validate document.epub --json
validator-b\.venv\Scripts\python.exe -m spd_validator_b validate document.epub --normalized --fixture my-fixture
```

EPUBCheck 5.3.0 may be supplied by `--epubcheck-command`, `--epubcheck-jar`, or `EPUBCHECK_JAR`. The JAR adapter verifies the pinned SHA-256. Validation never downloads it. When unavailable, inherited EPUB validation is `NOT_TESTED` and operational status is `TOOL_UNAVAILABLE`; SPD-native failures remain document failures.

## Library API

```python
from spd_validator_b import validate

report = validate("document.epub")
print(report.normalized("fixture-id"))
```

Resource limits are implementation controls exposed through `ValidationOptions`; exceeding them yields `RESOURCE_LIMIT`, not a document conformance failure. Run `python -m pytest validator-b/tests` before submitting validator changes. The qualifying RC1 aggregate is summarized in [`../reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md`](../reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md).
