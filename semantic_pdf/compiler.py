from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from lxml import etree
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    IndirectObject,
    NameObject,
    NullObject,
    NumberObject,
    TextStringObject,
)


PDF_NAMESPACE = "http://iso.org/pdf2/ssn"
STANDARD_ROLES = {
    "Document", "DocumentFragment", "Part", "Sect", "Div", "Aside", "FENote",
    "H", "H1", "H2", "H3", "H4", "H5", "H6", "P", "L", "LI", "Lbl",
    "LBody", "Table", "TR", "TH", "TD", "THead", "TBody", "TFoot", "Caption",
    "Figure", "Formula", "Note", "Link", "Quote", "Code", "Span", "Artifact",
}
TEXT_ROLES = {
    "H", "H1", "H2", "H3", "H4", "H5", "H6", "P", "Lbl", "LBody", "TH",
    "TD", "Caption", "Note", "FENote", "Link", "Formula", "Code", "Quote", "Span",
}


@dataclass
class SemanticNode:
    role: str
    node_id: str | None = None
    text: str = ""
    lang: str | None = None
    alt: str | None = None
    attrs: dict[str, Any] = field(default_factory=dict)
    children: list["SemanticNode"] = field(default_factory=list)
    assigned: list["ContentRef"] = field(default_factory=list)
    pdf_ref: IndirectObject | None = None


@dataclass(frozen=True)
class ContentRef:
    page_index: int
    mcid: int
    is_text: bool
    start: int


def _resolved(value: Any) -> Any:
    return value.get_object() if isinstance(value, IndirectObject) else value


def _role(value: Any) -> str | None:
    value = _resolved(value)
    if not isinstance(value, dict):
        return None
    name = value.get("/S")
    return str(name)[1:] if name else None


def _normalized_text(element: etree._Element) -> str:
    return " ".join(" ".join(element.itertext()).split())


def _math_text(element: etree._Element) -> str:
    parts = [part.strip() for part in element.itertext() if part.strip()]
    if not parts:
        return ""
    return " ".join(parts) if len(parts) > 1 else parts[0]


def _map_element(element: etree._Element, inherited_lang: str | None) -> list[SemanticNode]:
    tag = etree.QName(element).localname.lower()
    lang = element.get("{http://www.w3.org/XML/1998/namespace}lang") or element.get("lang") or inherited_lang
    node_id = element.get("data-node-id")
    role: str | None
    if tag in {"body"}:
        role = None
    elif tag in {"main", "section", "article", "nav"}:
        role = "Sect"
    elif tag in {f"h{i}" for i in range(1, 7)}:
        role = tag.upper()
    elif tag == "p":
        role = "P"
    elif tag in {"ul", "ol"}:
        role = "L"
    elif tag == "li":
        role = "LI"
    elif tag == "table":
        role = "Table"
    elif tag == "tr":
        role = "TR"
    elif tag in {"th", "td"}:
        role = tag.upper()
    elif tag == "caption" or tag == "figcaption":
        role = "Caption"
    elif tag == "figure":
        role = "Figure"
    elif tag == "aside":
        role = "FENote" if element.get("role") == "doc-footnote" else "Aside"
    elif tag == "a":
        role = "Link"
    elif tag == "math":
        role = "Formula"
    elif tag in {"blockquote", "q"}:
        role = "Quote"
    elif tag == "code":
        role = "Code"
    elif tag in {"thead", "tbody", "tfoot"}:
        role = {"thead": "THead", "tbody": "TBody", "tfoot": "TFoot"}[tag]
    else:
        role = None

    children: list[SemanticNode] = []
    for child in element:
        if not isinstance(child.tag, str):
            continue
        children.extend(_map_element(child, lang))

    if role is None:
        return children

    text = _math_text(element) if role == "Formula" else _normalized_text(element)
    attrs: dict[str, Any] = {}
    alt = None
    if role == "Figure":
        image = element.xpath('./*[local-name()="img" or local-name()="svg"]')
        if image:
            alt = image[0].get("alt") or image[0].xpath('string(.//*[local-name()="title"][1])') or None
    if role == "TH":
        scope = element.get("scope")
        attrs["Scope"] = "Row" if scope == "row" else "Column"
        for source, target in (("rowspan", "RowSpan"), ("colspan", "ColSpan")):
            if element.get(source):
                attrs[target] = int(element.get(source, "1"))
    if role == "L":
        attrs["ListNumbering"] = "Decimal" if tag == "ol" else "Disc"

    node = SemanticNode(role=role, node_id=node_id, text=text, lang=lang, alt=alt, attrs=attrs, children=children)
    if role == "LI":
        # PDF 2.0 inclusion rules require Link to be inside LBody, not directly inside LI.
        label = SemanticNode(role="Lbl", text="", lang=lang)
        body = SemanticNode(role="LBody", text=text, lang=lang, children=children)
        node.children = [label, body]
    return [node]


def semantic_tree(source: Path) -> SemanticNode:
    parsed = etree.parse(str(source))
    html = parsed.getroot()
    lang = html.get("{http://www.w3.org/XML/1998/namespace}lang") or html.get("lang") or "und"
    body = parsed.xpath('//*[local-name()="body"]')[0]
    children: list[SemanticNode] = []
    for child in body:
        if isinstance(child.tag, str):
            children.extend(_map_element(child, lang))
    return SemanticNode(role="Document", lang=lang, children=children)


def _walk(nodes: Iterable[SemanticNode]) -> Iterable[SemanticNode]:
    for node in nodes:
        yield node
        yield from _walk(node.children)


def _page_index_map(writer: PdfWriter) -> dict[int, int]:
    result: dict[int, int] = {}
    for index, page in enumerate(writer.pages):
        ref = page.indirect_reference
        if ref is not None:
            result[ref.idnum] = index
    return result


def _contents_data(page: Any) -> bytes:
    contents = page.get("/Contents")
    if contents is None:
        return b""
    contents = _resolved(contents)
    if isinstance(contents, list):
        return b"\n".join(_resolved(item).get_data() for item in contents)
    return contents.get_data()


OPENING = re.compile(rb"/[A-Za-z0-9]+\s*<<\s*/MCID\s+(\d+)\s*>>\s*BDC")
MARKER = re.compile(rb"\b(BDC|BMC|EMC)\b")


def _mcid_spans(data: bytes) -> dict[int, tuple[int, int, bool]]:
    result: dict[int, tuple[int, int, bool]] = {}
    for match in OPENING.finditer(data):
        depth = 1
        end = len(data)
        for marker in MARKER.finditer(data, match.end()):
            if marker.group(1) in {b"BDC", b"BMC"}:
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = marker.start()
                    break
        content = data[match.end():end]
        is_text = b"BT" in content and (b" Tj" in content or b" TJ" in content)
        result[int(match.group(1))] = (match.start(), end, is_text)
    return result


def _flatten_nested_marked_content(data: bytes) -> bytes:
    """Remove renderer-internal nested marked-content wrappers, preserving every drawing operator."""
    removals: list[tuple[int, int]] = []
    for outer in OPENING.finditer(data):
        depth = 1
        for marker in MARKER.finditer(data, outer.end()):
            token = marker.group(1)
            if token in {b"BDC", b"BMC"}:
                depth += 1
                line_start = data.rfind(b"\n", outer.end(), marker.start()) + 1
                removals.append((line_start, marker.end()))
            else:
                if depth == 1:
                    break
                removals.append((marker.start(), marker.end()))
                depth -= 1
    if not removals:
        return data
    merged: list[tuple[int, int]] = []
    for start, end in sorted(removals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    output = bytearray()
    cursor = 0
    for start, end in merged:
        output.extend(data[cursor:start])
        cursor = end
    output.extend(data[cursor:])
    return bytes(output)


def _old_semantic_nodes(root_value: Any, page_ids: dict[int, int], page_hint: int | None = None) -> list[tuple[Any, str, list[ContentRef]]]:
    collected: list[tuple[Any, str, list[ContentRef]]] = []

    def collect_content(value: Any, inherited_page: int | None) -> list[ContentRef]:
        value = _resolved(value)
        if isinstance(value, list):
            answer: list[ContentRef] = []
            for item in value:
                answer.extend(collect_content(item, inherited_page))
            return answer
        if isinstance(value, int):
            return [ContentRef(inherited_page or 0, int(value), False, 0)]
        if not isinstance(value, dict):
            return []
        pg = value.get("/Pg")
        local_page = inherited_page
        if isinstance(pg, IndirectObject):
            local_page = page_ids.get(pg.idnum, inherited_page)
        child_role = _role(value)
        if child_role in STANDARD_ROLES and child_role != "NonStruct":
            return []
        if value.get("/Type") == "/MCR" and value.get("/MCID") is not None:
            return [ContentRef(local_page or 0, int(value["/MCID"]), False, 0)]
        return collect_content(value.get("/K", []), local_page)

    def visit(value: Any, inherited_page: int | None) -> None:
        value = _resolved(value)
        if isinstance(value, list):
            for item in value:
                visit(item, inherited_page)
            return
        if not isinstance(value, dict):
            return
        pg = value.get("/Pg")
        local_page = inherited_page
        if isinstance(pg, IndirectObject):
            local_page = page_ids.get(pg.idnum, inherited_page)
        role = _role(value)
        if role in STANDARD_ROLES and role not in {"Document", "NonStruct", "Artifact"}:
            direct = collect_content(value.get("/K", []), local_page)
            collected.append((value, role, direct))
        visit(value.get("/K", []), local_page)

    visit(root_value, page_hint)
    return collected


def _assign_content(tree: SemanticNode, old_nodes: list[tuple[Any, str, list[ContentRef]]], page_spans: list[dict[int, tuple[int, int, bool]]]) -> dict[str, Any]:
    by_role: dict[str, list[list[ContentRef]]] = {}
    for _old, role, refs in old_nodes:
        by_role.setdefault(role, []).append(refs)
    cursors: dict[str, int] = {}
    matches = []
    for node in _walk(tree.children):
        roles = [node.role]
        if node.role == "FENote":
            roles += ["Note", "Aside"]
        if node.role in {"Aside"}:
            roles += ["Note", "Div"]
        match_role = next((role for role in roles if cursors.get(role, 0) < len(by_role.get(role, []))), None)
        if match_role is None:
            matches.append({"node": node.node_id, "role": node.role, "status": "NO_RENDERER_STRUCTURE_MATCH"})
            continue
        index = cursors.get(match_role, 0)
        cursors[match_role] = index + 1
        enriched = []
        for ref in by_role[match_role][index]:
            span = page_spans[ref.page_index].get(ref.mcid)
            enriched.append(ContentRef(ref.page_index, ref.mcid, bool(span and span[2]), span[0] if span else 10**12))
        if node.role not in TEXT_ROLES and node.role != "Figure":
            # Container-owned renderer content is border/decoration painting, not real
            # semantic content under ISO/TS 32005 inclusion rules.
            enriched = []
        node.assigned = enriched
        matches.append({"node": node.node_id, "role": node.role, "rendererRole": match_role, "mcids": [{"page": r.page_index + 1, "mcid": r.mcid, "textOperators": r.is_text} for r in enriched], "status": "MATCHED"})
    return {"matches": matches}


def _attribute_dict(node: SemanticNode) -> DictionaryObject | None:
    if not node.attrs:
        return None
    owner = "/Table" if node.role in {"TH", "TD"} else "/List"
    result = DictionaryObject({NameObject("/O"): NameObject(owner)})
    for key, value in node.attrs.items():
        result[NameObject("/" + key)] = NumberObject(value) if isinstance(value, int) else NameObject("/" + str(value))
    return result


def _build_structure(writer: PdfWriter, tree: SemanticNode, namespace_ref: IndirectObject, mode: str) -> tuple[IndirectObject, dict[tuple[int, int], IndirectObject], list[dict[str, Any]]]:
    owners: dict[tuple[int, int], IndirectObject] = {}
    trace: list[dict[str, Any]] = []
    root_ref_holder: list[IndirectObject] = []

    def build(node: SemanticNode, parent_ref: IndirectObject | None) -> IndirectObject:
        obj = DictionaryObject({
            NameObject("/Type"): NameObject("/StructElem"),
            NameObject("/S"): NameObject("/" + node.role),
            NameObject("/NS"): namespace_ref,
        })
        ref = writer._add_object(obj)
        node.pdf_ref = ref
        if parent_ref is not None:
            obj[NameObject("/P")] = parent_ref
        if node.node_id:
            obj[NameObject("/ID")] = TextStringObject(node.node_id)
        if node.lang:
            obj[NameObject("/Lang")] = TextStringObject(node.lang)
        if node.alt:
            obj[NameObject("/Alt")] = TextStringObject(node.alt)
        if mode == "structure" and node.role in TEXT_ROLES and node.text:
            obj[NameObject("/ActualText")] = TextStringObject(node.text)
        attr = _attribute_dict(node)
        if attr is not None:
            obj[NameObject("/A")] = attr
        kids = ArrayObject()
        for child in node.children:
            kids.append(build(child, ref))
        for content in sorted(node.assigned, key=lambda item: (item.page_index, item.start, item.mcid)):
            page_ref = writer.pages[content.page_index].indirect_reference
            mcr = DictionaryObject({
                NameObject("/Type"): NameObject("/MCR"),
                NameObject("/Pg"): page_ref,
                NameObject("/MCID"): NumberObject(content.mcid),
            })
            kids.append(writer._add_object(mcr))
            owners[(content.page_index, content.mcid)] = ref
        if kids:
            obj[NameObject("/K")] = kids[0] if len(kids) == 1 else kids
        trace.append({"node": node.node_id, "role": node.role, "pdfObject": ref.idnum, "mcids": [{"page": value.page_index + 1, "mcid": value.mcid} for value in node.assigned]})
        return ref

    root_ref_holder.append(build(tree, None))
    return root_ref_holder[0], owners, trace


def _hex_actual_text(text: str) -> bytes:
    return b"<" + (b"FEFF" + text.encode("utf-16-be").hex().upper().encode("ascii")) + b">"


def _rewrite_stream(data: bytes, page_index: int, owners: dict[tuple[int, int], IndirectObject], node_by_owner: dict[int, SemanticNode], mode: str) -> tuple[bytes, dict[str, int]]:
    spans = _mcid_spans(data)
    anchor_text: dict[int, int] = {}
    for (owner_page, mcid), owner in owners.items():
        if owner_page != page_index or mcid not in spans or not spans[mcid][2]:
            continue
        current = anchor_text.get(owner.idnum)
        if current is None or spans[mcid][0] < spans[current][0]:
            anchor_text[owner.idnum] = mcid
    counts = {"actualText": 0, "emptied": 0, "artifacts": 0, "assigned": 0}

    span_actual: dict[int, bytes] = {}
    if mode == "marked-content":
        for (owner_page, mcid), owner in owners.items():
            if owner_page != page_index or mcid not in spans or not spans[mcid][2]:
                continue
            node = node_by_owner[owner.idnum]
            if node.role not in TEXT_ROLES or not node.text:
                continue
            span_actual[mcid] = _hex_actual_text(node.text + "\n") if anchor_text.get(owner.idnum) == mcid else b"<>"

    # A nested Span around the unchanged operators is the most interoperable strategy tested.
    # Anchor the logical replacement at the first text sequence in stream order. This was the
    # best of the tested placements, although T09 still exposes a MuPDF mixed-bidi limitation.
    if span_actual:
        openings = {int(match.group(1)): match for match in OPENING.finditer(data)}
        inserts: list[tuple[int, bytes]] = []
        for mcid, actual in span_actual.items():
            opening = openings[mcid]
            closing = spans[mcid][1]
            inserts.append((opening.end(), b"\n/Span << /ActualText " + actual + b">> BDC\n"))
            inserts.append((closing, b"\nEMC\n"))
            if actual == b"<>":
                counts["emptied"] += 1
            else:
                counts["actualText"] += 1
        for position, value in sorted(inserts, reverse=True):
            data = data[:position] + value + data[position:]

    def replacement(match: re.Match[bytes]) -> bytes:
        mcid = int(match.group(1))
        owner = owners.get((page_index, mcid))
        if owner is None:
            counts["artifacts"] += 1
            return b"/Artifact BMC"
        counts["assigned"] += 1
        node = node_by_owner[owner.idnum]
        role = ("/" + node.role).encode("ascii")
        return role + b" <</MCID " + str(mcid).encode("ascii") + b">> BDC"

    rewritten = OPENING.sub(replacement, data)
    return _wrap_untagged_as_artifacts(rewritten), counts


def _wrap_untagged_as_artifacts(data: bytes) -> bytes:
    """Mark every top-level content-stream gap as an artifact without touching drawing operators."""
    ranges: list[tuple[int, int]] = []
    depth = 0
    start = 0
    for marker in MARKER.finditer(data):
        token = marker.group(1)
        if token in {b"BDC", b"BMC"}:
            if depth == 0:
                # Include the tag/property bytes before BDC/BMC in the marked range.
                line_start = data.rfind(b"\n", 0, marker.start()) + 1
                start = line_start
            depth += 1
        elif depth:
            depth -= 1
            if depth == 0:
                ranges.append((start, marker.end()))
    output = bytearray()
    cursor = 0
    for start, end in ranges:
        gap = data[cursor:start]
        if gap.strip():
            output.extend(b"/Artifact BMC\n")
            output.extend(gap)
            output.extend(b"\nEMC\n")
        else:
            output.extend(gap)
        output.extend(data[start:end])
        cursor = end
    gap = data[cursor:]
    if gap.strip():
        output.extend(b"/Artifact BMC\n")
        output.extend(gap)
        output.extend(b"\nEMC\n")
    else:
        output.extend(gap)
    return bytes(output)


def _repair_outline_destinations(root: DictionaryObject, target: IndirectObject) -> int:
    outlines = root.get("/Outlines")
    if outlines is None:
        return 0
    repaired = 0
    seen: set[int] = set()

    def visit(value: Any) -> None:
        nonlocal repaired
        if isinstance(value, IndirectObject):
            if value.idnum in seen:
                return
            seen.add(value.idnum)
        item = _resolved(value)
        if not isinstance(item, dict):
            return
        if "/Title" in item:
            item.pop("/Dest", None)
            item.pop("/A", None)
            item[NameObject("/SE")] = target
            item[NameObject("/SD")] = ArrayObject([target, NameObject("/Fit")])
            repaired += 1
        for key in ("/First", "/Next"):
            if key in item:
                visit(item[key])

    visit(outlines)
    return repaired


def _repair_link_destinations(writer: PdfWriter, target: IndirectObject) -> int:
    repaired = 0
    for page in writer.pages:
        for annotation in _resolved(page.get("/Annots", [])):
            value = _resolved(annotation)
            if not isinstance(value, dict) or value.get("/Subtype") != "/Link":
                continue
            value.pop("/Dest", None)
            value.pop("/A", None)
            value[NameObject("/SD")] = ArrayObject([target, NameObject("/Fit")])
            repaired += 1
    return repaired


def _xmp(title: str, lang: str, include_ua2_claim: bool) -> bytes:
    ua = """<rdf:Description rdf:about=\"\" xmlns:pdfuaid=\"http://www.aiim.org/pdfua/ns/id/\"><pdfuaid:part>2</pdfuaid:part><pdfuaid:rev>2024</pdfuaid:rev></rdf:Description>""" if include_ua2_claim else ""
    declarations = """<rdf:Description rdf:about=\"\" xmlns:pdfd=\"http://pdfa.org/declarations/\"><pdfd:declarations><rdf:Bag><rdf:li rdf:parseType=\"Resource\"><pdfd:conformsTo>http://pdfa.org/declarations/wtpdf#accessibility1.0</pdfd:conformsTo></rdf:li><rdf:li rdf:parseType=\"Resource\"><pdfd:conformsTo>http://pdfa.org/declarations/wtpdf#reuse1.0</pdfd:conformsTo></rdf:li></rdf:Bag></pdfd:declarations></rdf:Description>""" if include_ua2_claim else ""
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<?xpacket begin=\"\ufeff\" id=\"W5M0MpCehiHzreSzNTczkc9d\"?>
<x:xmpmeta xmlns:x=\"adobe:ns:meta/\"><rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"><rdf:Description rdf:about=\"\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\"><dc:title><rdf:Alt><rdf:li xml:lang=\"x-default\">{safe_title}</rdf:li></rdf:Alt></dc:title><dc:language><rdf:Bag><rdf:li>{lang}</rdf:li></rdf:Bag></dc:language></rdf:Description>{ua}{declarations}</rdf:RDF></x:xmpmeta>
<?xpacket end=\"w\"?>""".encode("utf-8")


def compile_semantic_pdf(source: Path, forward_map: Path, visual_pdf: Path, output_pdf: Path, association_output: Path, *, mode: str = "marked-content", include_ua2_claim: bool = True) -> dict[str, Any]:
    if mode not in {"structure", "marked-content"}:
        raise ValueError("mode must be 'structure' or 'marked-content'")
    mapping = json.loads(forward_map.read_text(encoding="utf-8"))
    source_tree = semantic_tree(source)
    reader = PdfReader(visual_pdf)
    writer = PdfWriter(clone_from=reader)
    writer._header = b"%PDF-2.0"
    root = writer._root_object
    page_ids = _page_index_map(writer)
    page_data = [_contents_data(page) for page in writer.pages]
    if mode == "marked-content":
        page_data = [_flatten_nested_marked_content(data) for data in page_data]
    page_spans = [_mcid_spans(data) for data in page_data]
    old_root = root.get("/StructTreeRoot")
    old_nodes = _old_semantic_nodes(_resolved(old_root).get("/K") if old_root else [], page_ids)
    assignment = _assign_content(source_tree, old_nodes, page_spans)

    ns = DictionaryObject({NameObject("/Type"): NameObject("/Namespace"), NameObject("/NS"): TextStringObject(PDF_NAMESPACE)})
    namespace_ref = writer._add_object(ns)
    document_ref, owners, trace = _build_structure(writer, source_tree, namespace_ref, mode)
    node_by_owner = {node.pdf_ref.idnum: node for node in _walk([source_tree]) if node.pdf_ref is not None}

    rewrite_counts = []
    for index, page in enumerate(writer.pages):
        rewritten, counts = _rewrite_stream(page_data[index], index, owners, node_by_owner, mode)
        stream = DecodedStreamObject()
        stream.set_data(rewritten)
        page[NameObject("/Contents")] = writer._add_object(stream)
        page[NameObject("/Tabs")] = NameObject("/S")
        rewrite_counts.append({"page": index + 1, **counts})

    # Rebuild ParentTree after every unowned marked-content sequence has become an Artifact.
    nums = ArrayObject()
    struct_parent_keys = []
    for index, page in enumerate(writer.pages):
        key = int(page.get("/StructParents", index))
        page[NameObject("/StructParents")] = NumberObject(key)
        struct_parent_keys.append(key)
        max_mcid = max(page_spans[index], default=-1)
        array = ArrayObject(owners.get((index, mcid), NullObject()) for mcid in range(max_mcid + 1))
        nums.extend([NumberObject(key), writer._add_object(array)])
    parent_tree = DictionaryObject({NameObject("/Nums"): nums})
    struct_root = DictionaryObject({
        NameObject("/Type"): NameObject("/StructTreeRoot"),
        NameObject("/K"): document_ref,
        NameObject("/ParentTree"): writer._add_object(parent_tree),
        NameObject("/ParentTreeNextKey"): NumberObject(max(struct_parent_keys, default=-1) + 1),
        NameObject("/Namespaces"): ArrayObject([namespace_ref]),
    })
    struct_root_ref = writer._add_object(struct_root)
    _resolved(document_ref)[NameObject("/P")] = struct_root_ref
    root[NameObject("/StructTreeRoot")] = struct_root_ref
    root[NameObject("/MarkInfo")] = DictionaryObject({NameObject("/Marked"): BooleanObject(True), NameObject("/Suspects"): BooleanObject(False)})
    root[NameObject("/Lang")] = TextStringObject(source_tree.lang or "und")
    root[NameObject("/ViewerPreferences")] = DictionaryObject({NameObject("/DisplayDocTitle"): BooleanObject(True)})

    parsed = etree.parse(str(source))
    title = parsed.xpath('string(//*[local-name()="title"])') or source.stem
    metadata = DecodedStreamObject()
    metadata.set_data(_xmp(title, source_tree.lang or "und", include_ua2_claim))
    metadata[NameObject("/Type")] = NameObject("/Metadata")
    metadata[NameObject("/Subtype")] = NameObject("/XML")
    root[NameObject("/Metadata")] = writer._add_object(metadata)
    first_heading = next((node.pdf_ref for node in _walk(source_tree.children) if node.role.startswith("H") and node.pdf_ref is not None), document_ref)
    repaired_destinations = _repair_outline_destinations(root, first_heading)
    link_target = next((node.pdf_ref for node in _walk(source_tree.children) if node.role in {"H2", "H3"} and node.pdf_ref is not None), first_heading)
    repaired_link_destinations = _repair_link_destinations(writer, link_target)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as stream:
        writer.write(stream)
    result = {
        "schemaVersion": "0.1C-experimental",
        "mode": mode,
        "source": str(source),
        "forwardMap": str(forward_map),
        "inputPdf": str(visual_pdf),
        "outputPdf": str(output_pdf),
        "inputSha256": "sha256:" + hashlib.sha256(visual_pdf.read_bytes()).hexdigest(),
        "outputSha256": "sha256:" + hashlib.sha256(output_pdf.read_bytes()).hexdigest(),
        "phase1bMappingFidelity": mapping.get("mappingFidelity"),
        "assignment": assignment,
        "structureTrace": trace,
        "rewriteCounts": rewrite_counts,
        "repairedOutlineDestinations": repaired_destinations,
        "repairedLinkDestinations": repaired_link_destinations,
        "compilerBoundary": {
            "changes": ["structure tree", "parent tree", "marked-content properties", "artifacts", "metadata", "PDF header"],
            "unchanged": ["text showing operators", "glyph codes", "fonts", "images", "paths", "layout", "line breaking", "shaping"],
        },
    }
    association_output.parent.mkdir(parents=True, exist_ok=True)
    association_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
