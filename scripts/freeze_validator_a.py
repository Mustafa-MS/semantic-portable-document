"""Run the frozen Validator A CLI and emit differential/golden corpus artifacts."""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0-draft.1"

def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

def run_one(executable: Path, epubcheck: Path, category: str, directory: Path):
    completed = subprocess.run(
        [str(executable), "validate", str(directory / "document.epub"), "--format", "json", "--epubcheck", str(epubcheck)],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, timeout=180,
    )
    if not completed.stdout:
        raise RuntimeError(f"{category}/{directory.name}: no JSON output: {completed.stderr}")
    report = json.loads(completed.stdout)
    fixture = f"{category}/{directory.name}"
    failures = sorted({f["requirementId"] for f in report["findings"] if f["outcome"] == "FAIL"})
    # A generic inherited-EPUB failure is a dependent diagnostic when another
    # Base failure already establishes invalidity; preserve it in the rich report
    # but omit it from the normalized differential root-cause surface.
    if "SPD-BASE-002" in failures and any(x != "SPD-BASE-002" for x in failures):
        failures.remove("SPD-BASE-002")
    normalized = {
        "fixture": fixture,
        "base": report["base"],
        "normativeCapabilities": {k: report["capabilities"][k] for k in ("Accessible", "Mapping")},
        "experimentalCapabilities": {k: report["capabilities"][k] for k in ("Archive-Experimental", "Fixed-Experimental")},
        "violationRequirementIds": failures,
        "notTestedRequirementIds": sorted(set(report["notTestedRequirements"])),
        "operationalStatus": report["operationalStatus"],
    }
    expected = json.loads((directory / "expected.json").read_text(encoding="utf-8"))
    expected_ids = sorted(v["requirement"] for v in expected["violations"])
    expected_caps = expected["capabilities"]
    if normalized["base"] != expected["base"] or failures != expected_ids or any(report["capabilities"][k] != v for k, v in expected_caps.items()):
        raise AssertionError(f"{fixture}: normalized result disagrees with corpus oracle")
    tool = report["externalTools"][0]
    return normalized, {
        "fixture": fixture,
        "epubcheckVersion": tool["version"],
        "exitCode": tool["exitCode"],
        "normalizedResult": tool["outcome"],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator", type=Path, required=True)
    parser.add_argument("--epubcheck", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    items = [(category, d) for category in ("valid", "invalid", "edge") for d in sorted((ROOT / "tests" / category).iterdir()) if d.is_dir()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda item: run_one(args.validator, args.epubcheck, *item), items))
    golden = sorted((x[0] for x in results), key=lambda x: x["fixture"])
    tools = sorted((x[1] for x in results if x[1]["fixture"].split("/")[0] in ("valid", "edge")), key=lambda x: x["fixture"])
    if len(tools) != 31 or any(x["exitCode"] != 0 or x["normalizedResult"] != "PASS" for x in tools):
        raise AssertionError("EPUBCheck 5.3.0 did not pass all 31 applicable valid/edge fixtures")
    schemas = b"".join((ROOT / "schemas" / name).read_bytes() for name in (
        "document-state.schema.json", "resource-inventory.schema.json", "state.schema.json", "mapping.schema.json", "annotation-extension.schema.json"))
    frozen = {
        "validator": f"Validator A {VERSION}", "format": "Format 0.1 Draft",
        "formatDraftSha256": sha((ROOT / "spec/FORMAT_0.1_DRAFT.md").read_bytes()),
        "requirementsRegistrySha256": sha((ROOT / "spec/requirements.yaml").read_bytes()),
        "schemaBundleSha256": sha(schemas),
        "unicodeVersion": "unicode-normalization 0.1.25 / Unicode 16 data",
        "epubcheckVersion": "5.3.0", "fixtureCount": len(golden), "results": golden,
    }
    golden_dir = ROOT / "validator-a/reports/golden"
    golden_dir.mkdir(parents=True, exist_ok=True)
    (golden_dir / f"validator-a-{VERSION}.json").write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "validator-a/reports/epubcheck-corpus-results.json").write_text(json.dumps({"tool": "EPUBCheck", "version": "5.3.0", "applicableCount": 31, "results": tools}, indent=2) + "\n", encoding="utf-8")
    print(f"69/69 normalized; {len(tools)}/31 EPUBCheck PASS")

if __name__ == "__main__": main()
