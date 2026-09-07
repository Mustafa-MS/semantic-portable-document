from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from lxml import etree


FO = "http://www.w3.org/1999/XSL/Format"
FOX = "http://xmlgraphics.apache.org/fop/extensions"
XMP = "adobe:ns:meta/"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
DC = "http://purl.org/dc/elements/1.1/"


def _fo(name: str, **attrs: str) -> etree._Element:
    return etree.Element(f"{{{FO}}}{name}", attrs)


def _text(element: etree._Element) -> str:
    return " ".join(" ".join(element.itertext()).split())


def _append(parent: etree._Element, source: etree._Element, base: Path, direction: str) -> None:
    tag = etree.QName(source).localname.lower()
    if tag in {"main", "article", "section", "nav", "thead", "tbody", "tfoot"}:
        for child in source:
            if isinstance(child.tag, str):
                _append(parent, child, base, direction)
        return
    if tag in {f"h{i}" for i in range(1, 7)}:
        size = {"h1": "24pt", "h2": "18pt", "h3": "14pt"}.get(tag, "12pt")
        block = _fo("block", **{"font-size": size, "font-weight": "bold", "space-before": "8pt", "space-after": "6pt", "keep-with-next": "always"})
        block.text = _text(source)
        parent.append(block)
        return
    if tag in {"p", "aside", "figcaption"}:
        block = _fo("block", **{"space-after": "6pt", "line-height": "1.35"})
        block.text = _text(source)
        parent.append(block)
        return
    if tag == "table":
        caption = source.xpath('./*[local-name()="caption"]')
        if caption:
            cap = _fo("block", **{"font-weight": "bold", "space-before": "6pt", "space-after": "3pt"})
            cap.text = _text(caption[0]); parent.append(cap)
        table = _fo("table", **{"table-layout": "fixed", "width": "100%", "border-collapse": "collapse", "space-after": "8pt"})
        rows = source.xpath('.//*[local-name()="tr"]')
        width = max((len(row.xpath('./*[local-name()="th" or local-name()="td"]')) for row in rows), default=1)
        for _ in range(width): table.append(_fo("table-column", **{"column-width": f"{100/width:.4f}%"}))
        body = _fo("table-body"); table.append(body)
        for row in rows:
            fo_row = _fo("table-row"); body.append(fo_row)
            for cell in row.xpath('./*[local-name()="th" or local-name()="td"]'):
                attrs = {"border": "0.6pt solid #777777", "padding": "4pt"}
                if cell.get("colspan"): attrs["number-columns-spanned"] = cell.get("colspan")
                if cell.get("rowspan"): attrs["number-rows-spanned"] = cell.get("rowspan")
                fo_cell = _fo("table-cell", **attrs)
                value = _fo("block", **({"font-weight": "bold"} if etree.QName(cell).localname.lower() == "th" else {}))
                value.text = _text(cell); fo_cell.append(value); fo_row.append(fo_cell)
        parent.append(table)
        return
    if tag == "figure":
        block = _fo("block", **{"space-before": "6pt", "space-after": "8pt"})
        image = source.xpath('./*[local-name()="img"]')
        if image:
            image_path = (base / image[0].get("src")).resolve()
            graphic = _fo("external-graphic", src=f"url('file:///{quote(image_path.as_posix())}')", **{"content-width": "90mm", f"{{{FOX}}}alt-text": image[0].get("alt", "")})
            block.append(graphic)
        caption = source.xpath('./*[local-name()="figcaption"]')
        if caption:
            cap = _fo("block", **{"font-style": "italic", "space-before": "3pt"}); cap.text = _text(caption[0]); block.append(cap)
        parent.append(block)
        return
    if tag in {"ul", "ol"}:
        items = source.xpath('./*[local-name()="li"]')
        listing = _fo("list-block", **{"provisional-distance-between-starts": "18pt", "provisional-label-separation": "6pt", "space-after": "6pt"})
        for index, item in enumerate(items, 1):
            list_item = _fo("list-item")
            label = _fo("list-item-label", **{"end-indent": "label-end()"}); label_block = _fo("block"); label_block.text = f"{index}." if tag == "ol" else "•"; label.append(label_block)
            body = _fo("list-item-body", **{"start-indent": "body-start()"}); body_block = _fo("block"); body_block.text = _text(item); body.append(body_block)
            list_item.extend([label, body]); listing.append(list_item)
        parent.append(listing)
        return
    if tag == "img" and not source.get("alt"):
        return
    if tag == "math":
        block = _fo("block"); block.text = " ".join(part.strip() for part in source.itertext() if part.strip()); parent.append(block)
        return
    for child in source:
        if isinstance(child.tag, str):
            _append(parent, child, base, direction)


def xhtml_to_fo(source: Path, output: Path) -> None:
    parsed = etree.parse(str(source)); html = parsed.getroot()
    lang = html.get("{http://www.w3.org/XML/1998/namespace}lang") or html.get("lang") or "en"
    direction = html.get("dir", "ltr")
    title = parsed.xpath('string(//*[local-name()="title"])') or source.stem
    root = etree.Element(f"{{{FO}}}root", nsmap={"fo": FO, "fox": FOX})
    declarations = _fo("declarations")
    xmpmeta = etree.SubElement(declarations, f"{{{XMP}}}xmpmeta", nsmap={"x": XMP, "rdf": RDF, "dc": DC})
    rdf = etree.SubElement(xmpmeta, f"{{{RDF}}}RDF")
    description = etree.SubElement(rdf, f"{{{RDF}}}Description", {f"{{{RDF}}}about": ""})
    dc_title = etree.SubElement(description, f"{{{DC}}}title")
    alt = etree.SubElement(dc_title, f"{{{RDF}}}Alt")
    etree.SubElement(alt, f"{{{RDF}}}li", {"{http://www.w3.org/XML/1998/namespace}lang": "x-default"}).text = title
    etree.SubElement(description, f"{{{DC}}}creator").text = "Phase 1C experimental harness"
    etree.SubElement(description, f"{{{DC}}}description").text = "Accessibility-aware independent PDF generation baseline"
    masters = _fo("layout-master-set"); root.append(masters)
    master = _fo("simple-page-master", **{"master-name": "A4", "page-width": "210mm", "page-height": "297mm", "margin": "18mm"}); master.append(_fo("region-body")); masters.append(master)
    root.append(declarations)
    sequence = _fo("page-sequence", **{"master-reference": "A4", "language": lang[:2], "writing-mode": "rl-tb" if direction == "rtl" else "lr-tb", "font-family": "Arial", "font-size": "10.5pt"})
    root.append(sequence); flow = _fo("flow", **{"flow-name": "xsl-region-body"}); sequence.append(flow)
    body = parsed.xpath('//*[local-name()="body"]')[0]
    for child in body:
        if isinstance(child.tag, str): _append(flow, child, source.parent, direction)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(etree.tostring(root, xml_declaration=True, encoding="UTF-8", pretty_print=True))


def write_fop_config(output: Path) -> None:
    arial = Path(r"C:\Windows\Fonts\arial.ttf").as_uri()
    arial_bold = Path(r"C:\Windows\Fonts\arialbd.ttf").as_uri()
    xml = f"""<?xml version=\"1.0\"?>
<fop version=\"1.0\">
  <accessibility keep-empty-tags=\"false\">true</accessibility>
  <complex-scripts disabled=\"false\"/>
  <renderers><renderer mime=\"application/pdf\"><pdf-ua-mode>PDF/UA-1</pdf-ua-mode><fonts>
    <font embed-url=\"{arial}\" embedding-mode=\"full\"><font-triplet name=\"Arial\" style=\"normal\" weight=\"normal\"/></font>
    <font embed-url=\"{arial_bold}\" embedding-mode=\"full\"><font-triplet name=\"Arial\" style=\"normal\" weight=\"bold\"/></font>
  </fonts></renderer></renderers>
</fop>"""
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(xml, encoding="utf-8")
