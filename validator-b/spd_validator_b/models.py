from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class Outcome(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_TESTED = "NOT_TESTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INFORMATIVE = "INFORMATIVE"


class OperationalStatus(StrEnum):
    COMPLETE = "COMPLETE"
    TOOL_UNAVAILABLE = "TOOL_UNAVAILABLE"
    RESOURCE_LIMIT = "RESOURCE_LIMIT"
    MALFORMED_INPUT = "MALFORMED_INPUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SPEC_BLOCKER = "SPEC_BLOCKER"


@dataclass(slots=True)
class ResourceLimits:
    max_entries: int = 10_000
    max_package_bytes: int = 1_000_000_000
    max_entry_bytes: int = 256_000_000
    max_total_decompressed_bytes: int = 2_000_000_000
    max_compression_ratio: float = 1_000.0
    max_xml_bytes: int = 32_000_000
    max_json_bytes: int = 32_000_000
    max_json_depth: int = 128


@dataclass(slots=True)
class ValidationOptions:
    epubcheck_command: str | None = None
    epubcheck_jar: str | None = None
    require_epubcheck_version: str = "5.3.0"
    lineage_evidence: bool = False
    limits: ResourceLimits = field(default_factory=ResourceLimits)


@dataclass(slots=True, frozen=True)
class Finding:
    requirement_id: str
    outcome: Outcome
    message: str
    resource: str | None = None
    node: str | None = None
    evidence: Any = None

    def sort_key(self) -> tuple[str, str, str, str, str]:
        return (
            self.requirement_id,
            self.outcome.value,
            self.resource or "",
            self.node or "",
            self.message,
        )


@dataclass(slots=True)
class ValidationReport:
    path: str
    findings: list[Finding] = field(default_factory=list)
    base: str = "NOT_TESTED"
    normative_capabilities: dict[str, str] = field(
        default_factory=lambda: {"Accessible": "NOT_CLAIMED", "Mapping": "NOT_CLAIMED"}
    )
    experimental_capabilities: dict[str, str] = field(
        default_factory=lambda: {
            "Archive-Experimental": "NOT_CLAIMED",
            "Fixed-Experimental": "NOT_CLAIMED",
        }
    )
    operational_status: OperationalStatus = OperationalStatus.COMPLETE
    metadata: dict[str, Any] = field(default_factory=dict)
    requirement_outcomes: dict[str, str] = field(default_factory=dict)

    def add(
        self,
        requirement_id: str,
        outcome: Outcome,
        message: str,
        *,
        resource: str | None = None,
        node: str | None = None,
        evidence: Any = None,
    ) -> None:
        candidate = Finding(requirement_id, outcome, message, resource, node, evidence)
        if candidate not in self.findings:
            self.findings.append(candidate)

    @property
    def violation_requirement_ids(self) -> list[str]:
        return sorted({f.requirement_id for f in self.findings if f.outcome == Outcome.FAIL})

    @property
    def not_tested_requirement_ids(self) -> list[str]:
        return sorted({f.requirement_id for f in self.findings if f.outcome == Outcome.NOT_TESTED} - set(self.violation_requirement_ids))

    def normalized(self, fixture: str | None = None) -> dict[str, Any]:
        return {
            "fixture": fixture or Path(self.path).stem,
            "base": self.base,
            "normativeCapabilities": dict(sorted(self.normative_capabilities.items())),
            "experimentalCapabilities": dict(sorted(self.experimental_capabilities.items())),
            "violationRequirementIds": self.violation_requirement_ids,
            "notTestedRequirementIds": self.not_tested_requirement_ids,
            "operationalStatus": self.operational_status.value,
            "authoritativeClaimsStatus": self.metadata.get("authoritativeClaimsStatus", "UNKNOWN"),
            "experimentalReporting": self.metadata.get("experimentalReporting", {}),
        }

    def detailed(self) -> dict[str, Any]:
        return {
            "validator": "Validator B",
            "path": self.path,
            **self.normalized(),
            "findings": [
                {**asdict(f), "outcome": f.outcome.value}
                for f in sorted(self.findings, key=Finding.sort_key)
            ],
            "requirementOutcomes": dict(sorted(self.requirement_outcomes.items())),
            "metadata": self.metadata,
        }


class ResourceLimitExceeded(Exception):
    pass


class PackageInvalid(Exception):
    pass
