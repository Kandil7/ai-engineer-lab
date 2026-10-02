"""
Data Engineering — 11: Data Quality Frameworks
===============================================
Topics: six dimensions, record validation, dataset expectations,
        anomaly detection, the quality gate.

Why this matters:
    Bad data that passes silently lands in the index and then in cited
    answers. This exercise builds a record validator, a batch expectation
    suite, and a z-score volume detector, all pure stdlib, proving the
    gate fails loudly at the boundary.

Run:      python 11-data-quality.py
Verify:   python 11-data-quality.py --verify
"""

from __future__ import annotations

import sys


class Passage:
    """Record-boundary validation (a minimal Pydantic stand-in)."""

    def __init__(self, book_id: str, page: int, original: str) -> None:
        if not book_id:
            raise ValueError("book_id must not be empty")
        if page < 1:
            raise ValueError(f"page must be >= 1, got {page}")
        if not original.strip():
            raise ValueError("original must not be empty")
        self.book_id = book_id
        self.page = page
        self.original = original


def check_column_not_null(rows: list[dict], column: str) -> bool:
    return all(r.get(column) is not None for r in rows)


def check_column_unique(rows: list[dict], column: str) -> bool:
    vals = [r[column] for r in rows]
    return len(vals) == len(set(vals))


def is_anomalous(count: int, history: list[int]) -> bool:
    """Z-score volume anomaly: more than 3 std deviations from the mean."""
    if len(history) == 0:
        return False
    mean = sum(history) / len(history)
    sd = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5
    return sd > 0 and abs(count - mean) > 3 * sd


def main() -> None:
    # Record boundary: invalid records cannot be constructed.
    for bad in (
        lambda: Passage("", 1, "نص"),
        lambda: Passage("b1", 0, "نص"),
        lambda: Passage("b1", 1, "   "),
    ):
        try:
            bad()
            raise AssertionError("expected ValueError")
        except ValueError:
            pass

    rows = [
        {"passage_id": "p1", "book_id": "b1", "page": 1, "original": "نص ١"},
        {"passage_id": "p2", "book_id": "b1", "page": 2, "original": "نص ٢"},
    ]

    # Dataset expectations: non-null and unique.
    assert check_column_not_null(rows, "book_id")
    assert check_column_unique(rows, "passage_id")

    dup_rows = rows + [
        {"passage_id": "p1", "book_id": "b1", "page": 1, "original": "نص ١"}
    ]
    assert not check_column_unique(dup_rows, "passage_id")

    # Anomaly detection: a halved volume is flagged against history.
    history = [100, 98, 101, 99, 102]
    assert not is_anomalous(100, history)
    assert is_anomalous(50, history)

    print("record boundary: invalid passages cannot be constructed")
    print(
        f"batch expectations: not_null={check_column_not_null(rows, 'book_id')} "
        f"unique={check_column_unique(rows, 'passage_id')}"
    )
    print("volume anomaly: 50 against history [100..102] is flagged")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
