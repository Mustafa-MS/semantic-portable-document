from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from .descriptors import Descriptors
from .integrity import IntegrityState, sha256_digest
from .models import Outcome, ValidationReport
from .package import SecurePackage, valid_package_path
from .schemas import SchemaStore
from .semantics import SemanticModel
from .strictjson import StrictJSONError, loads


@dataclass(slots=True)
class MappingState:
    value: dict[str, Any] | None = None
    path: str | None = None


def _schema_requirement(error: str) -> str:
    if "reason" in error or "fragments" in error or "status" in error:
        return "SPD-MAP-005"
    if "coordinateSystem" in error or "pages" in error or "quad" in error:
        return "SPD-MAP-012"
    return "SPD-MAP-002"


def validate_mapping(
    package: SecurePackage,
    descriptors: Descriptors,
    integrity: IntegrityState,
    semantics: SemanticModel,
    schemas: SchemaStore,
    claimed: set[str] | None,
    report: ValidationReport,
) -> MappingState:
    result = MappingState()
    state = descriptors.state or {}
    binding = state.get("mapping")
    if claimed is None or "Mapping" not in claimed or descriptors.state is None:
        return result
    if not integrity.fixed_current or not isinstance(binding, dict):
        report.add("SPD-STATE-007", Outcome.FAIL, "Mapping claim requires current fixed rendition and mapping binding")
        return result
    path = binding.get("path")
    if not isinstance(path, str) or not valid_package_path(path) or not package.exists(path):
        report.add("SPD-STATE-007", Outcome.FAIL, "mapping binding path is unsafe or missing", resource=str(path))
        return result
    actual_hash = sha256_digest(package.read(path))
    if binding.get("sha256") != actual_hash:
        if state.get("lifecycle") == "SEALED":
            report.add("SPD-STATE-002", Outcome.FAIL, "SEALED mapping binding digest mismatch", resource=path, evidence=actual_hash)
        report.add("SPD-INT-003", Outcome.FAIL, "mapping modification detected", resource=path)
    try:
        value = loads(package.read(path, limit=package.limits.max_json_bytes), max_depth=package.limits.max_json_depth)
    except StrictJSONError as exc:
        report.add("SPD-MAP-002", Outcome.FAIL, f"mapping strict JSON parse failed: {exc}", resource=path)
        return result
    if not isinstance(value, dict):
        report.add("SPD-MAP-002", Outcome.FAIL, "mapping root is not an object", resource=path)
        return result
    result.value, result.path = value, path
    for error in schemas.errors("mapping", value):
        report.add(_schema_requirement(error), Outcome.FAIL, f"mapping schema validation: {error}", resource=path)

    document = descriptors.document or {}
    revision = document.get("revision") if isinstance(document.get("revision"), dict) else {}
    fixed = state.get("fixedRendition") if isinstance(state.get("fixedRendition"), dict) else {}
    mapped_fixed = value.get("fixedRendition") if isinstance(value.get("fixedRendition"), dict) else {}
    if (
        value.get("documentId") != document.get("documentId")
        or value.get("revisionId") != revision.get("revisionId")
        or mapped_fixed.get("id") != fixed.get("id")
        or mapped_fixed.get("sha256") != fixed.get("sha256")
    ):
        report.add("SPD-MAP-002", Outcome.FAIL, "mapping identity/fixed binding disagrees with current state", resource=path)

    pages: dict[str, tuple[float, float]] = {}
    for page in value.get("pages", []) if isinstance(value.get("pages"), list) else []:
        if not isinstance(page, dict):
            continue
        page_id = page.get("id")
        width, height = page.get("width"), page.get("height")
        if page_id in pages:
            report.add("SPD-MAP-011", Outcome.FAIL, "duplicate rendition-local Page ID", resource=path, evidence=page_id)
        if isinstance(page_id, str) and isinstance(width, (int, float)) and isinstance(height, (int, float)):
            pages[page_id] = (float(width), float(height))

    for record in value.get("records", []) if isinstance(value.get("records"), list) else []:
        if not isinstance(record, dict):
            continue
        node_id = record.get("nodeId")
        text = semantics.text_value(node_id) if isinstance(node_id, str) else None
        if text is None:
            report.add("SPD-MAP-011", Outcome.FAIL, "mapping record references unknown Node ID", resource=path, node=str(node_id))
        fragments = record.get("fragments", [])
        if not isinstance(fragments, list):
            continue
        for fragment in fragments:
            if not isinstance(fragment, dict):
                continue
            page_id = fragment.get("pageId")
            if page_id not in pages:
                report.add("SPD-MAP-011", Outcome.FAIL, "mapping fragment references unknown Page ID", resource=path, node=str(node_id), evidence=page_id)
                continue
            text_range = fragment.get("textRange")
            if isinstance(text_range, dict) and text is not None:
                start, end = text_range.get("start"), text_range.get("end")
                if (
                    text_range.get("unit") != "unicode-scalar-value"
                    or not isinstance(start, int) or isinstance(start, bool)
                    or not isinstance(end, int) or isinstance(end, bool)
                    or not (0 <= start <= end <= len(text))
                ):
                    report.add(
                        "SPD-MAP-008", Outcome.FAIL, "logical range is outside the Node Unicode-scalar-value text",
                        resource=path, node=str(node_id), evidence={"scalarLength": len(text), "range": text_range},
                    )
            quad = fragment.get("quad")
            if isinstance(quad, list) and len(quad) == 8 and all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in quad):
                width, height = pages[page_id]
                xs, ys = quad[0::2], quad[1::2]
                ordered = xs[0] <= xs[1] and xs[3] <= xs[2] and ys[0] <= ys[3] and ys[1] <= ys[2]
                bounded = all(0 <= x <= width for x in xs) and all(0 <= y <= height for y in ys)
                if not ordered or not bounded:
                    report.add("SPD-MAP-012", Outcome.FAIL, "quad is not TL-TR-BR-BL ordered and page-bounded", resource=path, node=str(node_id), evidence=quad)
                    report.add("SPD-MAP-011", Outcome.FAIL, "Mapping claim contains invalid page-bounded geometry", resource=path, node=str(node_id))
            else:
                report.add("SPD-MAP-012", Outcome.FAIL, "quad must contain eight finite numbers", resource=path, node=str(node_id))
                report.add("SPD-MAP-011", Outcome.FAIL, "Mapping claim contains invalid geometry", resource=path, node=str(node_id))
    return result
