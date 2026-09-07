from __future__ import annotations

import os
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path
from typing import Any

import pdfplumber
from pypdf import PdfReader

from harness.util import sha256_file


def _find_browser() -> Path | None:
    candidates = [
        shutil.which("chrome"), shutil.which("chromium"), shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    return next((Path(item) for item in candidates if item and Path(item).exists()), None)


def available_renderers() -> list[dict[str, Any]]:
    browser = _find_browser()
    return [
        {"id": "chromium", "available": bool(browser), "executable": str(browser) if browser else None},
        {"id": "weasyprint", "available": bool(shutil.which("weasyprint")), "executable": shutil.which("weasyprint")},
        {"id": "vivliostyle_or_pagedjs", "available": bool(shutil.which("vivliostyle")), "executable": shutil.which("vivliostyle")},
    ]


def render_chromium(source: Path, output: Path) -> dict[str, Any]:
    browser = _find_browser()
    if not browser:
        return {"renderer": "chromium", "success": False, "error": "browser executable not found"}
    output.parent.mkdir(parents=True, exist_ok=True)
    profile = output.parent / (".profile-" + output.stem)
    cmd = [
        str(browser), "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
        "--disable-extensions", "--disable-background-networking", "--export-tagged-pdf",
        f"--user-data-dir={profile}", f"--print-to-pdf={output.resolve()}", "--no-pdf-header-footer",
        source.resolve().as_uri(),
    ]
    started = time.perf_counter()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if profile.exists():
            shutil.rmtree(profile, ignore_errors=True)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    if proc.returncode != 0 or not output.exists():
        return {"renderer": "chromium", "success": False, "render_time_ms": elapsed_ms, "error": (proc.stderr or proc.stdout)[-2000:]}
    result = inspect_pdf(output)
    result.update({"renderer": "chromium", "success": True, "render_time_ms": elapsed_ms, "stderr": proc.stderr[-1000:]})
    return result


def render_weasyprint(source: Path, output: Path, variant: str = "pdf/ua-2") -> dict[str, Any]:
    executable = Path(__file__).resolve().parents[1] / ".phase1b" / "tools" / "weasyprint" / "dist" / "weasyprint.exe"
    if not executable.exists():
        return {"renderer": "weasyprint", "success": False, "error": "portable WeasyPrint executable not found"}
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(executable), "--pdf-variant", variant, str(source.resolve()), str(output.resolve())]
    started = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    if proc.returncode != 0 or not output.exists():
        return {"renderer": "weasyprint", "success": False, "variant": variant, "render_time_ms": elapsed_ms, "error": (proc.stderr or proc.stdout)[-4000:]}
    result = inspect_pdf(output)
    result.update({"renderer": "weasyprint", "renderer_version": "69.0", "variant": variant, "success": True, "render_time_ms": elapsed_ms, "stderr": proc.stderr[-2000:]})
    return result


def inspect_pdf(path: Path) -> dict[str, Any]:
    reader = PdfReader(path)
    root = reader.trailer["/Root"]
    link_count = 0
    has_fonts = False
    font_count = 0
    embedded_font_count = 0
    to_unicode_count = 0

    def resolved(value: Any) -> Any:
        return value.get_object() if hasattr(value, "get_object") else value

    def font_is_embedded(font: Any) -> bool:
        font = resolved(font)
        candidates = [font]
        candidates.extend(resolved(item) for item in font.get("/DescendantFonts", []))
        for candidate in candidates:
            descriptor = resolved(candidate.get("/FontDescriptor")) if candidate.get("/FontDescriptor") else None
            if descriptor and any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                return True
        return False

    for page in reader.pages:
        resources = page.get("/Resources", {})
        if "/Font" in resources:
            has_fonts = True
            fonts = resolved(resources["/Font"])
            for ref in fonts.values():
                font = resolved(ref)
                font_count += 1
                if "/ToUnicode" in font:
                    to_unicode_count += 1
                if font_is_embedded(font):
                    embedded_font_count += 1
        annotations = page.get("/Annots", [])
        for annotation in annotations:
            obj = annotation.get_object()
            if obj.get("/Subtype") == "/Link":
                link_count += 1
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text(x_tolerance=2, y_tolerance=3) or "" for page in pdf.pages)
        image_count = sum(len(page.images) for page in pdf.pages)

    role_counts: Counter[str] = Counter()
    alt_text_count = 0
    actual_text_count = 0
    structure_languages: Counter[str] = Counter()
    visited: set[tuple[int, int] | int] = set()

    def walk_structure(value: Any) -> None:
        nonlocal alt_text_count, actual_text_count
        if value is None or isinstance(value, (int, float, str, bytes)):
            return
        identity: tuple[int, int] | int
        if hasattr(value, "idnum"):
            identity = (value.idnum, value.generation)
        else:
            identity = id(value)
        if identity in visited:
            return
        visited.add(identity)
        obj = resolved(value)
        if isinstance(obj, list):
            for child in obj:
                walk_structure(child)
            return
        if not hasattr(obj, "get"):
            return
        role = obj.get("/S")
        if role:
            role_counts[str(role)] += 1
        if obj.get("/Alt") is not None:
            alt_text_count += 1
        if obj.get("/ActualText") is not None:
            actual_text_count += 1
        if obj.get("/Lang"):
            structure_languages[str(obj.get("/Lang"))] += 1
        walk_structure(obj.get("/K"))

    if "/StructTreeRoot" in root:
        walk_structure(root["/StructTreeRoot"])
    return {
        "page_count": len(reader.pages),
        "pdf_size": path.stat().st_size,
        "pdf_sha256": sha256_file(path),
        "font_resources_present": has_fonts,
        "font_resource_count": font_count,
        "embedded_font_resource_count": embedded_font_count,
        "to_unicode_font_count": to_unicode_count,
        "text_characters_extracted": len(text),
        "link_annotations": link_count,
        "image_objects": image_count,
        "structure_tree_present": "/StructTreeRoot" in root,
        "marked_content": bool(root.get("/MarkInfo", {}).get("/Marked", False)) if root.get("/MarkInfo") else False,
        "pdf_language": str(root.get("/Lang", "")),
        "structure_role_counts": dict(sorted(role_counts.items())),
        "structure_alt_text_count": alt_text_count,
        "structure_actual_text_count": actual_text_count,
        "structure_language_counts": dict(sorted(structure_languages.items())),
    }
