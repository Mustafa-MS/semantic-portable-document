"""External adapter tests only; no fixture expected-result files are read."""
import hashlib
import subprocess
from pathlib import Path
from unittest.mock import patch

from spd_validator_b.epubcheck import (
    ACCEPTED_JAR_SHA256,
    ACCEPTED_RELEASE_ZIP_SHA256,
    EPUBCheckAdapter,
)
from spd_validator_b.models import ValidationOptions, ValidationReport

ROOT = Path(__file__).resolve().parents[2]
JAR = ROOT / "validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar"
ZIP = ROOT / "validator-b/tools/epubcheck-5.3.0.zip"


def test_official_pins_and_version():
    assert hashlib.sha256(ZIP.read_bytes()).hexdigest() == ACCEPTED_RELEASE_ZIP_SHA256
    assert hashlib.sha256(JAR.read_bytes()).hexdigest() == ACCEPTED_JAR_SHA256
    adapter = EPUBCheckAdapter.detect(ValidationOptions(epubcheck_jar=str(JAR)))
    assert adapter.command is not None
    assert adapter.version == "5.3.0"
    assert adapter.detail == "EPUBCheck v5.3.0"


def test_independent_real_invocation_records_exit_and_diagnostics():
    adapter = EPUBCheckAdapter.detect(ValidationOptions(epubcheck_jar=str(JAR)))
    path = ROOT / "tests/valid/minimal-base/document.epub"
    report = ValidationReport(str(path))
    adapter.validate(path, report)
    evidence = report.metadata["epubcheck"]
    assert report.operational_status.value == "COMPLETE"
    assert isinstance(evidence["exitCode"], int)
    assert evidence["result"] in {"PASS", "FAIL"}
    assert isinstance(evidence["diagnosticCodes"], list)


def test_pinned_release_zip_is_not_mistaken_for_a_jar():
    adapter = EPUBCheckAdapter.detect(ValidationOptions(epubcheck_jar=str(ZIP)))
    assert adapter.command is None
    assert "SHA-256 mismatch" in adapter.detail


def test_explicit_missing_tool_is_not_document_failure():
    adapter = EPUBCheckAdapter.detect(ValidationOptions(epubcheck_jar=str(ROOT / "validator-b/tools/missing.jar")))
    report = ValidationReport("absent.epub")
    adapter.validate(Path("absent.epub"), report)
    assert report.operational_status.value == "TOOL_UNAVAILABLE"
    assert report.violation_requirement_ids == []
    assert report.not_tested_requirement_ids == ["SPD-BASE-002"]


def test_timeout_keeps_frozen_operational_semantics():
    adapter = EPUBCheckAdapter(["java", "-jar", str(JAR)], "5.3.0", "AVAILABLE")
    report = ValidationReport("example.epub")
    with patch("spd_validator_b.epubcheck.subprocess.run", side_effect=subprocess.TimeoutExpired("java", 120)):
        adapter.validate(Path("example.epub"), report)
    assert report.operational_status.value == "TOOL_UNAVAILABLE"
    assert report.violation_requirement_ids == []


def test_fixture_error_uses_guarded_attribution_and_records_codes():
    adapter = EPUBCheckAdapter(["java"], "5.3.0", "AVAILABLE")
    report = ValidationReport("example.epub")
    completed = subprocess.CompletedProcess(["java"], 1, "EPUBCheck completed", "ERROR(RSC-005): EPUB/content.xhtml: bad XML\nERROR(OPF-012): bad metadata")
    with patch("spd_validator_b.epubcheck.subprocess.run", return_value=completed):
        adapter.validate(Path("example.epub"), report)
    assert report.violation_requirement_ids == ["SPD-BASE-002", "SPD-SEM-002"]
    assert report.metadata["epubcheck"]["diagnosticCodes"] == ["OPF-012", "RSC-005"]


def test_crash_after_partial_diagnostic_is_not_document_failure():
    adapter = EPUBCheckAdapter(["java"], "5.3.0", "AVAILABLE")
    report = ValidationReport("example.epub")
    completed = subprocess.CompletedProcess(["java"], 1, "", "ERROR(OPF-014): partial error\nException in thread main")
    with patch("spd_validator_b.epubcheck.subprocess.run", return_value=completed):
        adapter.validate(Path("example.epub"), report)
    assert report.violation_requirement_ids == []
    assert report.operational_status.value == "TOOL_UNAVAILABLE"
