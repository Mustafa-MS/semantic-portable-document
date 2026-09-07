"""Render the requirements registry as a reviewable conformance matrix."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "spec" / "requirements.yaml"
TARGET = ROOT / "spec" / "CONFORMANCE_MATRIX.md"

NEGATIVE = {
    "SPD-BASE-001": "path-traversal",
    "SPD-BASE-002": "path-traversal; duplicate-normalized-path",
    "SPD-BASE-006": "multiple-rootfiles",
    "SPD-SEC-001": "javascript; event-handler",
    "SPD-SEC-002": "javascript",
    "SPD-SEC-003": "external-required-css/image/font",
    "SPD-SEC-004": "external-required-font",
    "SPD-SEC-005": "external-required-css",
    "SPD-SEC-006": "external-required-image",
    "SPD-SEC-007": "javascript",
    "SPD-SEC-008": "external-required-css/image/font",
    "SPD-SEM-002": "invalid-xhtml",
    "SPD-SEM-006": "invalid-table-semantics",
    "SPD-SEM-013": "invalid-table-semantics",
    "SPD-ID-001": "missing-document-id",
    "SPD-ID-002": "missing-revision-id",
    "SPD-ID-003": "sealed-after-semantic-modification",
    "SPD-ID-005": "invalid-table-semantics",
    "SPD-ID-006": "duplicate-node-id",
    "SPD-ID-010": "invalid-table-semantics",
    "SPD-ID-011": "— (lineage-history editor harness)",
    "SPD-ID-012": "— (lineage-history editor harness)",
    "SPD-ID-013": "same-semantic-different-revision-id",
    "SPD-I18N-001": "visual-order-arabic-source",
    "SPD-I18N-002": "visual-order-arabic-source",
    "SPD-I18N-003": "missing-root-language",
    "SPD-I18N-004": "missing-root-direction",
    "SPD-I18N-005": "visual-order-arabic-source",
    "SPD-I18N-006": "mapping-invalid-range",
    "SPD-STATE-001": "stale-fixed-rendition",
    "SPD-STATE-002": "sealed-after-semantic-modification",
    "SPD-STATE-003": "sealed-after-semantic-modification",
    "SPD-STATE-004": "mutation-fixed",
    "SPD-STATE-005": "stale-fixed-rendition; css-change-stales-fixed",
    "SPD-STATE-006": "semantic-only-sealed (positive boundary)",
    "SPD-STATE-007": "mapping-with-stale-fixed",
    "SPD-RES-001": "missing-document-id (schema analogue)",
    "SPD-RES-002": "bad-resource-hash",
    "SPD-RES-003": "unlisted-normative-resource",
    "SPD-RES-004": "bad-resource-hash",
    "SPD-RES-005": "capability-status-not-user-controlled (schema analogue)",
    "SPD-RES-006": "unlisted-non-normative-resource",
    "SPD-INT-001": "bad-resource-hash",
    "SPD-INT-002": "bad-resource-hash",
    "SPD-INT-003": "mutation-semantic/css/asset/mapping/fixed",
    "SPD-INT-004": "semantic-change-new-revision; same-semantic-different-revision-id",
    "SPD-INT-005": "css-change-stales-fixed; font-change-stales-fixed",
    "SPD-INT-006": "mutation-semantic (descriptor verification)",
    "SPD-FIX-001": "mapping-wrong-revision",
    "SPD-MAP-001": "stale-fixed-rendition",
    "SPD-MAP-002": "mapping-wrong-revision; mapping-wrong-rendition",
    "SPD-MAP-005": "unsupported-mapping (positive edge status)",
    "SPD-MAP-007": "mapping-invalid-page (schema analogue)",
    "SPD-MAP-008": "mapping-invalid-range",
    "SPD-MAP-009": "visual-order-arabic-source",
    "SPD-MAP-011": "mapping-invalid-page; mapping-invalid-range; mapping-invalid-geometry",
    "SPD-MAP-012": "mapping-invalid-geometry",
    "SPD-ANN-002": "lineage-scoped-annotation",
    "SPD-ANN-003": "revision-scoped-annotation",
    "SPD-ANN-004": "sealed-after-annotation-modification",
    "SPD-ACC-004": "accessible (positive plus human evaluation)",
    "SPD-CAP-002": "capability-status-not-user-controlled",
    "SPD-CAP-003": "descriptor-discovery-conflict",
    "SPD-DISC-001": "descriptor-discovery-missing",
    "SPD-DISC-002": "descriptor-discovery-conflict",
    "SPD-DISC-003": "descriptor-discovery-missing",
}

POSITIVE = {
    "BASE": "minimal-base",
    "SEC": "minimal-base; figure-svg",
    "SEM": "minimal-base; table; figure-svg; mathml",
    "ID": "minimal-base; multi-spine",
    "I18N": "arabic; mixed-bidi; rtl-range",
    "ANN": "annotations",
    "STATE": "sealed; minimal-base (editable/absent)",
    "RES": "minimal-base; sealed",
    "INT": "sealed",
    "FIX": "mapped; sealed",
    "MAP": "mapped; partial-mapping; node-not-visible; unsupported-mapping",
    "ACC": "table; figure-svg; mathml; arabic",
    "PROV": "minimal-base",
    "IMP": "—",
    "API": "minimal-base",
    "CAP": "mapped; minimal-base",
    "DISC": "minimal-base; descriptor discovery links",
    "EXT": "—",
    "TEST": "arabic; mixed-bidi; edge corpus",
    "GOV": "—",
    "ARCH": "minimal-base; mapped",
}

APPROACH = {
    "SCHEMA": "JSON Schema plus cross-document identity checks.",
    "PACKAGE": "Safe ZIP/OCF inspection and EPUBCheck; no extraction before path checks.",
    "SEMANTIC": "XML/DOM rules plus targeted source-oracle and lineage checks.",
    "SECURITY": "Parse URL-bearing markup/CSS/SVG and reject active or required remote dependencies.",
    "INTEGRITY": "Recompute exact resource-byte SHA-256 and state bindings.",
    "MAPPING": "Schema plus referenced-ID, range, page, geometry, status, and binding checks.",
    "ACCESSIBILITY": "Automated structural rules plus explicit human evaluation where noted.",
    "MANUAL": "Documented human/process review; no false automated certification.",
}


def parse() -> list[dict[str, str]]:
    rows = []
    pattern = re.compile(
        r"id: (?P<id>SPD-[A-Z0-9]+-\d{3}).*?capability: \[(?P<caps>[^]]+)\].*?testability: (?P<test>[A-Z_]+), testType: (?P<type>[A-Z]+)"
    )
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("- {id:"):
            continue
        match = pattern.search(line)
        if not match:
            raise ValueError(f"Cannot parse requirement line: {line}")
        row = match.groupdict()
        row["caps"] = row["caps"].replace(", ", ",")
        rows.append(row)
    return rows


def main() -> None:
    rows = parse()
    lines = [
        "# Format 0.1 conformance matrix",
        "",
        "This matrix is generated from `requirements.yaml`. A dash in the fixture column means the requirement is governance/manual or has a defined procedural strategy without a dedicated package. Physical fixtures are intentionally concentrated on critical security, integrity, identity, RTL, and mapping invariants.",
        "",
        "| Requirement | Capability | Automated? | Schema? | Positive fixture | Negative fixture | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        domain = row["id"].split("-")[1]
        schema = "Yes" if row["type"] == "SCHEMA" else ("Partial" if row["type"] in {"MAPPING", "INTEGRITY"} else "No")
        positive = POSITIVE.get(domain, "minimal-base")
        negative = NEGATIVE.get(row["id"], "—")
        note = APPROACH[row["type"]]
        if row["test"] == "INFORMATIVE_ONLY":
            note = "Specification/project governance; retained in registry but not document validity."
        elif row["test"] == "MANUAL":
            note = "Manual evidence required. " + note
        elif row["test"] == "PARTIALLY_AUTOMATED":
            note = "Partial automation only. " + note
        lines.append(f"| {row['id']} | {row['caps']} | {row['test']} | {schema} | {positive} | {negative} | {note} |")
    lines += [
        "",
        f"Registry rows: **{len(rows)}**.",
        "",
        "The corpus checker fails if a fixture references an unknown requirement ID or if a registry row cannot be rendered. Dedicated negative fixtures are mandatory for the critical categories identified in the task; remaining automated rules have the validation approach shown above and can share compound fixtures in the future validator suite.",
    ]
    TARGET.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
