"""
Challenge 36: Separation of Concerns — Starter Code
====================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def wire_pipeline(index, config: dict) -> dict:
    """Assemble a pipeline record from collaborators (constructor injection)."""
    raise NotImplementedError


def run_engine_swap_test(
    pipeline_factory: Callable[[str], object],
    corpus: list[dict],
) -> bool:
    """Run identical input through two engines; True iff validation errors match."""
    raise NotImplementedError


def build_engine(engine_kind: str) -> object:
    """Build a NEW search engine (add/search) without touching validation logic."""
    raise NotImplementedError
