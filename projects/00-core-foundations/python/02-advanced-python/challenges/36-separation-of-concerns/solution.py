"""
Challenge 36: Separation of Concerns — Reference Solution
=========================================================
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, cast, runtime_checkable


@runtime_checkable
class _Ingestable(Protocol):
    """Contract the swap test needs from any pipeline."""

    def ingest(self, corpus: list[dict]) -> dict: ...


def wire_pipeline(index, config: dict) -> dict:
    """Assemble a pipeline record from collaborators.

    Why this approach: the composition root is the ONLY place that binds
    concrete objects together. Returning a plain dict keeps this function
    free of any business logic — wiring, not work.
    """
    return {"index": index, "config": config, "engine_kind": config["engine"]}


def run_engine_swap_test(
    pipeline_factory: Callable[[str], object],
    corpus: list[dict],
) -> bool:
    """Run identical input through two engines; True iff validation errors match.

    Why this approach: validation must be a function of the record and the
    config only. Comparing the error lists of two pipelines built on
    different engines proves the validator never consulted the engine —
    if it had, the errors could differ.
    """
    errors_a = cast(_Ingestable, pipeline_factory("memory")).ingest(corpus)["errors"]
    errors_b = cast(_Ingestable, pipeline_factory("prefix")).ingest(corpus)["errors"]
    return errors_a == errors_b


class _PrefixEngine:
    """Prefix-bucket engine: groups records by the first 3 chars of the key."""

    def __init__(self) -> None:
        self._buckets: dict[str, list[dict]] = {}

    def add(self, record: dict) -> None:
        key = record.get("search_key", "")
        self._buckets.setdefault(key[:3], []).append(record)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        hits = self._buckets.get(query[:3], [])
        return hits[:limit]


class _KeywordEngine:
    """Substring engine: naive but contract-identical add/search surface."""

    def __init__(self) -> None:
        self._records: list[dict] = []

    def add(self, record: dict) -> None:
        self._records.append(record)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        return [r for r in self._records if query in r.get("search_key", "")][:limit]


def build_engine(engine_kind: str) -> object:
    """Build a NEW search engine without touching validation logic.

    Why this approach: the engine only satisfies the SearchIndex contract
    (add/search). It knows nothing about validation rules — swapping it
    out is one line at the composition root, and the validator's tests
    are untouched.
    """
    if engine_kind == "prefix":
        return _PrefixEngine()
    return _KeywordEngine()
