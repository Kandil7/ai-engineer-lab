"""Offline validation for DevMate prompt golden cases (no API, no network)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# File lives at <repo>/projects/04-ai-engineering/devmate/src/devmate/eval/
# Repo root is six parents up from this file.
REPO_ROOT = Path(__file__).resolve().parents[6]
GOLDEN_PATH = REPO_ROOT / "evaluations" / "prompts" / "golden-cases" / "devmate.jsonl"

REQUIRED_TOP_LEVEL = {
    "id",
    "prompt_id",
    "prompt_version",
    "question",
    "category",
    "expected_context",
    "expected_answer",
    "expected_properties",
    "metadata",
}

ALLOWED_PROPERTY_KEYS = {
    "must_be_grounded_in_context",
    "must_cite_sources",
    "must_not_invent_api",
    "min_context_sources",
    "forbidden_phrases",
    "expected_tool_names",
}


def _load_cases(path: Path = GOLDEN_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Golden cases file missing: {path}")
    cases: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                cases.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return cases


def _validate_case_structure(idx: int, case: dict[str, Any], errors: list[str]) -> None:
    label = case.get("id", f"case[{idx}]")
    missing = REQUIRED_TOP_LEVEL - case.keys()
    if missing:
        errors.append(f"{label}: missing keys {sorted(missing)}")

    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id.startswith("devmate-ask-"):
        errors.append(f"{label}: id must start with 'devmate-ask-'")

    prompt_id = case.get("prompt_id")
    if prompt_id != "devmate.rag.answer":
        errors.append(f"{label}: prompt_id must be 'devmate.rag.answer', got {prompt_id!r}")

    expected_context = case.get("expected_context")
    if not isinstance(expected_context, list) or not expected_context:
        errors.append(f"{label}: expected_context must be a non-empty list")
    elif not all(isinstance(x, str) and x for x in expected_context):
        errors.append(f"{label}: expected_context items must be non-empty strings")

    expected_answer = case.get("expected_answer")
    if not isinstance(expected_answer, str) or len(expected_answer) < 20:
        errors.append(f"{label}: expected_answer must be a string of at least 20 chars")


def _validate_properties(label: str, props: Any, errors: list[str]) -> None:
    if not isinstance(props, dict) or not props:
        errors.append(f"{label}: expected_properties must be a non-empty object")
        return
    unknown = {k for k in (set(props) - ALLOWED_PROPERTY_KEYS) if not k.startswith("must_")}
    if unknown:
        errors.append(f"{label}: unknown expected_properties keys {sorted(unknown)}")
    if props.get("must_be_grounded_in_context") is not True:
        errors.append(f"{label}: must_be_grounded_in_context must be true")
    if props.get("must_cite_sources") is not True:
        errors.append(f"{label}: must_cite_sources must be true")
    min_ctx = props.get("min_context_sources", 1)
    if not isinstance(min_ctx, int) or min_ctx < 1:
        errors.append(f"{label}: min_context_sources must be int >= 1")
    forbidden = props.get("forbidden_phrases", [])
    if forbidden and not all(isinstance(x, str) and x for x in forbidden):
        errors.append(f"{label}: forbidden_phrases must be non-empty strings")


def _validate_metadata(label: str, metadata: Any, errors: list[str]) -> None:
    if not isinstance(metadata, dict) or "expected_source_files" not in metadata:
        errors.append(f"{label}: metadata.expected_source_files is required")
        return
    sources = metadata["expected_source_files"]
    if not isinstance(sources, list) or not sources:
        errors.append(f"{label}: metadata.expected_source_files must be non-empty list")
    elif not all(isinstance(x, str) and "devmate" in x for x in sources):
        errors.append(f"{label}: metadata.expected_source_files must reference devmate paths")


def validate_cases(cases: list[dict[str, Any]] | None = None) -> list[str]:
    """Return a list of validation errors. Empty list means the set is valid."""
    if cases is None:
        cases = _load_cases()

    errors: list[str] = []
    if len(cases) != 10:
        errors.append(f"expected 10 golden cases, found {len(cases)}")

    seen_ids: set[str] = set()
    for idx, case in enumerate(cases):
        label = case.get("id", f"case[{idx}]")
        _validate_case_structure(idx, case, errors)
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in seen_ids:
                errors.append(f"{label}: duplicate id")
            else:
                seen_ids.add(case_id)
        _validate_properties(label, case.get("expected_properties"), errors)
        _validate_metadata(label, case.get("metadata"), errors)

    return errors


def main() -> int:
    cases = _load_cases()
    errors = validate_cases(cases)
    if errors:
        sys.stderr.write(f"FAIL: {len(errors)} validation error(s)\n")
        for err in errors:
            sys.stderr.write(f"  - {err}\n")
        return 1
    sys.stdout.write(f"OK: {len(cases)} DevMate prompt golden cases validated\n")
    sys.stdout.write(f"Path: {GOLDEN_PATH}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
