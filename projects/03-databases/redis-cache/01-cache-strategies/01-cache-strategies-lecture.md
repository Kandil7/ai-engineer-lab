# Redis 01: Cache Strategies

## Topic Overview

A cache sits between the application and the source of truth. The strategy decides when data enters the
cache and how it stays consistent with the database, and that decision is a consistency decision before
it is a performance one. The wrong strategy serves stale data or loses writes; the right one is chosen
from the data's consistency needs, not from habit.

This lecture covers cache-aside, write-through, and write-behind, the TTL that bounds staleness in every
strategy, and how to choose for a given data type.

The recurring idea is that a cache always trades some consistency for speed, and the strategy is how you
choose which consistency you are willing to give up. Stating the trade explicitly is what separates a
deliberate cache from an accidental one.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain cache-aside and its miss path.
2. Explain write-through and its consistency.
3. Explain write-behind and its risk.
4. Choose a strategy from the data's consistency needs.
5. Set a TTL to bound staleness.
6. Explain why the strategy is a consistency decision.

## Prerequisites

- PostgreSQL 01 (schema design) for the source of truth.
- RAG System 06 (caching) for the version-key discipline.

---

## 1. Cache-Aside

### The pattern

Cache-aside is the lazy pattern: check the cache, and on a miss load from the database and store:

```python
def cache_aside(cache, db, key, now, ttl):
    """Check the cache; on a miss load from the DB and store."""
    hit = cache.get(key, now)
    if hit is not None:
        return hit
    value = db[key]
    cache.set(key, value, ttl, now)
    return value
```

### Why it is the default

The cache is populated on demand, so only the data that is actually requested is cached, and the
database remains the source of truth. It is the default for read-heavy data.

### The exit test

The roadmap's exit test is that cache-aside is used for read-heavy data, exactly because it does not
require the write path to know about the cache.

## 2. Write-Through

### The pattern

Write-through writes to the cache and the database together, so both are always in sync and there are no
stale reads.

### The cost

The write path does double work, which slows writes. The benefit is consistency, which matters for data
that must be immediately correct: sessions, counters, permissions.

### When

Write-through is right when a stale read is a correctness problem. For data where a brief lag is
acceptable, cache-aside is cheaper.

## 3. Write-Behind

### The pattern

Write-behind writes to the cache immediately and flushes to the database asynchronously. The write is
fast because it returns before the database commits.

### The risk

If the cache dies before the flush, the write is lost. Write-behind trades durability for write speed,
so it is wrong for data that must not be lost.

### When

Write-behind is right for non-critical, high-write data: view counters, metrics, analytics events. The
loss of a few events is acceptable; the write throughput is the point.

## 4. Choosing the Strategy

### The decision

The choice follows from the data's consistency needs:

| Data | Strategy | Why |
| --- | --- | --- |
| Read-heavy, tolerable staleness | Cache-aside | Lazy, source of truth preserved |
| Must be immediately consistent | Write-through | No stale reads |
| High-write, loss-tolerant | Write-behind | Write speed over durability |

### The exit test

The roadmap's exit test is that the strategy matches the data's consistency needs. One strategy for all
data means some of it is handled wrongly: durable data risks loss or read-heavy data pays a write cost
it does not need.

## 5. TTL and Staleness

### The TTL

Every cache entry has a TTL that bounds its staleness:

```python
assert cache.get("user:123", now=31) is None, "expired entry evicted"
```

A TTL too long serves stale data; a TTL too short defeats the cache. The TTL is the staleness contract,
and it is set per data type.

### TTL and invalidation together

TTL is the safety net; event invalidation (RAG System 06) is the freshness mechanism. Production uses
both: TTL bounds the worst case even when an invalidation is missed.

### The exercise

The exercise's `Cache` expires entries by `now >= ttl`, showing that the TTL is what limits how stale a
read can be.

## 6. The Exercise

### What it models

The exercise models cache-aside, TTL expiry, and write-through.

### The assertions

```python
assert cache_aside(cache, db, "user:123", now=0, ttl=30) == "alice"
assert cache.get("user:123", now=31) is None, "expired entry evicted"
```

The first shows the miss-then-load path; the second shows the TTL bound.

## Real-World Application

- Cache-aside for user profiles, where a short staleness is acceptable.
- Write-through for session state, where a stale read would log someone out.
- Write-behind for view counters, where losing a few is acceptable.
- A TTL per data type so profiles expire in minutes and sessions in hours.

## Common Mistakes

1. **Write-through for read-heavy data.** Double write cost for no consistency need.
2. **Write-behind for critical data.** Loss risk on a cache failure.
3. **No TTL.** Stale data persists forever.
4. **Cache-aside with no invalidation.** A write leaves the old value cached.
5. **One strategy for all data.** Some data is handled wrongly.
6. **A TTL longer than the data's tolerance.** Stale reads.

## Key Takeaways

1. Cache-aside loads on demand and is the default for reads.
2. Write-through keeps cache and database in sync at the cost of double writes.
3. Write-behind is fast but risks loss; use it only for loss-tolerant data.
4. The strategy matches the data's consistency needs.
5. The TTL is the staleness contract and is set per data type.

## Self-Check Questions

1. Why is cache-aside the default for read-heavy data?
2. What does write-through buy, and what does it cost?
3. When is write-behind acceptable, and what is its risk?
4. Why does the cache strategy depend on the data's consistency needs?
5. Why keep both a TTL and event invalidation?

## Further Reading / Connections

- Redis 02 (key patterns and TTL) — the TTL per data type.
- RAG System 06 (caching) — the version-key discipline for answers.
- PostgreSQL 01 (schema design) — the source of truth the cache fronts.
- `docs/cheat-sheets/qdrant.md` and `docs/cheat-sheets/git.md` — related references.
