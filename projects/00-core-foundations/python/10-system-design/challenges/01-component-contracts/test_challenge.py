"""
Challenge 01: Component Contracts — Tests
==========================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 10-system-design/challenges/01-component-contracts/test_challenge.py -q

Guards use comparison counting and mutation checks — never wall-clock time.
"""

from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402

V1 = {
    "required": {
        "id": "str, unique",
        "book": "str, canonical title",
        "page": "int, 1-based",
        "text": "str, verbatim",
    }
}

V2 = {
    "required": {
        **V1["required"],
        "edition": "str, edition label",
    }
}

V2_OPTIONAL = {
    "required": {
        **V2["required"],
        "migrated_at": "ts, optional, backfill marker",
    }
}


class CountingStr(str):
    __slots__ = ("counter",)

    def __new__(cls, val: str, counter: list[int]) -> "CountingStr":
        obj = super().__new__(cls, val)
        obj.counter = counter
        return obj

    def __eq__(self, other: object) -> bool:
        self.counter[0] += 1
        return super().__eq__(other)

    def __hash__(self) -> int:
        return super().__hash__()


class TestClassifyChange:
    """Bronze: compatible vs needs-migration vs breaking."""

    def test_add_required(self) -> None:
        assert mod.classify_change(V1, V2) == "needs-migration"

    def test_add_optional(self) -> None:
        assert mod.classify_change(V2, V2_OPTIONAL) == "compatible"

    def test_remove_field(self) -> None:
        broken = {"required": {"id": "str, unique"}}
        assert mod.classify_change(V2, broken) == "breaking"

    def test_change_semantic(self) -> None:
        changed = copy.deepcopy(V2)
        changed["required"]["page"] = "int, PDF page"  # semantic drift
        assert mod.classify_change(V2, changed) == "breaking"

    def test_identical(self) -> None:
        assert mod.classify_change(V2, copy.deepcopy(V2)) == "compatible"


class TestValidatePayload:
    """Silver: completeness + immutability."""

    GOOD = {"id": "a", "book": "bukhari", "page": 3, "text": "نص", "source_ref": "bukhari/p3"}

    def test_valid(self) -> None:
        assert mod.validate_payload(self.GOOD, V1) == []

    def test_reports_all_violations(self) -> None:
        bad = {"id": "a", "book": "bukhari", "page": 3, "text": "   ", "source_ref": "wrong"}
        problems = mod.validate_payload(bad, V1)
        assert len(problems) >= 2, "fail-fast validation hides violations; collect them all"
        assert any("text" in p for p in problems)
        assert any("source_ref" in p for p in problems)

    def test_three_rules_broken_at_once(self) -> None:
        bad = {"id": "a", "book": "bukhari", "page": 3, "text": "   ", "source_ref": "wrong"}
        problems = mod.validate_payload(bad, V2)  # edition missing too
        assert len(problems) >= 3
        assert any("edition" in p for p in problems)

    def test_names_missing_field(self) -> None:
        problems = mod.validate_payload({"text": "t"}, V1)
        assert any("id" in p and "missing" in p for p in problems)

    def test_payload_not_mutated(self) -> None:
        payload = {
            "id": "a",
            "book": "bukhari",
            "page": 3,
            "text": "  نص  ",
            "source_ref": "bukhari/p3",
        }
        before = copy.deepcopy(payload)
        mod.validate_payload(payload, V1)
        assert payload == before, "a validator must not normalize the payload in place"

    def test_empty_inputs(self) -> None:
        assert mod.validate_payload({}, {"required": {}}) != []  # empty text still fails


class TestPlanAndSimulate:
    """Gold: rolling-upgrade semantics + comparison budget."""

    OLD_REC = {"id": "a", "book": "b", "page": 1, "text": "t"}
    NEW_REC = {"id": "a", "book": "b", "page": 1, "text": "t", "edition": "d"}

    def test_plan_for_required_field(self) -> None:
        assert mod.plan_migration(V1, V2) == [
            "emit-default",
            "consumers-tolerate",
            "backfill",
            "require",
        ]

    def test_plan_empty_for_compatible(self) -> None:
        assert mod.plan_migration(V2, V2_OPTIONAL) == []

    def test_plan_empty_for_breaking(self) -> None:
        assert mod.plan_migration(V2, {"required": {"id": "x"}}) == []

    def test_full_plan_is_safe(self) -> None:
        plan = mod.plan_migration(V1, V2)
        assert mod.simulate_migration(plan, self.OLD_REC, self.NEW_REC) is True

    def test_one_step_plan_rejected(self) -> None:
        """The naive 'just require it' plan kills old producers on day one."""
        assert mod.simulate_migration(["require"], self.OLD_REC, self.NEW_REC) is False

    def test_plan_without_require_rejected(self) -> None:
        plan = ["emit-default", "consumers-tolerate", "backfill"]
        assert mod.simulate_migration(plan, self.OLD_REC, self.NEW_REC) is False

    def test_empty_plan_rejected(self) -> None:
        assert mod.simulate_migration([], self.OLD_REC, self.NEW_REC) is False

    def test_comparison_budget(self) -> None:
        """Set-based diff is O(n); pairwise field comparison is O(n^2)."""
        n = 1000
        counter = [0]
        old = {"required": {CountingStr(f"f{i}", counter): "str" for i in range(n)}}
        new = {"required": {CountingStr(f"f{i}", counter): "str" for i in range(n - 1)}}
        mod.classify_change(old, new)
        assert counter[0] <= 6 * n, (
            f"comparisons {counter[0]} exceed budget {6 * n}; "
            "pairwise old x new field comparison is O(n^2) and must fail this guard"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
