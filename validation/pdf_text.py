from __future__ import annotations

import json
import os
import re
import subprocess
import shutil
import unicodedata
from pathlib import Path
from typing import Any

import pdfplumber
from lxml import etree
from pypdf import PdfReader

from harness.util import ROOT, normalize_text
from mapping.generate import ADDRESSABLE


def _arabic_phrases(source: Path) -> list[str]:
    tree = etree.parse(str(source))
    phrases: list[str] = []
    seen = set()
    for element in tree.xpath('//*[@data-node-id]'):
        if etree.QName(element).localname not in ADDRESSABLE:
            continue
        if element.xpath('.//*[@data-node-id]'):
            continue
        value = normalize_text(" ".join(element.itertext()))
        if value and any("\u0600" <= character <= "\u06ff" for character in value) and value not in seen:
            phrases.append(value); seen.add(value)
    return phrases


def _variants(text: str) -> dict[str, str]:
    return {"raw": text, "NFC": unicodedata.normalize("NFC", text), "NFKC": unicodedata.normalize("NFKC", text)}


def _evaluate(raw: str, phrases: list[str]) -> dict[str, Any]:
    normalized = _variants(raw)
    recoveries = {}
    for form, value in normalized.items():
        matched = [phrase for phrase in phrases if (phrase in value if form == "raw" else unicodedata.normalize(form, phrase) in value)]
        recoveries[form] = {"matched": len(matched), "expected": len(phrases), "ratio": round(len(matched)/len(phrases), 4) if phrases else 1.0, "matchedPhrases": matched}
    mixed_probes = ["FROC = 0.906", "Model-X", "https://example.org/run?id=42", "١٢٣", "123", "x = 0.906", "[Smith 2025]"]
    return {"outputs": normalized, "phraseRecovery": recoveries, "mixedBidiProbes": {probe: probe in normalized["NFKC"] for probe in mixed_probes}}


def extract_pdf_text(pdf: Path, source: Path) -> dict[str, Any]:
    phrases = _arabic_phrases(source)
    reader = PdfReader(pdf)
    pypdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    with pdfplumber.open(pdf) as fixed:
        pdfplumber_text = "\n".join(page.extract_text(use_text_flow=True) or "" for page in fixed.pages)
    runtime = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
    node = runtime / "bin" / "node.exe"
    pdfjs = runtime / "node_modules" / "pdfjs-dist" / "legacy" / "build" / "pdf.mjs"
    script = ROOT / "scripts" / "pdfjs_extract.mjs"
    proc = subprocess.run([str(node), str(script), str(pdf), str(pdfjs)], capture_output=True, text=True, timeout=120)
    pdfjs_result = json.loads(proc.stdout)["text"] if proc.returncode == 0 else ""
    try:
        import pymupdf
        with pymupdf.open(pdf) as document:
            mupdf_text = "\n".join(page.get_text() for page in document)
        mupdf_result: dict[str, Any] = _evaluate(mupdf_text, phrases)
    except Exception as exc:
        mupdf_result = {"status": "NOT AVAILABLE", "error": repr(exc)}
    poppler = shutil.which("pdftotext")
    if poppler:
        poppler_proc = subprocess.run([poppler, "-enc", "UTF-8", str(pdf), "-"], capture_output=True, timeout=120)
        poppler_text = poppler_proc.stdout.decode("utf-8", errors="replace") if poppler_proc.returncode == 0 else ""
        poppler_result: dict[str, Any] = _evaluate(poppler_text, phrases)
    else:
        poppler_result = {"status": "NOT AVAILABLE", "reason": "pdftotext executable absent; bundled Poppler contains only pdfinfo and pdftoppm"}
    return {
        "expectedArabicPhrases": phrases,
        "extractors": {
            "pypdf": _evaluate(pypdf_text, phrases),
            "pdfplumber": _evaluate(pdfplumber_text, phrases),
            "pdfjs": _evaluate(pdfjs_result, phrases),
            "mupdf": mupdf_result,
            "poppler_pdftotext": poppler_result,
        },
    }
