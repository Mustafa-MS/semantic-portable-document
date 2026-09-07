"""Read-only frozen comparison. Writes only Stage 2 analysis artifacts."""
from pathlib import Path
import collections
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "validator-differential"
A_PATH = ROOT / "validator-a/reports/golden/validator-a-0.1.0-draft.1.json"
B_PATH = ROOT / "validator-b/reports/blind-results-with-epubcheck.json"
FIELDS = ["base", "normativeCapabilities", "violationRequirementIds", "notTestedRequirementIds", "operationalStatus"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_result(row):
    statuses = [row["base"], *[s for s in row["normativeCapabilities"].values() if s != "NOT_CLAIMED"]]
    return "INVALID" if "FAIL" in statuses else "UNDETERMINED" if "NOT_TESTED" in statuses else "VALID"


def main():
    pins = {
        "validator-b/reports/blind-results-with-epubcheck.json": "af68e0e02182cf6a212c437ba19f6faa8a2d08409b65c3d77aa848e895cc2ed4",
        "spec/FORMAT_0.1_DRAFT.md": "fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849",
        "spec/requirements.yaml": "a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a",
    }
    for path, expected in pins.items():
        assert digest(ROOT / path) == expected, "DIFFERENTIAL_FREEZE_FAILURE: " + path
    a, b = read(A_PATH), read(B_PATH)
    assert a["validator"] == "Validator A 0.1.0-draft.1"
    assert a["epubcheckVersion"] == "5.3.0"
    assert a["formatDraftSha256"] == "sha256:" + pins["spec/FORMAT_0.1_DRAFT.md"]
    assert a["requirementsRegistrySha256"] == "sha256:" + pins["spec/requirements.yaml"]
    env = read(ROOT / "validator-b/reports/epubcheck-completion-environment.json")
    assert env["epubcheckVersionOutput"] == "EPUBCheck v5.3.0"
    aa = {x["fixture"]: x for x in a["results"]}
    bb = {x["fixture"]: x for x in b["results"]}
    assert len(aa) == len(a["results"]) == len(bb) == len(b["results"]) == 69
    assert set(aa) == set(bb)
    rows = []
    for fid in sorted(aa):
        left, right = aa[fid], bb[fid]
        for side in (left, right):
            for key in ("violationRequirementIds", "notTestedRequirementIds"):
                assert side[key] == sorted(set(side[key])), (fid, key)
        av, bv = set(left["violationRequirementIds"]), set(right["violationRequirementIds"])
        rows.append({
            "fixture": fid,
            "equalFields": {key: left[key] == right[key] for key in FIELDS},
            "completeSurfaceAgreement": all(left[k] == right[k] for k in FIELDS),
            "A_ONLY": sorted(av - bv), "B_ONLY": sorted(bv - av), "COMMON": sorted(av & bv),
            "strictASubsetOfB": av < bv,
            "A": {key: left[key] for key in FIELDS},
            "B": {key: right[key] for key in FIELDS},
            "semanticClassification": {"A": semantic_result(left), "B": semantic_result(right)},
            "experimental": {"A": left["experimentalCapabilities"], "B": right["experimentalCapabilities"], "equal": left["experimentalCapabilities"] == right["experimentalCapabilities"]},
        })
    metrics = {"fixtureIdentityAgreement": 69, "fixtureCount": 69}
    metrics.update({key + "Agreement": sum(x["equalFields"][key] for x in rows) for key in FIELDS})
    metrics["completeDifferentialSurfaceAgreement"] = sum(x["completeSurfaceAgreement"] for x in rows)
    metrics["normativeInvalidityAgreement"] = sum((x["semanticClassification"]["A"] == "INVALID") == (x["semanticClassification"]["B"] == "INVALID") for x in rows)
    metrics["threeValuedSemanticAgreement"] = sum(x["semanticClassification"]["A"] == x["semanticClassification"]["B"] for x in rows)
    metrics["experimentalAgreementExcludedFromNormative"] = sum(x["experimental"]["equal"] for x in rows)
    disagreements = [x for x in rows if not x["equalFields"]["violationRequirementIds"]]
    metrics["violationSetDisagreements"] = len(disagreements)
    metrics["strictASubsetOfBForEveryViolationDisagreement"] = all(x["strictASubsetOfB"] for x in disagreements)
    result = {
        "stage": "Stage 2 analysis only", "contractFields": FIELDS,
        "freezeVerification": {
            "A": {"path": A_PATH.relative_to(ROOT).as_posix(), "sha256": digest(A_PATH), "method": "Expected artifact path/version and frozen metadata match; no prior independent oracle checksum supplied."},
            "B": {"path": B_PATH.relative_to(ROOT).as_posix(), "sha256": digest(B_PATH), "method": "Exact user-supplied digest verified"},
            "normativePins": pins,
            "epubcheckVersionA": a["epubcheckVersion"], "epubcheckVersionB": "5.3.0",
            "unicodeA": a["unicodeVersion"], "unicodeB": env["unicodeData"],
            "environmentCaveat": "Known Unicode data difference and independent schema-set digest conventions retained; same official EPUBCheck release, but A recorded only 31 valid/edge tool runs versus B 69.",
        },
        "metrics": metrics,
        "fixtures": rows,
    }
    (OUT / "raw-diff.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(metrics, indent=2))
    for row in disagreements:
        print(row["fixture"], "A_ONLY=" + ",".join(row["A_ONLY"]), "B_ONLY=" + ",".join(row["B_ONLY"]), "COMMON=" + ",".join(row["COMMON"]))


if __name__ == "__main__":
    main()
