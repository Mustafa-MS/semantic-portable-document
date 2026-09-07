from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

import pytest

from spd_validator_b.epub import discover
from spd_validator_b.models import ResourceLimits, ValidationReport
from spd_validator_b.package import SecurePackage
from spd_validator_b.validator import validate

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "fixture",
    [
        "tests/corpus-0.1-rc1/invalid/path-traversal/document.epub",
        "tests/corpus-0.1-rc1/invalid/multiple-rootfiles/document.epub",
        "tests/corpus-0.1-rc1/invalid/invalid-xhtml/document.epub",
        "tests/corpus-0.1-rc1/invalid/capability-status-not-user-controlled/document.epub",
        "tests/corpus-0.1-rc1/invalid/mapping-invalid-geometry/document.epub",
    ],
)
def test_malformed_packages_are_contained_without_internal_error(fixture: str) -> None:
    report = validate(ROOT / fixture)
    assert report.operational_status.value != "INTERNAL_ERROR"
    assert report.violation_requirement_ids


def test_all_current_corpus_fixtures_execute_without_internal_error() -> None:
    manifest = json.loads((ROOT / "tests/corpus-0.1-rc1/manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["fixtures"]) == manifest["fixtureCount"] == 107
    for fixture in manifest["fixtures"]:
        report = validate(ROOT / fixture["package"])
        assert report.operational_status.value != "INTERNAL_ERROR", fixture["id"]


def test_mapping_range_geometry_and_capability_dependencies() -> None:
    range_report = validate(ROOT / "tests/corpus-0.1-rc1/invalid/mapping-invalid-range/document.epub")
    geometry_report = validate(ROOT / "tests/corpus-0.1-rc1/invalid/mapping-invalid-geometry/document.epub")
    stale_report = validate(ROOT / "tests/corpus-0.1-rc1/invalid/mapping-with-stale-fixed/document.epub")
    assert "SPD-MAP-008" in range_report.violation_requirement_ids
    assert {"SPD-MAP-011", "SPD-MAP-012"} <= set(geometry_report.violation_requirement_ids)
    assert "SPD-STATE-007" in stale_report.violation_requirement_ids


def test_missing_epubcheck_is_operational_not_document_failure() -> None:
    report = validate(ROOT / "tests/corpus-0.1-rc1/valid/minimal-base/document.epub")
    assert report.operational_status.value == "TOOL_UNAVAILABLE"
    assert report.base == "NOT_TESTED"
    assert "SPD-BASE-002" in report.not_tested_requirement_ids
    assert "SPD-BASE-002" not in report.violation_requirement_ids


def test_malformed_container_xml_is_reported_without_escape_or_crash(tmp_path: Path) -> None:
    archive = tmp_path / "bad-container.epub"
    with ZipFile(archive, "w") as package:
        package.writestr("mimetype", b"application/epub+zip", compress_type=ZIP_STORED)
        package.writestr("META-INF/container.xml", b"<!DOCTYPE x [<!ENTITY y SYSTEM 'file:///etc/passwd'>]><x>&y;</x>", compress_type=ZIP_DEFLATED)
    report = ValidationReport(str(archive))
    opened = SecurePackage.open(archive, ResourceLimits(), report)
    try:
        discover(opened, report)
    finally:
        opened.close()
    assert {"SPD-BASE-002", "SPD-DISC-001"} <= set(report.violation_requirement_ids)
