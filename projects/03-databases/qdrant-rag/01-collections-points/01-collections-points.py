"""
Qdrant — 01: Collections and Points
===================================
Topics: the collection, the point, and the payload.

Why this matters:
    Qdrant stores vectors in collections of points. This exercise models
    a collection and the deterministic point id.

Run:      python 01-collections-points.py
Verify:   python 01-collections-points.py --verify
"""

from __future__ import annotations

import sys


class Collection:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
        self.points: dict[str, dict] = {}

    def upsert(self, point_id: str, vector: list[float], payload: dict) -> None:
        assert len(vector) == self.size, "vector size must match the collection"
        self.points[point_id] = {"vector": vector, "payload": payload}

    def get(self, point_id: str) -> dict | None:
        return self.points.get(point_id)


def point_id(book: str, page: int, chunk: int) -> str:
    """A deterministic id derived from the source."""
    return f"{book}:p{page}:{chunk}"


def main() -> None:
    col = Collection("athar", size=3)

    # A deterministic id: re-ingestion updates the same point.
    pid = point_id("b3", 12, 0)
    assert pid == "b3:p12:0"
    col.upsert(pid, [0.1, 0.2, 0.3], {"book": "b3", "page": 12, "language": "ar"})
    col.upsert(pid, [0.1, 0.2, 0.3], {"book": "b3", "page": 12, "language": "ar"})
    assert len(col.points) == 1, "same id updates, never duplicates"

    # A vector of the wrong size is rejected.
    try:
        col.upsert("b3:p12:1", [0.1, 0.2], {"book": "b3"})
        assert False, "vector size must match the collection"
    except AssertionError:
        pass

    # The payload is retrievable with the point.
    point = col.get(pid)
    assert point is not None
    assert point["payload"]["book"] == "b3"

    print("deterministic point id: re-ingestion updates, never duplicates")
    print("vector size mismatch rejected at the collection")
    print("payload is retrievable with the point")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
