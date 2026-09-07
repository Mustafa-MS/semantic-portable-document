from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import ValidationOptions
from .validator import validate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spd-validator-b")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate one SPD/EPUB package")
    validate_parser.add_argument("path", type=Path)
    validate_parser.add_argument("--json", action="store_true", dest="json_output")
    validate_parser.add_argument("--normalized", action="store_true")
    validate_parser.add_argument("--fixture")
    validate_parser.add_argument("--epubcheck-command")
    validate_parser.add_argument("--epubcheck-jar")
    corpus_parser = subparsers.add_parser("corpus", help="blind-run a corpus manifest without reading expected results")
    corpus_parser.add_argument("manifest", type=Path)
    corpus_parser.add_argument("--output", type=Path, required=True)
    return parser


def _corpus(manifest_path: Path, output: Path) -> int:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    repository = manifest_path.resolve().parents[1]
    results = []
    for fixture in manifest["fixtures"]:
        package = repository / fixture["package"]
        report = validate(package)
        results.append(report.normalized(fixture["id"]))
    payload = {
        "validator": "Validator B",
        "version": "0.1.3-rc1",
        "format": "Semantic Portable Document Format 0.1 RC1",
        "fixtureCount": len(results),
        "results": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return 0 if all(item["operationalStatus"] != "INTERNAL_ERROR" for item in results) else 2


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "corpus":
        return _corpus(args.manifest, args.output)
    options = ValidationOptions(epubcheck_command=args.epubcheck_command, epubcheck_jar=args.epubcheck_jar)
    report = validate(args.path, options)
    if args.normalized:
        print(json.dumps(report.normalized(args.fixture), indent=2, ensure_ascii=False))
    elif args.json_output:
        print(json.dumps(report.detailed(), indent=2, ensure_ascii=False))
    else:
        print(f"Base: {report.base}")
        print(f"Operational status: {report.operational_status.value}")
        for finding in sorted(report.findings, key=lambda item: item.sort_key()):
            location = f" [{finding.resource}]" if finding.resource else ""
            print(f"{finding.outcome.value} {finding.requirement_id}{location}: {finding.message}")
    return 2 if report.operational_status.value in {"INTERNAL_ERROR", "RESOURCE_LIMIT", "SPEC_BLOCKER"} else (1 if report.base == "FAIL" else 0)


if __name__ == "__main__":
    sys.exit(main())
