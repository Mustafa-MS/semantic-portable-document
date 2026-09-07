from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .constants import STABLE_NODE_SELECTOR
from .descriptors import Descriptors
from .epub import PackageDocument
from .models import Outcome, ValidationReport
from .package import SecurePackage
from .schemas import SchemaStore
from .semantics import SemanticModel
from .strictjson import StrictJSONError, loads


def _selectors(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if value.get("type") == STABLE_NODE_SELECTOR:
            yield value
        for child in value.values():
            yield from _selectors(child)
    elif isinstance(value, list):
        for child in value:
            yield from _selectors(child)


def validate_annotations(
    package: SecurePackage,
    opf: PackageDocument | None,
    descriptors: Descriptors,
    semantics: SemanticModel,
    schemas: SchemaStore,
    report: ValidationReport,
) -> None:
    if opf is None or descriptors.document is None:
        return
    document_id = descriptors.document.get("documentId")
    revision = descriptors.document.get("revision") if isinstance(descriptors.document.get("revision"), dict) else {}
    revision_id = revision.get("revisionId")
    for item in opf.manifest.values():
        if item["mediaType"] not in {"application/ld+json", "application/annotation+json"}:
            continue
        path = item["path"]
        try:
            value = loads(package.read(path, limit=package.limits.max_json_bytes), max_depth=package.limits.max_json_depth)
        except StrictJSONError as exc:
            report.add("SPD-ANN-002", Outcome.FAIL, f"annotation strict JSON parse failed: {exc}", resource=path)
            continue
        for selector in _selectors(value):
            errors = schemas.errors("annotation", selector)
            requirement = "SPD-ANN-003" if selector.get("scope") == "revision" else "SPD-ANN-002"
            for error in errors:
                report.add(requirement, Outcome.FAIL, f"StableNodeSelector schema validation: {error}", resource=path, node=selector.get("nodeId"))
            if selector.get("documentId") != document_id or selector.get("nodeId") not in semantics.nodes:
                report.add(requirement, Outcome.FAIL, "StableNodeSelector document/node binding is unresolved", resource=path, node=selector.get("nodeId"))
            if selector.get("scope") == "revision" and selector.get("revisionId") != revision_id:
                report.add("SPD-ANN-003", Outcome.FAIL, "revision-scoped selector does not bind current revision", resource=path, node=selector.get("nodeId"))
            refinement = selector.get("refinement")
            if isinstance(refinement, dict) and refinement.get("type") == "TextPositionSelector":
                text = semantics.text_value(selector.get("nodeId"))
                start, end = refinement.get("start"), refinement.get("end")
                if text is not None and (not isinstance(start, int) or not isinstance(end, int) or not 0 <= start <= end <= len(text)):
                    report.add(requirement, Outcome.FAIL, "annotation scalar range is outside Node text", resource=path, node=selector.get("nodeId"))
