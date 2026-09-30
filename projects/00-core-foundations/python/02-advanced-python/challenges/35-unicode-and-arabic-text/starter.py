"""
Challenge 35: Unicode and Arabic Text — Starter Code
=====================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def normalize_record(record: dict) -> dict:
    """Return a normalized copy: page -> ASCII int, text cleaned, search_key folded."""
    raise NotImplementedError


def find_duplicates(records: list[dict]) -> list[list[dict]]:
    """Group records whose search_key collides. O(n) comparisons, not O(n^2)."""
    raise NotImplementedError


def import_corpus(
    lines: Iterable[str],
    batch_size: int,
    on_error: Callable[[int, str], None],
) -> dict:
    """Stream JSONL in batches; report broken records via on_error(line_no, msg)."""
    raise NotImplementedError
