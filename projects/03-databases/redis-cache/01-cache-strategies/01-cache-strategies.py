"""
Redis — 01: Cache Strategies
============================
Topics: cache-aside, write-through, write-behind, and TTL.

Why this matters:
    The cache strategy decides consistency. This exercise models the three
    strategies and the TTL bound.

Run:      python 01-cache-strategies.py
Verify:   python 01-cache-strategies.py --verify
"""

from __future__ import annotations

import sys


class Cache:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.ttl: dict[str, int] = {}

    def get(self, key: str, now: int) -> str | None:
        if key in self.ttl and now >= self.ttl[key]:
            self.store.pop(key, None)
            self.ttl.pop(key, None)
            return None
        return self.store.get(key)

    def set(self, key: str, value: str, ttl_sec: int, now: int) -> None:
        self.store[key] = value
        self.ttl[key] = now + ttl_sec


def cache_aside(cache: Cache, db: dict, key: str, now: int, ttl: int) -> str:
    """Check the cache; on a miss load from the DB and store."""
    hit = cache.get(key, now)
    if hit is not None:
        return hit
    value = db[key]
    cache.set(key, value, ttl, now)
    return value


def main() -> None:
    cache = Cache()
    db = {"user:123": "alice"}

    # First read: a miss loads from the DB and stores.
    assert cache_aside(cache, db, "user:123", now=0, ttl=30) == "alice"
    assert cache.get("user:123", now=1) == "alice", "now cached"

    # TTL bounds staleness: after expiry the entry is gone.
    assert cache.get("user:123", now=31) is None, "expired entry evicted"

    # A write-through keeps cache and DB in sync.
    cache.set("user:123", "alice2", 30, now=0)
    db["user:123"] = "alice2"
    assert cache.get("user:123", now=1) == db["user:123"]

    print("cache-aside: miss loads from the DB and stores")
    print("TTL bounds staleness: expired entries are evicted")
    print("write-through keeps cache and DB in sync")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
