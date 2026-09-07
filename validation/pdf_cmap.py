from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from pypdf import PdfReader


def _resolve(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def _destination_strings(cmap: bytes) -> list[str]:
    text = cmap.decode("latin-1", errors="replace")
    values: list[str] = []
    for match in re.finditer(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", text):
        destination = match.group(2)
        try:
            raw = bytes.fromhex(destination)
            if len(raw) % 2:
                continue
            values.append(raw.decode("utf-16-be", errors="replace"))
        except ValueError:
            continue
    return values


def inspect_tounicode(pdf: Path) -> dict[str, Any]:
    reader = PdfReader(pdf)
    seen_fonts = set()
    destinations: list[str] = []
    cmap_samples = []
    cmap_count = 0
    for page in reader.pages:
        resources = _resolve(page.get("/Resources", {}))
        fonts = _resolve(resources.get("/Font", {})) if resources else {}
        for name, reference in fonts.items():
            identity = (getattr(reference, "idnum", None), getattr(reference, "generation", None), str(name))
            if identity in seen_fonts:
                continue
            seen_fonts.add(identity)
            font = _resolve(reference)
            cmap_ref = font.get("/ToUnicode") if hasattr(font, "get") else None
            if not cmap_ref:
                continue
            cmap_count += 1
            data = _resolve(cmap_ref).get_data()
            strings = _destination_strings(data)
            destinations.extend(strings)
            cmap_samples.append({"font": str(name), "bytes": len(data), "destinations": strings[:20]})
    codepoints = [ord(character) for value in destinations for character in value]
    counts = Counter()
    for codepoint in codepoints:
        if 0x0600 <= codepoint <= 0x06FF:
            counts["base_arabic"] += 1
        elif 0x0750 <= codepoint <= 0x077F or 0x08A0 <= codepoint <= 0x08FF:
            counts["arabic_supplement_or_extended"] += 1
        elif 0xFB50 <= codepoint <= 0xFDFF or 0xFE70 <= codepoint <= 0xFEFF:
            counts["arabic_presentation_forms"] += 1
        elif codepoint == 0xFFFD:
            counts["replacement_character"] += 1
        else:
            counts["other"] += 1
    return {"toUnicodeCMapCount": cmap_count, "mappedDestinationStrings": len(destinations), "codepointClasses": dict(counts), "samples": cmap_samples}

