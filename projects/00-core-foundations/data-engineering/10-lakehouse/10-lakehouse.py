"""
Data Engineering — 10: Lakehouse — Iceberg and Delta Lake
==========================================================
Topics: lake vs warehouse vs lakehouse, table format, snapshots and
        time travel, schema and partition evolution.

Why this matters:
    A lakehouse adds ACID and time travel to cheap open storage. This
    exercise builds a miniature table format — a manifest of snapshots
    over data files — proving atomic commits, time travel, and additive
    schema evolution with pure stdlib.

Run:      python 10-lakehouse.py
Verify:   python 10-lakehouse.py --verify
"""

from __future__ import annotations

import sys


class LakehouseTable:
    """A minimal table format: append-only snapshots over immutable files."""

    def __init__(self) -> None:
        self.snapshots: dict[str, list[dict]] = {}  # snapshot_id -> rows
        self.history: list[str] = []  # ordered snapshot ids
        self.current: str | None = None

    def commit(self, snapshot_id: str, rows: list[dict]) -> None:
        """Atomic write: a new snapshot is added, the old one is untouched."""
        self.snapshots[snapshot_id] = list(rows)  # copy, never mutate in place
        self.history.append(snapshot_id)
        self.current = snapshot_id

    def time_travel(self, snapshot_id: str) -> list[dict]:
        """Read the table as it existed at a past snapshot."""
        if snapshot_id not in self.snapshots:
            raise KeyError(f"unknown snapshot {snapshot_id}")
        return self.snapshots[snapshot_id]


def add_column(rows: list[dict], name: str, default=None) -> list[dict]:
    """Schema evolution: add a column additively without rewriting old data."""
    return [{**r, name: default} for r in rows]


def main() -> None:
    table = LakehouseTable()
    table.commit(
        "snap_v1",
        [
            {"book_id": "b1", "page": 1, "source_version": "v1", "original": "نص ١"},
            {"book_id": "b1", "page": 2, "source_version": "v1", "original": "نص ٢"},
        ],
    )
    table.commit(
        "snap_v2",
        [
            {
                "book_id": "b1",
                "page": 1,
                "source_version": "v2",
                "original": "نص ١ معدل",
            },
            {"book_id": "b1", "page": 2, "source_version": "v1", "original": "نص ٢"},
        ],
    )

    # Atomic commit: old snapshot is untouched after a new write.
    v1 = table.time_travel("snap_v1")
    v2 = table.time_travel("snap_v2")
    assert len(v1) == 2 and all(r["source_version"] == "v1" for r in v1)
    assert v2[0]["original"] == "نص ١ معدل"

    # Time travel resolves an old citation against its original state.
    assert table.time_travel("snap_v1")[0]["original"] == "نص ١"
    assert table.current == "snap_v2"

    # Unknown snapshot fails loudly, never guesses.
    try:
        table.time_travel("snap_v9")
        raise AssertionError("expected KeyError")
    except KeyError:
        pass

    # Schema evolution: add a column additively; old rows read null.
    evolved = add_column(v1, "source_hash", None)
    assert all("source_hash" in r and r["source_hash"] is None for r in evolved)

    print(f"history: {' -> '.join(table.history)}")
    print(
        f"time travel: snap_v1 resolves "
        f"({len(table.time_travel('snap_v1'))} rows, all source_version v1)"
    )
    print("additive schema evolution: old rows read the new column as null")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
