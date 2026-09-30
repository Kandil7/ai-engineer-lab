"""
Challenge 03: Consistency and Staleness — Tests
================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 10-system-design/challenges/03-consistency-and-staleness/test_challenge.py -q

Guards use call counting and tracemalloc — never wall-clock time. `now` is an
injected clock value; no real time is read.
"""

from __future__ import annotations

import importlib.util
import os
import random
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class TestStalenessState:
    """Bronze: the state machine mapping."""

    def test_healthy(self) -> None:
        assert mod.staleness_state(0, 5, 100) == "healthy"

    def test_stale(self) -> None:
        assert mod.staleness_state(3, 5, 100) == "stale"

    def test_boundary_stale(self) -> None:
        assert mod.staleness_state(5, 5, 100) == "stale"

    def test_degraded(self) -> None:
        assert mod.staleness_state(50, 5, 100) == "degraded"

    def test_broken(self) -> None:
        assert mod.staleness_state(500, 5, 100) == "broken"

    def test_negative_drift_healthy(self) -> None:
        assert mod.staleness_state(-1, 5, 100) == "healthy"


class TestCacheGet:
    """Silver: TTL expiry + eviction invalidation, loader call counting."""

    def _spy_loader(self):
        calls = {"n": 0}

        def loader(key: str) -> dict:
            calls["n"] += 1
            return {"value": f"v{calls['n']}", "key": key}

        return loader, calls

    def test_fresh_hit_no_load(self) -> None:
        loader, calls = self._spy_loader()
        cache: dict = {}
        mod.cache_get(cache, "k", 100.0, 5.0, loader)
        out = mod.cache_get(cache, "k", 101.0, 5.0, loader)
        assert out["value"] == "v1" and calls["n"] == 1

    def test_expiry_refetches(self) -> None:
        loader, calls = self._spy_loader()
        cache: dict = {}
        mod.cache_get(cache, "k", 100.0, 5.0, loader)
        mod.cache_get(cache, "k", 106.0, 5.0, loader)  # past TTL
        assert calls["n"] == 2

    def test_eviction_refetches(self) -> None:
        loader, calls = self._spy_loader()
        cache: dict = {}
        mod.cache_get(cache, "k", 100.0, 5.0, loader)
        cache.pop("k")  # the event-invalidation hook
        mod.cache_get(cache, "k", 101.0, 5.0, loader)
        assert calls["n"] == 2

    def test_ttl_zero_always_loads(self) -> None:
        loader, calls = self._spy_loader()
        cache: dict = {}
        mod.cache_get(cache, "k", 100.0, 0.0, loader)
        mod.cache_get(cache, "k", 100.0, 0.0, loader)
        assert calls["n"] == 2

    def test_adversarial_boundary(self) -> None:
        loader, calls = self._spy_loader()
        cache: dict = {}
        mod.cache_get(cache, "k", 100.0, 5.0, loader)
        mod.cache_get(cache, "k", 104.999, 5.0, loader)  # just under TTL: fresh
        mod.cache_get(cache, "k", 105.0, 5.0, loader)  # exactly at TTL: expired
        assert calls["n"] == 2

    def test_timeline_call_budget(self) -> None:
        """18-access timeline must produce exactly 3 loader calls."""
        loader, calls = self._spy_loader()
        cache: dict = {}
        timeline = [
            (100.0, "get"),
            (101.0, "get"),
            (102.0, "get"),
            (103.0, "get"),
            (104.0, "get"),
            (105.0, "get"),
            (106.0, "expire"),
            (107.0, "get"),
            (108.0, "get"),
            (109.0, "get"),
            (110.0, "get"),
            (111.0, "get"),
            (112.0, "evict"),
            (113.0, "get"),
            (114.0, "get"),
            (115.0, "get"),
            (116.0, "get"),
            (117.0, "get"),
            (118.0, "get"),
        ]
        for now, action in timeline:
            if action == "evict":
                cache.pop("k", None)
                continue
            mod.cache_get(cache, "k", now, 6.0, loader)
        assert calls["n"] == 3, (
            f"loader called {calls['n']} times over the timeline; expected 3 "
            "(initial miss, post-TTL miss, post-eviction miss)"
        )


class TestApplyEvents:
    """Gold: per-key monotonic apply under shuffle + redelivery; recover."""

    def _reference(self, events: list[tuple[int, str, dict]]) -> dict:
        best: dict[str, tuple[int, dict]] = {}
        for version, key, value in events:
            if key not in best or version > best[key][0]:
                best[key] = (version, value)
        return {k: v for k, (_ver, v) in best.items()}

    def test_shuffled_events(self) -> None:
        rng = random.Random(42)
        events = [(i + 1, f"k{i % 7}", {"seq": i}) for i in range(200)]
        rng.shuffle(events)
        index: dict = {}
        stamps: dict[str, int] = {}
        out = mod.apply_events(index, events, stamps)
        assert index == self._reference(events), "a late old event must never overwrite a newer one"
        assert out["accepted"] + out["rejected"] == len(events)

    def test_duplicate_redelivery_rejected(self) -> None:
        events = [(1, "a", {"v": 1}), (1, "a", {"v": 1})]
        index: dict = {}
        stamps: dict[str, int] = {}
        out = mod.apply_events(index, events, stamps)
        assert out == {"accepted": 1, "rejected": 1}
        assert index == {"a": {"v": 1}}

    def test_late_old_value_loses(self) -> None:
        events = [(5, "a", {"v": "new"}), (3, "a", {"v": "old"})]
        index: dict = {}
        stamps: dict[str, int] = {}
        mod.apply_events(index, events, stamps)
        assert index["a"] == {"v": "new"}

    def test_empty_events(self) -> None:
        out = mod.apply_events({}, [], {})
        assert out == {"accepted": 0, "rejected": 0}

    def test_counts_exact(self) -> None:
        events = [(1, "a", {}), (2, "a", {}), (1, "a", {}), (3, "b", {})]
        out = mod.apply_events({}, events, {})
        assert out == {"accepted": 3, "rejected": 1}

    def test_recover_restores_truth(self) -> None:
        source = {f"s{i}": {"text": f"نص {i}"} for i in range(3)}
        index: dict = {"stale": {}}
        stamps: dict[str, int] = {"stale": 9}
        out = mod.recover(source, index, stamps, source_version=10)
        assert out == 3
        assert index == source
        assert all(v == 10 for v in stamps.values())

    def test_memory_ceiling_50k_events(self) -> None:
        """50k events: per-event result histories blow the 8 MB ceiling."""
        events = [(i + 1, f"k{i % 100}", {"seq": i}) for i in range(50_000)]
        index: dict = {}
        stamps: dict[str, int] = {}
        tracemalloc.start()
        try:
            out = mod.apply_events(index, events, stamps)
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert out["accepted"] + out["rejected"] == 50_000
        assert peak < 8 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 8 MB ceiling; "
            "counters and per-key stamps only — no per-event history"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
