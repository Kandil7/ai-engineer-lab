"""
Challenge 35: Unicode and Arabic Text — Tests
==============================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/35-unicode-and-arabic-text/test_challenge.py -q

Performance guards use comparison counting and tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import json
import os
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingStr(str):
    """String that counts every equality/order comparison."""

    __slots__ = ("counter",)

    def __new__(cls, val: str, counter: list[int]) -> "CountingStr":
        obj = super().__new__(cls, val)
        obj.counter = counter
        return obj

    def __eq__(self, other: object) -> bool:
        self.counter[0] += 1
        return super().__eq__(other)

    def __lt__(self, other: object) -> bool:
        self.counter[0] += 1
        return str.__lt__(self, str(other))

    def __hash__(self) -> int:
        return super().__hash__()


class TestNormalizeRecord:
    """Bronze: Arabic normalization mechanics."""

    def test_harakat_stripped(self) -> None:
        out = mod.normalize_record({"id": "a", "page": "١٢", "text": "مُحَمَّد"})
        assert out["page"] == 12
        assert out["text"] == "محمد"
        assert out["search_key"] == "محمد"

    def test_hamza_folds_in_key_only(self) -> None:
        out = mod.normalize_record({"id": "b", "page": "7", "text": "أَحْمَد"})
        assert out["page"] == 7
        assert out["search_key"] == "احمد"

    def test_ta_marbuta_folds_in_key_only(self) -> None:
        out = mod.normalize_record({"id": "c", "page": "۵", "text": "مَدْرَسَة"})
        assert out["page"] == 5
        assert out["search_key"] == "مدرسه"

    def test_presentation_form_lam_alef(self) -> None:
        out = mod.normalize_record({"id": "d", "page": 1, "text": "\ufefb\u0628"})
        assert (
            out["text"] == "لاب" or out["text"] == "لا ب" or out["text"].replace(" ", "") == "لاب"
        )

    def test_whitespace_collapsed(self) -> None:
        out = mod.normalize_record({"id": "e", "page": 2, "text": "  hello   world  "})
        assert out["text"] == "hello world"

    def test_id_preserved(self) -> None:
        out = mod.normalize_record({"id": "keep", "page": 1, "text": "x"})
        assert out["id"] == "keep"


class TestFindDuplicates:
    """Silver: O(n) grouping, comparison budget guard."""

    def test_basic_grouping(self) -> None:
        recs = [
            {"id": "1", "search_key": "محمد"},
            {"id": "2", "search_key": "محمد"},
            {"id": "3", "search_key": "علي"},
        ]
        groups = mod.find_duplicates(recs)
        assert len(groups) == 1
        assert [r["id"] for r in groups[0]] == ["1", "2"]

    def test_no_duplicates(self) -> None:
        recs = [{"id": str(i), "search_key": f"k{i}"} for i in range(5)]
        assert mod.find_duplicates(recs) == []

    def test_empty(self) -> None:
        assert mod.find_duplicates([]) == []

    def test_triple(self) -> None:
        recs = [{"id": "a", "search_key": "x"}] * 3 + [{"id": "b", "search_key": "y"}]
        groups = mod.find_duplicates(recs)
        assert len(groups) == 1 and len(groups[0]) == 3

    def test_order_by_first_appearance(self) -> None:
        recs = [
            {"id": "1", "search_key": "b"},
            {"id": "2", "search_key": "a"},
            {"id": "3", "search_key": "b"},
            {"id": "4", "search_key": "a"},
        ]
        groups = mod.find_duplicates(recs)
        assert groups[0][0]["id"] == "1"
        assert groups[1][0]["id"] == "2"

    def test_comparison_budget(self) -> None:
        """n=5000 distinct keys: dict grouping stays ~n, pairwise is n^2."""
        n = 5000
        counter = [0]
        recs = [{"id": str(i), "search_key": CountingStr(f"key{i}", counter)} for i in range(n)]
        mod.find_duplicates(recs)
        assert counter[0] <= 3 * n, (
            f"comparisons {counter[0]} exceed budget {3 * n}; "
            "pairwise key comparison is O(n^2) and must fail this guard"
        )

    def test_comparison_budget_adversarial(self) -> None:
        """All keys equal: the worst case for a pairwise comparison loop."""
        n = 2000
        counter = [0]
        recs = [{"id": str(i), "search_key": CountingStr("محمد", counter)} for i in range(n)]
        mod.find_duplicates(recs)
        assert counter[0] <= 3 * n, "all-equal keys must not explode comparisons"


class TestImportCorpus:
    """Gold: streaming import, memory ceiling, located errors."""

    def test_basic_counts(self) -> None:
        lines = [json.dumps({"id": str(i), "text": f"t{i}"}) for i in range(3)]
        out = mod.import_corpus(lines, 2, lambda n, m: None)
        assert out == {"imported": 3, "batches": 2, "errors": 0}

    def test_broken_json_located(self) -> None:
        seen: list[tuple[int, str]] = []
        lines = [
            json.dumps({"id": "1", "text": "ok"}),
            "{not json}",
            json.dumps({"id": "3", "text": "ok"}),
        ]
        out = mod.import_corpus(lines, 10, lambda n, m: seen.append((n, m)))
        assert out["errors"] == 1 and out["imported"] == 2
        assert seen[0][0] == 2

    def test_missing_field_located(self) -> None:
        seen: list[tuple[int, str]] = []
        lines = [json.dumps({"id": "1"}), json.dumps({"id": "2", "text": "x"})]
        out = mod.import_corpus(lines, 10, lambda n, m: seen.append((n, m)))
        assert out["errors"] == 1 and out["imported"] == 1
        assert seen[0][0] == 1 and "missing" in seen[0][1].lower()

    def test_empty_corpus(self) -> None:
        assert mod.import_corpus([], 5, lambda n, m: None) == {
            "imported": 0,
            "batches": 0,
            "errors": 0,
        }

    def test_adversarial_corrupt_line_123(self) -> None:
        seen: list[int] = []
        lines = []
        for i in range(1, 201):
            if i == 123:
                lines.append("{corrupt}")
            else:
                lines.append(json.dumps({"id": str(i), "text": "t"}))
        out = mod.import_corpus(lines, 50, lambda n, m: seen.append(n))
        assert out["errors"] == 1 and out["imported"] == 199
        assert seen == [123]

    def test_memory_ceiling(self) -> None:
        """200k lines must stream: materializing them blows 8 MB."""
        n = 200_000
        big = [json.dumps({"id": str(i), "text": f"نص رقم {i}"}) for i in range(n)]
        tracemalloc.start()
        try:
            out = mod.import_corpus(iter(big), 500, lambda a, b: None)
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert out["imported"] == n
        assert peak < 8 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 8 MB ceiling; "
            "the corpus must be streamed in batches, not materialized"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
