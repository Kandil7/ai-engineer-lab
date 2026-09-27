"""
Qdrant — 04: Metadata Filtering
================================
Topics: payload filters and tenant isolation.

Why this matters:
    Filters narrow a search and enforce correctness boundaries. This
    exercise models filters and the tenant-isolation rule.

Run:      python 04-metadata-filtering.py
Verify:   python 04-metadata-filtering.py --verify
"""

from __future__ import annotations

import sys


def apply_filter(points: list[dict], conditions: dict) -> list[dict]:
    """must conditions: every condition must hold on the payload."""
    return [
        p
        for p in points
        if all(p["payload"].get(k) == v for k, v in conditions.items())
    ]


def tenant_query(points: list[dict], tenant: str, query_terms: list[str]) -> list[dict]:
    """Every query carries the tenant filter — a missing one is a leak."""
    scoped = apply_filter(points, {"tenant": tenant})
    return [p for p in scoped if any(t in p["payload"]["text"] for t in query_terms)]


def main() -> None:
    points = [
        {"id": "a1", "payload": {"tenant": "t1", "book": "b3", "text": "القصر جائز"}},
        {"id": "a2", "payload": {"tenant": "t1", "book": "b5", "text": "الجمع جائز"}},
        {"id": "b1", "payload": {"tenant": "t2", "book": "b3", "text": "القصر جائز"}},
    ]

    # A filter narrows by payload.
    filtered = apply_filter(points, {"book": "b3"})
    assert {p["id"] for p in filtered} == {"a1", "b1"}

    # Tenant isolation: t1 never sees t2's data.
    results = tenant_query(points, "t1", ["القصر"])
    assert {p["id"] for p in results} == {"a1"}, "t2 data excluded"

    # A missing tenant filter is a data leak.
    leak = apply_filter(points, {"book": "b3"})
    assert any(p["payload"]["tenant"] == "t2" for p in leak), (
        "leak without tenant filter"
    )

    print("filters narrow points by payload")
    print("tenant isolation: t1 never sees t2's data")
    print("a query without the tenant filter leaks data")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
