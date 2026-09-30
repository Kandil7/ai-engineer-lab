"""
Challenge 04: Failure Modes and Resilience — Starter Code
=========================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def classify_failure(error: Exception | None, context: dict) -> str:
    """Map an error + context to 'transient' | 'permanent' | 'partial' | 'silent'."""
    raise NotImplementedError


def run_with_bulkhead(
    tasks: list[dict], handler: Callable[[dict], None], bulkhead: dict, clock
) -> dict[str, int]:
    """Run tasks with concurrency cap + fail-fast timeouts; return accounting."""
    raise NotImplementedError


def degradation_ladder(state: dict, factory: Callable[[str], dict]) -> dict:
    """Map failure state to the degradation rung; never fabricate an answer."""
    raise NotImplementedError
