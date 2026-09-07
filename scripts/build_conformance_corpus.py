"""Generate deterministic SPD 0.1 conformance packages and expected results.

This is fixture tooling, not the production validator.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import unicodedata
import uuid
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
STAMP = "2026-09-03T00:00:00Z"
DOC = "urn:uuid:11111111-1111-4111-8111-111111111111"
REV = "urn:uuid:22222222-2222-4222-8222-222222222222"
OLD_REV = "urn:uuid:33333333-3333-4333-8333-333333333333"
ALT_REV = "urn:uuid:44444444-4444-4444-8444-444444444444"


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def jbytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jcs_bytes(value: object) -> bytes:
    """RFC 8785 JCS for the I-JSON subset used by SPD state descriptors."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def minimal_pdf(label: str = "SPD fixed fixture") -> bytes:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>",
        f"<< /Length 0 >>\nstream\n\nendstream\n% {label}".encode(),
    ]
    out = bytearray(b"%PDF-2.0\n")
    offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out.extend(f"{index} 0 obj\n".encode() + obj + b"\nendobj\n")
    start = len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        out.extend(f"{offset:010d} 00000 n \n".encode())
    out.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    return bytes(out)


def xhtml(body: str, *, lang: str = "en", direction: str = "ltr", title: str = "Fixture") -> bytes:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}" lang="{lang}" dir="{direction}">
<head><title>{title}</title><link rel="stylesheet" href="style.css"/></head>
<body><article id="n_article01">{body}</article></body></html>
'''.encode("utf-8")


def base_body() -> str:
    return '''<h1 id="n_heading01">Conformance fixture</h1>
<section id="n_section01"><h2 id="n_heading02">Semantic section</h2>
<p id="n_paragraph01">Logical Unicode text is authoritative.</p>
<ul id="n_list0001"><li id="n_listitem01">A persistent list item.</li></ul></section>'''


def opf(items: list[tuple[str, ...]], spine: list[str], *, include_ids: bool = True, language: str = "en", capabilities: list[str] | None = None) -> bytes:
    capability_meta = "\n    ".join(f'<meta property="dcterms:conformsTo">https://example.invalid/spd/capability/{cap}/0.1</meta>' for cap in (capabilities or ["Base"]))
    metas = capability_meta
    manifest_parts = []
    for item in items:
        i, h, m = item[:3]
        properties = list(item[3:])
        if i == "nav": properties.insert(0, "nav")
        prop_text = f' properties="{" ".join(properties)}"' if properties else ""
        manifest_parts.append(f'<item id="{i}" href="{h}" media-type="{m}"{prop_text}/>')
    manifest = "\n    ".join(manifest_parts)
    refs = "\n    ".join(f'<itemref idref="{i}"/>' for i in spine)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0" unique-identifier="pub-id">
<metadata><dc:identifier id="pub-id">{DOC}</dc:identifier><dc:title>SPD fixture</dc:title><dc:language>{language}</dc:language><meta property="dcterms:modified">2026-09-03T00:00:00Z</meta>{metas}</metadata>
<manifest>{manifest}</manifest><spine>{refs}</spine></package>
'''.encode()


def container_xml(rootfiles: list[str] | None = None, *, include_links: bool = True) -> bytes:
    roots = "".join(f'<rootfile full-path="{path}" media-type="application/oebps-package+xml"/>' for path in (rootfiles or ["EPUB/package.opf"]))
    links = ""
    if include_links:
        links = '''<links>
<link href="META-INF/spd/document-state.json" rel="https://example.invalid/spd/rel/document-state" media-type="application/json"/>
<link href="META-INF/spd/inventory.json" rel="https://example.invalid/spd/rel/resource-inventory" media-type="application/json"/>
<link href="META-INF/spd/state.json" rel="https://example.invalid/spd/rel/lifecycle-state" media-type="application/json"/>
</links>'''
    return f'''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>{roots}</rootfiles>{links}</container>'''.encode()
def nav(target: str, language: str = "en", direction: str = "ltr") -> bytes:
    return xhtml(f'<nav id="n_navigation" epub:type="toc" xmlns:epub="http://www.idpf.org/2007/ops"><h1 id="n_navhead01">Contents</h1><ol><li id="n_navitem01"><a href="{target}">Fixture</a></li></ol></nav>', lang=language, direction=direction)
CSS = b'''body { font-family: serif; } table { border-collapse: collapse; } td, th { border: 1px solid; }'''


def projection_digest(resources: dict[str, bytes], effects: dict[str, list[str]], scope: str) -> str:
    rows = []
    for path in sorted(resources):
        selected = scope in effects.get(path, []) if scope == "semantic" else bool(set(effects.get(path, [])) & {"semantic", "rendering"})
        if selected:
            data = resources[path]
            rows.append(f"{path}\0{len(data)}\0{digest(data)}\n")
    return digest("".join(rows).encode())


def descriptor_bytes(state: dict) -> bytes:
    value = copy.deepcopy(state)
    value.pop("descriptorDigest", None)
    state["descriptorDigest"] = digest(jcs_bytes(value))
    return jbytes(state)


def package_model(body: str | None = None, *, lang="en", direction="ltr", chapters: list[tuple[str, bytes]] | None = None,
                  mapped=False, fixed=False, sealed=False, annotations=False, annotation_scope="lineage",
                  accessible=False, extra: dict[str, bytes] | None = None, revision_id=REV, parents: list[str] | None = None) -> dict[str, bytes]:
    fixed_requested = fixed or mapped
    capability_ids = ["Base"] + (["Mapping"] if mapped else []) + (["Fixed-Experimental"] if fixed_requested and not mapped else []) + (["Accessible"] if accessible else [])
    resources: dict[str, bytes] = {
        "mimetype": b"application/epub+zip",
        "META-INF/container.xml": container_xml(),
        "EPUB/style.css": CSS,
    }
    chapter_list = chapters or [("content.xhtml", xhtml(body or base_body(), lang=lang, direction=direction))]
    resources["EPUB/nav.xhtml"] = nav(chapter_list[0][0], lang, direction)
    for name, data in chapter_list:
        resources["EPUB/" + name] = data
    manifest = [("nav", "nav.xhtml", "application/xhtml+xml"), ("css", "style.css", "text/css")]
    spine = []
    for index, (name, _) in enumerate(chapter_list, 1):
        item_id = f"c{index}"
        manifest.append((item_id, name, "application/xhtml+xml", "mathml") if b"<math" in _ else (item_id, name, "application/xhtml+xml"))
        spine.append(item_id)
    if annotations:
        manifest.append(("ann", "annotations.json", "application/ld+json"))
        selector = {"type": "StableNodeSelector", "documentId": DOC, "nodeId": "n_paragraph01", "scope": annotation_scope}
        if annotation_scope == "revision":
            selector["revisionId"] = revision_id
        resources["EPUB/annotations.json"] = jbytes({
            "@context": "http://www.w3.org/ns/anno.jsonld", "type": "Annotation", "id": "urn:uuid:aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "target": {"source": "content.xhtml", "selector": selector},
            "body": {"type": "TextualBody", "value": "A note", "format": "text/plain"}
        })
    if extra:
        resources.update(extra)
        for index, path in enumerate(sorted(extra), 1):
            if path.startswith("EPUB/"):
                manifest.append((f"extra{index}", path.removeprefix("EPUB/"), media_type(path)))
    resources["EPUB/package.opf"] = opf(manifest, spine, language=lang, capabilities=capability_ids)

    roles: dict[str, str] = {p: "authoritative" for p in resources if p.startswith("EPUB/")}
    effects: dict[str, list[str]] = {p: ["semantic", "rendering"] for p in resources if p.startswith("EPUB/")}
    roles.update({"mimetype": "control", "META-INF/container.xml": "control"})
    effects.update({"mimetype": [], "META-INF/container.xml": [], "EPUB/style.css": ["rendering"]})
    for path in list(resources):
        if path.lower().endswith((".woff", ".woff2", ".otf", ".ttf")):
            effects[path] = ["rendering"]
    if "EPUB/annotations.json" in resources:
        roles["EPUB/annotations.json"] = "non-normative"
        effects["EPUB/annotations.json"] = []
    semantic_digest = projection_digest(resources, effects, "semantic")
    rendition_digest = projection_digest(resources, effects, "rendering")
    caps = [{"id": cap, "version": "0.1"} for cap in capability_ids]
    doc_state = {"schemaVersion": "0.1", "documentId": DOC, "revision": {"revisionId": revision_id, "parents": parents or [], "created": STAMP, "generator": {"name": "SPD corpus generator", "version": "0.1"}}, "semanticStateDigest": semantic_digest, "renditionInputDigest": rendition_digest, "capabilities": caps}
    if accessible:
        doc_state["accessibilityTarget"] = {"epubAccessibility": "1.1", "wcag": "2.2-AA"}
    resources["META-INF/spd/document-state.json"] = jbytes(doc_state)
    roles["META-INF/spd/document-state.json"] = "control"
    effects["META-INF/spd/document-state.json"] = []

    fixed_bytes = None
    mapping = None
    if fixed_requested:
        fixed_bytes = minimal_pdf()
        resources["EPUB/fixed.pdf"] = fixed_bytes
        roles["EPUB/fixed.pdf"] = "generated"
        effects["EPUB/fixed.pdf"] = []
    if mapped:
        node_text = "Logical Unicode text is authoritative."
        mapping = {
            "schemaVersion": "0.1", "documentId": DOC, "revisionId": revision_id,
            "fixedRendition": {"id": "f_fixture01", "sha256": digest(fixed_bytes), "mediaType": "application/pdf"},
            "provenance": {"method": "forward-layout", "generator": "fixture-renderer", "version": "0.1"},
            "coordinateSystem": {"unit": "css-px", "origin": "top-left", "xDirection": "right", "yDirection": "down", "quadOrder": "top-left,top-right,bottom-right,bottom-left"},
            "pages": [{"id": "p_1", "width": 816, "height": 1056, "toFixed": [0.75, 0, 0, -0.75, 0, 792]}],
            "records": [{"nodeId": "n_paragraph01", "status": "MAPPED", "provenance": {"method": "forward-layout", "generator": "fixture-renderer", "version": "0.1"}, "fragments": [{"pageId": "p_1", "textRange": {"unit": "unicode-scalar-value", "start": 0, "end": len(node_text)}, "quad": [48, 96, 500, 96, 500, 120, 48, 120]}]}]
        }
        resources["META-INF/spd/mapping.json"] = jbytes(mapping)
        roles["META-INF/spd/mapping.json"] = "generated"
        effects["META-INF/spd/mapping.json"] = []

    inventory_resources = []
    omitted = {"META-INF/spd/inventory.json", "META-INF/spd/state.json"}
    for path in sorted(resources):
        if path not in omitted:
            data = resources[path]
            inventory_resources.append({"path": path, "mediaType": media_type(path), "byteLength": len(data), "sha256": digest(data), "role": roles.get(path, "non-normative"), "affects": effects.get(path, [])})
    inventory = {"schemaVersion": "0.1", "documentId": DOC, "revisionId": revision_id, "resources": inventory_resources}
    resources["META-INF/spd/inventory.json"] = jbytes(inventory)
    state = {
        "schemaVersion": "0.1", "lifecycle": "SEALED" if sealed else "EDITABLE", "documentId": DOC, "revisionId": revision_id,
        "semanticStateDigest": semantic_digest,
        "renditionInputDigest": rendition_digest,
        "inventory": {"path": "META-INF/spd/inventory.json", "sha256": digest(resources["META-INF/spd/inventory.json"])},
        "fixedRendition": {"status": "current", "id": "f_fixture01", "revisionId": revision_id, "renditionInputDigest": rendition_digest, "path": "EPUB/fixed.pdf", "sha256": digest(fixed_bytes)} if fixed_requested else {"status": "absent"}
    }
    if mapped:
        state["mapping"] = {"path": "META-INF/spd/mapping.json", "sha256": digest(resources["META-INF/spd/mapping.json"])}
    if sealed:
        state["sealedAt"] = STAMP
    resources["META-INF/spd/state.json"] = descriptor_bytes(state)
    return resources


def media_type(path: str) -> str:
    if path == "mimetype":
        return "application/epub+zip"
    if path == "META-INF/container.xml":
        return "application/xml"
    if path.endswith("annotations.json"):
        return "application/ld+json"
    ext = Path(path).suffix.lower()
    return {".xhtml": "application/xhtml+xml", ".opf": "application/oebps-package+xml", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".pdf": "application/pdf", ".png": "image/png"}.get(ext, "application/octet-stream")


def write_zip(path: Path, resources: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        names = list(resources)
        if "mimetype" in names:
            names.remove("mimetype")
            names.insert(0, "mimetype")
        for name in names:
            info = zipfile.ZipInfo(name, (2026, 9, 3, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, resources[name])


def result(name: str, category: str, violations: list[dict] | None = None, *, mapped=False, experimental=False, accessible=False, notes=None) -> dict:
    bad = violations or []
    capability_only = bool(bad) and all(v["requirement"].startswith("SPD-MAP-") or v["requirement"] in {"SPD-STATE-001", "SPD-STATE-007"} for v in bad)
    caps = {"Mapping": "PASS" if mapped and not bad else ("FAIL" if mapped else "NOT_CLAIMED"), "Fixed-Experimental": "PRESENT_EXPERIMENTAL" if experimental or mapped else "NOT_CLAIMED", "Accessible": "PASS" if accessible and not bad else ("FAIL" if accessible else "NOT_CLAIMED"), "Archive-Experimental": "NOT_CLAIMED"}
    return {"fixture": f"{category}/{name}", "base": "PASS" if not bad or capability_only else "FAIL", "capabilities": caps, "violations": bad, "notes": notes or []}


def emit(category: str, name: str, resources: dict[str, bytes], expected: dict, description: str) -> None:
    folder = TESTS / category / name
    folder.mkdir(parents=True, exist_ok=True)
    write_zip(folder / "document.epub", resources)
    (folder / "expected.json").write_bytes(jbytes(expected))
    (folder / "README.md").write_text(f"# {name}\n\n{description}\n\nPackage: `document.epub`. Expected result: `expected.json`.\n", encoding="utf-8")


def mutate_json(resources: dict[str, bytes], path: str, fn) -> None:
    value = json.loads(resources[path])
    fn(value)
    resources[path] = jbytes(value)


def rebind(resources: dict[str, bytes]) -> None:
    """Refresh expected hashes after constructing a semantically invalid fixture."""
    inventory = json.loads(resources["META-INF/spd/inventory.json"])
    effects = {item["path"]: item["affects"] for item in inventory["resources"]}
    semantic = projection_digest(resources, effects, "semantic")
    rendition = projection_digest(resources, effects, "rendering")
    doc_state = json.loads(resources["META-INF/spd/document-state.json"])
    if "semanticStateDigest" in doc_state:
        doc_state["semanticStateDigest"] = semantic
        doc_state["renditionInputDigest"] = rendition
    resources["META-INF/spd/document-state.json"] = jbytes(doc_state)
    for item in inventory["resources"]:
        if item["path"] in resources:
            data = resources[item["path"]]
            item["byteLength"] = len(data)
            item["sha256"] = digest(data)
    resources["META-INF/spd/inventory.json"] = jbytes(inventory)
    state = json.loads(resources["META-INF/spd/state.json"])
    state["semanticStateDigest"] = semantic
    state["renditionInputDigest"] = rendition
    state["inventory"]["sha256"] = digest(resources["META-INF/spd/inventory.json"])
    if state["fixedRendition"]["status"] != "absent" and "EPUB/fixed.pdf" in resources:
        state["fixedRendition"]["sha256"] = digest(resources["EPUB/fixed.pdf"])
    if "mapping" in state and "META-INF/spd/mapping.json" in resources:
        state["mapping"]["sha256"] = digest(resources["META-INF/spd/mapping.json"])
    resources["META-INF/spd/state.json"] = descriptor_bytes(state)


def main() -> None:
    for category in ("valid", "invalid", "edge"):
        target = TESTS / category
        if target.exists():
            for child in target.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)

    valid = {
        "minimal-base": (package_model(), "Smallest representative Base package."),
        "multi-spine": (package_model(chapters=[("chapter1.xhtml", xhtml(base_body(), title="One")), ("chapter2.xhtml", xhtml('<section id="n_section02"><h1 id="n_heading03">Second</h1><p id="n_paragraph02">Second spine item.</p></section>', title="Two"))]), "Two ordered XHTML spine items."),
        "arabic": (package_model('<h1 id="n_heading01">وثيقة عربية</h1><section id="n_section01"><h2 id="n_heading02">الأرقام والجداول</h2><p id="n_paragraph01">هذا نص عربي منطقي ١٢٣ و 123.</p><table id="n_table0001"><thead><tr id="n_row000001"><th id="n_cell00001" scope="col">العنصر</th><th id="n_cell00002" scope="col">القيمة</th></tr></thead><tbody><tr id="n_row000002"><td id="n_cell00003">نتيجة</td><td id="n_cell00004">٩٠٫٦</td></tr></tbody></table></section>', lang="ar", direction="rtl"), "Pure Arabic, Arabic-Indic/European digits, and an Arabic table in logical order."),
        "mixed-bidi": (package_model('<h1 id="n_heading01">تقرير Model X</h1><section id="n_section01"><h2 id="n_heading02">نص مختلط</h2><p id="n_paragraph01">النتيجة (Model X) هي 0.906، راجع [12] و https://example.org/a?x=1.</p><p id="n_paragraph02">المعادلة <math xmlns="http://www.w3.org/1998/Math/MathML" id="n_equation01"><mi>x</mi><mo>=</mo><mn>2</mn></math> صحيحة.</p></section>', lang="ar", direction="rtl"), "Arabic plus English, URL, model name, European digits, parentheses, citation brackets, and MathML."),
        "table": (package_model('<h1 id="n_heading01">Table</h1><section id="n_section01"><h2 id="n_heading02">Results</h2><table id="n_table0001"><thead><tr id="n_row000001"><th id="n_cell00001" scope="col">Name</th><th id="n_cell00002" scope="col">Score</th></tr></thead><tbody><tr id="n_row000002"><td id="n_cell00003">A</td><td id="n_cell00004">1</td></tr></tbody></table></section>'), "Native table with addressable rows/cells and explicit headers."),
        "figure-svg": (package_model('<h1 id="n_heading01">Figure</h1><section id="n_section01"><h2 id="n_heading02">Static SVG</h2><figure id="n_figure001"><img src="figure.svg" alt="Blue circle"/><figcaption id="n_caption001">A safe static SVG.</figcaption></figure></section>', extra={"EPUB/figure.svg": b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="blue"/></svg>'}), "Static local SVG with native figure and caption."),
        "mathml": (package_model('<h1 id="n_heading01">Math</h1><section id="n_section01"><h2 id="n_heading02">Equation</h2><p id="n_paragraph01">Value <math xmlns="http://www.w3.org/1998/Math/MathML" id="n_equation01"><mi>x</mi><mo>=</mo><mn>2</mn></math>.</p></section>'), "Semantic MathML in XHTML."),
        "annotations": (package_model(annotations=True), "Web Annotation with a lineage-scoped StableNodeSelector."),
        "mapped": (package_model(mapped=True), "Forward-layout mapping bound to a fixed rendition."),
        "sealed": (package_model(mapped=True, sealed=True), "Sealed revision with verified inventory, fixed rendition, and mapping bindings."),
        "semantic-only-sealed": (package_model(sealed=True), "SEALED semantic revision with no fixed rendition."),
        "fixed-without-mapping": (package_model(fixed=True), "Current fixed rendition with no Mapping claim or artifact."),
        "mapping-with-current-fixed": (package_model(mapped=True), "Mapping claim with a current bound fixed rendition."),
        "same-semantic-different-revision-id": (package_model(revision_id=ALT_REV, parents=[REV]), "Same authoritative bytes as minimal-base, committed under a different opaque Revision ID with the same semanticStateDigest."),
        "semantic-change-new-revision": (package_model('<h1 id="n_heading01">Conformance fixture</h1><section id="n_section01"><h2 id="n_heading02">Semantic section</h2><p id="n_paragraph01">Changed semantic content.</p></section>', revision_id=ALT_REV, parents=[REV]), "Semantic content change committed under a new Revision ID and semanticStateDigest."),
        "lineage-scoped-annotation": (package_model(annotations=True, annotation_scope="lineage"), "StableNodeSelector follows a Node ID across the document lineage."),
        "revision-scoped-annotation": (package_model(annotations=True, annotation_scope="revision"), "StableNodeSelector anchors Document, Revision, and Node identity."),
        "accessible": (package_model(accessible=True), "Accessible 0.1 declaration with exact EPUB Accessibility 1.1 and WCAG 2.2 AA target."),
    }
    for name, (resources, desc) in valid.items():
        mapped_names = {"mapped", "sealed", "mapping-with-current-fixed"}
        fixed_names = mapped_names | {"fixed-without-mapping"}
        emit("valid", name, resources, result(name, "valid", mapped=name in mapped_names, experimental=name in fixed_names, accessible=name == "accessible"), desc)

    invalid_specs: list[tuple[str, dict[str, bytes], list[dict], str]] = []
    def inv(name, resources, req, resource, desc, node=None, preserve_integrity_break=False):
        if not preserve_integrity_break:
            rebind(resources)
        violation = {"requirement": req, "resource": resource}
        if node: violation["node"] = node
        invalid_specs.append((name, resources, [violation], desc))

    r = package_model(); r["EPUB/content.xhtml"] = xhtml(base_body() + '<p id="n_paragraph01">Duplicate.</p>'); inv("duplicate-node-id", r, "SPD-ID-006", "EPUB/content.xhtml", "Duplicate persistent Node ID.", "n_paragraph01")
    r = package_model(); mutate_json(r, "META-INF/spd/document-state.json", lambda x: x.pop("documentId")); inv("missing-document-id", r, "SPD-ID-001", "META-INF/spd/document-state.json", "Document ID absent.")
    r = package_model(); mutate_json(r, "META-INF/spd/document-state.json", lambda x: x["revision"].pop("revisionId")); inv("missing-revision-id", r, "SPD-ID-002", "META-INF/spd/document-state.json", "Revision ID absent.")
    r = package_model(); mutate_json(r, "META-INF/spd/inventory.json", lambda x: x["resources"][0].update(sha256="sha256:" + "0"*64)); inv("bad-resource-hash", r, "SPD-INT-003", "META-INF/spd/inventory.json", "Inventory digest does not match resource bytes.", preserve_integrity_break=True)
    r = package_model(); r["EPUB/extra.css"] = b"p{color:red}"; r["EPUB/package.opf"] = r["EPUB/package.opf"].replace(b"</manifest>", b'<item id="unlisted" href="extra.css" media-type="text/css"/></manifest>'); inv("unlisted-normative-resource", r, "SPD-RES-003", "EPUB/extra.css", "Manifest resource is outside the inventory.")
    r = package_model(); r["EPUB/content.xhtml"] = xhtml(base_body() + '<script>window.bad=1</script>'); inv("javascript", r, "SPD-SEC-001", "EPUB/content.xhtml", "Executable JavaScript is present.")
    r = package_model(); r["EPUB/content.xhtml"] = xhtml('<h1 id="n_heading01" onclick="bad()">Bad event</h1>' + base_body()); inv("event-handler", r, "SPD-SEC-001", "EPUB/content.xhtml", "Inline event handler is present.")
    r = package_model(); r["EPUB/style.css"] += b'\n@font-face{font-family:x;src:url("https://example.org/x.woff2")}'; inv("external-required-font", r, "SPD-SEC-004", "EPUB/style.css", "Required remote font.")
    r = package_model(); r["EPUB/content.xhtml"] = xhtml(base_body()).replace(b'href="style.css"', b'href="https://example.org/x.css"'); inv("external-required-css", r, "SPD-SEC-005", "EPUB/content.xhtml", "Required remote stylesheet.")
    r = package_model(); r["EPUB/content.xhtml"] = xhtml(base_body() + '<img src="https://example.org/x.png" alt="required"/>'); inv("external-required-image", r, "SPD-SEC-006", "EPUB/content.xhtml", "Required remote image.")
    r = package_model(extra={"../escape.txt": b"escape"}); inv("path-traversal", r, "SPD-BASE-002", "../escape.txt", "Traversal ZIP entry.")
    r = package_model(extra={"EPUB/café.txt": b"one", "EPUB/cafe\u0301.txt": b"two"}); inv("duplicate-normalized-path", r, "SPD-BASE-002", "EPUB/café.txt", "Two names collide after NFC normalization.")
    r = package_model(); r["EPUB/content.xhtml"] = b'<html xmlns="http://www.w3.org/1999/xhtml"><body><p id="n_paragraph01">broken</body></html>'; inv("invalid-xhtml", r, "SPD-SEM-002", "EPUB/content.xhtml", "Not XML well formed.")
    r = package_model(); r["EPUB/content.xhtml"] = r["EPUB/content.xhtml"].replace(b' dir="ltr"', b''); inv("missing-root-direction", r, "SPD-I18N-004", "EPUB/content.xhtml", "Root XHTML direction is not explicit.")
    r = package_model(); r["EPUB/content.xhtml"] = r["EPUB/content.xhtml"].replace(b' xml:lang="en" lang="en"', b''); inv("missing-root-language", r, "SPD-I18N-003", "EPUB/content.xhtml", "Root XHTML language pair is absent.")
    r = package_model(); r["EPUB/content.xhtml"] = xhtml('<h1 id="n_heading01">Bad table</h1><table id="n_table0001"><tr id="n_row000001"><td id="n_cell00001">Header-looking cell</td></tr></table>'); inv("invalid-table-semantics", r, "SPD-SEM-013", "EPUB/content.xhtml", "Header relationship is only visual.", "n_table0001")
    r = package_model('<h1 id="n_heading01">يبرع</h1><section id="n_section01"><h2 id="n_heading02">رابتخا</h2><p id="n_paragraph01">.يقطنم ريغ يبرع صن اذه</p></section>', lang="ar", direction="rtl"); inv("visual-order-arabic-source", r, "SPD-I18N-001", "EPUB/content.xhtml", "Known Arabic oracle text serialized in reversed visual order.", "n_paragraph01")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: x.update(revisionId=OLD_REV)); inv("mapping-wrong-revision", r, "SPD-MAP-002", "META-INF/spd/mapping.json", "Mapping Revision ID differs from state.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: x["fixedRendition"].update(sha256="sha256:"+"0"*64)); inv("mapping-wrong-rendition", r, "SPD-MAP-002", "META-INF/spd/mapping.json", "Mapping fixed digest differs from rendition.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: x["records"][0]["fragments"][0].update(pageId="p_missing")); inv("mapping-invalid-page", r, "SPD-MAP-011", "META-INF/spd/mapping.json", "Fragment names no declared page.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: x["records"][0]["fragments"][0]["textRange"].update(end=9999)); inv("mapping-invalid-range", r, "SPD-MAP-008", "META-INF/spd/mapping.json", "Range exceeds node scalar length.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: x["records"][0]["fragments"][0].update(quad=[-1, 0, 900, 0, 900, 1200, -1, 1200])); inv("mapping-invalid-geometry", r, "SPD-MAP-011", "META-INF/spd/mapping.json", "Quad is outside page bounds.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/state.json", lambda x: x["fixedRendition"].update(status="stale")); inv("stale-fixed-rendition", r, "SPD-STATE-001", "META-INF/spd/state.json", "Mapping claim treats stale fixed output as usable.")
    r = package_model(mapped=True, sealed=True); r["EPUB/content.xhtml"] = r["EPUB/content.xhtml"].replace(b"authoritative", b"modified-authoritative"); inv("sealed-after-semantic-modification", r, "SPD-STATE-003", "EPUB/content.xhtml", "Semantic bytes changed after sealing.", preserve_integrity_break=True)

    # Targeted integrity mutation fixtures.
    for name, path, marker in [
        ("mutation-semantic", "EPUB/content.xhtml", b"<!--mutated-->"),
        ("mutation-css", "EPUB/style.css", b"\n/*mutated*/"),
        ("mutation-asset", "EPUB/figure.svg", b"<!--mutated-->")
    ]:
        source = package_model(mapped=True, sealed=True, extra={"EPUB/figure.svg": b'<svg xmlns="http://www.w3.org/2000/svg"/>'})
        source[path] += marker
        inv(name, source, "SPD-INT-003", path, f"Sealed {path} changed without rebinding.", preserve_integrity_break=True)
    r = package_model(mapped=True, sealed=True); r["META-INF/spd/mapping.json"] += b" "; inv("mutation-mapping", r, "SPD-INT-003", "META-INF/spd/mapping.json", "Mapping bytes changed after sealing.", preserve_integrity_break=True)
    r = package_model(mapped=True, sealed=True); r["EPUB/fixed.pdf"] += b"%mutated"; inv("mutation-fixed", r, "SPD-INT-003", "EPUB/fixed.pdf", "Fixed bytes changed after sealing.", preserve_integrity_break=True)
    r = package_model(annotations=True, sealed=True); r["EPUB/annotations.json"] += b" "; inv("sealed-after-annotation-modification", r, "SPD-ANN-004", "EPUB/annotations.json", "In-package annotation bytes changed after sealing.", preserve_integrity_break=True)

    r = package_model(mapped=True); r["EPUB/style.css"] += b"\np{color:#123456}"; rebind(r); mutate_json(r, "META-INF/spd/state.json", lambda x: x["fixedRendition"].update(status="stale")); inv("mapping-with-stale-fixed", r, "SPD-STATE-007", "META-INF/spd/state.json", "Mapping is claimed while its fixed rendition is stale.")
    r = package_model(); r["EPUB/cache.bin"] = b"untracked cache"; inv("unlisted-non-normative-resource", r, "SPD-RES-006", "EPUB/cache.bin", "Even a non-normative cache must be inventoried.")
    r = package_model(); r["META-INF/container.xml"] = container_xml(["EPUB/package.opf", "EPUB/package.opf"]); inv("multiple-rootfiles", r, "SPD-BASE-006", "META-INF/container.xml", "SPD Base permits exactly one OCF rootfile.")
    r = package_model(); r["META-INF/container.xml"] = container_xml(include_links=False); inv("descriptor-discovery-missing", r, "SPD-DISC-001", "META-INF/container.xml", "Required SPD descriptor discovery links are absent.")
    r = package_model(); r["META-INF/container.xml"] = r["META-INF/container.xml"].replace(b'META-INF/spd/document-state.json', b'META-INF/spd/state.json', 1); inv("descriptor-discovery-conflict", r, "SPD-DISC-002", "META-INF/container.xml", "Document-state relationship resolves to the lifecycle descriptor.")
    r = package_model(); mutate_json(r, "META-INF/spd/document-state.json", lambda x: x["capabilities"][0].update(status="normative")); inv("capability-status-not-user-controlled", r, "SPD-CAP-002", "META-INF/spd/document-state.json", "Document attempts to control capability normative status.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: (x["records"][0].update(status="PARTIALLY_MAPPED"), x["records"][0].pop("reason", None))); inv("partial-mapping-reason", r, "SPD-MAP-005", "META-INF/spd/mapping.json", "PARTIALLY_MAPPED lacks required reason.")
    r = package_model(mapped=True); mutate_json(r, "META-INF/spd/mapping.json", lambda x: (x["records"][0].update(status="NOT_VISIBLE", fragments=[]), x["records"][0].pop("reason", None))); inv("not-visible-reason", r, "SPD-MAP-005", "META-INF/spd/mapping.json", "NOT_VISIBLE lacks required reason.")

    for name, resources, violations, desc in invalid_specs:
        try:
            claims = {item["id"] for item in json.loads(resources["META-INF/spd/document-state.json"]).get("capabilities", [])}
        except (KeyError, json.JSONDecodeError):
            claims = set()
        emit("invalid", name, resources, result(name, "invalid", violations, mapped="Mapping" in claims, experimental="EPUB/fixed.pdf" in resources), desc)

    edges: dict[str, tuple[dict[str, bytes], str, bool]] = {}
    edges["empty-section"] = (package_model('<h1 id="n_heading01">Empty</h1><section id="n_section01"></section>'), "Empty semantic section is valid.", False)
    edges["very-long-paragraph"] = (package_model('<h1 id="n_heading01">Long</h1><section id="n_section01"><h2 id="n_heading02">Text</h2><p id="n_paragraph01">' + ('long logical text ' * 3000) + '</p></section>'), "Long logical paragraph stresses range length.", False)
    deep = "".join('<ul id="n_list%04d"><li id="n_item%04d">L%d' % (i, i, i) for i in range(1, 21)) + "</li></ul>" * 20
    edges["deep-lists"] = (package_model('<h1 id="n_heading01">Deep</h1><section id="n_section01"><h2 id="n_heading02">Lists</h2>' + deep + '</section>'), "Twenty nested lists remain structurally valid.", False)
    edges["table-spanning-pages"] = (package_model('<h1 id="n_heading01">Long table</h1><section id="n_section01"><h2 id="n_heading02">Rows</h2><table id="n_table0001"><thead><tr id="n_rowhead01"><th id="n_cellhead1" scope="col">N</th></tr></thead><tbody>' + ''.join(f'<tr id="n_row{i:06d}"><td id="n_cell{i:06d}">{i}</td></tr>' for i in range(1, 101)) + '</tbody></table></section>'), "Large table intended to paginate.", False)
    for status, name in [("NOT_VISIBLE", "node-not-visible"), ("PARTIALLY_MAPPED", "partial-mapping"), ("UNSUPPORTED", "unsupported-mapping")]:
        r = package_model(mapped=True)
        def set_status(x, status=status):
            rec = x["records"][0]; rec["status"] = status
            if status in {"NOT_VISIBLE", "UNSUPPORTED"}: rec["fragments"] = []; rec["reason"] = "Intentional fixture outcome"
            else: rec["reason"] = "Only first visual fragment represented"
        mutate_json(r, "META-INF/spd/mapping.json", set_status)
        rebind(r)
        edges[name] = (r, f"Valid explicit {status} mapping outcome.", True)
    for name, text_value, body_value, language, direction_value, description in [
        ("emoji-range", "Family 👨‍👩‍👧‍👦 and flag 🇮🇶.", '<h1 id="n_heading01">Emoji</h1><section id="n_section01"><h2 id="n_heading02">Range</h2><p id="n_paragraph01">Family 👨‍👩‍👧‍👦 and flag 🇮🇶.</p></section>', "en", "ltr", "Emoji ZWJ/regional-indicator scalar offsets."),
        ("combining-character-range", "a\u0328\u0301 and क्षि.", '<h1 id="n_heading01">Combining</h1><section id="n_section01"><h2 id="n_heading02">Range</h2><p id="n_paragraph01">a\u0328\u0301 and क्षि.</p></section>', "en", "ltr", "Combining and Indic sequences expose scalar versus grapheme assumptions."),
        ("rtl-range", "النص Model 5 ثم ١٢٣.", '<h1 id="n_heading01">مدى</h1><section id="n_section01"><h2 id="n_heading02">مختلط</h2><p id="n_paragraph01">النص Model 5 ثم ١٢٣.</p></section>', "ar", "rtl", "Logical scalar range over RTL/LTR text."),
    ]:
        r = package_model(body_value, lang=language, direction=direction_value, mapped=True)
        mutate_json(r, "META-INF/spd/mapping.json", lambda x, n=len(text_value): x["records"][0]["fragments"][0]["textRange"].update(end=n))
        rebind(r)
        edges[name] = (r, description, True)
    edges["cjk-vertical"] = (package_model('<h1 id="n_heading01">縦書き</h1><section id="n_section01"><h2 id="n_heading02">日本語</h2><p id="n_paragraph01" style="writing-mode:vertical-rl">意味のある順序。</p></section>', lang="ja"), "CJK vertical writing retains DOM logical order.", False)
    r = package_model(fixed=True); r["EPUB/style.css"] += b"\np{letter-spacing:0.01em}"; rebind(r); mutate_json(r, "META-INF/spd/state.json", lambda x: x["fixedRendition"].update(status="stale")); rebind(r)
    edges["css-change-stales-fixed"] = (r, "Presentation-only CSS change preserves Revision ID/semanticStateDigest, changes renditionInputDigest, and stales fixed.", False)
    r = package_model(fixed=True, extra={"EPUB/font.woff2": b"fixture-font-v1"}); r["EPUB/font.woff2"] = b"fixture-font-v2"; rebind(r); mutate_json(r, "META-INF/spd/state.json", lambda x: x["fixedRendition"].update(status="stale")); rebind(r)
    edges["font-change-stales-fixed"] = (r, "Rendering-only font change stales fixed without creating a semantic revision.", False)
    for name, (resources, desc, mapped) in edges.items():
        emit("edge", name, resources, result(name, "edge", mapped=mapped, experimental=mapped or name in {"css-change-stales-fixed", "font-change-stales-fixed"}), desc)

    manifest = {"schemaVersion": "0.1", "generated": STAMP, "counts": {category: len([p for p in (TESTS/category).iterdir() if p.is_dir()]) for category in ("valid", "invalid", "edge")}}
    (TESTS / "corpus-manifest.json").write_bytes(jbytes(manifest))


if __name__ == "__main__":
    main()
