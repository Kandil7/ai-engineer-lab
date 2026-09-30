"""Load DevMate evaluation datasets from the workspace repo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from devmate.eval.validate_prompt_golden import REPO_ROOT

RAG_GOLDEN_PATH = REPO_ROOT / "evaluations" / "rag" / "datasets" / "devmate-golden.jsonl"
PROMPT_GOLDEN_PATH = REPO_ROOT / "evaluations" / "prompts" / "golden-cases" / "devmate.jsonl"
REPORTS_DIR = REPO_ROOT / "evaluations" / "rag" / "reports"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset missing: {path}")
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def load_rag_golden(path: Path = RAG_GOLDEN_PATH) -> list[dict[str, Any]]:
    rows = load_jsonl(path)
    required = {"id", "question", "expected_context", "expected_answer"}
    for idx, row in enumerate(rows):
        missing = required - row.keys()
        if missing:
            raise ValueError(f"rag golden case[{idx}] missing keys {sorted(missing)}")
    return rows


def load_prompt_golden(path: Path = PROMPT_GOLDEN_PATH) -> list[dict[str, Any]]:
    rows = load_jsonl(path)
    required = {"id", "question", "expected_answer", "expected_properties"}
    for idx, row in enumerate(rows):
        missing = required - row.keys()
        if missing:
            raise ValueError(f"prompt golden case[{idx}] missing keys {sorted(missing)}")
    return rows


def write_report(filename: str, body: str, reports_dir: Path = REPORTS_DIR) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / filename
    path.write_text(body, encoding="utf-8")
    return path
