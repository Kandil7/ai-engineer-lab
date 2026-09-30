"""
Challenge 38: Test Strategy — Starter Code
==========================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def provenance_violations(before: list[dict], after: dict[str, dict]) -> list[str]:
    """Return invariant violations: lost, phantom, empty text, broken source_ref."""
    raise NotImplementedError


def idempotent_ingest(lines: list[str], store: dict) -> dict[str, int]:
    """Parse JSONL into store keyed by id, inserting only when absent."""
    raise NotImplementedError


def regression_suite_runner(
    cases: list[tuple[str, str, str]],
    parser: Callable[[str], dict],
) -> list[str]:
    """Run known-failure cases; return sorted regressed ids, each at most once."""
    raise NotImplementedError
