"""
Data Engineering — 14: Data Versioning and Lineage
====================================================
Topics: content-addressed versioning, DVC-style pointers, column-level
        lineage, impact analysis, audit trails.

Why this matters:
    Unversioned data cannot be reproduced, and untracked lineage cannot be
    audited. This exercise builds a content-addressed manifest, a column-
    level lineage graph, an impact traversal, and an audit log with pure
    stdlib.

Run:      python 14-data-versioning-lineage.py
Verify:   python 14-data-versioning-lineage.py --verify
"""

from __future__ import annotations

import hashlib
import sys


def content_hash(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


class Manifest:
    """DVC-style pointer store: version -> content hash."""

    def __init__(self) -> None:
        self.pointers: dict[str, str] = {}
        self.audit: list[dict] = []

    def add(self, version: str, data: bytes, actor: str) -> None:
        h = content_hash(data)
        self.pointers[version] = h
        self.audit.append({"actor": actor, "version": version, "hash": h})

    def hash_of(self, version: str) -> str:
        if version not in self.pointers:
            raise KeyError(f"unknown version {version}")
        return self.pointers[version]


def affected(nodes: dict[str, list[str]], changed: str) -> set[str]:
    """Breadth-first impact traversal from a changed node."""
    seen: set[str] = set()
    frontier = [changed]
    while frontier:
        n = frontier.pop()
        if n in seen:
            continue
        seen.add(n)
        frontier.extend(nodes.get(n, []))
    return seen


def main() -> None:
    # Content-addressed versioning: same bytes -> same hash, changed bytes -> new hash.
    v1 = "نص ١".encode()
    v2 = "نص ١ معدل".encode()
    m = Manifest()
    m.add("v1", v1, "ingest-bot")
    m.add("v2", v2, "ingest-bot")
    assert m.hash_of("v1") == content_hash(v1)
    assert m.hash_of("v1") != m.hash_of("v2")  # a change is a new identity
    assert content_hash(v1) == content_hash("نص ١".encode())  # deterministic

    # Unknown version fails loudly, never guesses.
    try:
        m.hash_of("v9")
        raise AssertionError("expected KeyError")
    except KeyError:
        pass

    # Column-level lineage and impact analysis.
    lineage = {
        "corpus.original": ["passage.searchable"],
        "passage.searchable": ["vector_store.embedding"],
        "corpus.page": ["passage.page"],
        "vector_store.embedding": ["index.row"],
        "passage.page": ["passage.row"],
    }
    impact = affected(lineage, "corpus.original")
    assert impact == {
        "corpus.original",
        "passage.searchable",
        "vector_store.embedding",
        "index.row",
    }
    # A change to 'page' does NOT touch the embedding path.
    page_impact = affected(lineage, "corpus.page")
    assert "vector_store.embedding" not in page_impact

    # Audit trail: every version change is attributable to an actor.
    assert len(m.audit) == 2 and all("actor" in a and "hash" in a for a in m.audit)

    print(f"v1 hash: {m.hash_of('v1')[:12]}...  v2 hash: {m.hash_of('v2')[:12]}...")
    print(f"impact of corpus.original change: {sorted(impact)}")
    print(f"impact of corpus.page change: {sorted(page_impact)}")
    print(f"audit trail: {len(m.audit)} attributable records")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
