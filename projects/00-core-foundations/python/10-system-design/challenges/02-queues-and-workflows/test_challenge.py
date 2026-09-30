"""
Challenge 02: Queues and Workflows — Tests
==========================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 10-system-design/challenges/02-queues-and-workflows/test_challenge.py -q

Guards use call counting and tracemalloc — never wall-clock time. The sleep
callable is a spy; no real sleeping ever happens.
"""

from __future__ import annotations

import importlib.util
import os
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402

POLICY = {"max_attempts": 3, "base_delay": 0.25, "transient": (TimeoutError,)}


class Transient(Exception):
    pass


POLICY_T = {"max_attempts": 3, "base_delay": 0.25, "transient": (Transient,)}


class SleepSpy:
    def __init__(self) -> None:
        self.durations: list[float] = []

    def __call__(self, delay: float) -> None:
        self.durations.append(delay)


class TestInsertIfAbsent:
    """Bronze: the idempotent write primitive."""

    def test_fresh_insert(self) -> None:
        store: dict = {}
        assert mod.insert_if_absent(store, "k", 1) is True
        assert store == {"k": 1}

    def test_duplicate_insert(self) -> None:
        store = {"k": 1}
        assert mod.insert_if_absent(store, "k", 2) is False
        assert store == {"k": 1}

    def test_empty_key(self) -> None:
        store: dict = {}
        assert mod.insert_if_absent(store, "", 0) is True


class TestRunJob:
    """Silver: backoff sequence, permanent no-retry, attempt cap."""

    def test_success_first_try(self) -> None:
        spy = SleepSpy()
        calls = {"n": 0}

        def handler(job: dict) -> bool:
            calls["n"] += 1
            return True

        assert mod.run_job({"id": "a"}, handler, POLICY_T, spy) == "done"
        assert calls["n"] == 1 and spy.durations == []

    def test_backoff_sequence_exact(self) -> None:
        spy = SleepSpy()
        calls = {"n": 0}

        def handler(job: dict) -> bool:
            calls["n"] += 1
            if calls["n"] < 3:
                raise Transient("blip")
            return True

        assert mod.run_job({"id": "a"}, handler, POLICY_T, spy) == "done"
        assert spy.durations == [0.25, 0.5], (
            f"sleeps {spy.durations}; expected exponential [base, 2*base]"
        )

    def test_permanent_not_retried(self) -> None:
        spy = SleepSpy()
        calls = {"n": 0}

        def handler(job: dict) -> bool:
            calls["n"] += 1
            raise ValueError("malformed payload")

        assert mod.run_job({"id": "a"}, handler, POLICY_T, spy) == "dead_letter"
        assert calls["n"] == 1, "permanent errors must not be retried"
        assert spy.durations == []

    def test_poison_exhausts_attempts(self) -> None:
        spy = SleepSpy()
        calls = {"n": 0}

        def handler(job: dict) -> bool:
            calls["n"] += 1
            raise Transient("down")

        assert mod.run_job({"id": "a"}, handler, POLICY_T, spy) == "dead_letter"
        assert calls["n"] == POLICY_T["max_attempts"]
        assert len(spy.durations) == POLICY_T["max_attempts"] - 1

    def test_adversarial_almost_gives_up(self) -> None:
        spy = SleepSpy()
        calls = {"n": 0}

        def handler(job: dict) -> bool:
            calls["n"] += 1
            if calls["n"] < POLICY_T["max_attempts"]:
                raise Transient("flaky")
            return True

        assert mod.run_job({"id": "a"}, handler, POLICY_T, spy) == "done"
        assert calls["n"] == POLICY_T["max_attempts"]


class TestWorkerPool:
    """Gold: idempotency under redelivery, retry accounting, memory ceiling."""

    def test_redelivery_accounting(self) -> None:
        jobs = [("a", "p"), ("b", "p"), ("c", "p"), ("a", "p"), ("b", "p")]
        calls = {"n": 0}

        def handler(job_id: str, payload: str) -> bool:
            calls["n"] += 1
            return True

        out = mod.run_worker_pool(jobs, handler, POLICY_T)
        assert out == {
            "done": 3,
            "dead_lettered": 0,
            "skipped_duplicates": 2,
            "handler_calls": 3,
        }

    def test_poison_retry_accounting(self) -> None:
        calls = {"n": 0}

        def handler(job_id: str, payload: str) -> bool:
            calls["n"] += 1
            raise Transient("down")

        out = mod.run_worker_pool([("p1", "x")], handler, POLICY_T)
        assert out["dead_lettered"] == 1
        assert out["handler_calls"] == POLICY_T["max_attempts"]

    def test_mixed_jobs(self) -> None:
        calls = {"n": 0}

        def handler(job_id: str, payload: str) -> bool:
            calls["n"] += 1
            if job_id == "bad":
                raise Transient("down")
            return True

        jobs = [("ok", "x"), ("bad", "y"), ("ok", "x")]
        out = mod.run_worker_pool(jobs, handler, POLICY_T)
        assert out["done"] == 1
        assert out["dead_lettered"] == 1
        assert out["skipped_duplicates"] == 1

    def test_empty(self) -> None:
        out = mod.run_worker_pool([], lambda a, b: True, POLICY_T)
        assert out == {
            "done": 0,
            "dead_lettered": 0,
            "skipped_duplicates": 0,
            "handler_calls": 0,
        }

    def test_permanent_failure_dead_letters_fast(self) -> None:
        calls = {"n": 0}

        def handler(job_id: str, payload: str) -> bool:
            calls["n"] += 1
            raise ValueError("poison permanent")

        out = mod.run_worker_pool([("x", "y")], handler, POLICY_T)
        assert out["dead_lettered"] == 1 and out["handler_calls"] == 1

    def test_memory_ceiling_10k_jobs(self) -> None:
        """10k jobs: per-job result histories blow the 8 MB ceiling."""
        jobs = [(f"job-{i}", "payload") for i in range(10_000)]
        jobs += [(f"job-{i}", "payload") for i in range(0, 10_000, 2)]  # redeliveries

        def handler(job_id: str, payload: str) -> bool:
            return True

        tracemalloc.start()
        try:
            out = mod.run_worker_pool(jobs, handler, POLICY_T)
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert out["done"] == 10_000
        assert out["skipped_duplicates"] == 5_000
        assert peak < 8 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 8 MB ceiling; "
            "counters and a dedupe set only — no per-job result history"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
