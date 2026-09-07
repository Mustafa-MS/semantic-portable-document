from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lxml import etree

from harness.util import sha256_bytes


class TransactionError(RuntimeError):
    code = "TRANSACTION_ERROR"


class StaleRevision(TransactionError):
    code = "STALE_REVISION"


class NodeConflict(TransactionError):
    code = "NODE_CONFLICT"


class InvalidOperation(TransactionError):
    code = "INVALID_OPERATION"


def _parse(data: bytes) -> etree._ElementTree:
    return etree.ElementTree(etree.fromstring(data, parser=etree.XMLParser(remove_blank_text=False)))


def _find(tree: etree._ElementTree, node_id: str) -> etree._Element:
    found = tree.xpath(f'//*[@data-node-id="{node_id}"]')
    if len(found) != 1:
        raise InvalidOperation(f"node target must resolve exactly once: {node_id}")
    return found[0]


def node_hash(element: etree._Element) -> str:
    return sha256_bytes(etree.tostring(element, method="c14n", with_comments=False))


@dataclass
class CommitResult:
    revision_id: str
    changed_nodes: list[str]
    bytes: bytes


class TransactionalDocument:
    def __init__(self, source: bytes) -> None:
        self._source = source
        self._tree = _parse(source)
        values = self._tree.xpath('//x:meta[@name="revision-id"]/@content', namespaces={"x": "http://www.w3.org/1999/xhtml"})
        if len(values) != 1:
            raise ValueError("document requires exactly one revision-id meta element")
        self.revision_id = str(values[0])

    @classmethod
    def from_path(cls, path: Path) -> "TransactionalDocument":
        return cls(path.read_bytes())

    def get_node_hash(self, node_id: str) -> str:
        return node_hash(_find(self._tree, node_id))

    def get_node_text(self, node_id: str) -> str:
        return " ".join(_find(self._tree, node_id).itertext()).strip()

    def apply_transaction(self, transaction: dict[str, Any]) -> CommitResult:
        if transaction.get("baseRevision") != self.revision_id:
            raise StaleRevision(f"expected {transaction.get('baseRevision')}; current {self.revision_id}")
        candidate = copy.deepcopy(self._tree)
        changed: list[str] = []
        for op in transaction.get("operations", []):
            node_id = op.get("node")
            if not node_id:
                raise InvalidOperation("operation is missing node")
            target = _find(candidate, node_id)
            expected_hash = op.get("expectedNodeHash")
            if expected_hash and expected_hash != node_hash(_find(self._tree, node_id)):
                raise NodeConflict(f"node hash precondition failed: {node_id}")
            operation = op.get("op")
            if operation in {"replaceText", "updateTableCell"}:
                for child in list(target):
                    target.remove(child)
                target.text = str(op.get("value", ""))
            elif operation == "replaceFigure":
                images = target.xpath('.//*[local-name()="img"]')
                if len(images) != 1:
                    raise InvalidOperation("replaceFigure target must contain exactly one img")
                images[0].set("src", str(op["src"]))
                if "alt" in op:
                    images[0].set("alt", str(op["alt"]))
            elif operation == "moveSection":
                before = _find(candidate, str(op["before"]))
                parent = before.getparent()
                if parent is None or target.getparent() is None:
                    raise InvalidOperation("moveSection targets must have parents")
                target.getparent().remove(target)
                parent.insert(parent.index(before), target)
            elif operation == "insertCitation":
                citation = etree.Element("li")
                citation.set("data-node-id", str(op.get("newNodeId", "n_" + uuid.uuid4().hex)))
                citation.text = str(op["value"])
                target.append(citation)
            else:
                raise InvalidOperation(f"unsupported operation: {operation}")
            changed.append(node_id)

        new_revision = "r_" + uuid.uuid4().hex
        meta = candidate.xpath('//x:meta[@name="revision-id"]', namespaces={"x": "http://www.w3.org/1999/xhtml"})[0]
        meta.set("content", new_revision)
        output = etree.tostring(candidate, xml_declaration=True, encoding="UTF-8", doctype="<!DOCTYPE html>")
        return CommitResult(new_revision, changed, output)

