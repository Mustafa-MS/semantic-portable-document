from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from harness.util import sha256_file
from validation.mapping import validate_mapping


XHTML = b'''<html xmlns="http://www.w3.org/1999/xhtml"><head><meta name="revision-id" content="r_ok"/></head><body><p data-node-id="n_a">hello world</p></body></html>'''


class MappingValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.source, self.pdf = root / "source.xhtml", root / "fixed.pdf"
        self.source.write_bytes(XHTML); self.pdf.write_bytes(b"fixed fixture")
        self.mapping = {"revision": "r_ok", "fixedRenditionHash": sha256_file(self.pdf), "pages": [{"id": "pg_1", "width": 100, "height": 100}], "mappings": [{"node": "n_a", "kind": "text", "fragments": [{"page": "pg_1", "textRange": [0, 5], "quad": [1, 1, 10, 1, 10, 5, 1, 5]}]}]}

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_mapping(self):
        self.assertTrue(validate_mapping(self.mapping, self.source, self.pdf)["valid"])

    def test_wrong_revision_and_hash(self):
        value = copy.deepcopy(self.mapping); value["revision"] = "r_wrong"; value["fixedRenditionHash"] = "sha256:bad"
        codes = {e["code"] for e in validate_mapping(value, self.source, self.pdf)["errors"]}
        self.assertIn("WRONG_REVISION", codes); self.assertIn("WRONG_FIXED_HASH", codes)

    def test_unknown_node_duplicate_quad_and_range(self):
        value = copy.deepcopy(self.mapping)
        value["mappings"].append(copy.deepcopy(value["mappings"][0]))
        value["mappings"].append({"node": "n_missing", "kind": "text", "fragments": [{"page": "pg_1", "quad": [0, 0]}]})
        value["mappings"][0]["fragments"][0]["textRange"] = [0, 999]
        codes = {e["code"] for e in validate_mapping(value, self.source, self.pdf)["errors"]}
        self.assertTrue({"DUPLICATE_MAPPING", "UNKNOWN_NODE", "INVALID_QUAD", "TEXT_RANGE_MISMATCH"}.issubset(codes))


if __name__ == "__main__":
    unittest.main()

