"""Auditable B-only external-dependency completion; never reads Validator A."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "validator-b"
REPORTS = B / "reports"
sys.path.insert(0, str(B))
ORIGINAL = "c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c"
JAR = B / "tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar"
BASELINE = REPORTS / "epubcheck-completion-baseline.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def protected_paths() -> list[Path]:
    fixtures = json.loads((ROOT / "tests/corpus-manifest.json").read_text(encoding="utf-8"))["fixtures"]
    return sorted([
        *list((B / "spd_validator_b").glob("*.py")),
        *list((B / "tests").glob("*.py")),
        B / "pyproject.toml",
        REPORTS / "blind-results.json", REPORTS / "BLIND_FREEZE_EVIDENCE.md",
        REPORTS / "SCHEMA_INPUT_MANIFEST.json", REPORTS / "requirement-coverage.json",
        ROOT / "spec/FORMAT_0.1_DRAFT.md", ROOT / "spec/requirements.yaml",
        *[ROOT / f["package"] for f in fixtures],
        *[ROOT / s["relativePath"] for s in json.loads((REPORTS / "SCHEMA_INPUT_MANIFEST.json").read_text())["schemas"]],
    ])


def prepare() -> None:
    assert sha(REPORTS / "blind-results.json") == ORIGINAL, "BLIND_FREEZE_INTEGRITY_FAILURE"
    if BASELINE.exists():
        raise RuntimeError("Baseline already exists; refusing to overwrite")
    write_json(BASELINE, {
        "originalBlindResultsSha256": ORIGINAL,
        "sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in protected_paths()},
        "adapterSourceBefore": (B / "spd_validator_b/epubcheck.py").read_text(encoding="utf-8"),
    })
    print("Baseline captured; original freeze verified", flush=True)


def check_preservation() -> dict:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    changes = []
    for relative, expected in baseline["sha256"].items():
        if sha(ROOT / relative) != expected:
            changes.append(relative)
    assert changes == ["validator-b/spd_validator_b/epubcheck.py"], changes
    return baseline


def run() -> None:
    from spd_validator_b import validate
    from spd_validator_b.coverage import build_coverage
    from spd_validator_b.epubcheck import EPUBCheckAdapter
    from spd_validator_b.models import ValidationOptions

    baseline = check_preservation()
    options = ValidationOptions(epubcheck_jar=str(JAR))
    adapter = EPUBCheckAdapter.detect(options)
    assert adapter.command and adapter.version == "5.3.0", "EPUBCHECK_5_3_0_UNAVAILABLE"
    original = json.loads((REPORTS / "blind-results.json").read_text(encoding="utf-8"))
    fixtures = json.loads((ROOT / "tests/corpus-manifest.json").read_text(encoding="utf-8"))["fixtures"]
    originals = {r["fixture"]: r for r in original["results"]}
    rows = {}
    evidence = {}
    unavailable_rows = {}
    native_differences = []

    def execute(fixture: dict) -> tuple:
        path = ROOT / fixture["package"]
        absent = validate(path, ValidationOptions(epubcheck_jar=str(B / "tools/explicitly-unavailable.jar")))
        report = validate(path, options)
        # Compare actual SPD-native findings, not only IDs: omit only the adapter's own finding.
        external_prefixes = ("inherited EPUB 3.3 validation was not completed", "EPUBCheck 5.3.0 reported inherited EPUB errors")
        def native(r):
            return [f for f in r.detailed()["findings"] if not f["message"].startswith(external_prefixes)]
        return fixture["id"], absent, report, native(absent) == native(report)

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(execute, f) for f in fixtures]
        for future in as_completed(futures):
            fid, absent, report, native_equal = future.result()
            unavailable_rows[fid] = absent.normalized(fid)
            rows[fid] = report.normalized(fid)
            evidence[fid] = {"fixture": fid, **report.metadata.get("epubcheck", {})}
            if not native_equal:
                native_differences.append(fid)
            print(f"{len(rows)}/69 {fid}: {report.operational_status.value}; EPUBCheck={evidence[fid].get('result')}", flush=True)

    ordered = [rows[f["id"]] for f in fixtures]
    recreated = {**original, "results": [unavailable_rows[f["id"]] for f in fixtures]}
    reproduced_path = REPORTS / "blind-results-unavailable-regression.json"
    write_json(reproduced_path, recreated)
    assert sha(reproduced_path) == ORIGINAL, "Unavailable regression no longer reproduces original blind bytes"
    assert not native_differences, native_differences
    assert len(ordered) == 69 and all(r["operationalStatus"] == "COMPLETE" for r in ordered)
    assert all(evidence[f["id"]].get("exitCode") is not None for f in fixtures)

    changes = []
    for after in ordered:
        before = originals[after["fixture"]]
        changed_fields = [key for key in before if before[key] != after[key]]
        old_native = set(before["violationRequirementIds"]) - {"SPD-BASE-002"}
        new_native = set(after["violationRequirementIds"]) - {"SPD-BASE-002"}
        expected = old_native == new_native and set(after["notTestedRequirementIds"]) == set(before["notTestedRequirementIds"]) - {"SPD-BASE-002"}
        # Check the exact frozen roll-up using the externally observed outcome, without changing code.
        tool_failed = evidence[after["fixture"]]["result"] == "FAIL"
        expected_base = "FAIL" if before["base"] == "FAIL" or tool_failed else "PASS"
        expected_caps = dict(before["normativeCapabilities"])
        if expected_caps["Mapping"] != "NOT_CLAIMED":
            expected_caps["Mapping"] = "FAIL" if expected_base == "FAIL" or expected_caps["Mapping"] == "FAIL" else "PASS"
        if expected_caps["Accessible"] != "NOT_CLAIMED":
            expected_caps["Accessible"] = "FAIL" if expected_base == "FAIL" or expected_caps["Accessible"] == "FAIL" else "NOT_TESTED"
        expected = expected and after["base"] == expected_base and after["normativeCapabilities"] == expected_caps
        expected = expected and before["experimentalCapabilities"] == after["experimentalCapabilities"]
        old_base2_failure = "SPD-BASE-002" in before["violationRequirementIds"]
        expected = expected and ("SPD-BASE-002" in after["violationRequirementIds"]) == (old_base2_failure or tool_failed)
        changes.append({
            "fixture": after["fixture"], "changedFields": changed_fields,
            "classification": "EPUBCHECK_NOW_EVALUATED" if expected else "UNEXPECTED_NON_EPUB_DIFFERENCE",
            "nativeDetailedFindingsIdentical": after["fixture"] not in native_differences,
            "before": before, "after": after,
        })
    assert all(c["classification"] == "EPUBCHECK_NOW_EVALUATED" for c in changes)
    complete = {**original, "results": ordered}
    write_json(REPORTS / "blind-results-with-epubcheck.json", complete)
    write_json(REPORTS / "epubcheck-fixture-execution.json", {"executionCount": 69, "results": [evidence[f["id"]] for f in fixtures]})
    write_json(REPORTS / "epubcheck-before-after.json", {"unexpectedDifferenceCount": 0, "unavailableRegressionSha256": sha(reproduced_path), "changes": changes})
    coverage = build_coverage(ROOT / "spec/requirements.yaml")
    java = subprocess.run([adapter.command[0], "-version"], capture_output=True, text=True)
    write_json(REPORTS / "epubcheck-completion-environment.json", {
        "python": platform.python_version(), "unicodeData": unicodedata.unidata_version,
        "javaExecutable": adapter.command[0], "javaVersionOutput": (java.stdout + java.stderr).strip(),
        "epubcheckJar": str(JAR), "epubcheckJarSha256": sha(JAR),
        "officialReleaseURL": "https://github.com/w3c/epubcheck/releases/tag/v5.3.0",
        "releaseZipSha256": sha(B / "tools/epubcheck-5.3.0.zip"),
        "epubcheckVersionOutput": adapter.detail, "availability": adapter.status,
        "fixturesExecuted": 69, "internalErrors": 0, "coverage": coverage["summary"],
        "nativeFilesAndOriginalFreezePreserved": True,
        "newBlindResultsSha256": sha(REPORTS / "blind-results-with-epubcheck.json"),
    })
    diff = "".join(difflib.unified_diff(
        baseline["adapterSourceBefore"].splitlines(keepends=True),
        (B / "spd_validator_b/epubcheck.py").read_text(encoding="utf-8").splitlines(keepends=True),
        fromfile="frozen/spd_validator_b/epubcheck.py", tofile="completed/spd_validator_b/epubcheck.py",
    ))
    (REPORTS / "epubcheck-adapter-only.diff").write_text(diff, encoding="utf-8", newline="\n")
    check_preservation()
    print("COMPLETE_SHA256=" + sha(REPORTS / "blind-results-with-epubcheck.json"), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else run()
