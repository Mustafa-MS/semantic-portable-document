from __future__ import annotations

import mimetypes
import zipfile
from pathlib import Path
from typing import Any

from lxml import etree

from harness.util import sha256_file


MIMETYPE = b"application/epub+zip"
CONTAINER = b'''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>'''


def build_epub(
    output: Path,
    source: Path,
    css: Path,
    assets: list[Path],
    metadata: dict[str, str],
    fixed_pdf: Path | None = None,
    mapping: Path | None = None,
    state: Path | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    asset_items = []
    for index, asset in enumerate(assets):
        media = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
        asset_items.append(f'<item id="asset-{index}" href="assets/{asset.name}" media-type="{media}"/>')
    experimental_items = []
    if fixed_pdf:
        experimental_items.append('<item id="fixed-pdf" href="experimental/fixed.pdf" media-type="application/pdf"/>')
    if mapping:
        experimental_items.append('<item id="mapping" href="experimental/mapping.json" media-type="application/json"/>')
    if state:
        experimental_items.append('<item id="state" href="experimental/state.json" media-type="application/json"/>')
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{metadata['lang']}" prefix="semantic-fixed: https://example.org/semantic-fixed/vocab#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{metadata['document_id']}</dc:identifier>
    <dc:title>{metadata['title']}</dc:title><dc:language>{metadata['lang']}</dc:language>
    <meta property="dcterms:modified">2026-08-30T00:00:00Z</meta>
    <meta property="semantic-fixed:revision">{metadata['revision_id']}</meta>
  </metadata>
  <manifest><item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="style.css" media-type="text/css"/>{''.join(asset_items)}{''.join(experimental_items)}</manifest>
  <spine><itemref idref="content"/></spine>
</package>'''
    nav = f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{metadata['lang']}">
<head><title>Navigation</title></head><body><nav epub:type="toc"><h1>Contents</h1><ol><li><a href="content.xhtml">{metadata['title']}</a></li></ol></nav></body></html>'''
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("mimetype", MIMETYPE, compress_type=zipfile.ZIP_STORED)
        archive.writestr("META-INF/container.xml", CONTAINER)
        archive.writestr("OEBPS/package.opf", opf.encode("utf-8"))
        archive.writestr("OEBPS/nav.xhtml", nav.encode("utf-8"))
        archive.write(source, "OEBPS/content.xhtml")
        archive.write(css, "OEBPS/style.css")
        for asset in assets:
            archive.write(asset, f"OEBPS/assets/{asset.name}")
        for path, name in [(fixed_pdf, "fixed.pdf"), (mapping, "mapping.json"), (state, "state.json")]:
            if path:
                archive.write(path, f"OEBPS/experimental/{name}")


def validate_epub(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = set(archive.namelist())
        if not infos or infos[0].filename != "mimetype":
            errors.append("mimetype is not the first ZIP entry")
        elif infos[0].compress_type != zipfile.ZIP_STORED:
            errors.append("mimetype is compressed")
        elif archive.read("mimetype") != MIMETYPE:
            errors.append("incorrect mimetype payload")
        required = {"META-INF/container.xml", "OEBPS/package.opf", "OEBPS/nav.xhtml", "OEBPS/content.xhtml"}
        errors.extend(f"missing required resource: {name}" for name in sorted(required - names))
        for name in names & required:
            if name.endswith((".xml", ".xhtml", ".opf")):
                try:
                    etree.fromstring(archive.read(name))
                except Exception as exc:
                    errors.append(f"invalid XML {name}: {exc}")
        duplicates = {name for name in names if archive.namelist().count(name) > 1}
        errors.extend(f"duplicate ZIP resource: {name}" for name in sorted(duplicates))
    return {"valid_internal_profile": not errors, "errors": errors, "sha256": sha256_file(path), "epubcheck": "NOT RUN"}


def make_phase1b_compatible_epub(source_epub: Path, output: Path) -> dict[str, Any]:
    """Copy a Phase 1 EPUB and add required rendition properties without mutating it."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source_epub, "r") as source_archive:
        content = etree.fromstring(source_archive.read("OEBPS/content.xhtml"))
        needed: list[str] = []
        if content.xpath('//*[local-name()="math"]'):
            needed.append("mathml")
        if content.xpath('//*[local-name()="svg"]'):
            needed.append("svg")

        opf = etree.fromstring(source_archive.read("OEBPS/package.opf"))
        ns = {"opf": "http://www.idpf.org/2007/opf"}
        content_item = opf.xpath('//opf:item[@id="content"]', namespaces=ns)[0]
        existing = content_item.get("properties", "").split()
        merged = sorted(set(existing + needed))
        if merged:
            content_item.set("properties", " ".join(merged))

        with zipfile.ZipFile(output, "w") as target_archive:
            for info in source_archive.infolist():
                payload = (etree.tostring(opf, xml_declaration=True, encoding="UTF-8")
                           if info.filename == "OEBPS/package.opf"
                           else source_archive.read(info.filename))
                copied = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                copied.compress_type = info.compress_type
                copied.external_attr = info.external_attr
                copied.comment = info.comment
                target_archive.writestr(copied, payload)
    return {"source": str(source_epub), "output": str(output), "addedContentProperties": needed, "sha256": sha256_file(output)}
