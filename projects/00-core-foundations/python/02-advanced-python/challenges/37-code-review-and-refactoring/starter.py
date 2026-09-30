"""
Challenge 37: Code Review and Refactoring — Starter Code
========================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations


def function_stats(src: str) -> dict[str, dict[str, int]]:
    """AST-based per-function metrics: lines, params, branches."""
    raise NotImplementedError


def split_god_function(src: str) -> str:
    """Refactor into extracted functions; max 6 branches each; behavior identical."""
    raise NotImplementedError


def refactor_with_locks(src: str, probes: list[dict]) -> tuple[str, list[dict]]:
    """Refactor + lock-test report; branch count down >= 40%; all locks pass."""
    raise NotImplementedError
