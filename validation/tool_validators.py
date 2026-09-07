from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from harness.util import ROOT


EPUBCHECK_JAR = ROOT / ".phase1b" / "tools" / "epubcheck" / "epubcheck-5.3.0" / "epubcheck.jar"
VERAPDF = ROOT / ".phase1b" / "tools" / "verapdf" / "verapdf.bat"


def run_epubcheck(epub: Path, output: Path) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["java", "-jar", str(EPUBCHECK_JAR), str(epub), "--json", str(output)], capture_output=True, text=True, timeout=180)
    data = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
    checker = data.get("checker", {})
    status = "FAIL" if checker.get("nFatal", 0) or checker.get("nError", 0) else "WARN" if checker.get("nWarning", 0) else "PASS"
    return {"status": status, "exitCode": proc.returncode, "version": checker.get("checkerVersion", "5.3.0"), "fatals": checker.get("nFatal"), "errors": checker.get("nError"), "warnings": checker.get("nWarning"), "usages": checker.get("nUsage"), "diagnostics": data.get("messages", []), "rawResult": str(output.relative_to(ROOT)).replace("\\", "/")}


def run_verapdf(pdf: Path, profile: str) -> dict[str, Any]:
    proc = subprocess.run([str(VERAPDF), "--format", "json", "-f", profile, "--maxfailures", "50", str(pdf)], capture_output=True, text=True, timeout=180)
    try:
        data = json.loads(proc.stdout)
        result = data["report"]["jobs"][0]["validationResult"][0]
        details = result.get("details", {})
        failures = []
        for summary in details.get("ruleSummaries", []):
            failures.append({"specification": summary.get("specification"), "clause": summary.get("clause"), "testNumber": summary.get("testNumber"), "description": summary.get("description"), "failedChecks": summary.get("failedChecks")})
        return {"profile": profile, "profileName": result.get("profileName"), "compliant": bool(result.get("compliant")), "statement": result.get("statement"), "passedRules": details.get("passedRules"), "failedRules": details.get("failedRules"), "failedChecks": details.get("failedChecks"), "failures": failures, "toolVersion": "1.30.2", "exitCode": proc.returncode}
    except Exception as exc:
        return {"profile": profile, "compliant": False, "toolVersion": "1.30.2", "exitCode": proc.returncode, "error": repr(exc), "stderr": proc.stderr[-2000:], "stdout": proc.stdout[-2000:]}

