"""Offline tests for DevMate prompt golden cases (A2 evidence)."""

from __future__ import annotations

import json

from devmate.eval.validate_prompt_golden import GOLDEN_PATH, _load_cases, validate_cases


def test_golden_file_exists() -> None:
    assert GOLDEN_PATH.exists(), f"missing golden cases file: {GOLDEN_PATH}"
    assert GOLDEN_PATH.name == "devmate.jsonl"


def test_ten_cases_load() -> None:
    cases = _load_cases()
    assert len(cases) == 10
    ids = [c["id"] for c in cases]
    assert len(set(ids)) == 10
    assert ids[0] == "devmate-ask-001"
    assert ids[-1] == "devmate-ask-010"


def test_schema_validates_clean() -> None:
    errors = validate_cases()
    assert errors == [], f"schema errors: {errors}"


def test_cases_are_jsonl_objects_not_markdown() -> None:
    raw = GOLDEN_PATH.read_text(encoding="utf-8").strip().splitlines()
    assert len(raw) == 10
    for line in raw:
        obj = json.loads(line)
        assert isinstance(obj, dict)
        assert obj["expected_properties"]["must_be_grounded_in_context"] is True
        assert obj["expected_properties"]["must_cite_sources"] is True


def test_expected_sources_point_at_devmate_package() -> None:
    for case in _load_cases():
        sources = case["metadata"]["expected_source_files"]
        assert any("devmate" in s for s in sources)
        # At least one path should be under the src tree or package root
        assert any("devmate" in s and (s.endswith(".py") or s.endswith(".toml")) for s in sources)
