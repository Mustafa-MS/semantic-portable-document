from __future__ import annotations

import json
import math
import statistics
import subprocess
import time
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any

import pdfplumber
from lxml import etree

from harness.util import ROOT, sha256_file, write_json
from mapping.generate import ADDRESSABLE


def _quad(rect: list[float], x_scale: float, y_scale: float) -> list[float]:
    x0, y0, x1, y1 = rect
    return [round(x0*x_scale, 3), round(y0*y_scale, 3), round(x1*x_scale, 3), round(y0*y_scale, 3), round(x1*x_scale, 3), round(y1*y_scale, 3), round(x0*x_scale, 3), round(y1*y_scale, 3)]


def _union_rects(rects: list[list[float]]) -> list[float]:
    return [min(r[0] for r in rects), min(r[1] for r in rects), max(r[2] for r in rects), max(r[3] for r in rects)]


def run_pagedjs_forward(source: Path, pdf: Path, output: Path, raw_output: Path) -> dict[str, Any]:
    runtime = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
    node = runtime / "bin" / "node.exe"
    chrome = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    polyfill = ROOT / ".phase1b" / "deps" / "node" / "node_modules" / "pagedjs" / "dist" / "paged.polyfill.js"
    script = ROOT / "renderers" / "pagedjs_forward.cjs"
    env_path = str(ROOT / ".phase1b" / "deps" / "node" / "node_modules") + ";" + str(runtime / "node_modules")
    import os
    env = os.environ.copy(); env["NODE_PATH"] = env_path
    started = time.perf_counter()
    proc = subprocess.run([str(node), str(script), str(source), str(pdf), str(raw_output), str(chrome), str(polyfill)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
    elapsed = round((time.perf_counter() - started) * 1000, 2)
    if proc.returncode != 0:
        raise RuntimeError(f"Paged.js adapter failed: {proc.stderr[-4000:]}")
    raw = json.loads(raw_output.read_text(encoding="utf-8"))
    with pdfplumber.open(pdf) as fixed:
        pdf_pages = [{"id": f"pg_{i+1}", "width": float(p.width), "height": float(p.height), "unit": "pt"} for i, p in enumerate(fixed.pages)]
    if len(pdf_pages) != len(raw["pages"]):
        raise RuntimeError(f"Paged DOM/PDF page mismatch: {len(raw['pages'])} vs {len(pdf_pages)}")
    transforms = {}
    for dom_page, pdf_page in zip(raw["pages"], pdf_pages):
        transforms[dom_page["id"]] = {"x": pdf_page["width"] / dom_page["widthCssPx"], "y": pdf_page["height"] / dom_page["heightCssPx"]}

    blocks: dict[str, dict[str, list[list[float]]]] = defaultdict(lambda: defaultdict(list))
    for fragment in raw["blockFragments"]:
        blocks[fragment["node"]][fragment["page"]].append(fragment["rectCssPx"])
    text: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fragment in raw["textFragments"]:
        text[fragment["node"]].append(fragment)

    tree = etree.parse(str(source))
    elements = {el.get("data-node-id"): el for el in tree.xpath('//*[@data-node-id]') if etree.QName(el).localname in ADDRESSABLE}
    records = []
    mapped_visible = 0
    expected_visible = 0
    mapped_chars = 0
    expected_chars = 0
    for node_id, element in elements.items():
        catalog = raw["catalog"]["nodes"].get(node_id, {})
        visible = bool(catalog.get("visibleInSourceLayout", True))
        if visible:
            expected_visible += 1
        block_pages = blocks.get(node_id, {})
        method = "forward:pagedjs-dom"
        confidence = "EXACT_IDENTITY_PROPAGATION"
        if not block_pages:
            # Ancestor correspondence is the union of explicitly identified descendants, not a
            # second remapping of their text.
            descendant_ids = element.xpath('.//*[@data-node-id]/@data-node-id')
            union_pages: dict[str, list[list[float]]] = defaultdict(list)
            for descendant in descendant_ids:
                for page_id, rects in blocks.get(descendant, {}).items():
                    union_pages[page_id].extend(rects)
            if union_pages:
                block_pages = union_pages
                method = "forward:pagedjs-descendant-union"
        block_fragments = []
        for page_id, rects in sorted(block_pages.items()):
            scale = transforms[page_id]
            block_fragments.append({"type": "block", "page": page_id, "quad": _quad(_union_rects(rects), scale["x"], scale["y"]), "transform": [round(scale["x"], 8), 0, 0, round(scale["y"], 8), 0, 0]})
        range_fragments = []
        mapped_intervals = set()
        for fragment in text.get(node_id, []):
            page_id = fragment["page"]; scale = transforms[page_id]
            start, end = fragment["logicalRange"]
            mapped_intervals.update(range(start, end))
            range_fragments.append({"type": "text-range", "page": page_id, "logicalRange": [start, end], "quad": _quad(fragment["rectCssPx"], scale["x"], scale["y"]), "transform": [round(scale["x"], 8), 0, 0, round(scale["y"], 8), 0, 0]})
        node_expected_chars = int(catalog.get("expectedNonWhitespaceCharacters", 0))
        node_mapped_chars = min(len(mapped_intervals), node_expected_chars)
        expected_chars += node_expected_chars
        mapped_chars += node_mapped_chars
        if block_fragments or range_fragments:
            mapped_visible += int(visible)
            status = "MAPPED" if node_expected_chars == 0 or node_mapped_chars >= node_expected_chars else "PARTIALLY_MAPPED"
            if range_fragments:
                confidence = "EXACT_TEXT_RANGE_LAYOUT"
        else:
            status = "NOT_VISIBLE" if not visible else "UNMAPPABLE"
            confidence = "UNVERIFIED"
        records.append({
            "node": node_id, "tag": etree.QName(element).localname, "status": status,
            "method": method, "confidence": confidence,
            "rangeCoverage": {"mappedCharacters": node_mapped_chars, "expectedCharacters": node_expected_chars, "ratio": round(node_mapped_chars/node_expected_chars, 4) if node_expected_chars else None},
            "nonVisualCharacters": int(catalog.get("nonVisualNonWhitespaceCharacters", 0)),
            "fragments": block_fragments + range_fragments,
        })
    result = {
        "schemaVersion": "0.1B-experimental",
        "document": raw["catalog"]["documentId"], "revision": raw["catalog"]["revisionId"],
        "fixedRendition": "f_" + uuid.uuid4().hex, "fixedRenditionHash": sha256_file(pdf),
        "adapter": raw["adapter"], "processingTimeMs": elapsed,
        "coordinateSystem": {"unit": "pt", "origin": "page-top-left", "calibration": "per-page CSS-pixel to PDF-point scale"},
        "pages": pdf_pages, "records": records,
        "mappingFidelity": {
            "visibleNodeMapping": {"mapped": mapped_visible, "expected": expected_visible, "ratio": round(mapped_visible/expected_visible, 4) if expected_visible else 1.0},
            "logicalRangeMapping": {"mappedCharacters": mapped_chars, "expectedCharacters": expected_chars, "ratio": round(mapped_chars/expected_chars, 4) if expected_chars else 1.0},
        },
    }
    write_json(output, result)
    return result


def _bbox(quad: list[float]) -> tuple[float, float, float, float]:
    return min(quad[0::2]), min(quad[1::2]), max(quad[0::2]), max(quad[1::2])


def _iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ix0, iy0, ix1, iy1 = max(a[0],b[0]), max(a[1],b[1]), min(a[2],b[2]), min(a[3],b[3])
    inter = max(0, ix1-ix0) * max(0, iy1-iy0)
    union = max(0,(a[2]-a[0])*(a[3]-a[1])) + max(0,(b[2]-b[0])*(b[3]-b[1])) - inter
    return inter/union if union else 0.0


def calibrate_geometry(forward: dict[str, Any], backward: dict[str, Any]) -> dict[str, Any]:
    forward_by = {}
    for record in forward["records"]:
        page_groups: dict[str, list[list[float]]] = defaultdict(list)
        for fragment in record["fragments"]:
            if fragment["type"] == "text-range": page_groups[fragment["page"]].append(list(_bbox(fragment["quad"])))
        for page, rects in page_groups.items():
            forward_by[(record["node"],page)] = tuple(_union_rects(rects))
    backward_by = {}
    for item in backward.get("mappings", []):
        for fragment in item.get("fragments", []):
            backward_by[(item["node"],fragment["page"])] = _bbox(fragment["quad"])
    pairs = sorted(set(forward_by) & set(backward_by))
    deviations, ious = [], []
    for key in pairs:
        a,b=forward_by[key],backward_by[key]
        deviations.extend(abs(a[i]-b[i]) for i in range(4)); ious.append(_iou(a,b))
    forward_pages = {key[1] for key in forward_by}; matched_pages = sum(1 for key in forward_by if key in backward_by)
    return {
        "comparisonPairs": len(pairs),
        "medianEdgeDeviationPt": round(statistics.median(deviations),3) if deviations else None,
        "p95EdgeDeviationPt": round(sorted(deviations)[max(0,math.ceil(len(deviations)*.95)-1)],3) if deviations else None,
        "medianIoU": round(statistics.median(ious),4) if ious else None,
        "pageAssignmentAgreement": round(matched_pages/len(forward_by),4) if forward_by else None,
        "warning": "Backward PDF extraction is an independent cross-check, not geometric ground truth.",
    }
