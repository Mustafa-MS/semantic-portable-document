from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .models import OperationalStatus, Outcome, ValidationOptions, ValidationReport
from .policy import external_ids

# The previously supplied digest identifies the official release ZIP, not its JAR.
# This JAR digest was obtained only after verifying that pinned official ZIP.
ACCEPTED_RELEASE_ZIP_SHA256 = "6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5"
ACCEPTED_JAR_SHA256 = "f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65"


@dataclass(slots=True)
class EPUBCheckAdapter:
    command: list[str] | None
    version: str | None
    status: str
    detail: str | None = None

    @classmethod
    def detect(cls, options: ValidationOptions) -> EPUBCheckAdapter:
        command: list[str] | None = None
        jar = options.epubcheck_jar or os.environ.get("EPUBCHECK_JAR")
        if jar:
            path = Path(jar)
            if not path.is_file():
                return cls(None, None, "TOOL_UNAVAILABLE", "configured EPUBCheck JAR is missing")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != ACCEPTED_JAR_SHA256:
                return cls(None, None, "TOOL_UNAVAILABLE", f"EPUBCheck JAR SHA-256 mismatch: {actual}")
            java = shutil.which("java")
            if not java:
                return cls(None, None, "TOOL_UNAVAILABLE", "Java runtime is unavailable")
            command = [java, "-jar", str(path)]
        else:
            executable = options.epubcheck_command or shutil.which("epubcheck")
            if executable:
                command = [executable]
        if command is None:
            return cls(None, None, "TOOL_UNAVAILABLE", "EPUBCheck 5.3.0 is not configured")
        try:
            completed = subprocess.run(
                [*command, "--version"], capture_output=True, text=True, timeout=20,
                check=False, encoding="utf-8", errors="replace",
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return cls(None, None, "TOOL_UNAVAILABLE", str(exc))
        output = (completed.stdout + "\n" + completed.stderr).strip()
        match = re.search(r"\bEPUBCheck\s+v?(\d+\.\d+\.\d+)\b", output, re.IGNORECASE)
        version = match.group(1) if match else None
        if version != options.require_epubcheck_version:
            return cls(None, version, "TOOL_UNAVAILABLE", f"required {options.require_epubcheck_version}; found {version or 'unknown'}; exit={completed.returncode}; output={output}")
        return cls(command, version, "AVAILABLE", output)

    def validate(self, path: Path, report: ValidationReport) -> None:
        report.metadata["epubcheck"] = {"status": self.status, "version": self.version, "detail": self.detail,
                                       "executed": False, "skipReason": None, "attributionVersion": "0.1.2",
                                       "fixtureSha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None}
        if self.command is None:
            report.metadata["epubcheck"]["skipReason"] = self.detail
            report.operational_status = OperationalStatus.TOOL_UNAVAILABLE
            report.add(
                "SPD-BASE-002", Outcome.NOT_TESTED,
                "inherited EPUB 3.3 validation was not completed because EPUBCheck 5.3.0 is unavailable",
            )
            return
        try:
            completed = subprocess.run(
                [*self.command, str(path)], capture_output=True, text=True, timeout=120,
                check=False, encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            report.operational_status = OperationalStatus.TOOL_UNAVAILABLE
            report.add("SPD-BASE-002", Outcome.NOT_TESTED, "EPUBCheck exceeded the adapter time limit")
            return
        except OSError as exc:
            report.operational_status = OperationalStatus.TOOL_UNAVAILABLE
            report.add("SPD-BASE-002", Outcome.NOT_TESTED, f"EPUBCheck invocation failed: {exc}")
            return
        output = completed.stdout + "\n" + completed.stderr
        completed_normally = 'EPUBCheck completed' in output and completed.returncode in (0, 1)
        attributed = external_ids(output) if completed_normally else []
        # Execution evidence is metadata only; normalized findings/roll-up are unchanged.
        report.metadata["epubcheck"].update({
            "exitCode": completed.returncode,
            "executed": True,
            "normalizedSpdAttributionIds": attributed,
            "result": "PASS" if completed.returncode == 0 else ("ERROR" if completed.returncode < 0 else "FAIL"),
            "diagnosticCodes": sorted(set(re.findall(r"\b[A-Z]{2,8}-[0-9]{3}[a-z]?\b", output))),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        })
        if not completed_normally or (completed.returncode != 0 and 'SPD-BASE-002' not in attributed):
            report.operational_status = OperationalStatus.TOOL_UNAVAILABLE
            report.metadata['epubcheck']['result'] = 'ERROR'
            report.add('SPD-BASE-002', Outcome.NOT_TESTED, 'tool did not establish a completed conformance result')
        for requirement in attributed:
            report.add(requirement, Outcome.FAIL, "EPUBCheck diagnostic matches Contract 0.1.1 predicate", evidence=output[-8000:])
