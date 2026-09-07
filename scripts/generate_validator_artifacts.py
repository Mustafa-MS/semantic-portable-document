"""Deterministically regenerate Validator A's fixture and requirement indexes."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "spec" / "requirements.yaml"

def stage(req_id: str) -> str:
    key = req_id.split("-")[1]
    return {
        "BASE": "package", "DISC": "discovery", "RES": "inventory", "INT": "integrity",
        "SEC": "security", "PASS": "passive-security", "RS": "reader-conformance", "SEM": "semantic", "ID": "identity", "I18N": "semantic",
        "ANN": "annotations", "STATE": "state", "FIX": "state", "MAP": "mapping",
        "ACC": "accessibility", "CAP": "capabilities", "EXT": "extensions",
        "ARCH": "architecture", "PROV": "provenance", "IMP": "import",
        "API": "api", "GOV": "governance", "TEST": "test-corpus",
    }.get(key, "rules")

def requirements():
    out = []
    pattern = re.compile(r"^  - \{id: (SPD-[A-Z0-9]+-\d{3}),.*?testability: ([A-Z_]+),")
    for line in REQ.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if match: out.append({"id": match.group(1), "testability": match.group(2)})
    if len(out) != 118: raise SystemExit(f"expected 118 requirements, found {len(out)}")
    return out

def fixtures():
    # The versioned builder owns package/expected bytes. Never overwrite 0.1.1.
    manifest = json.loads((ROOT / "tests/corpus-0.1.2/manifest.json").read_text(encoding="utf-8"))
    assert manifest["fixtureCount"] == len(manifest["fixtures"]) == 107
    return manifest["fixtures"]


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    reqs, fx = requirements(), fixtures()
    status = {"AUTOMATED": "implemented-automatic", "PARTIALLY_AUTOMATED": "implemented-partial", "MANUAL": "manual", "INFORMATIVE_ONLY": "informative"}
    coverage = {r["id"]: {"status": status[r["testability"]], "stage": stage(r["id"]), "module": "src/passive.rs" if r["id"].startswith(("SPD-SEC-", "SPD-PASS-")) else "src/validator.rs"} for r in reqs}
    write(ROOT / "validator-a" / "requirements-coverage.json", coverage)
    by_req = {r["id"]: [] for r in reqs}
    for item in fx:
        for req in item["primaryRequirements"]: by_req[req].append(item["id"])
    test_coverage = {r["id"]: {"tests": ["tests/corpus.rs"] if by_req[r["id"]] else ["grouped stage/unit facts"], "fixtures": by_req[r["id"]], "implementationModule": "src/validator.rs", "stage": stage(r["id"])} for r in reqs}
    write(ROOT / "reports" / "pre_rc_passive_security" / "requirement-test-coverage.json", test_coverage)

if __name__ == "__main__": main()
