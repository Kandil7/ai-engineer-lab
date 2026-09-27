"""
PostgreSQL — 02: Indexes and Queries
====================================
Topics: the index lookup, composite order, and the sequential-scan signal.

Why this matters:
    An index is the database's shortcut to the rows a query needs. This
    exercise models the index lookup and the composite-order rule.

Run:      python 02-indexes-queries.py
Verify:   python 02-indexes-queries.py --verify
"""

from __future__ import annotations

import sys


class Index:
    """A sorted index mapping a key to row ids."""

    def __init__(self, entries: list[tuple]) -> None:
        self.entries = sorted(entries)

    def lookup(self, key) -> list[int]:
        return [row_id for k, row_id in self.entries if k == key]


def composite_matches(columns: tuple, query_cols: tuple) -> bool:
    """A composite index serves a query when the query's leading columns
    match the index's leading columns in order."""
    return query_cols == columns[: len(query_cols)]


def main() -> None:
    # An index maps session_id to message rows.
    idx = Index([("s1", 1), ("s1", 2), ("s2", 3)])
    assert idx.lookup("s1") == [1, 2], "index lookup returns the rows"
    assert idx.lookup("s3") == [], "no rows for a missing key"

    # Composite order: (session_id, created_at) serves a session filter.
    composite = ("session_id", "created_at")
    assert composite_matches(composite, ("session_id",)), "leading column matches"
    assert composite_matches(composite, ("session_id", "created_at"))
    assert not composite_matches(composite, ("created_at",)), (
        "a query on the second column alone cannot use the index"
    )

    print("index lookup returns the rows for a key")
    print("composite index serves the query's leading columns in order")
    print("a query on the second column alone misses the index")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
