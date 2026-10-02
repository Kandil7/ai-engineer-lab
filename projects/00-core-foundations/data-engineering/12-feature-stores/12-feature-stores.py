"""
Data Engineering — 12: Feature Stores
======================================
Topics: training-serving skew, registry/offline/online stores,
        point-in-time joins, feature versioning.

Why this matters:
    One feature, two code paths, produces skew. This exercise builds a
    minimal feature store — a registry, an offline store with history,
    an online store, and a point-in-time join — proving the single-source
    rule and leakage prevention with pure stdlib.

Run:      python 12-feature-stores.py
Verify:   python 12-feature-stores.py --verify
"""

from __future__ import annotations

import sys


class FeatureStore:
    def __init__(self) -> None:
        self.registry: dict[str, dict] = {}  # feature -> definition
        self.offline: dict[str, list[tuple[int, float]]] = {}  # feature -> (ts, value)
        self.online: dict[str, float] = {}  # feature -> latest value

    def register(self, name: str, entity: str, source: str) -> None:
        self.registry[name] = {"entity": entity, "source": source, "version": 1}

    def record(self, name: str, ts: int, value: float) -> None:
        self.offline.setdefault(name, []).append((ts, value))
        self.online[name] = value  # latest value wins

    def get_online(self, name: str) -> float:
        return self.online[name]

    def point_in_time(self, name: str, ts: int) -> float:
        """Latest value as of ts, never later (no future leakage)."""
        past = [v for t, v in self.offline[name] if t <= ts]
        if not past:
            raise KeyError(f"no value for {name} as of {ts}")
        return past[-1]


def main() -> None:
    fs = FeatureStore()
    fs.register("chunk_count", entity="repo", source="ingest.counts")

    # Feature history over time (offline store) and latest (online store).
    fs.record("chunk_count", 100, 100.0)
    fs.record("chunk_count", 200, 150.0)
    fs.record("chunk_count", 300, 412.0)

    # Single source: online value is the latest recorded value.
    assert fs.get_online("chunk_count") == 412.0

    # Point-in-time join: as of ts=200, the value is 150, not 412 (no leakage).
    assert fs.point_in_time("chunk_count", 200) == 150.0
    assert fs.point_in_time("chunk_count", 300) == 412.0

    # A naive "as of now" read would leak the future value into a past label.
    naive_now = fs.get_online("chunk_count")
    past_correct = fs.point_in_time("chunk_count", 200)
    assert naive_now == 412.0 and past_correct == 150.0
    assert naive_now != past_correct  # the skew the store prevents

    # No future leakage possible before the first record exists.
    try:
        fs.point_in_time("chunk_count", 50)
        raise AssertionError("expected KeyError")
    except KeyError:
        pass

    print(f"registry: {fs.registry}")
    print(f"online (serving) chunk_count = {fs.get_online('chunk_count')}")
    print(f"point-in-time at ts=200 = {fs.point_in_time('chunk_count', 200)}")
    print("naive 'as of now' would leak future value; point-in-time join prevents it")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
