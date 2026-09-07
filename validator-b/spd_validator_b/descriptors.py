from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .epub import Discovery
from .models import Outcome, ValidationReport
from .package import SecurePackage
from .schemas import SchemaStore
from .strictjson import StrictJSONError, loads


@dataclass(slots=True)
class Descriptors:
    document: dict[str, Any] | None = None
    inventory: dict[str, Any] | None = None
    state: dict[str, Any] | None = None
    paths: dict[str, str] = field(default_factory=dict)


def _schema_requirement(kind: str, message: str) -> str:
    if kind == "document-state":
        if "documentId" in message:
            return "SPD-ID-001"
        if "revision" in message or "revisionId" in message:
            return "SPD-ID-002"
        if "capabilit" in message or "status" in message:
            return "SPD-CAP-002"
        if "extension" in message or "uri" in message:
            return "SPD-EXT-001"
        return "SPD-BASE-005"
    if kind == "resource-inventory":
        return "SPD-RES-005" if "affects" in message else "SPD-RES-002"
    return "SPD-STATE-006"


def load_descriptors(
    package: SecurePackage, discovery: Discovery, schemas: SchemaStore, report: ValidationReport
) -> Descriptors:
    result = Descriptors(paths=dict(discovery.descriptors))
    targets = {
        "document-state": "document",
        "resource-inventory": "inventory",
        "lifecycle-state": "state",
    }
    for kind, attr in targets.items():
        path = discovery.descriptors.get(kind)
        if path is None:
            continue
        try:
            data = package.read(path, limit=package.limits.max_json_bytes)
            value = loads(data, max_depth=package.limits.max_json_depth)
        except (StrictJSONError, UnicodeError) as exc:
            report.add(_schema_requirement(kind, str(exc)), Outcome.FAIL, f"strict JSON parse failed: {exc}", resource=path)
            continue
        if not isinstance(value, dict):
            report.add(_schema_requirement(kind, "root"), Outcome.FAIL, "descriptor JSON root must be an object", resource=path)
            continue
        errors = schemas.errors(kind, value)
        for error in errors:
            report.add(_schema_requirement(kind, error), Outcome.FAIL, f"schema validation: {error}", resource=path)
        setattr(result, attr, value)
    return result

