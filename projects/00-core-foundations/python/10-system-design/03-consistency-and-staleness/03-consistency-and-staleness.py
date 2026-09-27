"""
Consistency and Staleness - System Design Exercises
====================================================
Topics: source of truth vs derived stores, cache-aside, TTL and
invalidation, staleness detection, read-your-writes, event ordering,
the stale-index problem.

Why this matters for AI engineering:
    The Athar mastery question: "what happens if the index becomes
    older than the source?" The answer must be a designed state, not a
    surprise. PostgreSQL is the source of truth; the vector index and
    any cache are DERIVED and therefore eventually consistent. This
    file builds the staleness model: version stamps to detect drift,
    invalidation strategies, read-your-writes for users, and the
    rebuild path that makes a stale index a measurable, recoverable
    state instead of corrupted retrieval.

Environment note:
    Pure standard library. Runnable offline.

Run:      python 03-consistency-and-staleness.py
Verify:   python 03-consistency-and-staleness.py --verify
Reference: https://martinfowler.com/articles/cacheInvalidation.html
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. Source of truth vs derived store
# ============================================================
# Rule: exactly ONE store is authoritative for each fact. Everything
# else is a cache/derived view and may be behind. For Athar:
#   AUTHORITATIVE: PostgreSQL (books, editions, pages, permissions)
#   DERIVED:       vector index, search cache, embedding store
# The derived store is rebuildable FROM the source. If you cannot
# rebuild it, it is not derived - it is a second source of truth and
# you now have a consistency problem you cannot fix.

print("1. one source of truth per fact")
print("   truth: PostgreSQL   derived: vector index, caches")
print("   derived stores are REBUILDABLE from truth")
print()


# ============================================================
# 2. Version stamps: detecting staleness mechanically
# ============================================================
# Staleness is not a feeling; it is a number. Every write bumps a
# version on the source; the derived store records the version it was
# built from. drift = source_version - derived_version. If drift > 0
# the index is stale by that many changes - measurable and alertable.


@dataclass
class SourceOfTruth:
    """Postgres stand-in: authoritative rows + a write version."""

    rows: dict[str, dict] = field(default_factory=dict)
    version: int = 0

    def upsert(self, key: str, value: dict) -> int:
        self.rows[key] = value
        self.version += 1
        return self.version


@dataclass
class DerivedIndex:
    """Vector-index stand-in: rows + the source version it reflects."""

    rows: dict[str, dict] = field(default_factory=dict)
    built_from_version: int = 0

    def rebuild_from(self, source: SourceOfTruth) -> int:
        """Full rebuild - the recovery path for any drift."""
        self.rows = dict(source.rows)
        self.built_from_version = source.version
        return self.built_from_version

    def apply_change(self, key: str, value: dict, new_version: int) -> None:
        """Incremental update; keeps the version stamp honest."""
        self.rows[key] = value
        self.built_from_version = new_version


def drift(source: SourceOfTruth, index: DerivedIndex) -> int:
    """How many writes the index is behind the source."""
    return source.version - index.built_from_version


print("2. version stamps make staleness a number")
src = SourceOfTruth()
idx = DerivedIndex()
src.upsert("bukhari/p1", {"text": "نص ١"})
idx.rebuild_from(src)
src.upsert("bukhari/p2", {"text": "نص ٢"})  # index did not see this
print(f"   drift after one unseen write: {drift(src, idx)} (stale!)")
idx.rebuild_from(src)
print(f"   drift after rebuild: {drift(src, idx)} (current)")
print()


# ============================================================
# 3. Cache-aside with TTL and invalidation
# ============================================================
# The classic read cache: check cache -> hit: return; miss: read
# source, populate cache, return. Two invalidation styles:
#   TTL     - expire after N seconds (simple, always slightly stale)
#   Event   - invalidate on write (fresh, but needs a write hook)
# TTL is honest staleness; event invalidation is best-effort freshness.


@dataclass
class CachedValue:
    value: dict
    stored_at: float
    ttl: float

    def expired(self, now: float) -> bool:
        return now - self.stored_at > self.ttl


class Cache:
    """Cache-aside store with TTL expiry and write-time invalidation."""

    def __init__(self, ttl: float = 5.0) -> None:
        self._data: dict[str, CachedValue] = {}
        self._ttl = ttl
        self.hits = 0
        self.misses = 0

    def get(self, key: str, now: float, loader) -> dict:
        cached = self._data.get(key)
        if cached is not None and not cached.expired(now):
            self.hits += 1
            return cached.value
        self.misses += 1
        value = loader(key)
        self._data[key] = CachedValue(value=value, stored_at=now, ttl=self._ttl)
        return value

    def invalidate(self, key: str) -> None:
        """Event invalidation: called by the write path."""
        self._data.pop(key, None)


print("3. cache-aside: TTL + event invalidation")
cache = Cache(ttl=5.0)
loader = lambda k: {"text": f"value-for-{k}"}  # noqa: E731
t0 = 100.0
print(
    f"   miss then hit: {cache.get('a', t0, loader)['text']}, hits={cache.hits} misses={cache.misses}"
)
print(f"   same second:   hits={cache.get('a', t0, loader) is not None}, hits={cache.hits}")
print(
    f"   after TTL:     expired -> {cache.get('a', t0 + 6.0, loader) is not None}, misses={cache.misses}"
)
cache.get("b", t0, loader)
cache.invalidate("b")
print(f"   after invalidate: misses={cache.misses + 1} (b refetched)")
print()


# ============================================================
# 4. Read-your-writes consistency
# ============================================================
# The user-visible bug of eventual consistency: I edit a record, refresh
# the page, and see the OLD version (stale replica/cache). Read-your-
# writes (RYW) guarantees: after YOUR write, YOUR reads see it. Cheap
# version: session pinning - read from the version-stamped source for
# the writer's own session (or simply skip the cache after own writes).


def read_after_write(
    source: SourceOfTruth, index: DerivedIndex, cache: Cache, key: str, writer_session: bool
) -> dict:
    """RYW: a writer's own read bypasses derived stores."""
    if writer_session:
        return source.rows[key]  # read your own write from truth
    return cache.get(key, time.time(), lambda k: index.rows.get(k, {}))


print("4. read-your-writes: writer reads truth, others may read cache")
src2 = SourceOfTruth()
idx2 = DerivedIndex()
src2.upsert("k", {"text": "old"})
idx2.rebuild_from(src2)
src2.upsert("k", {"text": "new"})  # write; index not yet updated
writer_view = read_after_write(src2, idx2, Cache(), "k", writer_session=True)
other_view = read_after_write(src2, idx2, Cache(), "k", writer_session=False)
print(
    f"   writer sees: {writer_view['text']}   other sees: {other_view.get('text', 'stale/empty')}"
)
print()


# ============================================================
# 5. The stale-index problem - detection and recovery
# ============================================================
# The mastery question: the index is older than the source. The
# designed state machine:
#   healthy:     drift == 0
#   stale:       drift > 0  -> alert + incremental catch-up
#   degraded:    drift > threshold -> stop serving derived answers OR
#                serve with an explicit staleness warning
#   broken:      drift unbounded -> full rebuild from source
# The recovery path (rebuild) exists because the index is derived.


def staleness_state(
    source: SourceOfTruth,
    index: DerivedIndex,
    stale_threshold: int = 5,
    broken_threshold: int = 100,
) -> str:
    d = drift(source, index)
    if d == 0:
        return "healthy"
    if d <= stale_threshold:
        return "stale"
    return "degraded" if d <= broken_threshold else "broken"


print("5. staleness state machine")
src3 = SourceOfTruth()
idx3 = DerivedIndex()
idx3.rebuild_from(src3)
print(f"   initial: {staleness_state(src3, idx3)}")
for i in range(3):
    src3.upsert(f"p{i}", {"text": f"t{i}"})
print(f"   after 3 unseen writes: {staleness_state(src3, idx3)} (drift={drift(src3, idx3)})")
for i in range(10):
    src3.upsert(f"q{i}", {"text": f"t{i}"})
print(f"   after 13 total: {staleness_state(src3, idx3)} (drift={drift(src3, idx3)})")
idx3.rebuild_from(src3)
print(f"   after rebuild: {staleness_state(src3, idx3)}")
print()


# ============================================================
# 6. Event ordering and lost updates
# ============================================================
# Incremental index updates can arrive out of order (queue retries!).
# Applying an OLD update after a NEW one corrupts the index. Fix:
# version-stamp every update and reject stale applications - the same
# version discipline as section 2, applied per update.


def apply_versioned(index: DerivedIndex, key: str, value: dict, update_version: int) -> bool:
    """Apply an incremental update only if it is newer than what is applied."""
    if update_version <= index.built_from_version:
        return False  # stale event: ignore
    index.rows[key] = value
    index.built_from_version = update_version
    return True


print("6. out-of-order updates rejected by version stamp")
idx4 = DerivedIndex()
print(f"   apply v5: {apply_versioned(idx4, 'a', {'text': 'newer'}, 5)}")
print(f"   apply v3 (late): {apply_versioned(idx4, 'a', {'text': 'older'}, 3)} (rejected)")
print(f"   final text: {idx4.rows['a']['text']}")
print()


# ============================================================
# 7. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []
    s = SourceOfTruth()
    i = DerivedIndex()
    s.upsert("a", {"text": "1"})
    i.rebuild_from(s)
    checks.append(("drift zero when current", drift(s, i) == 0))
    s.upsert("b", {"text": "2"})
    checks.append(("drift positive when stale", drift(s, i) == 1))
    i.rebuild_from(s)
    checks.append(("rebuild clears drift", drift(s, i) == 0))

    c = Cache(ttl=5.0)
    calls = {"n": 0}

    def loader(k):
        calls["n"] += 1
        return {"v": calls["n"]}

    c.get("k", 0.0, loader)
    c.get("k", 1.0, loader)
    checks.append(("cache hit avoids loader", calls["n"] == 1 and c.hits == 1))
    c.get("k", 10.0, loader)
    checks.append(("TTL expiry refetches", calls["n"] == 2))
    c.invalidate("k")
    c.get("k", 11.0, loader)
    checks.append(("invalidation refetches", calls["n"] == 3))

    s2 = SourceOfTruth()
    i2 = DerivedIndex()
    s2.upsert("k", {"text": "old"})
    i2.rebuild_from(s2)
    s2.upsert("k", {"text": "new"})
    checks.append(
        (
            "read-your-writes sees own write",
            read_after_write(s2, i2, Cache(), "k", True)["text"] == "new",
        )
    )

    i3 = DerivedIndex()
    checks.append(("versioned apply accepts newer", apply_versioned(i3, "a", {"t": "n"}, 5)))
    checks.append(("versioned apply rejects older", not apply_versioned(i3, "a", {"t": "o"}, 3)))

    s3 = SourceOfTruth()
    i4 = DerivedIndex()
    for _ in range(20):
        s3.upsert("x", {"text": "t"})
    checks.append(
        ("broken state detected", staleness_state(s3, i4, broken_threshold=15) == "broken")
    )
    i4.rebuild_from(s3)
    checks.append(("rebuild restores healthy", staleness_state(s3, i4) == "healthy"))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 03-consistency-and-staleness.py --verify):")
    _verify()
