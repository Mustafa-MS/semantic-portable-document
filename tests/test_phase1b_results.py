from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Phase1BResultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase1 = json.loads((ROOT / "reports" / "results.json").read_text(encoding="utf-8"))
        cls.results = json.loads((ROOT / "reports" / "results_phase1b.json").read_text(encoding="utf-8"))
        cls.docs = {item["testId"]: item for item in cls.results["documents"]}

    def test_phase1_negative_baseline_is_preserved(self) -> None:
        ratios = [item["mapping"]["coverage"]["ratio"] for item in self.phase1["documents"]]
        self.assertAlmostEqual(sum(ratios) / len(ratios), 0.626, places=3)
        self.assertEqual(self.results["phase1ResultsPreservedAt"], "reports/results.json")

    def test_forward_mapping_targets_and_vocab(self) -> None:
        allowed = {"MAPPED", "PARTIALLY_MAPPED", "NOT_VISIBLE", "UNMAPPABLE", "UNSUPPORTED"}
        for test_id in [f"T{i:02d}" for i in range(1, 13)]:
            mapping = self.docs[test_id]["pagedjs"]["forward"]
            self.assertGreaterEqual(mapping["mappingFidelity"]["visibleNodeMapping"]["ratio"], 0.95)
            self.assertGreaterEqual(mapping["mappingFidelity"]["logicalRangeMapping"]["ratio"], 0.90)
            self.assertTrue({record["status"] for record in mapping["records"]} <= allowed)
            for record in mapping["records"]:
                self.assertIn(record["confidence"], {"EXACT_IDENTITY_PROPAGATION", "EXACT_TEXT_RANGE_LAYOUT", "UNVERIFIED"})
                self.assertTrue(record["method"].startswith("forward:pagedjs"))

    def test_rtl_forward_mapping_is_independent_and_complete(self) -> None:
        for test_id in ("T08", "T09"):
            mapping = self.docs[test_id]["pagedjs"]["forward"]
            self.assertEqual(mapping["mappingFidelity"]["visibleNodeMapping"]["ratio"], 1.0)
            self.assertEqual(mapping["mappingFidelity"]["logicalRangeMapping"]["ratio"], 1.0)

    def test_nonvisual_svg_title_is_explicit(self) -> None:
        records = self.docs["T04"]["pagedjs"]["forward"]["records"]
        self.assertEqual(sum(record.get("nonVisualCharacters", 0) for record in records), 22)

    def test_epub_baseline_and_corrected_packages_are_both_retained(self) -> None:
        self.assertEqual(sum(item["status"] == "PASS" for item in self.results["epubcheckOriginalPhase1Packages"]), 9)
        self.assertEqual(sum(item["status"] == "PASS" for item in self.results["epubcheck"]), 12)
        full_readers = [reader for reader in self.results["epubReaders"] if len(reader.get("results", [])) == 12 and all(item.get("opened") for item in reader["results"])]
        self.assertGreaterEqual(len(full_readers), 2)

    def test_t10_revision_invariants(self) -> None:
        revision = self.results["revisionExperiment"]
        for key in ("documentIdPreserved", "targetIdsPreserved", "targetHashesChanged", "revisionChanged", "newFixedRendition", "oldMappingRejectedForR2"):
            self.assertTrue(revision[key], key)
        self.assertEqual(revision["unrelatedSemanticChanges"], 0)
        self.assertEqual(revision["unchangedGeometry"]["samePageRatio"], 1.0)

    def test_specialist_validation_is_not_overclaimed(self) -> None:
        self.assertTrue(self.results["pdfValidation"])
        self.assertFalse(any(item.get("compliant") for item in self.results["pdfValidation"]))
        self.assertFalse(self.results["weasyprintPdfA4uExperiment"]["validation"]["compliant"])

    def test_summary_uses_an_allowed_single_recommendation(self) -> None:
        summary = (ROOT / "reports" / "phase1b_summary.md").read_text(encoding="utf-8").rstrip()
        self.assertTrue(summary.endswith("**RUN ANOTHER TARGETED RESEARCH PHASE**"))


if __name__ == "__main__":
    unittest.main()
