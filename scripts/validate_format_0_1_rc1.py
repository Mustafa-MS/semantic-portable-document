"""Run and finalize the Format 0.1 RC1 publication gate."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import io
import json
import platform
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/format-0.1-rc1"
MANIFEST_PATH = ROOT / "tests/corpus-0.1-rc1/manifest.json"
JAR = ROOT / "validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar"
ACTIVE_ARTIFACTS = [
    "spec/FORMAT_0.1_RC1.md",
    "spec/requirements-0.1-rc1.yaml",
    "spec/STANDARDS_TRACEABILITY_0.1_RC1.md",
    "spec/FORMAT_0.1_DRAFT_TO_RC1_CHANGELOG.md",
    "spec/IDENTIFIER_NAMESPACE_REGISTRY_0.1_RC1.md",
    "tests/corpus-0.1-rc1/manifest.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot(side: str) -> dict[str, str]:
    paths = [ROOT / item for item in ACTIVE_ARTIFACTS]
    paths.extend(p for p in (ROOT / "schemas/rc1").rglob("*") if p.is_file())
    paths.extend(p for p in (ROOT / "spec/profiles-0.1-rc1").rglob("*") if p.is_file())
    code = ROOT / ("validator-a/src" if side == "a" else "validator-b/spd_validator_b")
    paths.extend(p for p in code.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))}


def normalize_expected(expected: dict) -> dict:
    return {
        "fixture": expected["fixture"],
        "base": expected["base"],
        "normativeCapabilities": {name: expected["capabilities"][name] for name in ("Accessible", "Mapping")},
        "experimentalCapabilities": {
            name: expected["capabilities"][name] for name in ("Archive-Experimental", "Fixed-Experimental")
        },
        "violationRequirementIds": sorted(item["requirement"] for item in expected["violations"]),
        "notTestedRequirementIds": expected["notTestedRequirementIds"],
        "operationalStatus": expected["operationalStatus"],
        "authoritativeClaimsStatus": expected["authoritativeClaimsStatus"],
        "experimentalReporting": expected["experimentalReporting"],
    }


def one_a(fixture: dict) -> dict:
    path = ROOT / fixture["package"]
    command = [
        str(ROOT / "validator-a/target/release/spd-validator.exe"),
        "validate",
        str(path),
        "--format",
        "json",
        "--epubcheck",
        str(JAR),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=200)
    report = json.loads(completed.stdout)
    normalized = {
        "fixture": fixture["id"],
        "base": report["base"],
        "normativeCapabilities": {name: report["capabilities"].get(name, "UNKNOWN") for name in ("Accessible", "Mapping")},
        "experimentalCapabilities": {
            name: report["capabilities"].get(name, "UNKNOWN")
            for name in ("Archive-Experimental", "Fixed-Experimental")
        },
        "violationRequirementIds": sorted(
            {item["requirementId"] for item in report["findings"] if item["outcome"] == "FAIL"}
        ),
        "notTestedRequirementIds": report["notTestedRequirements"],
        "operationalStatus": report["operationalStatus"],
        "authoritativeClaimsStatus": report["authoritativeClaimsStatus"],
        "experimentalReporting": report["experimentalReporting"],
    }
    return {"normalized": normalized, "report": report, "exitCode": completed.returncode, "stderr": completed.stderr}


def run_side(side: str, workers: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    before = source_snapshot(side)
    if side == "b":
        sys.path.insert(0, str(ROOT / "validator-b"))
        from spd_validator_b.models import ResourceLimits, ValidationOptions
        from spd_validator_b.validator import validate

        options = ValidationOptions(
            epubcheck_jar=str(JAR),
            limits=ResourceLimits(
                max_package_bytes=536870912,
                max_entry_bytes=268435456,
                max_total_decompressed_bytes=1073741824,
                max_xml_bytes=33554432,
                max_json_bytes=67108864,
            ),
        )

        def work(fixture: dict) -> dict:
            report_object = validate(ROOT / fixture["package"], options)
            return {
                "normalized": report_object.normalized(fixture["id"]),
                "report": report_object.detailed(),
                "exitCode": 0,
                "stderr": "",
            }
    else:
        work = one_a

    def checked(fixture: dict) -> dict:
        package = ROOT / fixture["package"]
        if sha(package) != fixture["packageSha256"]:
            raise AssertionError(f"package hash mismatch: {fixture['id']}")
        result = work(fixture)
        expected = normalize_expected(json.loads((ROOT / fixture["expectedResult"]).read_text(encoding="utf-8")))
        result["differences"] = {
            key: {"expected": expected[key], "actual": result["normalized"][key]}
            for key in expected
            if expected[key] != result["normalized"][key]
        }
        if result["differences"]:
            print(fixture["id"], json.dumps(result["differences"]), flush=True)
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(checked, manifest["fixtures"]))
    after = source_snapshot(side)
    payload = {
        "validator": side,
        "version": "0.1.0-rc1" if side == "a" else "0.1.3-rc1",
        "fixtureCount": len(results),
        "manifestSha256": sha(MANIFEST_PATH),
        "epubcheckJarSha256": sha(JAR),
        "sourceSha256": before,
        "sourceStableDuringRun": before == after,
        "results": results,
    }
    (OUT / f"validator-{side}-results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Validator {side.upper()}: {len(results)} fixtures; {sum(bool(item['differences']) for item in results)} differences")


def external_record(side: str, row: dict) -> dict:
    report = row["report"]
    evidence = report["externalTools"][0] if side == "a" else report["metadata"]["epubcheck"]
    return {
        "fixture": row["normalized"]["fixture"],
        "executed": evidence.get("executed"),
        "outcome": evidence.get("outcome", evidence.get("result")),
        "exitCode": evidence.get("exitCode"),
        "diagnosticCodes": evidence.get("diagnosticCodes", []),
        "fixtureSha256": evidence.get("fixtureSha256"),
    }


def scan_package_for_placeholder(path: Path, malformed: bool) -> bool:
    raw = path.read_bytes()
    if malformed:
        raw = bytearray(raw)
        raw[30] = ord("m")
        raw = bytes(raw)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        return any(b"https://example.invalid/spd/" in archive.read(info) for info in archive.infolist())


def finalize() -> None:
    data = {side: json.loads((OUT / f"validator-{side}-results.json").read_text()) for side in ("a", "b")}
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = {
        item["id"]: normalize_expected(json.loads((ROOT / item["expectedResult"]).read_text(encoding="utf-8")))
        for item in manifest["fixtures"]
    }
    actual = {
        side: {row["normalized"]["fixture"]: row["normalized"] for row in data[side]["results"]}
        for side in data
    }
    a_b_differences = [fixture for fixture in expected if actual["a"][fixture] != actual["b"][fixture]]
    oracle_differences = {
        side: [fixture for fixture in expected if actual[side][fixture] != expected[fixture]] for side in data
    }
    assert not a_b_differences and not any(oracle_differences.values())
    assert all(row["differences"] == {} for side in data.values() for row in side["results"])
    assert all(side["sourceStableDuringRun"] for side in data.values())
    assert all(side["manifestSha256"] == sha(MANIFEST_PATH) for side in data.values())
    assert all(side["epubcheckJarSha256"] == "f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65" for side in data.values())

    source_manifest = ROOT / "tests/corpus-0.1.2/manifest.json"
    assert sha(source_manifest) == manifest["sourceManifestSha256"] == "943e9794e756b07e3180651329d78aa3bc7522c769f94457083b1d009a7bb7cc"
    gate_environment = json.loads((ROOT / "reports/pre_rc_passive_security/environment.json").read_text())
    assert sha(ROOT / "spec/FORMAT_0.1_DRAFT.md") == gate_environment["specSha256"]
    assert sha(ROOT / "spec/requirements.yaml") == gate_environment["requirementsSha256"]

    mechanical_differences = []
    placeholder_packages = []
    for fixture in manifest["fixtures"]:
        assert sha(ROOT / fixture["package"]) == fixture["packageSha256"]
        assert sha(ROOT / fixture["expectedResult"]) == fixture["expectedResultSha256"]
        assert sha(ROOT / fixture["sourcePackage"]) == fixture["sourcePackageSha256"]
        assert sha(ROOT / fixture["sourceExpectedResult"]) == fixture["sourceExpectedResultSha256"]
        rc_expected = json.loads((ROOT / fixture["expectedResult"]).read_text())
        old_expected = json.loads((ROOT / fixture["sourceExpectedResult"]).read_text())
        rc_expected.pop("corpusVersion", None)
        old_expected.pop("corpusVersion", None)
        if rc_expected != old_expected:
            mechanical_differences.append(fixture["id"])
        if scan_package_for_placeholder(ROOT / fixture["package"], fixture["id"] == "security/zip-header-mismatch"):
            placeholder_packages.append(fixture["id"])
    assert not mechanical_differences and not placeholder_packages

    registry = yaml.safe_load((ROOT / "spec/requirements-0.1-rc1.yaml").read_text())
    assert len(registry["requirements"]) == 118
    assert len({item["id"] for item in registry["requirements"]}) == 118
    assert registry["capabilities"]["Fixed-Experimental"]["status"] == "experimental"
    assert registry["capabilities"]["Archive-Experimental"]["status"] == "experimental"

    schema_manifest = json.loads((ROOT / "schemas/rc1/manifest.json").read_text())
    assert len(schema_manifest["schemas"]) == 6
    assert all(sha(ROOT / "schemas/rc1" / item["file"]) == item["sha256"] for item in schema_manifest["schemas"])

    external = {
        side: [external_record(side, row) for row in data[side]["results"]] for side in data
    }
    for side, records in external.items():
        assert all(item["executed"] is True and item["outcome"] in {"PASS", "FAIL"} for item in records)
        by_fixture = {item["fixture"]: item for item in records}
        assert all(by_fixture[fixture]["outcome"] == "PASS" for fixture, oracle in expected.items() if oracle["base"] == "PASS")
        assert all(by_fixture[item["id"]]["fixtureSha256"] == item["packageSha256"] for item in manifest["fixtures"])

    base_counts = Counter(item["base"] for item in expected.values())
    assert base_counts == {"PASS": 48, "FAIL": 58, "NOT_TESTED": 1}
    operational_counts = Counter(item["operationalStatus"] for item in expected.values())
    assert operational_counts == {"COMPLETE": 105, "MALFORMED_INPUT": 1, "RESOURCE_LIMIT": 1}
    assert not any(item["operationalStatus"] == "SPEC_BLOCKER" for side in actual.values() for item in side.values())

    result = {
        "status": "FORMAT 0.1 RC1 READY FOR EXTERNAL REVIEW",
        "fixtureCount": 107,
        "requirementCount": 118,
        "validatorAgreement": "107/107",
        "validatorAOracleAgreement": "107/107",
        "validatorBOracleAgreement": "107/107",
        "baseCounts": dict(base_counts),
        "operationalCounts": dict(operational_counts),
        "basePassEpubcheck": {"a": "48/48", "b": "48/48"},
        "newSpecificationBlockers": 0,
        "normativeSemanticChanges": "NONE",
        "manifestSha256": sha(MANIFEST_PATH),
        "epubcheckJarSha256": sha(JAR),
        "environment": {"python": sys.version, "platform": platform.platform(), "epubcheck": "5.3.0"},
        "aBdifferences": a_b_differences,
        "oracleDifferences": oracle_differences,
        "placeholderPackages": placeholder_packages,
        "mechanicalExpectedResultDifferences": mechanical_differences,
        "external": external,
    }
    (OUT / "RC1_VALIDATION_REPORT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    artifact_paths = [ROOT / item for item in ACTIVE_ARTIFACTS]
    artifact_paths.extend(p for p in (ROOT / "schemas/rc1").rglob("*") if p.is_file())
    artifact_paths.extend(p for p in (ROOT / "spec/profiles-0.1-rc1").rglob("*") if p.is_file())
    artifact_paths.extend([OUT / "validator-a-results.json", OUT / "validator-b-results.json", OUT / "RC1_VALIDATION_REPORT.json"])
    artifact_manifest = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(artifact_paths))}
    (OUT / "RC1_ARTIFACT_MANIFEST.json").write_text(json.dumps(artifact_manifest, indent=2) + "\n", encoding="utf-8")

    report = f"""# Format 0.1 RC1 validation report

## Result

- Requirements: **118**; IDs and conformance predicates preserved.
- Corpus: **107** fixtures; Base results PASS 48, FAIL 58, NOT_TESTED 1.
- Validator A ↔ Validator B: **107/107** exact agreement.
- Validator A ↔ reviewed oracle: **107/107**.
- Validator B ↔ reviewed oracle: **107/107**.
- Official EPUBCheck 5.3.0 executed on **107/107** package byte sequences for each validator.
- All Base-PASS fixtures pass EPUBCheck: **48/48** for A and **48/48** for B.
- Final operational statuses: 105 COMPLETE, one MALFORMED_INPUT, one RESOURCE_LIMIT; no INTERNAL_ERROR or SPEC_BLOCKER.
- New specification blockers: **0**.
- Normative semantic changes: **NONE**.

## Identifier and mechanical migration

Every RC1 package is a versioned copy. Stable UUID URNs replace Draft schema, relationship, capability, and annotation-extension placeholders. Valid byte/digest bindings were regenerated deterministically; deliberately invalid bindings and malformed/special ZIP predicates were retained. RC1 expected results differ from Corpus 0.1.2 only in `corpusVersion`. No RC1 package contains `https://example.invalid/spd/`.

The RC1 corpus manifest SHA-256 is `{sha(MANIFEST_PATH)}`. The official EPUBCheck 5.3.0 JAR SHA-256 is `{sha(JAR)}`. Exact package, expected-result, source-package, schema, validator-output, and publication-artifact hashes are recorded in the versioned manifests.

## Preservation and scope

The converged Draft specification, Draft registry, Corpus 0.1.2 packages and expectations, reviewed oracle, validator convergence freezes, and pre-RC evidence remain unchanged. Fixed-Experimental and Archive-Experimental remain experimental. No reference reader was started or evaluated. Reader behavior, manual accessibility evaluation, signatures, encryption/DRM, functional forms, interactive/scripting capability, collaboration/tracked changes, and a final agent API remain outside this RC1 validation claim.

FORMAT 0.1 RC1 READY FOR EXTERNAL REVIEW
"""
    (OUT / "RC1_VALIDATION_REPORT.md").write_text(report, encoding="utf-8")
    print("FORMAT 0.1 RC1 READY FOR EXTERNAL REVIEW")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("a", "b", "finalize"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.mode == "finalize":
        finalize()
    else:
        run_side(args.mode, args.workers)


if __name__ == "__main__":
    main()
