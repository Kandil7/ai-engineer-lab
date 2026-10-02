# Data Engineering 13: Feature Pipelines — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Feature pipeline | The machinery turning events into feature values | aggregate, cache, version |
| Tumbling window | Fixed, non-overlapping windows | per-minute count |
| Sliding window | Overlapping size-and-slide windows | last 5 min, every 1 min |
| Session window | Closes after a gap of inactivity | user session length |
| Exactly-once | A retried event is neither dropped nor double-counted | checkpointed counter |
| Cache-aside | Check cache, compute on miss, store, invalidate on write | the simple cache pattern |
| Invalidation rule | The named bound on a cache's staleness | TTL, versioned key |
| Thundering herd | A hot key expires and many requests recompute at once | single-flight lock fixes it |
| LRU | Least-recently-used eviction | bounded local cache |
| Feature version | The pinned definition+source of a feature | `chunk_count v2` |

---

## Alphabetical Glossary

### Cache-aside

**Definition:** The simplest cache pattern: on read check the cache; on miss compute and store; on write
invalidate the key. Correct and easy, but the invalidation rule is the caller's responsibility.

**Example:**
```python
value = cache.get(text) or cache.setdefault(text, compute(text))
```

**Related concepts:** Invalidation rule, Thundering herd

---

### Exactly-once

**Definition:** The aggregation guarantee that a retried event is neither dropped nor double-counted,
achieved by writing state atomically with a checkpoint. A counter without it inflates under crash.

**Example:**
```python
# checkpoint (offset, window_sum) written together
```

**Related concepts:** Sliding window, Idempotency

---

### Invalidation rule

**Definition:** The named, enforced bound on how stale a cached value may be — a TTL, a versioned key, or
explicit invalidation on change. A cache without one serves stale data indefinitely.

**Example:**
```python
key = f"emb:{model_version}:{text}"  # versioned key: bump invalidates
```

**Related concepts:** Cache-aside, Feature version

---

### LRU

**Definition:** Least-recently-used, an eviction policy that bounds a cache by dropping the entries least
recently accessed. Prevents unbounded growth.

**Example:**
```python
from functools import lru_cache
```

**Related concepts:** Cache-aside, Local cache

---

### Session window

**Definition:** A variable-length window that closes after a gap of inactivity, used to capture a
contiguous burst of activity such as a user session.

**Example:**
```python
# events with no gap > 30 min form one session
```

**Related concepts:** Tumbling window, Sliding window

---

### Sliding window

**Definition:** A window defined by a size and a slide, so consecutive windows overlap and one event can
belong to several. Answers "the last N over the last M".

**Example:**
```python
# sum over the last 5 minutes, reported every minute
```

**Related concepts:** Tumbling window, Session window

---

### Thundering herd

**Definition:** The cache failure where a hot key expires and many concurrent requests all recompute at
once, spiking the backend. Fixed with a single-flight lock or early refresh.

**Example:**
```python
# only one request recomputes; the rest wait for its result
```

**Related concepts:** Cache-aside, Invalidation rule

---

### Tumbling window

**Definition:** A fixed-size, non-overlapping window; each event belongs to exactly one window. Answers
"how many per unit of time".

**Example:**
```python
buckets[ts // 60 * 60] += value
```

**Related concepts:** Sliding window, Session window

---

## Related Concepts

- **Feature stores**: the stores these pipelines fill (topic 12)
- **Provenance**: the source version in the cache key (topic 06)
- **Batch vs streaming**: windows, ordering, exactly-once (topic 08)

## Key Takeaways

1. Window choice is semantic; a wrong window is a wrong answer.
2. Exactly-once is the counter's correctness requirement.
3. Every cache names its invalidation rule.
4. Cache-aside is the simple, correct pattern.
5. Versioning plus lineage closes the source-to-cache loop.
