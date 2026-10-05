"""
Challenge 39: Poetry - The CI Dependency Gate - Starter Code
============================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations


def expand_constraint(spec: str) -> tuple[str, str]:
    """Expand a Poetry constraint into a (lower, upper) PEP 508 pair."""
    raise NotImplementedError


def install_closure(locked: list[dict], roots: list[str]) -> list[str]:
    """Return every package reachable from roots, sorted ascending."""
    raise NotImplementedError


def audit_manifest(
    pyproject_text: str,
    lock_text: str,
    fetch_meta,
    *,
    only: list[str] | None = None,
    with_groups: list[str] | None = None,
    without: list[str] | None = None,
) -> dict:
    """Audit manifest against lock; see README for the exact return keys."""
    raise NotImplementedError
