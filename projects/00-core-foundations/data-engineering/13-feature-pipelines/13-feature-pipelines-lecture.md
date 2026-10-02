# Data Engineering 13: Feature Pipelines

## Topic Overview

A feature pipeline is the running machinery that turns raw events into feature values: real-time
aggregation over rolling windows, caching those values for low-latency reads, and versioning them so a
change is traceable. Where the feature store (Data Engineering 12) is the *where* of features, the
feature pipeline is the *how* — the computation and delivery path that keeps the online store fresh and
the training set honest.

Three ideas carry the whole lecture. Windows bound a stream into computable chunks; the choice of window
is a correctness decision, not an implementation detail. Caching trades freshness for latency and must
name its invalidation rule, or it serves stale answers. Versioning ties a feature to its definition and
source, so when an upstream changes, the feature is re-derived rather than silently trusted.

For our systems this is concrete. DevMate's semantic cache is a feature cache: the embedding of a query
is a feature, computed once, cached in Redis or locally, and invalidated by its source version. Athar's
passage statistics — how many passages a book contributed — are a real-time or batch aggregation keyed
by `book_id`. The same principles govern both.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish tumbling, sliding, and session windows and their aggregation semantics.
2. Explain why exactly-once aggregation matters for counters.
3. Choose a caching strategy (Redis vs local) and name its invalidation rule.
4. Implement cache-aside and explain its failure modes.
5. Version a feature and track its lineage to its source.
6. Map DevMate's semantic cache and Athar's passage counts onto these ideas.
7. Defend the freshness-versus-latency trade a cache always makes.

## Prerequisites

- Data Engineering 08 (batch vs streaming) for windows and ordering.
- Data Engineering 12 (feature stores) for the stores these pipelines fill.

---

## 1. Real-Time Aggregation and Windows

### The window types

A window bounds an unbounded stream so an aggregate is computable. The three shapes:

- **Tumbling** — fixed, non-overlapping windows; each event belongs to exactly one window.
- **Sliding (hopping)** — overlapping windows defined by a size and a slide; an event belongs to many.
- **Session** — variable-length windows that close after a gap of inactivity.

### Why the choice is semantic

A tumbling window answers "how many per minute"; a sliding window answers "how many in the last five
minutes, reported every minute"; a session window answers "how long did a user stay." Choosing the wrong
window produces a correct number for the wrong question, which is worse than a wrong number.

### The aggregation code

```python
def tumbling_sum(events: list[tuple[int, int]], window: int) -> dict[int, int]:
    buckets: dict[int, int] = {}
    for ts, value in events:
        bucket = ts // window * window
        buckets[bucket] = buckets.get(bucket, 0) + value
    return buckets
```

### Exactly-once counters

A counter that double-counts a retried event is corrupt. Streaming aggregations need the exactly-once
guarantee of Data Engineering 08 — state written atomically with the checkpoint — so a crash-and-retry
does not inflate the count. The link to idempotency (Data Engineering 03) is that the operation, not the
number of times it ran, determines the value.

## 2. Caching Strategies

### Redis versus local

Redis is the shared, distributed cache: one value for all instances, network round-trip, TTLs and
eviction built in. A local cache (an in-process dict or LRU) is per-instance, zero network cost, but
inconsistent across instances and lost on restart. The choice is about consistency needs and access
latency.

### The cache-aside pattern

Cache-aside is the simplest correct pattern: on read, check the cache; on miss, compute and store; on
write, invalidate the key.

```python
def get_embedding(text: str, cache: dict) -> str:
    if text in cache:
        return cache[text]
    value = compute_embedding(text)  # the expensive path
    cache[text] = value
    return value
```

### The invalidation rule

Every cache must name its invalidation rule, or it serves stale data. The rule is usually one of:
TTL (expire after a duration), key versioning (include the source version in the key), or explicit
invalidation on change. The source-version-in-key rule from Data Engineering 06 is the one that ties the
cache to provenance: bump the version, and the old key is simply never looked up again.

### The failure modes

A cache can return stale data (invalidation missed), thundering-herd (a hot key expired and every
request recomputes at once), or unbounded growth (no eviction). Each has a fix — versioned keys, a
single-flight lock, and an LRU — but each must be chosen consciously.

## 3. Feature Versioning and Lineage

### Versioning a feature

A feature's version captures its definition and source at a point in time. When the normalization,
window, or source changes, the version bumps. Consumers pin the version they trained against, so a
change is explicit rather than silent. This is the provenance discipline of Data Engineering 06, applied
to a computed value instead of a source row.

### The lineage map

Lineage records the chain from source to feature: which input columns, which transformation, which
window, which version. A lineage map makes two questions cheap: "where did this feature come from?" and
"if this source changes, which features must be recomputed?"

### The cache-key loop

Versioning and the cache key form a loop: the feature version is part of the key, so a version bump
invalidates the cache, which forces recomputation, which produces the new value. The loop is what makes
the pipeline self-healing under source change.

## 4. A Real-Time Feature Pipeline, End to End

### The shape

```text
events ──> window aggregation ──> online store ──> cache ──> model
                                    │
                                    └──> offline store (for training)
registry: feature name, version, window, source
```

### The DevMate mapping

DevMate's semantic cache is this pipeline in miniature: the "feature" is the embedding of a query, the
aggregation is the embed step, the cache is Redis or a local LRU keyed by the embedding model version,
and the lineage is the model version plus the source text. A model version bump invalidates every cached
embedding consistently.

### The Athar mapping

Athar's per-book passage count is a tumbling batch aggregation keyed by `book_id`, versioned by
`source_version`, and cached for the UI's "corpus size" readout. The same loop — aggregate, version,
cache, invalidate — applies at every scale.

## 5. Freshness Versus Latency

### The trade

Every cache trades freshness for latency: the cached value is always the value from some earlier
moment, in exchange for returning instantly. The question is never "should I cache?" but "how stale am I
willing to be, and how do I bound that staleness?"

### Bounding staleness

A TTL bounds staleness by age; a versioned key bounds it by correctness — the cache is never older than
its source version. For a citation corpus, versioned keys are the right bound: an answer must not cite a
passage from a superseded source, and the source version in the key guarantees it will not.

### The link to the exit test

The roadmap bar is that stale data does not silently serve. The cache's invalidation rule is exactly
that bar, applied to the serving path: a named, enforced bound on staleness, tied to provenance.

## 6. Choosing and Combining

### The choosing rules

- Batch, bounded history, training-focused → offline materialization into the feature store.
- Live events, freshness-sensitive → streaming windows with exactly-once state.
- Shared consistency across instances → Redis; single-instance hot path → local LRU.
- Citation or correctness-critical → versioned keys, not just TTL.

### The pragmatic floor

At DevMate's scale, the floor is: a local or Redis LRU keyed by the model version, plus a tumbling batch
aggregation for the stats. The full streaming pipeline with exactly-once windows is justified only when a
live dashboard or a real-time feature demands it, which is the same batch-first default as Data
Engineering 08.

### The composition

The pieces compose: windows feed the stores, the stores feed the cache, and versioning binds them all to
their source. The feature pipeline is not a single tool but a chain of decisions, each of which this
curriculum has already named.

## Real-World Application

- Aggregating DevMate usage into tumbling per-minute counts for a cost dashboard.
- Caching query embeddings in Redis keyed by the embedding-model version, invalidating on a model bump.
- Using a local LRU for the single-instance hot path where a network round-trip is too slow.
- Versioning Athar's per-book passage counts by `source_version` so a re-ingest recomputes, not silently
  serves, the old count.

## Common Mistakes

1. **Wrong window type.** A correct number for the wrong question.
2. **Double-counting on retry.** A counter without exactly-once state inflates under crash.
3. **No invalidation rule.** A cache that serves stale answers indefinitely.
4. **TTL-only for correctness-critical data.** A citation cache that can serve a superseded source.
5. **Thundering herd on a hot key.** Every request recomputes at once after expiry.
6. **Unbounded cache growth.** No eviction, and memory climbs until failure.

## Key Takeaways

1. Tumbling, sliding, and session windows answer different questions; the choice is semantic.
2. Exactly-once aggregation is the counter's correctness requirement.
3. Every cache names its invalidation rule; versioned keys bound staleness by correctness.
4. Cache-aside is the simple pattern: check, compute-on-miss, store, invalidate on write.
5. Feature versioning plus lineage closes the loop from source change to cache invalidation.

## Self-Check Questions

1. Why is choosing a window type a correctness decision rather than an implementation detail?
2. What happens to a counter that is not exactly-once, and why?
3. What are the three common cache failure modes and their fixes?
4. Why is a TTL the wrong staleness bound for a citation corpus?
5. How do feature versioning and the cache key form a self-healing loop?

## Further Reading / Connections

- Data Engineering 08 (batch vs streaming) — windows, ordering, exactly-once.
- Data Engineering 12 (feature stores) — the stores these pipelines fill.
- Data Engineering 06 (provenance) — the source version in the cache key.
- Data Engineering 03 (idempotency) — the property a retried aggregation needs.
- `projects/04-ai-engineering/devmate/src/devmate/cache/` — the semantic cache this describes.
