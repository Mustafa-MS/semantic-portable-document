from __future__ import annotations

import shutil
import subprocess
import unittest
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def package_json(fixture: str, path: str) -> dict:
    with zipfile.ZipFile(ROOT / "tests" / fixture / "document.epub") as archive:
        return json.loads(archive.read(path))


class ConformanceArtifactTests(unittest.TestCase):
    def test_conformance_model_artifacts(self) -> None:
        shell = shutil.which("pwsh") or shutil.which("powershell")
        self.assertIsNotNone(shell, "PowerShell is required for Draft 2020-12 Test-Json verification")
        completed = subprocess.run(
            [shell, "-NoProfile", "-File", str(ROOT / "scripts" / "verify_conformance_model.ps1")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=180,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + "\n" + completed.stderr)

    def test_digest_projections_and_jcs_descriptor_digest(self) -> None:
        for category in ("valid", "edge"):
            for fixture in (ROOT / "tests" / category).iterdir():
                if not fixture.is_dir():
                    continue
                with zipfile.ZipFile(fixture / "document.epub") as archive:
                    inventory = json.loads(archive.read("META-INF/spd/inventory.json"))
                    state = json.loads(archive.read("META-INF/spd/state.json"))
                    document_state = json.loads(archive.read("META-INF/spd/document-state.json"))
                    projections = {}
                    for scope in ("semantic", "rendering"):
                        selected = []
                        for item in inventory["resources"]:
                            include = scope in item["affects"] if scope == "semantic" else bool(set(item["affects"]) & {"semantic", "rendering"})
                            if include:
                                selected.append(item)
                        selected.sort(key=lambda item: item["path"].encode("utf-8"))
                        payload = b"".join(
                            item["path"].encode("utf-8") + b"\0" + str(item["byteLength"]).encode("ascii") + b"\0" + item["sha256"].encode("ascii") + b"\n"
                            for item in selected
                        )
                        projections[scope] = sha256(payload)
                    self.assertEqual(projections["semantic"], document_state["semanticStateDigest"])
                    self.assertEqual(projections["semantic"], state["semanticStateDigest"])
                    self.assertEqual(projections["rendering"], document_state["renditionInputDigest"])
                    self.assertEqual(projections["rendering"], state["renditionInputDigest"])
                    descriptor = dict(state)
                    claimed = descriptor.pop("descriptorDigest")
                    canonical = json.dumps(descriptor, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
                    self.assertEqual(claimed, sha256(canonical), f"JCS digest mismatch: {category}/{fixture.name}")

    def test_revision_and_rendition_digest_separation(self) -> None:
        baseline = package_json("valid/minimal-base", "META-INF/spd/document-state.json")
        same_semantic = package_json("valid/same-semantic-different-revision-id", "META-INF/spd/document-state.json")
        changed_semantic = package_json("valid/semantic-change-new-revision", "META-INF/spd/document-state.json")
        fixed_baseline = package_json("valid/fixed-without-mapping", "META-INF/spd/document-state.json")
        css_changed = package_json("edge/css-change-stales-fixed", "META-INF/spd/document-state.json")
        self.assertNotEqual(baseline["revision"]["revisionId"], same_semantic["revision"]["revisionId"])
        self.assertEqual(baseline["semanticStateDigest"], same_semantic["semanticStateDigest"])
        self.assertNotEqual(baseline["semanticStateDigest"], changed_semantic["semanticStateDigest"])
        self.assertEqual(fixed_baseline["semanticStateDigest"], css_changed["semanticStateDigest"])
        self.assertNotEqual(fixed_baseline["renditionInputDigest"], css_changed["renditionInputDigest"])
        stale_state = package_json("edge/css-change-stales-fixed", "META-INF/spd/state.json")
        self.assertEqual(stale_state["fixedRendition"]["status"], "stale")
        self.assertNotEqual(stale_state["fixedRendition"]["renditionInputDigest"], stale_state["renditionInputDigest"])

    def test_current_fixed_does_not_imply_mapping(self) -> None:
        document_state = package_json("valid/fixed-without-mapping", "META-INF/spd/document-state.json")
        state = package_json("valid/fixed-without-mapping", "META-INF/spd/state.json")
        self.assertEqual(state["fixedRendition"]["status"], "current")
        self.assertNotIn("mapping", state)
        self.assertNotIn("Mapping", {item["id"] for item in document_state["capabilities"]})

    def test_descriptor_and_capability_discovery(self) -> None:
        expected_rels = {
            "https://example.invalid/spd/rel/document-state": "META-INF/spd/document-state.json",
            "https://example.invalid/spd/rel/resource-inventory": "META-INF/spd/inventory.json",
            "https://example.invalid/spd/rel/lifecycle-state": "META-INF/spd/state.json",
        }
        ocf = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
        opf_ns = {"o": "http://www.idpf.org/2007/opf"}
        for category in ("valid", "edge"):
            for fixture in (ROOT / "tests" / category).iterdir():
                if not fixture.is_dir():
                    continue
                with zipfile.ZipFile(fixture / "document.epub") as archive:
                    container = ET.fromstring(archive.read("META-INF/container.xml"))
                    roots = container.findall("c:rootfiles/c:rootfile", ocf)
                    self.assertEqual(len(roots), 1, f"rootfile count: {category}/{fixture.name}")
                    links = container.findall("c:links/c:link", ocf)
                    self.assertEqual({link.attrib["rel"]: link.attrib["href"] for link in links}, expected_rels)
                    self.assertTrue(all(link.attrib.get("media-type") == "application/json" for link in links))
                    document_state = json.loads(archive.read(expected_rels["https://example.invalid/spd/rel/document-state"]))
                    package = ET.fromstring(archive.read(roots[0].attrib["full-path"]))
                    discovered = {
                        (meta.text or "").split("/capability/", 1)[1].rsplit("/0.1", 1)[0]
                        for meta in package.findall("o:metadata/o:meta", opf_ns)
                        if meta.attrib.get("property") == "dcterms:conformsTo" and "/capability/" in (meta.text or "")
                    }
                    declared = {item["id"] for item in document_state["capabilities"]}
                    self.assertEqual(discovered, declared, f"capability discovery mismatch: {category}/{fixture.name}")
                    state = json.loads(archive.read(expected_rels["https://example.invalid/spd/rel/lifecycle-state"]))
                    if "Mapping" in declared:
                        self.assertEqual(state["fixedRendition"]["status"], "current")
                        self.assertIn("mapping", state)


if __name__ == "__main__":
    unittest.main()
