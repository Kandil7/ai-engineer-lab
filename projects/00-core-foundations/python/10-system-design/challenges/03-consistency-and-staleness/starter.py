"""
Challenge 03: Consistency and Staleness — Starter Code
=======================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def staleness_state(drift: int, stale_threshold: int, broken_threshold: int) -> str:
    """Map drift to 'healthy' | 'stale' | 'degraded' | 'broken'."""
    raise NotImplementedError


def cache_get(cache: dict, key: str, now: float, ttl: float, loader: Callable[[str], dict]) -> dict:
    """Cache-aside: fresh hit returns cached; miss/expiry loads and stores."""
    raise NotImplementedError


def apply_events(
    index: dict, events: list[tuple[int, str, dict]], applied_versions: dict[str, int]
) -> dict[str, int]:
    """Apply version-stamped events per-key monotonically; return accepted/rejected."""
    raise NotImplementedError


def recover(
    source: dict, index: dict, applied_versions: dict[str, int], source_version: int
) -> int:
    """Rebuild the derived index from the source of truth; return entry count."""
    raise NotImplementedError
