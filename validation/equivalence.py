from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any

import pdfplumber
from lxml import etree
from pypdf import PdfReader

from harness.util import normalize_text


def check_equivalence(source: Path, pdf: Path, mapping: dict[str, Any]) -> dict[str, Any]:
    tree = etree.parse(str(source))
    body = tree.xpath('//*[local-name()="body"]')[0]
    semantic = normalize_text(" ".join(body.itertext()))
    with pdfplumber.open(pdf) as fixed:
        extracted = normalize_text(" ".join(page.extract_text(use_text_flow=True) or "" for page in fixed.pages))
    ratio = difflib.SequenceMatcher(None, semantic, extracted).ratio()
    reader = PdfReader(pdf)
    root = reader.trailer["/Root"]
    lang = tree.getroot().get("lang", "")
    is_rtl = tree.getroot().get("dir") == "rtl"
    arabic_samples = [normalize_text(" ".join(el.itertext())) for el in tree.xpath('//*[@data-node-id]') if any("\u0600" <= c <= "\u06ff" for c in " ".join(el.itertext()))]
    exact_arabic = sum(1 for sample in arabic_samples if sample and sample in extracted)
    semantic_links = len(tree.xpath('//*[local-name()="a"][@href]'))
    pdf_links = sum(1 for page in reader.pages for ref in page.get("/Annots", []) if ref.get_object().get("/Subtype") == "/Link")
    mapped_nodes = {item["node"] for item in mapping.get("mappings", [])}
    return {
        "E1_structural_presence": {"mapped_nodes": len(mapped_nodes), **mapping.get("coverage", {})},
        "E2_text_equivalence": {"sequence_similarity": round(ratio, 4), "semantic_characters": len(semantic), "fixed_characters": len(extracted)},
        "E3_table_equivalence": {"semantic_cells": len(tree.xpath('//*[local-name()="td" or local-name()="th"]')), "mapped_cells": sum(1 for item in mapping.get("mappings", []) if item.get("kind") == "table-cell"), "relationships_extractable": False},
        "E4_reference_equivalence": {"semantic_links": semantic_links, "pdf_link_annotations": pdf_links},
        "E5_accessibility_equivalence": {"semantic_language": lang, "pdf_language": str(root.get("/Lang", "")), "structure_tree_present": "/StructTreeRoot" in root, "conformance_proven": False},
        "rtl": {"is_rtl_document": is_rtl, "arabic_samples": len(arabic_samples), "exact_logical_order_matches": exact_arabic, "copy_paste_automated": False},
    }

