from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .constants import CANONICAL_SCHEMAS


class SchemaStore:
    def __init__(self, schema_dir: Path):
        self.schema_dir = schema_dir
        self.schemas: dict[str, dict[str, Any]] = {}
        self.validators: dict[str, Draft202012Validator] = {}
        for key, filename in CANONICAL_SCHEMAS.items():
            schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            self.schemas[key] = schema
            self.validators[key] = Draft202012Validator(schema, format_checker=FormatChecker())

    def errors(self, key: str, value: Any) -> list[str]:
        return [
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in sorted(self.validators[key].iter_errors(value), key=lambda e: list(e.absolute_path))
        ]


def find_repository_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "spec" / "FORMAT_0.1_RC1.md").is_file() and (candidate / "schemas" / "rc1").is_dir():
            return candidate
    package_root = Path(__file__).resolve().parents[2]
    if (package_root / "schemas").is_dir():
        return package_root
    raise FileNotFoundError("cannot locate frozen SPD specification and schemas")
