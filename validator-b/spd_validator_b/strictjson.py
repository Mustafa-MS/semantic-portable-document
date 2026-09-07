from __future__ import annotations

import json
from typing import Any


class StrictJSONError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJSONError(f"duplicate JSON member name: {key!r}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise StrictJSONError(f"non-I-JSON numeric constant: {value}")


def _walk(value: Any, depth: int, max_depth: int) -> None:
    if depth > max_depth:
        raise StrictJSONError(f"JSON nesting exceeds limit {max_depth}")
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise StrictJSONError("lone surrogate code point is not valid I-JSON text")
    elif isinstance(value, dict):
        for key, child in value.items():
            _walk(key, depth + 1, max_depth)
            _walk(child, depth + 1, max_depth)
    elif isinstance(value, list):
        for child in value:
            _walk(child, depth + 1, max_depth)


def loads(data: bytes, *, max_depth: int = 128) -> Any:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise StrictJSONError("normative JSON is not valid UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, StrictJSONError) as exc:
        raise StrictJSONError(str(exc)) from exc
    _walk(value, 0, max_depth)
    return value

