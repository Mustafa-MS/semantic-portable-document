from __future__ import annotations

from pathlib import Path

from spd_validator_b.coverage import build_coverage
from spd_validator_b.schemas import SchemaStore

ROOT = Path(__file__).resolve().parents[2]


def test_all_canonical_schemas_load_and_meta_validate() -> None:
    store = SchemaStore(ROOT / "schemas/rc1")
    assert len(store.schemas) == 6


def test_requirement_coverage_is_complete() -> None:
    coverage = build_coverage(ROOT / "spec" / "requirements-0.1-rc1.yaml")
    assert coverage["summary"] == {
        "total": 118,
        "represented": 118,
        "automated": 74,
        "automatedImplemented": 74,
    }

