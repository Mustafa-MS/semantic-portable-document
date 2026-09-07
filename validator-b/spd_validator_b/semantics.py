from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from lxml import etree

from .constants import XHTML_NS, XML_NS
from .epub import PackageDocument
from .models import Outcome, ValidationReport
from .package import SecurePackage
from .xmlutil import XMLValidationError, local_name, parse_xml

NODE_ID = re.compile(r"^n_[a-z0-9._-]{1,128}$")
LANGUAGE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
REMOTE_SCHEMES = {"http", "https", "ftp", "ws", "wss", "data", "javascript"}
ADDRESSABLE = {
    "article", "section", "nav", "h1", "h2", "h3", "h4", "h5", "h6", "p", "li",
    "figure", "figcaption", "table", "tr", "th", "td", "math", "aside", "blockquote", "pre",
}
RESOURCE_ATTRIBUTES = {
    "img": ("src",), "script": ("src",), "iframe": ("src",), "object": ("data",),
    "embed": ("src",), "source": ("src", "srcset"), "video": ("src", "poster"),
    "audio": ("src",), "image": ("href", "{http://www.w3.org/1999/xlink}href"),
    "use": ("href", "{http://www.w3.org/1999/xlink}href"),
}


@dataclass(slots=True)
class SemanticModel:
    documents: dict[str, etree._Element] = field(default_factory=dict)
    nodes: dict[str, etree._Element] = field(default_factory=dict)
    node_resources: dict[str, str] = field(default_factory=dict)

    def text_value(self, node_id: str) -> str | None:
        node = self.nodes.get(node_id)
        if node is None:
            return None
        pieces: list[str] = []

        def visit(element: etree._Element) -> None:
            if local_name(element) in {"head", "script", "style"}:
                return
            if element.text:
                pieces.append(element.text)
            for child in element:
                if isinstance(child.tag, str):
                    visit(child)
                if child.tail:
                    pieces.append(child.tail)

        visit(node)
        return "".join(pieces)


def validate_semantics(package: SecurePackage, opf: PackageDocument | None, report: ValidationReport) -> SemanticModel:
    model = SemanticModel()
    if opf is None:
        return model
    all_xhtml = {item["path"] for item in opf.manifest.values() if item["mediaType"] == "application/xhtml+xml"}
    spine = set(opf.spine_paths)
    for path in sorted(all_xhtml):
        try:
            root = parse_xml(package.read(path, limit=package.limits.max_xml_bytes), resource=path)
        except XMLValidationError as exc:
            requirement = "SPD-SEM-002" if path in spine else "SPD-BASE-002"
            report.add(requirement, Outcome.FAIL, f"XHTML is not well-formed XML: {exc}", resource=path)
            if path in spine:
                report.add("SPD-ID-006", Outcome.NOT_TESTED, "unparseable authoritative XHTML prevents complete Node-ID index", resource=path)
            continue
        model.documents[path] = root
        if root.tag != f"{{{XHTML_NS}}}html":
            report.add("SPD-SEM-002", Outcome.FAIL, "authoritative content root is not XHTML html", resource=path)
        lang = root.get("lang")
        xml_lang = root.get(f"{{{XML_NS}}}lang")
        if not lang or not xml_lang or lang.lower() != xml_lang.lower() or not LANGUAGE.fullmatch(lang):
            report.add("SPD-I18N-003", Outcome.FAIL, "root lang and xml:lang must be valid and equivalent", resource=path)
        if root.get("dir") not in {"ltr", "rtl"}:
            report.add("SPD-I18N-004", Outcome.FAIL, "root dir must explicitly be ltr or rtl", resource=path)

        for element in root.iter():
            if not isinstance(element.tag, str):
                continue
            name = local_name(element).lower()
            node_id = element.get("id")
            if path in spine and name in ADDRESSABLE and (not node_id or not NODE_ID.fullmatch(node_id)):
                report.add("SPD-ID-005", Outcome.FAIL, "addressable semantic element lacks a valid Node ID", resource=path, node=node_id, evidence=name)
            if path in spine and node_id:
                if not NODE_ID.fullmatch(node_id):
                    report.add("SPD-ID-005", Outcome.FAIL, "semantic id does not follow Node ID grammar", resource=path, node=node_id)
                elif node_id in model.nodes:
                    report.add("SPD-ID-006", Outcome.FAIL, "duplicate Node ID in authoritative revision", resource=path, node=node_id, evidence={"other": model.node_resources[node_id]})
                else:
                    model.nodes[node_id] = element
                    model.node_resources[node_id] = path
                if re.fullmatch(r"n_[0-9a-f]{64}", node_id):
                    report.add("SPD-ID-008", Outcome.FAIL, "Node ID appears to be a content digest", resource=path, node=node_id)
            if name == "table":
                headers = element.xpath(".//x:th", namespaces={"x": XHTML_NS})
                if not headers:
                    report.add("SPD-SEM-013", Outcome.FAIL, "table has no semantic header cells", resource=path, node=node_id)

        if path in spine and root.get("dir") == "rtl":
            for paragraph in root.xpath(".//x:p", namespaces={"x": XHTML_NS}):
                text = "".join(paragraph.itertext()).strip()
                arabic = sum("ARABIC" in unicodedata.name(ch, "") for ch in text)
                if text and text[0] in ".!?؟،؛" and arabic >= 3:
                    report.add("SPD-I18N-001", Outcome.FAIL, "source-order oracle detects visually reversed RTL sentence", resource=path, node=paragraph.get("id"))

    return model
