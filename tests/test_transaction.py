from __future__ import annotations

import unittest

from harness.transaction import InvalidOperation, NodeConflict, StaleRevision, TransactionalDocument


SOURCE = b'''<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><head><meta name="revision-id" content="r_one"/></head><body><p data-node-id="n_a">old</p><p data-node-id="n_b">keep</p></body></html>'''


class TransactionTests(unittest.TestCase):
    def test_atomic_update_preserves_id_and_changes_revision(self):
        doc = TransactionalDocument(SOURCE)
        result = doc.apply_transaction({"baseRevision": "r_one", "operations": [{"op": "replaceText", "node": "n_a", "expectedNodeHash": doc.get_node_hash("n_a"), "value": "new"}]})
        updated = TransactionalDocument(result.bytes)
        self.assertEqual("new", updated.get_node_text("n_a"))
        self.assertEqual("keep", updated.get_node_text("n_b"))
        self.assertNotEqual("r_one", updated.revision_id)

    def test_stale_revision_rejected(self):
        with self.assertRaises(StaleRevision):
            TransactionalDocument(SOURCE).apply_transaction({"baseRevision": "r_stale", "operations": []})

    def test_node_hash_conflict_rejected(self):
        with self.assertRaises(NodeConflict):
            TransactionalDocument(SOURCE).apply_transaction({"baseRevision": "r_one", "operations": [{"op": "replaceText", "node": "n_a", "expectedNodeHash": "wrong", "value": "unsafe"}]})

    def test_late_invalid_operation_keeps_original_object(self):
        doc = TransactionalDocument(SOURCE)
        with self.assertRaises(InvalidOperation):
            doc.apply_transaction({"baseRevision": "r_one", "operations": [{"op": "replaceText", "node": "n_a", "value": "new"}, {"op": "explode", "node": "n_b"}]})
        self.assertEqual("old", doc.get_node_text("n_a"))


if __name__ == "__main__":
    unittest.main()

