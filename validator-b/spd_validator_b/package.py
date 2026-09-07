from __future__ import annotations

import posixpath
import re
import stat
import struct
import unicodedata
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZIP_STORED, BadZipFile, ZipFile, ZipInfo

from .models import (
    Outcome,
    PackageInvalid,
    ResourceLimitExceeded,
    ResourceLimits,
    ValidationReport,
)

_DRIVE = re.compile(r"^[A-Za-z]:")


def valid_package_path(path: str) -> bool:
    if not path or path.startswith(("/", "\\")) or _DRIVE.match(path):
        return False
    if "\\" in path or "\x00" in path or "//" in path:
        return False
    if any(ord(ch) < 0x20 for ch in path):
        return False
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    return unicodedata.normalize("NFC", path) == path


def resolve_local(base_path: str, reference: str) -> str | None:
    split = urlsplit(reference)
    if split.scheme or split.netloc or split.query:
        return None
    try:
        decoded = unquote(split.path, errors="strict")
    except (UnicodeDecodeError, ValueError):
        return None
    if not decoded or decoded.startswith("/") or "\\" in decoded or _DRIVE.match(decoded):
        return None
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(base_path), decoded))
    if joined.startswith("../") or joined == ".." or not valid_package_path(joined):
        return None
    return joined


def resolve_root_local(reference: str) -> str | None:
    return resolve_local("__root__", reference)


@dataclass(slots=True)
class SecurePackage:
    path: Path
    limits: ResourceLimits
    zip: ZipFile
    infos: dict[str, ZipInfo]

    @classmethod
    def open(cls, path: Path, limits: ResourceLimits, report: ValidationReport) -> SecurePackage:
        if not path.is_file():
            raise PackageInvalid("input path is not a regular file")
        if path.stat().st_size > limits.max_package_bytes:
            raise ResourceLimitExceeded("compressed package exceeds max_package_bytes")
        try:
            archive = ZipFile(path, "r")
        except (BadZipFile, OSError) as exc:
            raise PackageInvalid(f"not a readable ZIP package: {exc}") from exc
        listed = archive.infolist()
        if len(listed) > limits.max_entries:
            archive.close()
            raise ResourceLimitExceeded("ZIP entry count exceeds max_entries")
        total = sum(info.file_size for info in listed)
        if total > limits.max_total_decompressed_bytes:
            archive.close()
            raise ResourceLimitExceeded("ZIP expansion exceeds max_total_decompressed_bytes")

        raw_seen: set[str] = set()
        decoded_seen: set[str] = set()
        nfc_seen: dict[str, str] = {}
        infos: dict[str, ZipInfo] = {}
        ranges = []
        with path.open('rb') as source:
            for info in listed:
                source.seek(info.header_offset)
                header = source.read(30)
                if len(header) != 30 or header[:4] != b'PK\x03\x04':
                    archive.close()
                    raise PackageInvalid('inconsistent ZIP local header')
                method, = struct.unpack_from('<H', header, 8)
                name_length, extra_length = struct.unpack_from('<HH', header, 26)
                raw = source.read(name_length)
                expected = info.orig_filename.encode('utf-8' if info.flag_bits & 0x800 else 'cp437')
                end = info.header_offset + 30 + name_length + extra_length + info.compress_size
                if raw != expected or method != info.compress_type or end > archive.start_dir:
                    archive.close()
                    raise PackageInvalid('inconsistent ZIP local/central identity or bounds')
                ranges.append((info.header_offset, end))
        ranges.sort()
        if any(left[1] > right[0] for left, right in pairwise(ranges)):
            archive.close()
            raise PackageInvalid('overlapping ZIP entries')
        for info in listed:
            name = info.filename
            if name in raw_seen:
                report.add("SPD-BASE-002", Outcome.FAIL, "duplicate ZIP entry name", resource=name)
            raw_seen.add(name)
            decoded = unicodedata.normalize('NFC', unquote(name))
            if decoded in decoded_seen:
                report.add('SPD-BASE-002', Outcome.FAIL, 'decoded entry identity collision', resource=name)
                report.add('SPD-RES-002', Outcome.FAIL, 'ambiguous inventory path identity', resource=name)
            decoded_seen.add(decoded)
            mode = stat.S_IFMT(info.external_attr >> 16) if info.create_system == 3 else 0
            if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
                report.add('SPD-BASE-002', Outcome.FAIL, 'symlink/device/special entry prohibited', resource=name)
            if not valid_package_path(name):
                report.add("SPD-BASE-002", Outcome.FAIL, "unsafe or non-NFC ZIP entry path", resource=name)
            normalized = unicodedata.normalize("NFC", name)
            previous = nfc_seen.get(normalized)
            if previous is not None and previous != name:
                report.add(
                    "SPD-BASE-002", Outcome.FAIL, "ZIP entry paths collide after NFC normalization",
                    resource=name, evidence={"other": previous},
                )
            nfc_seen[normalized] = name
            if info.flag_bits & 1:
                report.add("SPD-BASE-002", Outcome.FAIL, "encrypted ZIP entries are unsupported", resource=name)
            if info.compress_type not in (ZIP_STORED, ZIP_DEFLATED):
                report.add("SPD-BASE-002", Outcome.FAIL, "compression method is outside the SPD profile", resource=name)
            if info.file_size > limits.max_entry_bytes:
                archive.close()
                raise ResourceLimitExceeded(f"ZIP entry exceeds max_entry_bytes: {name}")
            if info.compress_size == 0:
                ratio = float("inf") if info.file_size else 1.0
            else:
                ratio = info.file_size / info.compress_size
            if ratio > limits.max_compression_ratio:
                archive.close()
                raise ResourceLimitExceeded(f"ZIP compression ratio exceeds limit: {name}")
            infos.setdefault(name, info)
        return cls(path, limits, archive, infos)

    def close(self) -> None:
        self.zip.close()

    def exists(self, path: str) -> bool:
        return path in self.infos

    def read(self, path: str, *, limit: int | None = None) -> bytes:
        info = self.infos[path]
        maximum = self.limits.max_entry_bytes if limit is None else min(limit, self.limits.max_entry_bytes)
        if info.file_size > maximum:
            raise ResourceLimitExceeded(f"resource exceeds parser limit: {path}")
        with self.zip.open(info, "r") as stream:
            data = stream.read(maximum + 1)
        if len(data) > maximum:
            raise ResourceLimitExceeded(f"resource exceeds parser limit while reading: {path}")
        return data

    @property
    def paths(self) -> set[str]:
        return set(self.infos)
