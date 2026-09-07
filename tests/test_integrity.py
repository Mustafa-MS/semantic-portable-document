from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validation.integrity import create_state, verify_state


class IntegrityTests(unittest.TestCase):
    def test_each_normative_resource_is_bound(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, pdf, mapping, state_path = root / "a.xhtml", root / "a.pdf", root / "a.json", root / "state.json"
            source.write_bytes(b"source"); pdf.write_bytes(b"pdf"); mapping.write_bytes(b"mapping")
            state = create_state(state_path, "d_x", "r_x", source, pdf, mapping, {"renderer": "fixture"})
            self.assertTrue(verify_state(state, source, pdf, mapping)["valid"])
            mapping.write_bytes(b"changed")
            self.assertFalse(verify_state(state, source, pdf, mapping)["valid"])


if __name__ == "__main__":
    unittest.main()

