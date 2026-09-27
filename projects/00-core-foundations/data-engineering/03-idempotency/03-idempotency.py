"""
Data Engineering — 03: Idempotency
===================================
Topics: idempotent writes, stable keys, upsert pattern, the run-twice test.

Why this matters:
    Idempotency is the roadmap's exit test: running twice must not
    duplicate data. This exercise builds an upsert store and proves it.

Run:      python 03-idempotency.py
Verify:   python 03-idempotency.py --verify
"""

from __future__ import annotations

import sys


class UpsertStore:
    """A minimal keyed store with idempotent upsert semantics."""

    def __init__(self) -> None:
        self._rows: dict[str, dict] = {}

    def upsert(self, key: str, values: dict) -> None:
        self._rows[key] = values  # insert if absent, replace if present

    def read_all(self) -> list[dict]:
        return [self._rows[k] for k in sorted(self._rows)]


def run_pipeline(store: UpsertStore, rows: list[dict]) -> None:
    """The load stage: idempotent upsert by passage_id."""
    for row in rows:
        store.upsert(row["passage_id"], row)


def main() -> None:
    rows = [
        {
            "passage_id": "b1:p1:0",
            "book_id": "b1",
            "page": 1,
            "text": "نص الصفحة الأولى",
        },
        {
            "passage_id": "b1:p2:0",
            "book_id": "b1",
            "page": 2,
            "text": "نص الصفحة الثانية",
        },
    ]

    store = UpsertStore()
    run_pipeline(store, rows)  # first run
    first = store.read_all()
    run_pipeline(store, rows)  # second run
    second = store.read_all()

    assert first == second, "idempotent: identical state after re-run"
    assert len(second) == 2, "no duplicates"

    # A changed row updates in place, does not duplicate.
    changed = [{"passage_id": "b1:p1:0", "book_id": "b1", "page": 1, "text": "نص محدث"}]
    run_pipeline(store, changed)
    after = store.read_all()
    assert len(after) == 2, "update in place, no new row"
    assert after[0]["text"] == "نص محدث"

    print(f"rows after first run: {len(first)}")
    print(f"rows after second run: {len(second)} (identical, no duplicates)")
    print("update in place: 2 rows, text replaced")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
