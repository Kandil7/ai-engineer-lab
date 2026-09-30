"""
Challenge 02: Queues and Workflows — Starter Code
==================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def insert_if_absent(store: dict, key: str, value) -> bool:
    """Insert only when absent; True if inserted, False if already present."""
    raise NotImplementedError


def run_job(
    job: dict, handler: Callable[[dict], bool], policy: dict, sleep: Callable[[float], None]
) -> str:
    """Run one job with retry policy; return 'done' or 'dead_letter'."""
    raise NotImplementedError


def run_worker_pool(
    jobs: list[tuple[str, str]], handler: Callable[[str, str], bool], policy: dict
) -> dict[str, int]:
    """Process redelivered/poison jobs; return done/dead_lettered/skipped/handler_calls."""
    raise NotImplementedError
