from __future__ import annotations

from dataclasses import dataclass, field

from lxml import etree

from .constants import (
    CAPABILITY_IRIS,
    DC_NS,
    OCF_NS,
    OPF_NS,
    RELATIONSHIPS,
)
from .models import Outcome, ValidationReport
from .package import SecurePackage, resolve_local, resolve_root_local
from .xmlutil import XMLValidationError, parse_xml


@dataclass(slots=True)
class PackageDocument:
    path: str
    root: etree._Element
    manifest: dict[str, dict[str, str]] = field(default_factory=dict)
    spine_paths: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    document_id: str | None = None


@dataclass(slots=True)
class Discovery:
    rootfile: str | None = None
    descriptors: dict[str, str] = field(default_factory=dict)
    package_document: PackageDocument | None = None


def _capability_from_iri(value: str) -> str | None:
    return CAPABILITY_IRIS.get(value)


def discover(package: SecurePackage, report: ValidationReport) -> Discovery:
    result = Discovery()
    container_path = "META-INF/container.xml"
    if not package.exists(container_path):
        report.add("SPD-BASE-006", Outcome.FAIL, "META-INF/container.xml is missing", resource=container_path)
        report.add("SPD-DISC-001", Outcome.FAIL, "SPD descriptor discovery container is missing", resource=container_path)
        return result
    try:
        root = parse_xml(package.read(container_path, limit=package.limits.max_xml_bytes), resource=container_path)
    except XMLValidationError as exc:
        report.add("SPD-BASE-002", Outcome.FAIL, f"invalid container.xml: {exc}", resource=container_path)
        report.add("SPD-DISC-001", Outcome.FAIL, "descriptor links cannot be processed", resource=container_path)
        return result

    rootfiles = root.xpath("./ocf:rootfiles/ocf:rootfile", namespaces={"ocf": OCF_NS})
    if len(rootfiles) != 1:
        report.add(
            "SPD-BASE-006", Outcome.FAIL, "container.xml must contain exactly one rootfile",
            resource=container_path, evidence={"count": len(rootfiles)},
        )
    elif rootfiles:
        candidate = rootfiles[0].get("full-path", "")
        media_type = rootfiles[0].get("media-type")
        safe = resolve_root_local(candidate)
        if safe is None or safe != candidate or not package.exists(candidate):
            report.add("SPD-BASE-006", Outcome.FAIL, "rootfile path is unsafe or missing", resource=candidate)
        elif media_type != "application/oebps-package+xml":
            report.add("SPD-BASE-002", Outcome.FAIL, "rootfile media type is not OPF", resource=candidate)
        else:
            result.rootfile = candidate

    links = root.xpath("./ocf:links/ocf:link", namespaces={"ocf": OCF_NS})
    for key, relation in RELATIONSHIPS.items():
        matches = [node for node in links if node.get("rel") == relation]
        if len(matches) != 1:
            report.add(
                "SPD-DISC-001", Outcome.FAIL, f"exactly one {key} discovery link is required",
                resource=container_path, evidence={"count": len(matches)},
            )
            continue
        node = matches[0]
        href = node.get("href", "")
        safe = resolve_root_local(href)
        if node.get("media-type") != "application/json" or safe is None or safe != href or not package.exists(href):
            report.add(
                "SPD-DISC-002", Outcome.FAIL, f"{key} link has wrong media type, unsafe href, or missing target",
                resource=href or container_path,
            )
            continue
        result.descriptors[key] = href

    report.metadata["descriptorCandidatePaths"] = dict(result.descriptors)
    if len(set(result.descriptors.values())) != len(result.descriptors):
        report.add("SPD-DISC-002", Outcome.FAIL, "distinct descriptor relationships resolve to the same resource")
        conflicted = {path for path in result.descriptors.values() if list(result.descriptors.values()).count(path) > 1}
        report.metadata["conflictingDescriptorCandidates"] = sorted(conflicted)
        result.descriptors = {key: path for key, path in result.descriptors.items() if path not in conflicted}

    if result.rootfile:
        result.package_document = parse_opf(package, report, result.rootfile)
    return result


def parse_opf(package: SecurePackage, report: ValidationReport, path: str) -> PackageDocument | None:
    try:
        root = parse_xml(package.read(path, limit=package.limits.max_xml_bytes), resource=path)
    except XMLValidationError as exc:
        report.add("SPD-BASE-002", Outcome.FAIL, f"invalid OPF XML: {exc}", resource=path)
        return None
    doc = PackageDocument(path, root)
    ns = {"opf": OPF_NS, "dc": DC_NS}
    identifiers = root.xpath("./opf:metadata/dc:identifier", namespaces=ns)
    unique_id = root.get("unique-identifier")
    for item in identifiers:
        if unique_id and item.get("id") == unique_id:
            doc.document_id = (item.text or "").strip()
            break
    if doc.document_id is None and identifiers:
        doc.document_id = (identifiers[0].text or "").strip()

    for item in root.xpath("./opf:manifest/opf:item", namespaces=ns):
        item_id = item.get("id", "")
        href = item.get("href", "")
        resolved = resolve_local(path, href)
        if not item_id or item_id in doc.manifest or resolved is None or not package.exists(resolved):
            report.add("SPD-BASE-002", Outcome.FAIL, "invalid, duplicate, unsafe, or missing OPF manifest item", resource=href or path)
            continue
        doc.manifest[item_id] = {
            "path": resolved,
            "mediaType": item.get("media-type", ""),
            "properties": item.get("properties", ""),
        }
    navs = [item for item in doc.manifest.values() if "nav" in item["properties"].split()]
    if len(navs) != 1:
        report.add("SPD-BASE-005", Outcome.FAIL, "exactly one EPUB navigation document is required", resource=path)
    for itemref in root.xpath("./opf:spine/opf:itemref", namespaces=ns):
        item = doc.manifest.get(itemref.get("idref", ""))
        if item is None or item["mediaType"] != "application/xhtml+xml":
            report.add("SPD-SEM-002", Outcome.FAIL, "spine item is missing or not XHTML", resource=path)
        else:
            doc.spine_paths.append(item["path"])
    if not doc.spine_paths:
        report.add("SPD-SEM-002", Outcome.FAIL, "authoritative XHTML spine is empty", resource=path)
        report.add("SPD-SEM-003", Outcome.FAIL, "primary reading order is not defined", resource=path)

    for node in root.xpath("./opf:metadata/opf:meta[@property='dcterms:conformsTo']", namespaces=ns):
        value = (node.text or "").strip()
        capability = _capability_from_iri(value)
        if capability is None:
            report.add("SPD-CAP-003", Outcome.FAIL, "unrecognized SPD capability discovery value", resource=path, evidence=value)
        else:
            doc.capabilities.add(capability)
    return doc
