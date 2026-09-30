"""
Challenge 36: Separation of Concerns — Tests
=============================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/36-separation-of-concerns/test_challenge.py -q

Guards use call counting and tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import inspect
import os
import tracemalloc
import unicodedata
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402

_HARAKAT = set(range(0x064B, 0x0653)) | {0x0670}


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ord(ch) not in _HARAKAT)
    return " ".join(text.split())


class SpyIndex:
    """Records every call the pipeline makes through the index contract."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def add(self, record: dict) -> None:
        self.calls.append("add")

    def search(self, query: str, limit: int = 5) -> list[dict]:
        self.calls.append("search")
        return []


class CountingNormalizer:
    """Counts normalize invocations — the once-per-record budget."""

    def __init__(self) -> None:
        self.count = 0

    def __call__(self, text: str) -> str:
        self.count += 1
        return normalize_text(text)


class _FakePipeline:
    """Reference pipeline: validates WITHOUT touching the index."""

    def __init__(self, engine_kind: str, index: SpyIndex, normalizer: CountingNormalizer) -> None:
        self.engine_kind = engine_kind
        self.index = index
        self.normalizer = normalizer

    def ingest(self, corpus: list[dict]) -> dict:
        errors: list[str] = []
        for rec in corpus:
            key = self.normalizer(str(rec.get("text", "")))
            if not key:
                errors.append(f"{rec.get('id')}: empty text")
                continue
            page = rec.get("page")
            if not isinstance(page, int) or page <= 0:
                errors.append(f"{rec.get('id')}: bad page")
                continue
            self.index.add({**rec, "search_key": key})
        return {"errors": errors, "engine": self.engine_kind}


def make_factory(normalizer: CountingNormalizer, index: SpyIndex):
    def factory(engine_kind: str) -> object:
        return _FakePipeline(engine_kind, index, normalizer)

    return factory


ADVERSARIAL_CORPUS = [
    {"id": "a", "page": 1, "text": "مُحَمَّد"},
    {"id": "b", "page": -3, "text": "\ufefb\u0628"},  # presentation form + bad page
    {"id": "c", "page": 2, "text": "   "},  # whitespace-only
]


class TestWirePipeline:
    """Bronze: wiring only, no business logic."""

    def test_basic(self) -> None:
        fake = SpyIndex()
        out = mod.wire_pipeline(fake, {"engine": "memory"})
        assert out["index"] is fake
        assert out["engine_kind"] == "memory"

    def test_other_engine(self) -> None:
        out = mod.wire_pipeline(SpyIndex(), {"engine": "prefix"})
        assert out["engine_kind"] == "prefix"

    def test_config_passthrough(self) -> None:
        cfg = {"engine": "x", "extra": 1}
        assert mod.wire_pipeline(SpyIndex(), cfg)["config"] is cfg


class TestEngineSwap:
    """Silver: mastery invariant + call budgets."""

    def test_swap_invariant_errors_identical(self) -> None:
        norm, idx = CountingNormalizer(), SpyIndex()
        assert mod.run_engine_swap_test(make_factory(norm, idx), ADVERSARIAL_CORPUS) is True

    def test_swap_invariant_all_valid(self) -> None:
        norm, idx = CountingNormalizer(), SpyIndex()
        corpus = [{"id": str(i), "page": 1, "text": f"نص {i}"} for i in range(10)]
        assert mod.run_engine_swap_test(make_factory(norm, idx), corpus) is True

    def test_swap_invariant_empty(self) -> None:
        norm, idx = CountingNormalizer(), SpyIndex()
        assert mod.run_engine_swap_test(make_factory(norm, idx), []) is True

    def test_normalize_once_per_record(self) -> None:
        """Call budget: normalize exactly once per record across BOTH engines."""
        norm, idx = CountingNormalizer(), SpyIndex()
        corpus = [{"id": str(i), "page": 1, "text": f"نص {i}"} for i in range(50)]
        mod.run_engine_swap_test(make_factory(norm, idx), corpus)
        assert norm.count == len(corpus) * 2, (
            f"normalize called {norm.count} times for {len(corpus)} records x 2 engines; "
            "a re-normalizing pipeline (parse + validate) doubles the calls"
        )

    def test_index_not_consulted_during_validation(self) -> None:
        """Spy guard: invalid records must never reach the index.

        The swap test runs the corpus through BOTH engines sharing one spy,
        so the only legal adds are: 1 valid record x 2 engines = 2.
        """
        norm, idx = CountingNormalizer(), SpyIndex()
        mod.run_engine_swap_test(make_factory(norm, idx), ADVERSARIAL_CORPUS)
        assert idx.calls.count("add") == 2, (
            f"index.add called {idx.calls.count('add')} times; only the 1 valid "
            "record x 2 engines may be added — validation must not route "
            "through the index"
        )


class TestBuildEngine:
    """Gold: a new engine satisfies the contract, decoupled from validation."""

    def test_prefix_engine_contract(self) -> None:
        engine = mod.build_engine("prefix")
        assert hasattr(engine, "add") and hasattr(engine, "search")
        engine.add({"id": "1", "search_key": "محمد"})
        engine.add({"id": "2", "search_key": "محمد"})
        hits = engine.search("محمد")
        assert len(hits) == 2

    def test_keyword_engine_contract(self) -> None:
        engine = mod.build_engine("keyword")
        engine.add({"id": "1", "search_key": "الدين النصيحة"})
        assert len(engine.search("دين")) == 1
        assert engine.search("غير موجود") == []

    def test_limit_respected(self) -> None:
        engine = mod.build_engine("keyword")
        for i in range(10):
            engine.add({"id": str(i), "search_key": "نص"})
        assert len(engine.search("نص", 3)) == 3

    def test_validation_outcomes_identical_across_kinds(self) -> None:
        """The mastery proof at 1000-record scale."""
        corpus = [
            {
                "id": str(i),
                "page": 1 if i % 7 else -1,
                "text": f"نص رقم {i}" if i % 5 else "  ",
            }
            for i in range(1000)
        ]
        results = set()
        for kind in ("prefix", "keyword"):
            norm, idx = CountingNormalizer(), SpyIndex()
            outcome = mod.run_engine_swap_test(make_factory(norm, idx), corpus)
            results.add((kind, outcome))
        assert all(flag for _kind, flag in results), (
            "validation outcomes must not depend on the engine"
        )

    def test_decoupled_source(self) -> None:
        """Structural guard: validation helpers never reference engine internals."""
        norm, idx = CountingNormalizer(), SpyIndex()
        mod.run_engine_swap_test(make_factory(norm, idx), ADVERSARIAL_CORPUS)
        # engine classes are defined AFTER the swap-test function; the swap
        # test body must not mention them
        func_src = inspect.getsource(mod.run_engine_swap_test)
        assert "Engine" not in func_src and "engine.add" not in func_src

    def test_memory_ceiling(self) -> None:
        """1000-record ingest+search must not load everything twice."""
        engine = mod.build_engine("keyword")
        records = [{"id": str(i), "search_key": f"نص رقم {i}" + " " * 200} for i in range(1000)]
        tracemalloc.start()
        try:
            for rec in records:
                engine.add(rec)
            for rec in records[:10]:
                engine.search(rec["search_key"][:2])
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert peak < 12 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 12 MB ceiling; "
            "do not materialize copies of the corpus per query"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
