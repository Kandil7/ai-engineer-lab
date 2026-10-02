"""
Data Engineering — 09: ETL vs ELT and CDC
==========================================
Topics: ETL vs ELT, transform-late, change data capture, applying
        before/after change records as upserts and deletes.

Why this matters:
    The transform's position and the capture of deltas decide whether a
    pipeline is re-runnable and whether downstream views stay in sync.
    This exercise builds a raw-layer transform and a CDC applier with pure
    stdlib, proving re-runnability and replay-idempotency.

Run:      python 09-elt-and-cdc.py
Verify:   python 09-elt-and-cdc.py --verify
"""

from __future__ import annotations

import sys


def transform_late(raw_rows: list[dict]) -> list[dict]:
    """ELT transform: re-run against the raw layer, never the source."""
    return [{**r, "title": r["title"].strip()} for r in raw_rows]


def apply_change(change: dict, index: dict) -> None:
    """Apply a CDC change record as an upsert or delete."""
    if change["op"] in ("c", "u"):
        index[change["after"]["id"]] = change["after"]
    elif change["op"] == "d":
        index.pop(change["before"]["id"], None)


def main() -> None:
    # ELT: raw layer is kept; the transform re-runs against it.
    raw = [
        {"id": 1, "title": "  النحو الواضح  "},
        {"id": 2, "title": "  فقه السنة  "},
    ]
    clean = transform_late(raw)
    assert clean[0]["title"] == "النحو الواضح"
    # A revised transform re-runs against the same raw layer.
    raw2 = [{**r, "title": "  " + r["title"] + "  "} for r in raw]
    assert transform_late(raw2)[0]["title"] == "النحو الواضح"

    # CDC: a change log with before/after images.
    changes = [
        {"op": "c", "before": None, "after": {"id": 1, "title": "الكتاب الأول"}},
        {
            "op": "u",
            "before": {"id": 1, "title": "الكتاب الأول"},
            "after": {"id": 1, "title": "الكتاب المعدل"},
        },
        {"op": "c", "before": None, "after": {"id": 2, "title": "الكتاب الثاني"}},
        {"op": "d", "before": {"id": 2, "title": "الكتاب الثاني"}, "after": None},
    ]

    index: dict[int, dict] = {}
    for ch in changes:
        apply_change(ch, index)

    assert index == {1: {"id": 1, "title": "الكتاب المعدل"}}  # 2 inserted then deleted
    assert 2 not in index

    # Replay-idempotency: replaying the log from scratch yields the same state.
    index2: dict[int, dict] = {}
    for ch in changes:
        apply_change(ch, index2)
    for ch in changes:
        apply_change(ch, index2)  # replay the whole log again
    assert index2 == index

    print("elt: transform re-runs against the raw layer, not the source")
    print(f"cdc final index keys: {sorted(index.keys())} (id 2 deleted)")
    print("cdc replay is idempotent (upsert/delete, not counts)")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
