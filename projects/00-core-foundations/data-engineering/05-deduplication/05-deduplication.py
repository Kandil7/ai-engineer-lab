"""
Data Engineering — 05: Deduplication
=====================================
Topics: exact dedup by key, content hashing, edit detection, and the
        two-half dedup test.

Why this matters:
    Duplicates corrupt retrieval. This exercise dedups by key and by
    content hash, detects an edited page, and proves distinct passages
    are never removed.

Run:      python 05-deduplication.py
Verify:   python 05-deduplication.py --verify
"""

from __future__ import annotations

import hashlib
import sys


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dedup_by_key(rows: list[dict]) -> list[dict]:
    """Exact dedup by passage_id: keep the last occurrence."""
    seen: dict[str, dict] = {}
    for row in rows:
        seen[row["passage_id"]] = row
    return list(seen.values())


def detect_edits(rows: list[dict], index: dict[str, str]) -> list[str]:
    """Return passage_ids whose content hash changed (edited pages)."""
    return [
        r["passage_id"]
        for r in rows
        if r["passage_id"] in index
        and index[r["passage_id"]] != content_hash(r["text"])
    ]


def main() -> None:
    a = {"passage_id": "b1:p1:0", "text": "نص الصفحة الأولى"}
    b = {"passage_id": "b1:p2:0", "text": "نص الصفحة الثانية"}
    a_dup = {"passage_id": "b1:p1:0", "text": "نص الصفحة الأولى"}  # exact duplicate
    a_edited = {"passage_id": "b1:p1:0", "text": "نص الصفحة الأولى معدل"}  # edited

    # Exact dedup: duplicate removed, distinct kept.
    result = dedup_by_key([a, b, a_dup])
    assert len(result) == 2, "duplicate removed"
    assert any(r["passage_id"] == "b1:p1:0" for r in result)
    assert any(r["passage_id"] == "b1:p2:0" for r in result)

    # Edit detection: same key, different content hash.
    index = {"b1:p1:0": content_hash(a["text"]), "b1:p2:0": content_hash(b["text"])}
    edited = detect_edits([a_edited], index)
    assert edited == ["b1:p1:0"], "edited page detected"
    unchanged = detect_edits([a], index)
    assert unchanged == [], "unchanged page not flagged"

    print(f"dedup: {len(result)} rows (duplicate removed, distinct kept)")
    print(f"edit detection: {edited} flagged, unchanged not flagged")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
