from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CHECK_GROUPS: dict[str, set[str]] = {
    "secure_package_and_ocf": {
        "SPD-ARCH-001", "SPD-BASE-001", "SPD-BASE-002", "SPD-BASE-005", "SPD-BASE-006",
        "SPD-SEM-001", "SPD-SEM-002", "SPD-SEM-003", "SPD-FIX-003",
        "SPD-DISC-001", "SPD-DISC-002", "SPD-DISC-003",
    },
    "active_content_and_local_resources": {
        "SPD-SEC-001", "SPD-SEC-002", "SPD-SEC-003", "SPD-SEC-004", "SPD-SEC-005",
        "SPD-SEC-006", "SPD-SEC-007", "SPD-SEC-008",
    },
    "identity_and_authoritative_xhtml": {
        "SPD-SEM-011", "SPD-ID-001", "SPD-ID-002", "SPD-ID-003", "SPD-ID-004",
        "SPD-ID-005", "SPD-ID-006", "SPD-ID-008", "SPD-ID-010", "SPD-ID-013",
        "SPD-I18N-003", "SPD-I18N-005",
    },
    "annotations": {"SPD-ANN-002", "SPD-ANN-003", "SPD-ANN-004"},
    "inventory_integrity_and_state": {
        "SPD-STATE-001", "SPD-STATE-002", "SPD-STATE-003", "SPD-STATE-004", "SPD-STATE-005",
        "SPD-STATE-006", "SPD-STATE-007", "SPD-RES-001", "SPD-RES-002", "SPD-RES-003",
        "SPD-RES-004", "SPD-RES-005", "SPD-RES-006", "SPD-INT-001", "SPD-INT-002",
        "SPD-INT-003", "SPD-INT-004", "SPD-INT-005", "SPD-INT-006", "SPD-FIX-001",
    },
    "mapping_schema_and_procedural_checks": {
        "SPD-I18N-006", "SPD-MAP-001", "SPD-MAP-002", "SPD-MAP-005", "SPD-MAP-007",
        "SPD-MAP-008", "SPD-MAP-009", "SPD-MAP-010", "SPD-MAP-011", "SPD-MAP-012",
    },
    "capability_extension_and_import_semantics": {
        "SPD-PROV-001", "SPD-IMP-001", "SPD-IMP-002", "SPD-CAP-001", "SPD-CAP-002",
        "SPD-CAP-003", "SPD-EXT-001", "SPD-EXT-002", "SPD-EXT-003",
    },
}


def automated_check_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for group, ids in CHECK_GROUPS.items():
        for requirement_id in ids:
            if requirement_id in result:
                raise AssertionError(f"duplicate automated coverage entry: {requirement_id}")
            result[requirement_id] = group
    return result


def load_registry(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_coverage(registry_path: Path) -> dict[str, Any]:
    registry = load_registry(registry_path)
    checks = automated_check_map()
    entries = []
    automated_ids = {item["id"] for item in registry["requirements"] if item["testability"] == "AUTOMATED"}
    if set(checks) != automated_ids:
        raise AssertionError(
            f"automated coverage mismatch: missing={sorted(automated_ids-set(checks))}, extra={sorted(set(checks)-automated_ids)}"
        )
    for requirement in registry["requirements"]:
        testability = requirement["testability"]
        entries.append({
            "requirementId": requirement["id"],
            "testability": testability,
            "capabilities": requirement["capability"],
            "implementation": checks.get(requirement["id"], "human_or_partial_evaluation_registry"),
            "represented": True,
            "automatedExecutableCoverage": testability == "AUTOMATED",
        })
    return {
        "registryVersion": registry["registryVersion"],
        "summary": {
            "total": len(entries),
            "represented": len(entries),
            "automated": len(automated_ids),
            "automatedImplemented": len(checks),
        },
        "requirements": entries,
    }

