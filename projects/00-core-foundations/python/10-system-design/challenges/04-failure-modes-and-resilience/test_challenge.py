"""
Challenge 04: Failure Modes and Resilience — Tests
===================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 10-system-design/challenges/04-failure-modes-and-resilience/test_challenge.py -q

Guards use call counting — never wall-clock time. The clock is a fake object.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0
        self.advances: list[float] = []

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt
        self.advances.append(dt)


CTX = {
    "staleness": 0,
    "work_started": False,
    "acknowledged": False,
    "transient_types": (TimeoutError, ConnectionError),
}


class TestClassifyFailure:
    """Bronze: the failure taxonomy."""

    def test_transient(self) -> None:
        assert mod.classify_failure(TimeoutError("down"), CTX) == "transient"

    def test_transient_connection(self) -> None:
        assert mod.classify_failure(ConnectionError("net"), CTX) == "transient"

    def test_permanent(self) -> None:
        assert mod.classify_failure(ValueError("malformed"), CTX) == "permanent"

    def test_permanent_when_no_error(self) -> None:
        assert mod.classify_failure(None, CTX) == "permanent"

    def test_silent(self) -> None:
        ctx = dict(CTX, staleness=3)
        assert mod.classify_failure(None, ctx) == "silent"

    def test_partial(self) -> None:
        ctx = dict(CTX, work_started=True, acknowledged=False)
        assert mod.classify_failure(None, ctx) == "partial"

    def test_acknowledged_not_partial(self) -> None:
        ctx = dict(CTX, work_started=True, acknowledged=True)
        assert mod.classify_failure(None, ctx) == "permanent"


class TestBulkhead:
    """Silver: saturation rejection, fail-fast timeouts, peak cap."""

    def test_saturation_rejects(self) -> None:
        tasks = [
            {"id": "a", "arrival": 0.0, "duration": 5.0},
            {"id": "b", "arrival": 0.0, "duration": 5.0},
            {"id": "c", "arrival": 0.0, "duration": 5.0},
        ]
        calls: list[str] = []
        clock = FakeClock()
        out = mod.run_with_bulkhead(
            tasks, lambda t: calls.append(t["id"]), {"capacity": 2, "timeout": 10.0}, clock
        )
        assert out["served"] == 2 and out["rejected"] == 1
        assert out["handler_calls"] == 2, "a rejected task must not invoke the handler"
        assert sorted(calls) == ["a", "b"]

    def test_timeout_fails_fast(self) -> None:
        tasks = [{"id": "slow", "arrival": 0.0, "duration": 20.0}]
        calls: list[str] = []
        out = mod.run_with_bulkhead(
            tasks, lambda t: calls.append(t["id"]), {"capacity": 2, "timeout": 10.0}, FakeClock()
        )
        assert out["timed_out"] == 1 and out["handler_calls"] == 0
        assert calls == [], "a task that cannot finish must not be started"

    def test_staggered_both_served(self) -> None:
        tasks = [
            {"id": "a", "arrival": 0.0, "duration": 5.0},
            {"id": "b", "arrival": 3.0, "duration": 5.0},
        ]
        out = mod.run_with_bulkhead(
            tasks, lambda t: None, {"capacity": 2, "timeout": 10.0}, FakeClock()
        )
        assert out["served"] == 2 and out["peak_in_flight"] <= 2

    def test_slot_release_allows_later_task(self) -> None:
        tasks = [
            {"id": "a", "arrival": 0.0, "duration": 5.0},
            {"id": "b", "arrival": 0.0, "duration": 5.0},
            {"id": "c", "arrival": 10.0, "duration": 5.0},  # after a and b finish
        ]
        out = mod.run_with_bulkhead(
            tasks, lambda t: None, {"capacity": 2, "timeout": 10.0}, FakeClock()
        )
        assert out["served"] == 3 and out["rejected"] == 0

    def test_peak_never_exceeds_capacity(self) -> None:
        tasks = [{"id": f"t{i}", "arrival": 0.0, "duration": 1.0} for i in range(50)]
        out = mod.run_with_bulkhead(
            tasks, lambda t: None, {"capacity": 4, "timeout": 10.0}, FakeClock()
        )
        assert out["peak_in_flight"] <= 4
        assert out["rejected"] == 46

    def test_clock_advanced_once_per_served(self) -> None:
        tasks = [
            {"id": "a", "arrival": 0.0, "duration": 2.0},
            {"id": "b", "arrival": 0.0, "duration": 3.0},
        ]
        clock = FakeClock()
        out = mod.run_with_bulkhead(tasks, lambda t: None, {"capacity": 2, "timeout": 10.0}, clock)
        assert out["served"] == 2
        assert clock.advances == [2.0, 3.0]


class TestDegradationLadder:
    """Gold: total state matrix + fabrication invariant + call budget."""

    def _factory(self):
        calls = {"n": 0, "kinds": []}

        def factory(kind: str) -> dict:
            calls["n"] += 1
            calls["kinds"].append(kind)
            return {"from": kind}

        return factory, calls

    def test_full_rung(self) -> None:
        factory, _ = self._factory()
        out = mod.degradation_ladder({"index": "current"}, factory)
        assert out["mode"] == "full" and out["data"] == {"from": "index"}

    def test_stale_rung(self) -> None:
        factory, _ = self._factory()
        out = mod.degradation_ladder({"index": "stale"}, factory)
        assert out["mode"] == "stale-warning"

    def test_fallback_rung(self) -> None:
        factory, calls = self._factory()
        out = mod.degradation_ladder({"index": "down", "source": True}, factory)
        assert out["mode"] == "keyword-fallback" and calls["kinds"] == ["source"]

    def test_cached_rung(self) -> None:
        factory, calls = self._factory()
        out = mod.degradation_ladder({"index": "down", "source": False, "cache": True}, factory)
        assert out["mode"] == "cached-only" and calls["kinds"] == ["cache"]

    def test_never_fabricate(self) -> None:
        """The integrity rule: an honest refusal beats a made-up answer."""
        factory, calls = self._factory()
        out = mod.degradation_ladder({"index": "down", "source": False, "cache": False}, factory)
        assert out == {"mode": "unavailable", "data": None}
        assert calls["n"] == 0, "no source available means no factory call at all"

    def test_factory_called_at_most_once(self) -> None:
        factory, calls = self._factory()
        mod.degradation_ladder({"index": "current"}, factory)
        assert calls["n"] == 1, "a try-everything fallback chain violates the call budget"

    def test_full_state_matrix(self) -> None:
        """All 12 states must map to the documented rung."""
        expected = {
            ("current", True, True): "full",
            ("current", True, False): "full",
            ("current", False, True): "full",
            ("current", False, False): "full",
            ("stale", True, True): "stale-warning",
            ("stale", True, False): "stale-warning",
            ("stale", False, True): "stale-warning",
            ("stale", False, False): "stale-warning",
            ("down", True, True): "keyword-fallback",
            ("down", True, False): "keyword-fallback",
            ("down", False, True): "cached-only",
            ("down", False, False): "unavailable",
        }
        for (index, source, cache), mode in expected.items():
            factory, _ = self._factory()
            out = mod.degradation_ladder(
                {"index": index, "source": source, "cache": cache}, factory
            )
            assert out["mode"] == mode, f"state {(index, source, cache)}"
            if mode == "unavailable":
                assert out["data"] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
