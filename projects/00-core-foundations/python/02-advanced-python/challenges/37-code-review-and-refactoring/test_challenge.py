"""
Challenge 37: Code Review and Refactoring — Tests
==================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/37-code-review-and-refactoring/test_challenge.py -q

Structural guards use ast branch counting and exec-and-compare locks —
never wall-clock time.
"""

from __future__ import annotations

import ast
import importlib.util
import os
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402

# The god endpoint: guards, normalizes, filters, paginates, caches — one
# function, 12 branches across 11 top-level statements. Every probe drives
# this exact behavior. `rows` is a parameter so the source is self-contained.
GOD_SRC = """
def handle_search_request(raw_query, user, book_filter, page_from, page_to, cache, rows):
    if not user:
        return {"error": "no-user"}
    if not raw_query:
        return {"error": "empty-query"}
    q = raw_query.lower().strip()
    for ch in q:
        if ord(ch) > 0x06FF:
            q = q.replace(ch, "")
    if q.startswith("author:"):
        q = q.split(":", 1)[1]
    hits = []
    for row in rows:
        if book_filter and row["book"] != book_filter:
            continue
        if page_from is not None and row["page"] < page_from:
            continue
        if page_to is not None and row["page"] > page_to:
            continue
        hits.append(row["id"])
    if len(hits) > 10:
        hits = hits[:10]
    result = {"hits": hits, "q": q}
    if cache is not None:
        cache[raw_query] = result
    return result
"""

ROWS = [
    {"id": "r1", "book": "bukhari", "page": 5},
    {"id": "r2", "book": "bukhari", "page": 12},
    {"id": "r3", "book": "muslim", "page": 3},
    {"id": "r4", "book": "muslim", "page": 20},
]

PROBES = [
    {
        "raw_query": "الدين",
        "user": "u1",
        "book_filter": "",
        "page_from": None,
        "page_to": None,
        "cache": None,
        "rows": ROWS,
    },
    {
        "raw_query": "",
        "user": "u1",
        "book_filter": "",
        "page_from": None,
        "page_to": None,
        "cache": None,
        "rows": ROWS,
    },
    {
        "raw_query": "x",
        "user": "",
        "book_filter": "",
        "page_from": None,
        "page_to": None,
        "cache": None,
        "rows": ROWS,
    },
    {
        "raw_query": "author:ibn",
        "user": "u1",
        "book_filter": "bukhari",
        "page_from": 1,
        "page_to": 10,
        "cache": None,
        "rows": ROWS,
    },
    {
        "raw_query": "q",
        "user": "u1",
        "book_filter": "bukhari",
        "page_from": 100,
        "page_to": 200,
        "cache": None,
        "rows": ROWS,
    },
    {
        "raw_query": "q",
        "user": "u1",
        "book_filter": "",
        "page_from": 4,
        "page_to": 15,
        "cache": {},
        "rows": ROWS,
    },
]


def _count_branches_func(fn_src: str) -> int:
    tree = ast.parse(fn_src)
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            total += 1
    return total


def _max_branches(src: str) -> int:
    tree = ast.parse(src)
    per_fn = [
        _count_branches_func(ast.unparse(n))
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return max(per_fn) if per_fn else 0


def _run_entry(src: str, probe: dict):
    namespace: dict = {}
    exec(compile(ast.parse(src), "<target>", "exec"), namespace)
    entry = None
    for name, val in namespace.items():
        if callable(val) and not name.startswith("_") and not isinstance(val, type):
            entry = val
            break
    assert entry is not None, "source defines no entry function"
    return entry(**probe)


class TestFunctionStats:
    """Bronze: ast-based smell measurement."""

    def test_simple(self) -> None:
        stats = mod.function_stats("def f(a, b):\n    return a")
        assert stats == {"f": {"lines": 2, "params": 2, "branches": 0}}

    def test_nested_branches(self) -> None:
        src = "def f(a):\n    if a:\n        if a > 1:\n            return 1\n    return 0"
        assert mod.function_stats(src)["f"]["branches"] == 2

    def test_async_counted(self) -> None:
        src = "async def g(x):\n    if x:\n        return x"
        assert mod.function_stats(src)["g"]["branches"] == 1

    def test_loop_counts(self) -> None:
        src = "def h(xs):\n    for x in xs:\n        while x:\n            x -= 1"
        assert mod.function_stats(src)["h"]["branches"] == 2

    def test_kwo_params(self) -> None:
        src = "def k(a, *, b, c=1):\n    return a"
        assert mod.function_stats(src)["k"]["params"] == 3


class TestSplitGod:
    """Silver: structure ceiling + behavior lock."""

    def test_branch_ceiling(self) -> None:
        out = mod.split_god_function(GOD_SRC)
        assert _max_branches(out) <= 6, "no function may exceed 6 branches after the split"

    def test_behavior_byte_identical(self) -> None:
        out = mod.split_god_function(GOD_SRC)
        for probe in PROBES:
            assert _run_entry(out, probe) == _run_entry(GOD_SRC, probe)

    def test_adversarial_edges(self) -> None:
        out = mod.split_god_function(GOD_SRC)
        edges = [
            {
                "raw_query": "  ",
                "user": "u",
                "book_filter": "",
                "page_from": None,
                "page_to": None,
                "cache": None,
                "rows": ROWS,
            },
            {
                "raw_query": "q",
                "user": "u",
                "book_filter": "nope",
                "page_from": 0,
                "page_to": 0,
                "cache": None,
                "rows": [],
            },
        ]
        for probe in edges:
            assert _run_entry(out, probe) == _run_entry(GOD_SRC, probe)

    def test_real_extraction(self) -> None:
        out = mod.split_god_function(GOD_SRC)
        n_funcs = sum(
            1
            for n in ast.walk(ast.parse(out))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        assert n_funcs >= 2, "a rename-only fake split is not a refactor"


class TestRefactorWithLocks:
    """Gold: locks preserved + 40% branch drop + real extraction."""

    def test_all_locks_preserved(self) -> None:
        _refactored, report = mod.refactor_with_locks(GOD_SRC, PROBES)
        assert len(report) == len(PROBES)
        assert all(item["preserved"] for item in report), "every lock must pass"

    def test_branch_drop_40_percent(self) -> None:
        refactored, _report = mod.refactor_with_locks(GOD_SRC, PROBES)
        before = _max_branches(GOD_SRC)
        after = _max_branches(refactored)
        assert before > 0
        assert after <= before * 0.6, f"max branches {before} -> {after} is not a >= 40% drop"

    def test_extraction_depth(self) -> None:
        refactored, _report = mod.refactor_with_locks(GOD_SRC, PROBES)
        n_funcs = sum(
            1
            for n in ast.walk(ast.parse(refactored))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        assert n_funcs >= 3, "real extraction: at least 3 functions after refactor"

    def test_lock_report_shape(self) -> None:
        _refactored, report = mod.refactor_with_locks(GOD_SRC, PROBES[:3])
        for i, item in enumerate(report):
            assert item["probe"] == i and isinstance(item["preserved"], bool)

    def test_empty_probes(self) -> None:
        refactored, report = mod.refactor_with_locks(GOD_SRC, [])
        assert report == []
        assert _max_branches(refactored) <= 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
