from __future__ import annotations

from pathlib import Path
from typing import Any

from harness.util import canonical_json, sha256_bytes, sha256_file, write_json


def create_state(output: Path, document_id: str, revision_id: str, source: Path, pdf: Path, mapping: Path, renderer: dict[str, Any], required_resources: list[Path] | None = None) -> dict[str, Any]:
    required_resources = required_resources or []
    state = {
        "schemaVersion": "0.1-experimental",
        "lifecycle": "SEALED",
        "document": document_id,
        "revision": revision_id,
        "resources": {
            "semantic": {"path": source.name, "hash": sha256_file(source), "normative": True},
            "fixed": {"path": pdf.name, "hash": sha256_file(pdf), "normative": True},
            "mapping": {"path": mapping.name, "hash": sha256_file(mapping), "normative": True},
            "required": [{"path": resource.name, "hash": sha256_file(resource), "normative": True} for resource in required_resources],
        },
        "rendererProvenance": renderer,
        "excluded": ["cache/", "debug/"],
    }
    state["descriptorHash"] = sha256_bytes(canonical_json(state))
    write_json(output, state)
    return state


def verify_state(state: dict[str, Any], source: Path, pdf: Path, mapping: Path, required_resources: list[Path] | None = None) -> dict[str, Any]:
    required_resources = required_resources or []
    actual = {"semantic": sha256_file(source), "fixed": sha256_file(pdf), "mapping": sha256_file(mapping)}
    mismatches = [name for name, digest in actual.items() if state["resources"][name]["hash"] != digest]
    expected_required = {item["path"]: item["hash"] for item in state["resources"].get("required", [])}
    actual_required = {resource.name: sha256_file(resource) for resource in required_resources}
    for name, digest in expected_required.items():
        if actual_required.get(name) != digest:
            mismatches.append("required:" + name)
    descriptor = dict(state)
    expected_descriptor_hash = descriptor.pop("descriptorHash", None)
    descriptor_ok = expected_descriptor_hash == sha256_bytes(canonical_json(descriptor))
    return {"valid": not mismatches and descriptor_ok, "mismatched_resources": mismatches, "descriptor_hash_valid": descriptor_ok}
