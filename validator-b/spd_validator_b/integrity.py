from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from typing import Any

import rfc8785

from .descriptors import Descriptors
from .epub import Discovery
from .models import Outcome, ValidationReport
from .package import SecurePackage, valid_package_path


def sha256_digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def projection_digest(resources: list[dict[str, Any]], effects: set[str]) -> str:
    records: list[tuple[bytes, bytes]] = []
    for entry in resources:
        affects = set(entry.get("affects", []))
        if affects & effects:
            path = entry["path"]
            encoded_path = path.encode("utf-8")
            record = (
                encoded_path + b"\0" + str(entry["byteLength"]).encode("ascii") + b"\0"
                + entry["sha256"].encode("ascii") + b"\n"
            )
            records.append((encoded_path, record))
    records.sort(key=lambda pair: pair[0])
    return sha256_digest(b"".join(record for _, record in records))


def lifecycle_descriptor_digest(state: dict[str, Any]) -> str:
    projected = dict(state)
    projected.pop("descriptorDigest", None)
    return sha256_digest(rfc8785.dumps(projected))


@dataclass(slots=True)
class IntegrityState:
    fixed_current: bool = False
    inventory_by_path: dict[str, dict[str, Any]] | None = None


def validate_integrity(
    package: SecurePackage, discovery: Discovery, descriptors: Descriptors, report: ValidationReport
) -> IntegrityState:
    result = IntegrityState(inventory_by_path={})
    document = descriptors.document
    inventory = descriptors.inventory
    state = descriptors.state
    if inventory is None:
        return result

    document_known = document is not None
    state_known = state is not None
    document = document if document_known else {}
    state = state if state_known else {}
    document_id = document.get("documentId")
    revision = document.get("revision") if isinstance(document.get("revision"), dict) else {}
    revision_id = revision.get("revisionId")
    if document_id and discovery.package_document and discovery.package_document.document_id != document_id:
        report.add("SPD-ID-001", Outcome.FAIL, "OPF and document-state Document IDs disagree", resource=discovery.rootfile)
    for name, value in (("inventory", inventory), ("state", state)):
        if not document_known or (name == "state" and not state_known):
            continue
        if value.get("documentId") != document_id:
            report.add("SPD-ID-001", Outcome.FAIL, f"{name} Document ID disagrees with document-state", resource=descriptors.paths.get("resource-inventory" if name == "inventory" else "lifecycle-state"))
        if value.get("revisionId") != revision_id:
            report.add("SPD-ID-002", Outcome.FAIL, f"{name} Revision ID disagrees with document-state", resource=descriptors.paths.get("resource-inventory" if name == "inventory" else "lifecycle-state"))

    resources = inventory.get("resources")
    if not isinstance(resources, list):
        return result
    inventory_path = descriptors.paths.get("resource-inventory")
    state_path = descriptors.paths.get("lifecycle-state") or report.metadata.get("descriptorCandidatePaths", {}).get("lifecycle-state")
    exceptions = {path for path in (inventory_path, state_path) if path}
    seen: set[str] = set()
    for entry in resources:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if not isinstance(path, str):
            continue
        if path in seen:
            report.add("SPD-RES-001", Outcome.FAIL, "duplicate inventory resource path", resource=path)
        seen.add(path)
        result.inventory_by_path[path] = entry
        if not valid_package_path(path) or unicodedata.normalize("NFC", path) != path:
            report.add("SPD-RES-002", Outcome.FAIL, "inventory path is unsafe or not NFC", resource=path)
        if path in exceptions:
            report.add("SPD-RES-003", Outcome.FAIL, "inventory includes a self-reference exception", resource=path)
            continue
        if not package.exists(path):
            report.add("SPD-RES-003", Outcome.FAIL, "inventory entry names a missing ZIP resource", resource=path)
            continue
        data = package.read(path)
        actual_length = len(data)
        actual_hash = sha256_digest(data)
        if entry.get("byteLength") != actual_length or entry.get("sha256") != actual_hash:
            report.add(
                "SPD-RES-004", Outcome.FAIL, "inventory byte length or digest does not match exact decompressed bytes",
                resource=path, evidence={"actualByteLength": actual_length, "actualSha256": actual_hash},
            )
            report.add("SPD-INT-003", Outcome.FAIL, "resource modification detected by integrity verification", resource=path)
            if state.get("lifecycle") == "SEALED" and "semantic" in entry.get("affects", []):
                report.add("SPD-STATE-003", Outcome.FAIL, "semantic-affecting resource bytes changed after sealing", resource=path)
            if state.get("lifecycle") == "SEALED" and (
                entry.get("mediaType") in {"application/ld+json", "application/annotation+json"}
                or "annotation" in path.lower()
            ):
                report.add(
                    "SPD-ANN-004", Outcome.FAIL,
                    "in-package annotation change invalidates the sealed inventory binding",
                    resource=path,
                )

    expected = package.paths - exceptions
    unlisted = expected - seen
    for path in sorted(unlisted):
        report.add("SPD-RES-003", Outcome.FAIL, "ZIP resource is absent from the complete inventory", resource=path)
        report.add("SPD-RES-006", Outcome.FAIL, "unlisted ZIP resource is prohibited", resource=path)
    extra = seen - expected
    for path in sorted(extra - exceptions):
        report.add("SPD-RES-003", Outcome.FAIL, "inventory resource does not correspond to one ZIP entry", resource=path)

    semantic_digest = projection_digest(resources, {"semantic"})
    rendition_digest = projection_digest(resources, {"semantic", "rendering"})
    if (document_known and document.get("semanticStateDigest") != semantic_digest) or (state_known and state.get("semanticStateDigest") != semantic_digest):
        report.add("SPD-INT-004", Outcome.FAIL, "semanticStateDigest does not match the normative inventory projection", evidence=semantic_digest)
    if (document_known and document.get("renditionInputDigest") != rendition_digest) or (state_known and state.get("renditionInputDigest") != rendition_digest):
        report.add("SPD-INT-005", Outcome.FAIL, "renditionInputDigest does not match the normative inventory projection", evidence=rendition_digest)

    if inventory_path and isinstance(state.get("inventory"), dict):
        binding = state["inventory"]
        actual = sha256_digest(package.read(inventory_path))
        if binding.get("path") != inventory_path or binding.get("sha256") != actual:
            if state.get("lifecycle") == "SEALED":
                report.add("SPD-STATE-002", Outcome.FAIL, "SEALED state does not bind the discovered exact inventory bytes", resource=state_path, evidence=actual)
            report.add("SPD-INT-003", Outcome.FAIL, "inventory modification detected", resource=inventory_path)

    if not state_known:
        return result
    try:
        expected_descriptor = lifecycle_descriptor_digest(state)
    except (rfc8785.CanonicalizationError, ValueError, TypeError) as exc:
        report.add("SPD-INT-006", Outcome.FAIL, f"state descriptor is not JCS-canonicalizable I-JSON: {exc}", resource=state_path)
    else:
        if state.get("descriptorDigest") != expected_descriptor:
            report.add("SPD-INT-006", Outcome.FAIL, "descriptorDigest does not match RFC 8785 projection", resource=state_path, evidence=expected_descriptor)

    fixed = state.get("fixedRendition")
    if isinstance(fixed, dict) and fixed.get("status") in {"current", "stale"}:
        fixed_path = fixed.get("path")
        fixed_hash_ok = isinstance(fixed_path, str) and package.exists(fixed_path) and sha256_digest(package.read(fixed_path)) == fixed.get("sha256")
        result.fixed_current = (
            fixed.get("status") == "current"
            and fixed.get("revisionId") == revision_id
            and fixed.get("renditionInputDigest") == rendition_digest
            and fixed_hash_ok
        )
        if fixed.get("status") == "current" and not result.fixed_current:
            report.add("SPD-STATE-005", Outcome.FAIL, "declared-current fixed rendition fails revision/input/resource binding", resource=fixed_path)
        if state.get("lifecycle") == "SEALED" and not result.fixed_current:
            report.add("SPD-STATE-006", Outcome.FAIL, "SEALED state may not contain a stale fixed rendition", resource=state_path)
    elif isinstance(fixed, dict) and fixed.get("status") == "absent":
        result.fixed_current = False
    return result
