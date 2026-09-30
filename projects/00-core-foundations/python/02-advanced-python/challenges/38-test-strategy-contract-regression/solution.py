"""
Challenge 38: Test Strategy — Reference Solution
================================================
"""

from __future__ import annotations

import json
from collections.abc import Callable


def provenance_violations(before: list[dict], after: dict[str, dict]) -> list[str]:
    """Return invariant violations: lost, phantom, empty text, broken source_ref.

    Why this approach: set difference on ids finds loss and phantoms in
    O(n); the per-record checks name the exact offending id so the
    operator can quarantine that record instead of restarting blind.
    """
    problems: list[str] = []
    source_ids = {str(rec["id"]) for rec in before}
    stored_ids = set(after.keys())

    lost = sorted(source_ids - stored_ids)
    if lost:
        problems.append(f"lost records: {lost}")
    phantom = sorted(stored_ids - source_ids)
    if phantom:
        problems.append(f"phantom records: {phantom}")

    for rid, rec in after.items():
        if not str(rec.get("text", "")).strip():
            problems.append(f"{rid}: empty text stored")
        ref = str(rec.get("source_ref", ""))
        book = str(rec.get("book", ""))
        page = str(rec.get("page", ""))
        if not ref.startswith(book) or f"p{page}" not in ref:
            problems.append(f"{rid}: source_ref does not carry book/page")
    return problems


def idempotent_ingest(lines: list[str], store: dict) -> dict[str, int]:
    """Parse JSONL into store keyed by id, inserting only when absent.

    Why this approach: the store dict IS the dedupe index — membership
    is a hash lookup, O(1). Scanning a list of imported records compares
    ids pairwise, O(n^2) total, and blows the comparison budget at n=2000.
    """
    imported = 0
    skipped = 0
    for raw in lines:
        if not raw.strip():
            continue
        rec = json.loads(raw)
        rid = str(rec["id"])
        if rid in store:
            skipped += 1
            continue
        store[rid] = rec
        imported += 1
    return {"imported": imported, "skipped_duplicates": skipped}


def regression_suite_runner(
    cases: list[tuple[str, str, str]],
    parser: Callable[[str], dict],
) -> list[str]:
    """Run known-failure cases; return sorted regressed ids, each at most once.

    Why this approach: one parser call per case keeps the gate cheap
    enough to run on every PR; the outcome comparison is accept-vs-raise,
    which catches both directions (a reject case that passes, an accept
    case that throws). A set dedupes ids when a case is seeded twice.
    """
    regressed: set[str] = set()
    for case_id, line, expected in cases:
        try:
            parser(line)
            outcome = "accept"
        except Exception:
            outcome = "reject"
        if outcome != expected:
            regressed.add(case_id)
    return sorted(regressed)
