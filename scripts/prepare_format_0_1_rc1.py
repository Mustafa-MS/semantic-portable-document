"""Prepare deterministic Format 0.1 RC1 publication inputs.

This script creates versioned RC1 artifacts. It never edits the frozen Draft,
the Draft registry, the Draft schema bundle, Corpus 0.1.2, or validation freezes.
Identifier migration changes lexical identifiers and package bytes only; it
preserves every reviewed expected conformance result.
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import re
import shutil
import struct
import uuid
import zipfile
from pathlib import Path

import rfc8785
ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "tests/corpus-0.1.2/manifest.json"
DEST = ROOT / "tests/corpus-0.1-rc1"
SCHEMA_DEST = ROOT / "schemas/rc1"
PROFILE_DEST = ROOT / "spec/profiles-0.1-rc1"

UUID_NAMESPACE = uuid.NAMESPACE_URL


def assigned(name: str) -> str:
    return "urn:uuid:" + str(uuid.uuid5(UUID_NAMESPACE, "spd-format-0.1:" + name))


SCHEMA_IDS = {
    "document-state.schema.json": assigned("schema:document-state"),
    "resource-inventory.schema.json": assigned("schema:resource-inventory"),
    "state.schema.json": assigned("schema:lifecycle-state"),
    "mapping.schema.json": assigned("schema:mapping"),
    "annotation-extension.schema.json": assigned("schema:annotation-extension"),
    "conformance-result.schema.json": assigned("schema:conformance-result"),
}

RELATIONSHIPS = {
    "document-state": assigned("rel:document-state"),
    "resource-inventory": assigned("rel:resource-inventory"),
    "lifecycle-state": assigned("rel:lifecycle-state"),
}

CAPABILITIES = {
    name: assigned(f"capability:{name}:0.1")
    for name in (
        "Base",
        "Mapping",
        "Accessible",
        "Fixed-Experimental",
        "Archive-Experimental",
    )
}

ANNOTATION_TERMS = {
    "StableNodeSelector": assigned("vocabulary:StableNodeSelector"),
    "documentId": assigned("vocabulary:documentId"),
    "nodeId": assigned("vocabulary:nodeId"),
    "scope": assigned("vocabulary:scope"),
    "revisionId": assigned("vocabulary:revisionId"),
    "refinement": assigned("vocabulary:refinement"),
}

OLD_RELATIONSHIPS = {
    "document-state": "https://example.invalid/spd/rel/document-state",
    "resource-inventory": "https://example.invalid/spd/rel/resource-inventory",
    "lifecycle-state": "https://example.invalid/spd/rel/lifecycle-state",
}
OLD_CAPABILITIES = {
    name: f"https://example.invalid/spd/capability/{name}/0.1" for name in CAPABILITIES
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tagged(data: bytes) -> str:
    return "sha256:" + sha256(data)


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def projection(inventory: dict, effects: set[str]) -> str | None:
    resources = inventory.get("resources")
    if not isinstance(resources, list):
        return None
    selected = []
    for item in resources:
        if not isinstance(item, dict) or not effects.intersection(item.get("affects", [])):
            continue
        if not all(key in item for key in ("path", "byteLength", "sha256")):
            return None
        selected.append(item)
    selected.sort(key=lambda item: item["path"].encode("utf-8"))
    payload = b"".join(
        item["path"].encode("utf-8")
        + b"\0"
        + str(item["byteLength"]).encode("ascii")
        + b"\0"
        + item["sha256"].encode("ascii")
        + b"\n"
        for item in selected
    )
    return tagged(payload)


def replace_public_identifiers(data: bytes) -> bytes:
    for key, old in OLD_RELATIONSHIPS.items():
        data = data.replace(old.encode("ascii"), RELATIONSHIPS[key].encode("ascii"))
    for key, old in OLD_CAPABILITIES.items():
        data = data.replace(old.encode("ascii"), CAPABILITIES[key].encode("ascii"))
    return data


def migrate_annotation(value: object) -> bool:
    changed = False
    if isinstance(value, dict):
        if value.get("type") == "StableNodeSelector":
            value["type"] = ANNOTATION_TERMS["StableNodeSelector"]
            changed = True
        for child in value.values():
            changed = migrate_annotation(child) or changed
    elif isinstance(value, list):
        for child in value:
            changed = migrate_annotation(child) or changed
    return changed


def migrate_annotation_document(data: bytes) -> bytes:
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return data
    if not migrate_annotation(value):
        return data
    context = value.get("@context") if isinstance(value, dict) else None
    extension_context = copy.deepcopy(ANNOTATION_TERMS)
    if isinstance(value, dict):
        if isinstance(context, list):
            value["@context"] = [*context, extension_context]
        elif context is None:
            value["@context"] = extension_context
        else:
            value["@context"] = [context, extension_context]
    return encoded(value)


def read_entries(path: Path, repair_header: bool) -> tuple[list[tuple[zipfile.ZipInfo, bytes]], bool]:
    raw = path.read_bytes()
    if repair_header:
        repaired = bytearray(raw)
        if repaired[30:38] != b"Mimetype":
            raise AssertionError(f"unexpected malformed fixture header in {path}")
        repaired[30] = ord("m")
        raw = bytes(repaired)
    result = []
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for info in archive.infolist():
            result.append((info, archive.read(info)))
    return result, repair_header


def descriptor_digest(value: dict) -> str | None:
    try:
        projected = {key: item for key, item in value.items() if key != "descriptorDigest"}
        return tagged(rfc8785.dumps(projected))
    except (ValueError, TypeError):
        return None


def migrate_package(source: Path, fixture_id: str) -> bytes:
    malformed = fixture_id == "security/zip-header-mismatch"
    entries, _ = read_entries(source, malformed)
    old = {info.filename: data for info, data in entries}
    new = dict(old)

    for path, data in list(new.items()):
        migrated = replace_public_identifiers(data)
        if path.endswith("annotations.json"):
            migrated = migrate_annotation_document(migrated)
        new[path] = migrated

    inventory_path = "META-INF/spd/inventory.json"
    document_path = "META-INF/spd/document-state.json"
    state_path = "META-INF/spd/state.json"
    try:
        old_inventory = json.loads(old[inventory_path])
        inventory = copy.deepcopy(old_inventory)
        old_document = json.loads(old[document_path])
        document = copy.deepcopy(old_document)
        old_state = json.loads(old[state_path])
        state = copy.deepcopy(old_state)
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError):
        old_inventory = inventory = old_document = document = old_state = state = None

    if isinstance(inventory, dict) and isinstance(inventory.get("resources"), list):
        for item in inventory["resources"]:
            if not isinstance(item, dict):
                continue
            path = item.get("path")
            if path in old and path in new:
                was_bound = item.get("byteLength") == len(old[path]) and item.get("sha256") == tagged(old[path])
                if was_bound:
                    item["byteLength"] = len(new[path])
                    item["sha256"] = tagged(new[path])

        old_semantic = projection(old_inventory, {"semantic"})
        old_rendering = projection(old_inventory, {"semantic", "rendering"})
        new_semantic = projection(inventory, {"semantic"})
        new_rendering = projection(inventory, {"semantic", "rendering"})
        for descriptor in (document, state):
            if isinstance(descriptor, dict):
                if descriptor.get("semanticStateDigest") == old_semantic:
                    descriptor["semanticStateDigest"] = new_semantic
                if descriptor.get("renditionInputDigest") == old_rendering:
                    descriptor["renditionInputDigest"] = new_rendering
        fixed = state.get("fixedRendition") if isinstance(state, dict) else None
        if isinstance(fixed, dict) and fixed.get("renditionInputDigest") == old_rendering:
            fixed["renditionInputDigest"] = new_rendering

        new[document_path] = encoded(document)
        for item in inventory["resources"]:
            if not isinstance(item, dict) or item.get("path") != document_path:
                continue
            if item.get("byteLength") == len(old[document_path]) and item.get("sha256") == tagged(old[document_path]):
                item["byteLength"] = len(new[document_path])
                item["sha256"] = tagged(new[document_path])

        new[inventory_path] = encoded(inventory)
        if isinstance(state, dict):
            binding = state.get("inventory")
            if isinstance(binding, dict) and binding.get("sha256") == tagged(old[inventory_path]):
                binding["sha256"] = tagged(new[inventory_path])
            if state.get("descriptorDigest") == descriptor_digest(old_state):
                state["descriptorDigest"] = descriptor_digest(state)
            new[state_path] = encoded(state)

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        for old_info, _ in entries:
            info = zipfile.ZipInfo(old_info.filename, (2026, 9, 6, 0, 0, 0))
            info.compress_type = old_info.compress_type
            info.create_system = old_info.create_system
            info.external_attr = old_info.external_attr
            info.internal_attr = old_info.internal_attr
            info.flag_bits = old_info.flag_bits
            archive.writestr(info, new[old_info.filename])
    data = output.getvalue()
    if malformed:
        broken = bytearray(data)
        if broken[30:38] != b"mimetype":
            raise AssertionError("deterministic output did not place mimetype first")
        broken[30] = ord("M")
        data = bytes(broken)
    return data


def write_specification() -> None:
    source = (ROOT / "spec/FORMAT_0.1_DRAFT.md").read_text(encoding="utf-8")
    text = source
    text = text.replace("## Draft Specification", "## Release Candidate 1")
    text = text.replace("**Working name:** SPD", "**Technical name:** SPD")
    text = text.replace("**File extension:** Not yet assigned", "**File extension:** Not assigned in Format 0.1 RC1")
    text = text.replace("**Media type:** Not yet assigned", "**Media type:** No SPD-specific media type assigned in Format 0.1 RC1")
    text = text.replace(
        "**Status:** Draft specification — pre-RC passive security clarification; not RC1",
        "**Status:** Format 0.1 Release Candidate 1 — external review",
    )
    text = text.replace(
        "The working name and identifiers are provisional and do not form part of conformance.",
        "SPD is a semantic portable-document format. Its Format 0.1 packaging profile is a strict conforming subset of the pinned EPUB 3.3 baseline.",
    )
    text = text.replace(
        "The Draft provisional type name is `StableNodeSelector`. A stable public IRI/context is REQUIRED before Release Candidate (section 75).",
        f"The selector type expands to the stable IRI `{ANNOTATION_TERMS['StableNodeSelector']}`. Its compact extension terms are mapped by the inline context defined in the annotation profile and identifier registry.",
    )
    for key, old in OLD_RELATIONSHIPS.items():
        text = text.replace(old, RELATIONSHIPS[key])
    text = text.replace(
        "Each href MUST be a safe OCF root-relative path-relative-scheme-less URL resolving to exactly one existing entry. Duplicate, missing, wrong-media-type, unresolved, or conflicting links fail Base. The provisional relationship identifiers are replaced before Release Candidate.",
        "Each href MUST be a safe OCF root-relative path-relative-scheme-less URL resolving to exactly one existing entry. Duplicate, missing, wrong-media-type, unresolved, or conflicting links fail Base. Relationship IRIs are permanent and MUST NOT be reassigned.",
    )
    text = text.replace(
        "# 75. Specification Governance and Release Candidate Blockers",
        "# 75. Specification Governance and Identifier Stability",
    )
    text = text.replace(
        "Before Format 0.1 Release Candidate, stable project-controlled identifiers MUST replace all `https://example.invalid/spd/` schema IDs, capability IRIs, container relationship identifiers, and the StableNodeSelector vocabulary/context. No production domain is assigned in this Draft.",
        "Format 0.1 public identifiers are the project-assigned UUID URNs in [IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md](IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md). They are permanent, globally unique IRIs and MUST NOT be reassigned. They make no DNS-ownership or IANA-registration claim.",
    )
    text = text.replace(
        "# Appendix A. Candidate-to-Draft Change Log",
        "# Appendix A. Prior Candidate-to-Draft Change Log (Historical)",
    )
    text = text.replace("PDF/A-4 is the current reference archival fixed-rendition target.", "PDF/A-4 is the Format 0.1 reference archival fixed-rendition target.")
    text = text.replace(
        "* a new cryptographic trust infrastructure.\n",
        "* a new cryptographic trust infrastructure.\n\nFormat 0.1 defers digital-signature profiles, encryption/DRM, functional forms, an interactive or scripting capability, collaboration and tracked changes, and a final agent API specification. Their mention does not define or reserve their future design.\n",
    )
    text = text.replace("| Decision | Draft sections | Normative result |", "| Decision | Format sections | Normative result |")
    text = text.replace("Detailed technology restrictions in [XHTML](profiles/xhtml-profile.md), [CSS](profiles/css-profile.md), [SVG](profiles/svg-profile.md), [MathML](profiles/mathml-profile.md) and [resource resolution](profiles/passive-resource-profile.md)", "Detailed technology restrictions in [XHTML](profiles-0.1-rc1/xhtml-profile.md), [CSS](profiles-0.1-rc1/css-profile.md), [SVG](profiles-0.1-rc1/svg-profile.md), [MathML](profiles-0.1-rc1/mathml-profile.md) and [resource resolution](profiles-0.1-rc1/passive-resource-profile.md)")
    (ROOT / "spec/FORMAT_0.1_RC1.md").write_text(text, encoding="utf-8")


def write_registry() -> None:
    text = (ROOT / "spec/requirements.yaml").read_text(encoding="utf-8")
    text = text.replace('registryVersion: "0.1-draft"', 'registryVersion: "0.1-rc1"')
    text = text.replace("source: spec/FORMAT_0.1_DRAFT.md", "source: spec/FORMAT_0.1_RC1.md")
    iri_lines = ["publicCapabilityIris:"] + [f"  {name}: {iri}" for name, iri in CAPABILITIES.items()]
    text = text.replace("requirements:\n", "\n".join(iri_lines) + "\nrequirements:\n", 1)
    text = text.replace(
        "The StableNodeSelector vocabulary and namespace are registered before final 0.1 publication.",
        "The StableNodeSelector type and extension terms use the stable project-assigned IRIs recorded in the Format 0.1 identifier registry.",
    )
    text = text.replace(
        "Each SPD descriptor link has the exact provisional relationship token, application/json media type, and a safe path resolving to one existing resource.",
        "Each SPD descriptor link has the exact registered Format 0.1 relationship IRI, application/json media type, and a safe path resolving to one existing resource.",
    )
    text = text.replace(
        "Provisional descriptor, capability, schema, and annotation identifiers are replaced by stable project-controlled identifiers before Release Candidate.",
        "Schema, capability, descriptor-relationship, and annotation identifiers are stable project-assigned IRIs recorded in the Format 0.1 identifier registry.",
    )
    (ROOT / "spec/requirements-0.1-rc1.yaml").write_text(text, encoding="utf-8")


def write_schemas() -> None:
    SCHEMA_DEST.mkdir(parents=True, exist_ok=True)
    manifest = {"bundle": "SPD Format 0.1 RC1 canonical schemas", "schemaDraft": "2020-12", "schemas": []}
    for name, schema_id in SCHEMA_IDS.items():
        source_path = ROOT / "schemas" / name
        value = json.loads(source_path.read_text(encoding="utf-8"))
        value["$id"] = schema_id
        if name == "annotation-extension.schema.json":
            value["properties"]["type"]["const"] = ANNOTATION_TERMS["StableNodeSelector"]
        data = encoded(value)
        (SCHEMA_DEST / name).write_bytes(data)
        manifest["schemas"].append(
            {
                "file": name,
                "id": schema_id,
                "sha256": sha256(data),
                "draftSourceSha256": sha256(source_path.read_bytes()),
            }
        )
    (SCHEMA_DEST / "manifest.json").write_bytes(encoded(manifest))
    (SCHEMA_DEST / "README.md").write_text(
        "# Format 0.1 RC1 canonical schema bundle\n\n"
        "These are the six canonical Draft 2020-12 schemas for RC1. Compared with the frozen Draft bundle, only stable `$id` values and the StableNodeSelector type IRI changed. Structural validation semantics are unchanged. `manifest.json` records both Draft and RC1 hashes.\n",
        encoding="utf-8",
    )


def write_profiles() -> None:
    if PROFILE_DEST.exists():
        shutil.rmtree(PROFILE_DEST)
    shutil.copytree(ROOT / "spec/profiles", PROFILE_DEST)
    ocf = (PROFILE_DEST / "ocf-profile.md").read_text(encoding="utf-8")
    for key, old in OLD_RELATIONSHIPS.items():
        ocf = ocf.replace(old, RELATIONSHIPS[key])
    ocf = ocf.replace("each provisional relationship", "each Format 0.1 relationship IRI")
    ocf = ocf.replace("- The provisional identifiers MUST be replaced with stable project-controlled identifiers before Release Candidate.\n", "- Relationship IRIs are stable, project-assigned, and MUST NOT be reassigned.\n")
    (PROFILE_DEST / "ocf-profile.md").write_text(ocf, encoding="utf-8")

    caps = (PROFILE_DEST / "capabilities-profile.md").read_text(encoding="utf-8")
    caps = caps.replace(
        "Provisional capability IRIs under `https://example.invalid/spd/` are Draft identifiers. Stable project-controlled capability, descriptor, schema, and annotation identifiers are a Release Candidate blocker.",
        "Each capability name maps to the stable project-assigned IRI in the Format 0.1 identifier registry. The authoritative descriptor retains the short name; `dcterms:conformsTo` uses the IRI. These two claim sets MUST agree exactly.",
    )
    rows = ["", "| Capability | Public IRI |", "|---|---|"]
    rows.extend(f"| {name} | `{iri}` |" for name, iri in CAPABILITIES.items())
    caps += "\n" + "\n".join(rows) + "\n"
    (PROFILE_DEST / "capabilities-profile.md").write_text(caps, encoding="utf-8")

    ann = (PROFILE_DEST / "annotation-profile.md").read_text(encoding="utf-8")
    ann = ann.replace('"type": "StableNodeSelector",', f'"type": "{ANNOTATION_TERMS["StableNodeSelector"]}",')
    ann = ann.replace(
        "The JSON structure is constrained by `schemas/annotation-extension.schema.json`. The provisional type name must be replaced by a registered IRI/context before final publication (SPD-ANN-001).",
        "The JSON structure is constrained by `schemas/rc1/annotation-extension.schema.json`. The selector type and compact extension terms use the permanent IRIs below (SPD-ANN-001). Annotation documents MUST provide these mappings inline so processing requires no network context fetch.",
    )
    ann += "\n## Inline extension context\n\n```json\n" + json.dumps(ANNOTATION_TERMS, indent=2) + "\n```\n"
    (PROFILE_DEST / "annotation-profile.md").write_text(ann, encoding="utf-8")


def write_traceability() -> None:
    text = (ROOT / "spec/STANDARDS_TRACEABILITY.md").read_text(encoding="utf-8")
    text = text.replace("# Standards traceability", "# Format 0.1 RC1 standards traceability")
    text = text.replace("| EPUB | 3.3 W3C Recommendation |", "| EPUB | 3.3 W3C Recommendation, 13 January 2026 |")
    text = text.replace("| HTML | Living Standard as referenced by EPUB 3.3 |", "| HTML | Living Standard baseline reviewed 3 September 2026, only as incorporated by pinned EPUB 3.3 |")
    text = text.replace("| CSS | Snapshot/reference set inherited through EPUB 3.3 |", "| CSS | Dated module set in UPSTREAM_DEPENDENCY_BASELINE_0.1.md, otherwise only as incorporated by pinned EPUB 3.3 |")
    text = text.replace("| MathML | Core/MathML 3 as applicable through EPUB 3.3 |", "| MathML | MathML 3 Second Edition, 10 April 2014, as incorporated by pinned EPUB 3.3 |")
    text = text.replace("| SVG | 2 as applicable through EPUB 3.3 |", "| SVG | SVG 1.1 Second Edition (16 August 2011) and SVG 2 CR (4 October 2018), as incorporated by pinned EPUB 3.3 |")
    text = text.replace("| Unicode | Current supported version, declared by processor |", "| Unicode | Unicode 17.0.0; UAX #15 rev. 57; UAX #9 rev. 51 |")
    text = text.replace("## Pre-RC dated inheritance and passive profile", "## RC1 dated inheritance and passive profile")
    text += "\n## RC1 identifier and artifact traceability\n\nStable public identifiers are listed in [IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md](IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md). The RC1 registry retains 118 requirement IDs. The RC1 corpus retains all 107 reviewed expected outcomes and changes only identifier-bearing bytes and their deterministic integrity bindings. No future upstream edition or erratum changes Format 0.1 without an explicit maintenance revision.\n"
    (ROOT / "spec/STANDARDS_TRACEABILITY_0.1_RC1.md").write_text(text, encoding="utf-8")


def write_corpus() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    manifest["schemaVersion"] = "0.1-rc1"
    manifest["corpusVersion"] = "0.1-rc1"
    manifest["sourceCorpusVersion"] = "0.1.2"
    manifest["sourceManifestSha256"] = sha256(SOURCE_MANIFEST.read_bytes())
    for fixture in manifest["fixtures"]:
        source_package = ROOT / fixture["package"]
        source_expected = ROOT / fixture["expectedResult"]
        package_data = migrate_package(source_package, fixture["id"])
        category, name = fixture["id"].split("/", 1)
        folder = DEST / category / name
        folder.mkdir(parents=True, exist_ok=True)
        package_path = folder / "document.epub"
        expected_path = folder / "expected.json"
        package_path.write_bytes(package_data)
        expected = json.loads(source_expected.read_text(encoding="utf-8"))
        expected["corpusVersion"] = "0.1-rc1"
        expected_data = encoded(expected)
        expected_path.write_bytes(expected_data)
        fixture["sourcePackage"] = fixture["package"]
        fixture["sourcePackageSha256"] = fixture["packageSha256"]
        fixture["package"] = package_path.relative_to(ROOT).as_posix()
        fixture["packageSha256"] = sha256(package_data)
        fixture["sourceExpectedResult"] = fixture["expectedResult"]
        fixture["sourceExpectedResultSha256"] = fixture["expectedResultSha256"]
        fixture["expectedResult"] = expected_path.relative_to(ROOT).as_posix()
        fixture["expectedResultSha256"] = sha256(expected_data)
    (DEST / "manifest.json").write_bytes(encoded(manifest))


def main() -> None:
    write_specification()
    write_registry()
    write_schemas()
    write_profiles()
    write_traceability()
    write_corpus()
    print(f"Prepared RC1 inputs: {len(json.loads((DEST / 'manifest.json').read_text())['fixtures'])} fixtures")


if __name__ == "__main__":
    main()
