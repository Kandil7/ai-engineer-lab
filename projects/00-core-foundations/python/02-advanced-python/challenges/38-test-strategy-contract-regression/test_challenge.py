"""
Challenge 38: Test Strategy — Tests
====================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/38-test-strategy-contract-regression/test_challenge.py -q

Guards use comparison counting and call counting — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingStr(str):
    """String that counts every equality comparison."""

    __slots__ = ("counter",)

    def __new__(cls, val: str, counter: list[int]) -> "CountingStr":
        obj = super().__new__(cls, val)
        obj.counter = counter
        return obj

    def __eq__(self, other: object) -> bool:
        self.counter[0] += 1
        return super().__eq__(other)

    def __ne__(self, other: object) -> bool:
        self.counter[0] += 1
        return super().__ne__(other)

    def __hash__(self) -> int:
        return super().__hash__()


def _good_parser(line: str) -> dict:
    obj = json.loads(line)
    if not obj.get("id"):
        raise ValueError("empty id")
    return obj


def _broken_parser(line: str) -> dict:
    """Accepts everything — the mutation the Gold guard must catch."""
    return json.loads(line) if line.strip().startswith("{") else {"id": line}


class TestProvenanceViolations:
    """Bronze: data invariants — no loss, no phantom, provenance intact."""

    def test_clean_run(self) -> None:
        before = [
            {"id": "a", "book": "bukhari", "page": 1, "text": "نص", "source_ref": "bukhari/p1"}
        ]
        after = {"a": before[0]}
        assert mod.provenance_violations(before, after) == []

    def test_lost_record(self) -> None:
        before = [{"id": "x", "book": "b", "page": 1, "text": "t", "source_ref": "b/p1"}]
        problems = mod.provenance_violations(before, {})
        assert any("lost" in p and "x" in p for p in problems)

    def test_phantom_record(self) -> None:
        after = {"y": {"id": "y", "book": "b", "page": 1, "text": "t", "source_ref": "b/p1"}}
        problems = mod.provenance_violations([], after)
        assert any("phantom" in p and "y" in p for p in problems)

    def test_empty_text(self) -> None:
        rec = {"id": "z", "book": "b", "page": 1, "text": "   ", "source_ref": "b/p1"}
        problems = mod.provenance_violations([rec], {"z": rec})
        assert any("empty text" in p for p in problems)

    def test_broken_source_ref(self) -> None:
        rec = {"id": "w", "book": "bukhari", "page": 3, "text": "t", "source_ref": "wrong"}
        problems = mod.provenance_violations([rec], {"w": rec})
        assert any("source_ref" in p for p in problems)

    def test_empty_inputs(self) -> None:
        assert mod.provenance_violations([], {}) == []


class TestIdempotentIngest:
    """Silver: double-ingest produces zero duplicates; comparison budget."""

    def test_first_run(self) -> None:
        lines = [json.dumps({"id": str(i), "book": "b", "page": i, "text": "t"}) for i in range(3)]
        store: dict = {}
        assert mod.idempotent_ingest(lines, store) == {
            "imported": 3,
            "skipped_duplicates": 0,
        }

    def test_second_run_skips_all(self) -> None:
        lines = [json.dumps({"id": str(i), "book": "b", "page": i, "text": "t"}) for i in range(3)]
        store: dict = {}
        mod.idempotent_ingest(lines, store)
        assert mod.idempotent_ingest(lines, store) == {
            "imported": 0,
            "skipped_duplicates": 3,
        }
        assert len(store) == 3

    def test_empty(self) -> None:
        assert mod.idempotent_ingest([], {}) == {
            "imported": 0,
            "skipped_duplicates": 0,
        }

    def test_inline_duplicates(self) -> None:
        lines = [json.dumps({"id": "a", "book": "b", "page": 1, "text": "t"})] * 4
        store: dict = {}
        out = mod.idempotent_ingest(lines, store)
        assert out == {"imported": 1, "skipped_duplicates": 3}

    def test_comparison_budget(self) -> None:
        """Dict-keyed insert stays ~n; list-scan dedupe is n^2 and fails."""
        n = 2000
        counter = [0]
        lines = [
            json.dumps({"id": CountingStr(f"k{i}", counter), "book": "b", "page": i, "text": "t"})
            for i in range(n)
        ]
        store: dict = {}
        mod.idempotent_ingest(lines, store)
        mod.idempotent_ingest(lines, store)  # second run is the adversarial case
        assert counter[0] <= 3 * n, (
            f"comparisons {counter[0]} exceed budget {3 * n}; "
            "list-scan dedupe is O(n^2) and must fail this guard"
        )


class TestRegressionGate:
    """Gold: mutation detection, call budget, dedupe."""

    def _cases(self) -> list[tuple[str, str, str]]:
        cases = []
        for i in range(10):
            cases.append((f"KF-REJ-{i}", '{"id": ""}', "reject"))
        for i in range(10):
            cases.append((f"KF-ACC-{i}", json.dumps({"id": f"a{i}"}), "accept"))
        return cases

    def test_correct_parser_clean(self) -> None:
        assert mod.regression_suite_runner(self._cases(), _good_parser) == []

    def test_broken_parser_detected(self) -> None:
        regressed = mod.regression_suite_runner(self._cases(), _broken_parser)
        assert regressed == sorted(f"KF-REJ-{i}" for i in range(10))

    def test_parser_called_once_per_case(self) -> None:
        calls = {"n": 0}

        def spy(line: str) -> dict:
            calls["n"] += 1
            return _good_parser(line)

        cases = self._cases()
        mod.regression_suite_runner(cases, spy)
        assert calls["n"] == len(cases), (
            f"parser called {calls['n']} times for {len(cases)} cases; "
            "a double-parse implementation fails this budget"
        )

    def test_regressed_id_reported_once(self) -> None:
        cases = [("KF-DUP", '{"id": ""}', "reject")] * 3
        regressed = mod.regression_suite_runner(cases, _broken_parser)
        assert regressed == ["KF-DUP"]

    def test_empty_cases(self) -> None:
        assert mod.regression_suite_runner([], _good_parser) == []

    def test_accept_case_that_throws_is_regressed(self) -> None:
        def flaky(line: str) -> dict:
            raise ValueError("unexpected")

        assert mod.regression_suite_runner([("KF-1", '{"id": "a"}', "accept")], flaky) == ["KF-1"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
