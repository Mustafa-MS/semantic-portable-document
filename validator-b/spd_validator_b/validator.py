from __future__ import annotations

import hashlib
import platform
import unicodedata
from pathlib import Path
from typing import Any

from .annotations import validate_annotations
from .constants import FORMAT_RC1_SHA256, REQUIREMENTS_SHA256
from .coverage import load_registry
from .descriptors import Descriptors, load_descriptors
from .epub import Discovery, discover
from .epubcheck import EPUBCheckAdapter
from .integrity import IntegrityState, validate_integrity
from .mapping import validate_mapping
from .models import (
    OperationalStatus,
    Outcome,
    PackageInvalid,
    ResourceLimitExceeded,
    ValidationOptions,
    ValidationReport,
)
from .package import SecurePackage
from .passive import validate_passive
from .policy import policy
from .schemas import SchemaStore, find_repository_root
from .semantics import SemanticModel, validate_semantics


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _claims(descriptors: Descriptors) -> set[str] | None:
    document = descriptors.document
    if document is None or not isinstance(document.get("capabilities"), list):
        return None
    result: set[str] = set()
    capabilities = document.get("capabilities")
    if isinstance(capabilities, list):
        for capability in capabilities:
            if isinstance(capability, dict) and isinstance(capability.get("id"), str):
                result.add(capability["id"])
    return result


def _validate_capabilities(
    discovery: Discovery, descriptors: Descriptors, claimed: set[str] | None, report: ValidationReport
) -> None:
    if claimed is None:
        return
    if "Base" not in claimed:
        report.add("SPD-CAP-002", Outcome.FAIL, "Base 0.1 capability declaration is required")
    if discovery.package_document and discovery.package_document.capabilities != claimed:
        report.add(
            "SPD-CAP-003", Outcome.FAIL, "OPF capability discovery and document-state claim sets disagree",
            evidence={"opf": sorted(discovery.package_document.capabilities), "descriptor": sorted(claimed)},
        )
    document = descriptors.document or {}
    extensions = document.get("extensions")
    if isinstance(extensions, list):
        unsupported: set[str] = set()
        for extension in extensions:
            if not isinstance(extension, dict):
                continue
            extension_id = extension.get("id")
            if not isinstance(extension_id, str) or ":" not in extension_id:
                report.add("SPD-EXT-001", Outcome.FAIL, "extension identifier is not globally unique", evidence=extension_id)
            if "required" not in extension or not isinstance(extension.get("required"), bool):
                report.add("SPD-EXT-002", Outcome.FAIL, "extension does not declare required/optional status", evidence=extension_id)
            if extension.get("required") is True:
                unsupported.update(str(value) for value in extension.get("capabilities", []))
        if unsupported:
            report.metadata["unsupportedCapabilities"] = sorted(unsupported)


def _roll_up(report: ValidationReport, registry: dict[str, Any], claimed: set[str] | None, epubcheck_available: bool) -> None:
    requirements = {item["id"]: item for item in registry["requirements"]}
    failed = set(report.violation_requirement_ids)
    not_tested = set(report.not_tested_requirement_ids)
    base_failed = any("Base" in requirements.get(req, {}).get("capability", []) for req in failed)
    if base_failed:
        report.base = "FAIL"
    elif not epubcheck_available or any("Base" in requirements.get(req, {}).get("capability", []) for req in not_tested - {"SPD-ID-013", "SPD-ACC-001", "SPD-ACC-004", "SPD-PASS-001", "SPD-PASS-002", "SPD-PASS-003", "SPD-RS-001", "SPD-RS-002"}):
        report.base = "NOT_TESTED"
    else:
        report.base = "PASS"

    for capability in ("Mapping", "Accessible"):
        if claimed is None:
            report.normative_capabilities[capability] = "UNKNOWN"
            continue
        if capability not in claimed:
            report.normative_capabilities[capability] = "NOT_CLAIMED"
            continue
        relevant_failed = {
            req for req in failed if capability in requirements.get(req, {}).get("capability", [])
        }
        if report.base == "FAIL" or relevant_failed:
            report.normative_capabilities[capability] = "FAIL"
        elif capability == "Accessible" or any(
            capability in requirements.get(req, {}).get("capability", []) for req in not_tested
        ) or report.base == "NOT_TESTED":
            report.normative_capabilities[capability] = "NOT_TESTED"
        else:
            report.normative_capabilities[capability] = "PASS"
    for capability in ("Archive-Experimental", "Fixed-Experimental"):
        report.experimental_capabilities[capability] = (
            "UNKNOWN" if claimed is None else "PRESENT_EXPERIMENTAL" if capability in claimed else "NOT_CLAIMED"
        )

    for requirement in registry["requirements"]:
        req = requirement["id"]
        if req in failed:
            status = "FAIL"
        elif req in not_tested:
            status = "NOT_TESTED"
        elif req == "SPD-STATE-001" or (
            req in {"SPD-STATE-002", "SPD-STATE-003", "SPD-STATE-006"}
            and report.metadata.get("lifecycle") == "EDITABLE"
        ):
            status = "NOT_APPLICABLE"
        elif requirement["testability"] == "INFORMATIVE_ONLY":
            status = "INFORMATIVE"
        elif requirement["testability"] in {"MANUAL", "PARTIALLY_AUTOMATED"}:
            status = "NOT_TESTED"
        else:
            status = "NOT_TESTED"
        report.requirement_outcomes[req] = status


def validate(path: str | Path, options: ValidationOptions | None = None) -> ValidationReport:
    input_path = Path(path).resolve()
    options = options or ValidationOptions()
    report = ValidationReport(str(input_path))
    repository = find_repository_root(input_path.parent)
    rc1_hash = _file_hash(repository / "spec" / "FORMAT_0.1_RC1.md")
    requirements_hash = _file_hash(repository / "spec" / "requirements-0.1-rc1.yaml")
    report.metadata.update({
        "validatorBVersion": "0.1.3-rc1",
        "differentialContract": "0.1.2",
        "formatRc1Sha256": rc1_hash,
        "requirementsSha256": requirements_hash,
        "python": platform.python_version(),
        "unicodeData": unicodedata.unidata_version,
        "environmentDifferences": ["IMPLEMENTATION_ENVIRONMENT_DIFFERENCE: Unicode data 15.1.0"]
        if unicodedata.unidata_version == "15.1.0" else [],
    })
    if rc1_hash != FORMAT_RC1_SHA256 or requirements_hash != REQUIREMENTS_SHA256:
        report.operational_status = OperationalStatus.SPEC_BLOCKER
        report.add("SPD-BASE-001", Outcome.NOT_TESTED, "INPUT_VERSION_MISMATCH: frozen normative input hash differs")
        return report
    registry = load_registry(repository / "spec" / "requirements-0.1-rc1.yaml")
    schemas = SchemaStore(repository / "schemas" / "rc1")
    adapter = EPUBCheckAdapter.detect(options)
    package: SecurePackage | None = None
    discovery = Discovery()
    descriptors = Descriptors()
    integrity = IntegrityState()
    semantics = SemanticModel()
    claimed: set[str] = set()
    try:
        package = SecurePackage.open(input_path, options.limits, report)
        if package.exists("mimetype"):
            if package.read("mimetype") != b"application/epub+zip":
                report.add("SPD-BASE-001", Outcome.FAIL, "EPUB mimetype entry has incorrect exact bytes", resource="mimetype")
            first = package.zip.infolist()[0] if package.zip.infolist() else None
            if first is None or first.filename != "mimetype" or first.compress_type != 0:
                report.add("SPD-BASE-002", Outcome.FAIL, "EPUB mimetype must be first and stored", resource="mimetype")
        else:
            report.add("SPD-BASE-001", Outcome.FAIL, "EPUB mimetype entry is missing")
        validate_passive(package, report)
        discovery = discover(package, report)
        descriptors = load_descriptors(package, discovery, schemas, report)
        claimed = _claims(descriptors)
        report.metadata["lifecycle"] = descriptors.state.get("lifecycle") if descriptors.state is not None else None
        report.metadata["authoritativeClaimsStatus"] = "UNKNOWN" if claimed is None else "KNOWN"
        for kind in ("document", "inventory", "state"):
            if getattr(descriptors, kind) is None:
                for req in policy()["blocked"][kind]:
                    report.add(req, Outcome.NOT_TESTED, f"required {kind} descriptor authority is unavailable", evidence={"blockedBy": kind})
        fixed_info = descriptors.state.get("fixedRendition", {}) if descriptors.state is not None else None
        report.metadata["experimentalReporting"] = {
            "physicalFixedRenditionPresent": None if fixed_info is None else bool(fixed_info.get("path") and package.exists(fixed_info["path"])),
            "fixedExperimentalCapabilityDeclared": None if claimed is None else "Fixed-Experimental" in claimed,
            "fixedExperimentalEvaluationStatus": "UNKNOWN" if claimed is None else "NOT_TESTED" if "Fixed-Experimental" in claimed else "NOT_CLAIMED",
        }
        _validate_capabilities(discovery, descriptors, claimed, report)
        integrity = validate_integrity(package, discovery, descriptors, report)
        semantics = validate_semantics(package, discovery.package_document, report)
        validate_annotations(package, discovery.package_document, descriptors, semantics, schemas, report)
        validate_mapping(package, descriptors, integrity, semantics, schemas, claimed, report)
        if not options.lineage_evidence:
            report.add(
                "SPD-ID-013", Outcome.NOT_TESTED,
                "historical Node-ID persistence and retired-ID reuse require unavailable lineage evidence",
            )
        if claimed is not None and "Accessible" in claimed:
            report.add(
                "SPD-ACC-001", Outcome.NOT_TESTED,
                "qualitative accessibility of authoritative semantic XHTML requires human evaluation",
            )
            report.add(
                "SPD-ACC-004", Outcome.NOT_TESTED,
                "Accessible 0.1 requires unresolved human WCAG 2.2 AA evaluation",
            )
        adapter.validate(input_path, report)
    except ResourceLimitExceeded as exc:
        report.operational_status = OperationalStatus.RESOURCE_LIMIT
        report.metadata["operationalError"] = str(exc)
        claimed = None
        for row in registry['requirements']:
            if row['testability'] == 'AUTOMATED':
                report.add(row['id'], Outcome.NOT_TESTED, 'package inspection stopped at an implementation limit')
        adapter.validate(input_path, report)
    except PackageInvalid as exc:
        report.operational_status = OperationalStatus.MALFORMED_INPUT
        report.metadata['operationalError'] = str(exc)
        claimed = None
        for row in registry['requirements']:
            if row['testability'] == 'AUTOMATED':
                report.add(row['id'], Outcome.NOT_TESTED, 'malformed container prevented package inspection')
        adapter.validate(input_path, report)
    except Exception as exc:  # noqa: BLE001 - API boundary contains hostile-input crashes.
        report.operational_status = OperationalStatus.INTERNAL_ERROR
        report.metadata["internalError"] = f"{type(exc).__name__}: {exc}"
    finally:
        if package is not None:
            package.close()
    for rid in ('SPD-PASS-001', 'SPD-PASS-002', 'SPD-PASS-003', 'SPD-RS-001', 'SPD-RS-002'):
        if rid not in report.violation_requirement_ids:
            report.add(rid, Outcome.NOT_TESTED, 'human semantic/processor portion not evaluated by package validator')
    _roll_up(report, registry, claimed, adapter.command is not None)
    return report
