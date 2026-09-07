from __future__ import annotations

import unicodedata

import pytest


@pytest.mark.parametrize(
    ("label", "value", "scalars"),
    [
        ("Arabic", "العربية", 7),
        ("mixed-bidi", "abc العربية", 11),
        ("combining", "e\u0301", 2),
        ("emoji", "\U0001f600", 1),
        ("ZWJ", "\U0001f469\u200d\U0001f4bb", 3),
        ("Indic", "क्\u200dष", 4),
        ("CJK", "漢字", 2),
    ],
)
def test_python_valid_text_length_is_unicode_scalar_count(label: str, value: str, scalars: int) -> None:
    assert len(value) == scalars, label
    assert not any(0xD800 <= ord(ch) <= 0xDFFF for ch in value)


def test_nfc_is_explicit_not_implicit() -> None:
    decomposed = "Cafe\u0301"
    assert len(decomposed) == 5
    assert unicodedata.normalize("NFC", decomposed) == "Café"
    assert len(unicodedata.normalize("NFC", decomposed)) == 4

