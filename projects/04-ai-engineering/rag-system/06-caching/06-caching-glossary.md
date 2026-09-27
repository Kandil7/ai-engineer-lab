# RAG System 06: Caching — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Cache key | Query + prompt version + corpus version | exact-match identity |
| Semantic caching | Returning cached answers for similar queries | embedding similarity |
| Similarity threshold | The semantic-cache precision-recall dial | 0.9 = strict |
| Invalidation | Dropping entries when inputs change | corpus/prompt version |
| Hit rate | Fraction of queries served from cache | cost lever |
| Stale answer | A cached answer from a changed corpus | version-keyed miss |
| Validate-before-cache | Never cache bad answers | schema + grounded |

---

## Alphabetical Glossary

### Cache key

**Definition:** The identity of a cache entry: normalized query plus prompt
version and corpus version. A change in any component misses.

**Example:**
```python
cache_key = (normalize(query), prompt_version, corpus_version)
```

**Related concepts:** Invalidation, Stale answer

---

### Hit rate

**Definition:** The fraction of queries served from cache. A first-class
cost lever — a 30% hit rate cuts a third of LLM spend.

**Example:**
```python
# 30% of queries never reach the LLM
```

**Related concepts:** Semantic caching, Cost

---

### Invalidation

**Definition:** Dropping cache entries when their inputs change. The cache
key carries the versions, so a change naturally misses.

**Example:**
```python
# corpus v2 -> v1 entries miss, never served stale
```

**Related concepts:** Cache key, Stale answer

---

### Semantic caching

**Definition:** Returning a cached answer when a new query is similar enough
to a cached one — same intent, different wording. Embedding-based.

**Example:**
```python
# "كيف أتعلم" and "كيف أتعلم البرمجة" -> same cached answer
```

**Related concepts:** Similarity threshold, Hit rate

---

### Similarity threshold

**Definition:** The semantic-cache dial: above it, a similar query reuses the
cached answer. Too low serves wrong answers; too high misses savings.

**Example:**
```python
# threshold 0.9: strict, few hits, safe
```

**Related concepts:** Semantic caching

---

### Stale answer

**Definition:** A cached answer from a changed corpus or prompt. Prevented by
version-keyed cache entries.

**Example:**
```python
# corpus updated, old answer still cached -> version key misses
```

**Related concepts:** Cache key, Invalidation

---

### Validate-before-cache

**Definition:** The rule that only schema-valid, grounded, non-abstained
answers are cached. Never cache a bad answer.

**Example:**
```python
# abstained or malformed -> not cached
```

**Related concepts:** Semantic caching, Abstention

---

## Related Concepts

- **Abstention**: abstained answers are never cached (topic 05)
- **Cost control**: hit rate as the cost lever (LLMOps)
- **Prompt versioning**: the version in the cache key

## Key Takeaways

1. Cache keys carry query + versions.
2. Semantic caching needs a tuned threshold.
3. Invalidate on change.
4. Never cache bad answers; measure the hit rate.