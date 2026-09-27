# Redis 01: Cache Strategies

## 🎯 Topic Overview

A cache sits between the application and the source of truth. The strategy
decides when data enters the cache and how it stays consistent. This
lecture covers cache-aside, write-through, and write-behind, and when each
is right.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain cache-aside and its miss path
2. Explain write-through and its consistency
3. Explain write-behind and its risk
4. Choose the strategy for the data's consistency needs
5. Set TTLs to bound staleness

---

## 1. Cache-Aside

Cache-aside is the lazy pattern: check the cache, and on a miss load from
the database and store. The cache is populated on demand. It is the
default for read-heavy data. The roadmap's exit test: "cache-aside is
used for read-heavy data."

```
GET user:123 -> HIT return | MISS -> SELECT -> SET -> return
```

## 2. Write-Through

Write-through writes to the cache and the database together. Both are
always in sync — no stale reads. The cost is the write path does double
work. It is right for data that must be immediately consistent: sessions,
counters.

## 3. Write-Behind

Write-behind writes to the cache immediately and flushes to the database
asynchronously. The write is fast; the risk is data loss if the cache
dies before the flush. It is right for non-critical counters and metrics.

## 4. Choosing the Strategy

The choice is a consistency decision. Read-heavy data with tolerable
staleness: cache-aside. Immediately consistent data: write-through.
High-write, loss-tolerant data: write-behind. The roadmap's exit test:
"the strategy matches the data's consistency needs."

## 5. TTL and Staleness

Every cache entry has a TTL that bounds staleness. A TTL too long serves
stale data; a TTL too short defeats the cache. The TTL is the staleness
contract — set deliberately per data type.

## Common Mistakes

- Write-through for read-heavy data (double write cost).
- Write-behind for critical data (loss risk).
- No TTL (stale data forever).
- Cache-aside with no invalidation.
- One strategy for all data.

## Key Takeaways

1. Cache-aside loads on demand; the default for reads.
2. Write-through keeps cache and DB in sync.
3. Write-behind is fast but risks loss.
4. The strategy matches the consistency needs.
5. TTL is the staleness contract.