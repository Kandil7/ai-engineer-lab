# Redis 01: Cache Strategies — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Cache-aside | Load on demand, store on miss | read-heavy default |
| Write-through | Write to cache and DB together | always in sync |
| Write-behind | Write to cache, flush async | fast, loss risk |
| TTL | The staleness bound | 30 min |
| Cache hit | The value is in the cache | return it |
| Cache miss | Load from the DB and store | populate |
| Staleness | How old the cached value is | bounded by TTL |

---

## Alphabetical Glossary

### Cache hit

**Definition:** The requested value is in the cache. Returned without
touching the database.

**Example:**
```python
# GET user:123 -> HIT -> return cached
```

**Related concepts:** Cache miss

---

### Cache miss

**Definition:** The requested value is not in the cache. Loaded from the
database and stored for next time.

**Example:**
```python
# MISS -> SELECT -> SET -> return
```

**Related concepts:** Cache hit, Cache-aside

---

### Cache-aside

**Definition:** The lazy pattern: check the cache, and on a miss load from
the database and store. The default for read-heavy data.

**Example:**
```python
# GET -> HIT return | MISS -> DB -> SET -> return
```

**Related concepts:** Cache miss

---

### Staleness

**Definition:** How old the cached value is relative to the source of
truth. Bounded by the TTL.

**Example:**
```python
# a 30-min TTL bounds staleness to 30 minutes
```

**Related concepts:** TTL

---

### TTL

**Definition:** Time to live: the staleness bound on a cache entry. Too
long serves stale data; too short defeats the cache.

**Example:**
```python
# SET user:123 value EX 1800
```

**Related concepts:** Staleness

---

### Write-behind

**Definition:** Writing to the cache immediately and flushing to the
database asynchronously. Fast writes; data loss risk if the cache dies
before the flush.

**Example:**
```python
# cache write now, background flush to DB
```

**Related concepts:** Write-through

---

### Write-through

**Definition:** Writing to the cache and the database together. Both are
always in sync; the write path does double work.

**Example:**
```python
# SET cache AND INSERT DB together
```

**Related concepts:** Write-behind

---

## Related Concepts

- **Key patterns**: keys and TTLs per data type (topic 02)
- **Rate limiting**: counters in Redis (topic 03)
- **Pub/Sub**: real-time delivery (topic 04)

## Key Takeaways

1. Cache-aside loads on demand; the default for reads.
2. Write-through keeps cache and DB in sync.
3. Write-behind is fast but risks loss.
4. The strategy matches the consistency needs.
5. TTL is the staleness contract.