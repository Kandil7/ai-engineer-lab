"""
Data Engineering — 13: Feature Pipelines
=========================================
Topics: window aggregation, cache-aside with invalidation, LRU,
        feature versioning and lineage.

Why this matters:
    Features must be aggregated, cached, and versioned correctly or the
    online store goes stale. This exercise builds tumbling/sliding windows,
    a versioned-key cache, an LRU, and a lineage map with pure stdlib.

Run:      python 13-feature-pipelines.py
Verify:   python 13-feature-pipelines.py --verify
"""

from __future__ import annotations

import sys
from collections import OrderedDict


def tumbling_sum(events: list[tuple[int, int]], window: int) -> dict[int, int]:
    """Fixed, non-overlapping window sums, bucketed by event time."""
    buckets: dict[int, int] = {}
    for ts, value in events:
        bucket = ts // window * window
        buckets[bucket] = buckets.get(bucket, 0) + value
    return buckets


def sliding_sum(events: list[tuple[int, int]], size: int, slide: int, end: int) -> int:
    """Overlapping window: sum events in (end-size, end]."""
    return sum(v for ts, v in events if end - size < ts <= end)


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._data: OrderedDict[str, str] = OrderedDict()

    def get(self, key: str) -> str | None:
        if key not in self._data:
            return None
        self._data.move_to_end(key)  # mark recently used
        return self._data[key]

    def put(self, key: str, value: str) -> None:
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)  # evict least recently used


def main() -> None:
    events = [(10, 1), (30, 2), (70, 4), (90, 8)]

    # Tumbling windows of size 60: [0,60) and [60,120).
    assert tumbling_sum(events, 60) == {0: 3, 60: 12}

    # Sliding window: size 60 ending at 90 includes ts 70 and 90.
    assert sliding_sum(events, 60, 60, 90) == 12

    # Versioned-key cache: a version bump changes the key, invalidating old.
    model_version = "v1"
    key = f"emb:{model_version}:hello"
    cache: dict[str, str] = {}
    cache[key] = "vec-111"
    assert cache.get(key) == "vec-111"
    # Bump the model version: the old key is never looked up again.
    new_key = "emb:v2:hello"
    assert new_key not in cache

    # LRU evicts the least recently used entry.
    lru = LRUCache(2)
    lru.put("a", "1")
    lru.put("b", "2")
    lru.get("a")  # 'a' is now most recent
    lru.put("c", "3")  # evicts 'b'
    assert lru.get("a") == "1"
    assert lru.get("b") is None
    assert lru.get("c") == "3"

    # Lineage: a source change identifies which feature to recompute.
    lineage = {"chunk_count": ["ingest.counts"], "embedding": ["corpus.original"]}
    affected = [f for f, sources in lineage.items() if "ingest.counts" in sources]
    assert affected == ["chunk_count"]

    print(f"tumbling sums: {tumbling_sum(events, 60)}")
    print(f"sliding sum (ts<=90, size=60): {sliding_sum(events, 60, 60, 90)}")
    print("versioned key: v2 bump leaves the v1 cache cold")
    print(f"lru after eviction: a={lru.get('a')} b={lru.get('b')} c={lru.get('c')}")
    print(f"lineage: source change affects {affected}")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
