from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader
from pypdf.generic import ContentStream, IndirectObject

from harness.reporting_phase1c import write_phase1c_reports
from harness.util import ROOT, write_json
from semantic_pdf.compiler import compile_semantic_pdf
from semantic_pdf.fop_baseline import write_fop_config, xhtml_to_fo
from validation.pdf_text import extract_pdf_text
from validation.tool_validators import run_verapdf


SELECTED = ("T03", "T04", "T08", "T09", "T10", "T12")
FOP_SELECTED = ("T08", "T09", "T10", "T12")
PYMUPDF_PATH = ROOT / ".phase1c" / "deps" / "python"
POPPLER_BIN = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "poppler" / "Library" / "bin"
PDFTOPPM = POPPLER_BIN / "pdftoppm.exe"
FOP = ROOT / ".phase1c" / "tools" / "fop-2.11" / "fop" / "fop.bat"


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _summary_text(value: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(value, ensure_ascii=False))
    for extractor in result.get("extractors", {}).values():
        if isinstance(extractor, dict):
            extractor.pop("outputs", None)
    return result


def _content_operator_digest(pdf: Path) -> str:
    reader = PdfReader(pdf)
    parts = []
    for page in reader.pages:
        stream = ContentStream(page.get("/Contents"), reader)
        for operands, operator in stream.operations:
            if operator in {b"BMC", b"BDC", b"EMC"}:
                continue
            parts.append(repr((operands, operator)).encode("utf-8", errors="replace"))
    return "sha256:" + hashlib.sha256(b"\n".join(parts)).hexdigest()


def _page_geometry(pdf: Path) -> list[dict[str, float]]:
    reader = PdfReader(pdf)
    return [{"width": round(float(page.mediabox.width), 5), "height": round(float(page.mediabox.height), 5)} for page in reader.pages]


def _render_poppler(pdf: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    prefix = destination / "page"
    subprocess.run([str(PDFTOPPM), "-png", "-r", "144", str(pdf), str(prefix)], check=True, capture_output=True, timeout=180)
    return sorted(destination.glob("page-*.png"))


def _compare_images(before: Path, after: Path) -> dict[str, Any]:
    with Image.open(before).convert("RGB") as a, Image.open(after).convert("RGB") as b:
        if a.size != b.size:
            return {"sameDimensions": False, "before": list(a.size), "after": list(b.size)}
        diff = ImageChops.difference(a, b)
        extrema = diff.getextrema()
        changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0))
        stat = ImageStat.Stat(diff)
        rms = math.sqrt(sum(value * value for value in stat.rms) / 3)
        return {
            "sameDimensions": True,
            "dimensions": list(a.size),
            "changedPixels": changed,
            "changedPixelRatio": round(changed / (a.width * a.height), 10),
            "maxChannelDifference": max(value[1] for value in extrema),
            "rmsDifference": round(rms, 8),
            "exact": changed == 0,
        }


def _mupdf_render(pdf: Path, destination: Path) -> list[Path]:
    import pymupdf
    destination.mkdir(parents=True, exist_ok=True)
    outputs = []
    with pymupdf.open(pdf) as document:
        for index, page in enumerate(document):
            output = destination / f"page-{index + 1}.png"
            page.get_pixmap(dpi=144, alpha=False).save(output)
            outputs.append(output)
    return outputs


def visual_preservation(test_id: str, before: Path, after: Path) -> dict[str, Any]:
    work = ROOT / ".phase1c" / "raster-work" / test_id
    if work.exists(): shutil.rmtree(work)
    pop_before = _render_poppler(before, work / "poppler-before")
    pop_after = _render_poppler(after, work / "poppler-after")
    mu_before = _mupdf_render(before, work / "mupdf-before")
    mu_after = _mupdf_render(after, work / "mupdf-after")
    durable_poppler = ROOT / "reports" / "screenshots" / "phase1c" / "poppler"
    durable_mupdf = ROOT / "reports" / "screenshots" / "phase1c" / "mupdf"
    durable_poppler.mkdir(parents=True, exist_ok=True); durable_mupdf.mkdir(parents=True, exist_ok=True)
    for index, path in enumerate(pop_after, 1): shutil.copy2(path, durable_poppler / f"{test_id}-page-{index}.png")
    for index, path in enumerate(mu_after, 1): shutil.copy2(path, durable_mupdf / f"{test_id}-page-{index}.png")
    return {
        "pageCountBefore": len(pop_before), "pageCountAfter": len(pop_after),
        "pageGeometryBefore": _page_geometry(before), "pageGeometryAfter": _page_geometry(after),
        "drawingOperatorDigestBefore": _content_operator_digest(before),
        "drawingOperatorDigestAfter": _content_operator_digest(after),
        "drawingOperatorsPreserved": _content_operator_digest(before) == _content_operator_digest(after),
        "poppler": [_compare_images(a, b) for a, b in zip(pop_before, pop_after)],
        "mupdf": [_compare_images(a, b) for a, b in zip(mu_before, mu_after)],
    }


def _resolve(value: Any) -> Any:
    return value.get_object() if isinstance(value, IndirectObject) else value


def structure_summary(pdf: Path) -> dict[str, Any]:
    reader = PdfReader(pdf); root = reader.trailer["/Root"]
    roles: dict[str, int] = {}; ids = 0; alts = 0; actual = 0; mcrs = 0
    seen: set[tuple[int, int]] = set()
    def walk(value: Any) -> None:
        nonlocal ids, alts, actual, mcrs
        if isinstance(value, IndirectObject):
            key = (value.idnum, value.generation)
            if key in seen: return
            seen.add(key)
        value = _resolve(value)
        if isinstance(value, list):
            for item in value: walk(item)
            return
        if not isinstance(value, dict): return
        role = value.get("/S")
        if role: roles[str(role)[1:]] = roles.get(str(role)[1:], 0) + 1
        ids += int("/ID" in value); alts += int("/Alt" in value); actual += int("/ActualText" in value)
        if value.get("/Type") == "/MCR": mcrs += 1
        if "/K" in value: walk(value["/K"])
    tree = root.get("/StructTreeRoot")
    if tree: walk(_resolve(tree).get("/K"))
    return {"roles": dict(sorted(roles.items())), "nodeIds": ids, "altEntries": alts, "structureActualTextEntries": actual, "markedContentReferences": mcrs, "lang": str(root.get("/Lang", "")), "pdfHeader": reader.pdf_header}


def _run_fop(test_id: str, source: Path, output: Path, config: Path) -> dict[str, Any]:
    fo = ROOT / ".phase1c" / "fop" / f"{test_id}.fo"
    xhtml_to_fo(source, fo)
    output.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([str(FOP), "-c", str(config), "-fo", str(fo), "-pdf", str(output)], cwd=ROOT, capture_output=True, text=True, timeout=180)
    return {"success": proc.returncode == 0 and output.exists(), "exitCode": proc.returncode, "fo": _relative(fo), "stderr": proc.stderr[-4000:]}


def main() -> int:
    if str(PYMUPDF_PATH) not in sys.path: sys.path.insert(0, str(PYMUPDF_PATH))
    out = ROOT / "corpus" / "generated" / "phase1c"
    for folder in (out / "compiled", out / "associations", out / "fop", ROOT / ".phase1c" / "tmp" / "strategies"):
        folder.mkdir(parents=True, exist_ok=True)
    phase1b = json.loads((ROOT / "reports" / "results_phase1b.json").read_text(encoding="utf-8"))
    results: dict[str, Any] = {
        "schemaVersion": "0.1C-experimental", "phase1bResultsPreservedAt": "reports/results_phase1b.json",
        "tools": {"compiler": "disposable pypdf semantic compiler", "pypdf": __import__("pypdf").__version__, "pymupdf": __import__("pymupdf").version[0], "fop": "2.11", "verapdf": "1.30.2", "pdfjs": "bundled legacy build", "popplerRaster": "bundled pdftoppm"},
        "preservedPhase1bEvidence": {"visibleNodeCoverage": 1.0, "logicalRangeCoverage": 1.0, "validFragments": "3094/3094", "T08": 1.0, "T09": 1.0, "mappingModel": "SMALL CORRESPONDENCE LAYER", "epub": "YES WITH PROFILE RESTRICTIONS"},
        "compiled": [], "fop": [], "strategyExperiments": {}, "rawComparisons": {}, "validations": [], "failures": [],
    }
    docs1b = {item["testId"]: item for item in phase1b["documents"]}

    for test_id in SELECTED:
        print(f"compile {test_id}", flush=True)
        source = ROOT / "corpus" / "sources" / f"{test_id}.xhtml"
        forward = ROOT / "corpus" / "generated" / "phase1b" / "forward" / f"{test_id}.json"
        visual = ROOT / "corpus" / "generated" / "phase1b" / "pagedjs" / f"{test_id}.pdf"
        output = out / "compiled" / f"{test_id}.pdf"
        association = out / "associations" / f"{test_id}.json"
        try:
            compiler = compile_semantic_pdf(source, forward, visual, output, association, mode="marked-content")
            fidelity = extract_pdf_text(output, source) if test_id in {"T08", "T09"} else None
            item = {"testId": test_id, "source": _relative(source), "inputPdf": _relative(visual), "outputPdf": _relative(output), "association": _relative(association), "compiler": compiler, "visualPreservation": visual_preservation(test_id, visual, output), "structure": structure_summary(output)}
            if fidelity:
                raw_path = out / "text" / f"{test_id}-compiled.json"; write_json(raw_path, fidelity)
                item["textFidelity"] = _summary_text(fidelity); item["rawAndNormalizedText"] = _relative(raw_path)
            results["compiled"].append(item)
        except Exception as exc:
            results["failures"].append({"testId": test_id, "stage": "compile", "error": repr(exc)})

    for test_id in ("T08", "T09"):
        source = ROOT / "corpus" / "sources" / f"{test_id}.xhtml"
        forward = ROOT / "corpus" / "generated" / "phase1b" / "forward" / f"{test_id}.json"
        visual = ROOT / "corpus" / "generated" / "phase1b" / "pagedjs" / f"{test_id}.pdf"
        strategy = {}
        for mode in ("structure", "marked-content"):
            output = ROOT / ".phase1c" / "tmp" / "strategies" / f"{test_id}-{mode}.pdf"
            association = output.with_suffix(".json")
            compile_semantic_pdf(source, forward, visual, output, association, mode=mode)
            fidelity = extract_pdf_text(output, source)
            strategy[mode] = {"text": _summary_text(fidelity), "structure": structure_summary(output), "ua2": run_verapdf(output, "ua2")}
        results["strategyExperiments"][test_id] = strategy
        results["rawComparisons"][test_id] = {}
        for renderer in ("pagedjs", "weasyprint"):
            pdf = ROOT / "corpus" / "generated" / "phase1b" / renderer / f"{test_id}.pdf"
            fidelity = extract_pdf_text(pdf, source)
            raw_path = out / "text" / f"{test_id}-{renderer}-raw.json"; write_json(raw_path, fidelity)
            results["rawComparisons"][test_id][renderer] = {"pdf": _relative(pdf), "text": _summary_text(fidelity), "rawAndNormalizedText": _relative(raw_path)}

    config = ROOT / ".phase1c" / "fop" / "fop.xconf"; write_fop_config(config)
    for test_id in FOP_SELECTED:
        print(f"FOP {test_id}", flush=True)
        source = ROOT / "corpus" / "sources" / f"{test_id}.xhtml"; output = out / "fop" / f"{test_id}.pdf"
        render = _run_fop(test_id, source, output, config)
        item: dict[str, Any] = {"testId": test_id, "source": _relative(source), "outputPdf": _relative(output), "render": render}
        if render["success"]:
            fidelity = extract_pdf_text(output, source) if test_id in {"T08", "T09"} else None
            item["structure"] = structure_summary(output); item["pageGeometry"] = _page_geometry(output)
            if fidelity:
                raw_path = out / "text" / f"{test_id}-fop.json"; write_json(raw_path, fidelity)
                item["textFidelity"] = _summary_text(fidelity); item["rawAndNormalizedText"] = _relative(raw_path)
            # Durable first-page FOP raster for visual inspection.
            rendered = _render_poppler(output, ROOT / "reports" / "screenshots" / "phase1c" / "fop" / test_id)
            item["screenshots"] = [_relative(path) for path in rendered]
        else:
            results["failures"].append({"testId": test_id, "stage": "fop", "error": render["stderr"]})
        results["fop"].append(item)

    print("veraPDF matrix", flush=True)
    jobs: list[tuple[str, str, Path, str]] = []
    for item in results["compiled"]:
        pdf = ROOT / item["outputPdf"]
        jobs.append((item["testId"], "compiled", pdf, "ua2"))
        if item["testId"] in {"T08", "T09", "T10", "T12"}:
            jobs.extend([(item["testId"], "compiled", pdf, "wt1a"), (item["testId"], "compiled", pdf, "wt1r")])
        if item["testId"] == "T10": jobs.append((item["testId"], "compiled", pdf, "4"))
    for item in results["fop"]:
        if item["render"]["success"]:
            pdf = ROOT / item["outputPdf"]
            jobs.extend([(item["testId"], "fop", pdf, "ua1"), (item["testId"], "fop", pdf, "ua2")])
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_verapdf, pdf, profile): (test_id, candidate, pdf, profile) for test_id, candidate, pdf, profile in jobs}
        for future in as_completed(futures):
            test_id, candidate, pdf, profile = futures[future]
            try: results["validations"].append({"testId": test_id, "candidate": candidate, "pdf": _relative(pdf), **future.result()})
            except Exception as exc: results["validations"].append({"testId": test_id, "candidate": candidate, "profile": profile, "compliant": False, "error": repr(exc)})
    results["validations"].sort(key=lambda item: (item["candidate"], item["testId"], item["profile"]))
    results["phase1bDocumentCount"] = len(docs1b)
    write_json(ROOT / "reports" / "results_phase1c.json", results)
    write_phase1c_reports(ROOT, results)
    print(json.dumps({"compiled": len(results["compiled"]), "fop": sum(i["render"]["success"] for i in results["fop"]), "failures": len(results["failures"])}, indent=2), flush=True)
    return 0 if not results["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
