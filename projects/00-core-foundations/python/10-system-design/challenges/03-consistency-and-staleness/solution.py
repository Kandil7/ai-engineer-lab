"""
Challenge 03: Consistency and Staleness — Reference Solution
============================================================
"""

from __future__ import annotations

from collections.abc import Callable


def staleness_state(drift: int, stale_threshold: int, broken_threshold: int) -> str:
    """Map drift to 'healthy' | 'stale' | 'degraded' | 'broken'.

    Why this approach: the states are a product decision encoded as pure
    thresholds — drift is a number, and each range has a designed response
    (alert, warning banner, rebuild).
    """
    if drift <= 0:
        return "healthy"
    if drift <= stale_threshold:
        return "stale"
    if drift <= broken_threshold:
        return "degraded"
    return "broken"


def cache_get(cache: dict, key: str, now: float, ttl: float, loader: Callable[[str], dict]) -> dict:
    """Cache-aside: fresh hit returns cached; miss/expiry loads and stores.

    Why this approach: TTL is the honest staleness bound — the cached
    entry states how old it may be. Eviction is the event-invalidation
    hook; expiry is the safety net when a hook is missed.
    """
    entry = cache.get(key)
    if entry is not None:
        value, stored_at = entry
        if ttl > 0 and now - stored_at < ttl:
            return value
    value = loader(key)
    cache[key] = (value, now)
    return value


def apply_events(
    index: dict, events: list[tuple[int, str, dict]], applied_versions: dict[str, int]
) -> dict[str, int]:
    """Apply version-stamped events per-key monotonically.

    Why this approach: per-key version stamps make a late arrival harmless
    — an old event cannot overwrite a newer one, so queue redelivery and
    reordering cannot corrupt the derived store. Arrival order is
    irrelevant when the check is monotonic per key.
    """
    accepted = 0
    rejected = 0
    for version, key, value in events:
        if version <= applied_versions.get(key, 0):
            rejected += 1
            continue
        index[key] = value
        applied_versions[key] = version
        accepted += 1
    return {"accepted": accepted, "rejected": rejected}


def recover(
    source: dict, index: dict, applied_versions: dict[str, int], source_version: int
) -> int:
    """Rebuild the derived index from the source of truth.

    Why this approach: the index is derived, so full rebuild is the
    universal recovery — the lineage is the key set, and the version
    stamps converge to the source's, making drift zero.
    """
    index.clear()
    applied_versions.clear()
    for key, value in source.items():
        index[key] = value
        applied_versions[key] = source_version
    return len(source)
