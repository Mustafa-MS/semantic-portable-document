from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from jsonschema import Draft202012Validator

from spd_validator_b.integrity import lifecycle_descriptor_digest, projection_digest
from spd_validator_b.models import PackageInvalid, ResourceLimits, ValidationReport
from spd_validator_b.package import SecurePackage, resolve_local, valid_package_path
from spd_validator_b.semantics import NODE_ID
from spd_validator_b.strictjson import StrictJSONError, loads

UUID_GOOD = "urn:uuid:123e4567-e89b-42d3-a456-426614174000"
ROOT = Path(__file__).resolve().parents[2]


def test_projection_sorting_and_digest_vector() -> None:
    resources = [
        {"path": "b.txt", "byteLength": 1, "sha256": "sha256:" + "00" * 32, "affects": ["semantic"]},
        {"path": "a.txt", "byteLength": 2, "sha256": "sha256:" + "11" * 32, "affects": ["semantic"]},
    ]
    assert projection_digest(resources, {"semantic"}) == "sha256:a2ee3811b0098b94ca9a5f4816ad71b7d001af1320e74d4d10b090c428ffd050"


def test_jcs_lifecycle_digest_omits_descriptor_digest() -> None:
    state = {"b": "x", "descriptorDigest": "sha256:" + "00" * 32, "a": 1}
    assert lifecycle_descriptor_digest(state) == "sha256:ecf9e98ec0641e23113ff3ce8bdc78d0ddd249886517fd4a7f68cc83d4e65667"


def test_duplicate_json_keys_and_non_i_json_rejected() -> None:
    with pytest.raises(StrictJSONError, match="duplicate"):
        loads(b'{"a":1,"a":2}')
    with pytest.raises(StrictJSONError, match="numeric"):
        loads(b'{"a":NaN}')
    with pytest.raises(StrictJSONError, match="surrogate"):
        loads(b'{"a":"\\ud800"}')


@pytest.mark.parametrize(
    ("path", "valid"),
    [
        ("EPUB/content.xhtml", True),
        ("../escape", False),
        ("/absolute", False),
        ("C:/drive", False),
        ("a\\b", False),
        ("a/./b", False),
        ("a//b", False),
        ("Cafe\u0301.txt", False),
        ("Caf\u00e9.txt", True),
    ],
)
def test_package_path_profile(path: str, valid: bool) -> None:
    assert valid_package_path(path) is valid


def test_uri_resolution_cannot_escape_package() -> None:
    assert resolve_local("EPUB/content.xhtml", "images/a.png") == "EPUB/images/a.png"
    assert resolve_local("EPUB/content.xhtml", "../../escape") is None
    assert resolve_local("EPUB/content.xhtml", "https://example.com/x") is None


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789._-", min_size=1, max_size=50))
def test_safe_generated_component_is_accepted(component: str) -> None:
    assume(component not in {".", ".."})
    assert valid_package_path("EPUB/" + component)


def test_exact_byte_hash_has_no_text_normalization() -> None:
    assert hashlib.sha256(b"a\r\n").digest() != hashlib.sha256(b"a\n").digest()


def test_uuid_node_fixed_and_page_id_syntax() -> None:
    document_schema = json.loads((ROOT / "schemas/rc1/document-state.schema.json").read_text(encoding="utf-8"))
    mapping_schema = json.loads((ROOT / "schemas/rc1/mapping.schema.json").read_text(encoding="utf-8"))
    uuid_pattern = re.compile(document_schema["$defs"]["documentId"]["pattern"])
    assert uuid_pattern.fullmatch(UUID_GOOD)
    assert not uuid_pattern.fullmatch(UUID_GOOD.upper())
    assert NODE_ID.fullmatch("n_opaque-token.1")
    assert not NODE_ID.fullmatch("n_UPPER")
    for name, good, bad in (("fixedId", "f_fixed-1", "fixed-1"), ("pageId", "p_page-1", "p_UPPER")):
        validator = Draft202012Validator(mapping_schema["$defs"][name])
        assert not list(validator.iter_errors(good))
        assert list(validator.iter_errors(bad))


def test_duplicate_nfc_normalized_zip_paths_detected(tmp_path: Path) -> None:
    archive = tmp_path / "collision.epub"
    with ZipFile(archive, "w", ZIP_DEFLATED) as package:
        package.writestr("Caf\u00e9.txt", b"a")
        package.writestr("Cafe\u0301.txt", b"b")
    report = ValidationReport(str(archive))
    opened = SecurePackage.open(archive, ResourceLimits(), report)
    opened.close()
    assert "SPD-BASE-002" in report.violation_requirement_ids


def test_malformed_zip_is_bounded_error(tmp_path: Path) -> None:
    archive = tmp_path / "not-a-zip.epub"
    archive.write_bytes(b"not a zip")
    with pytest.raises(PackageInvalid):
        SecurePackage.open(archive, ResourceLimits(), ValidationReport(str(archive)))
