# Embeddings 03: Caching — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Cache key | Model + content hash | embedding:{model}:{hash} |
| Content hash | SHA-256 of the normalized text | same text, same key |
| L1 memory | Process memory, fastest, lost on restart | dict |
| L2 Redis | Fast, survives restarts, TTL-bounded | embedding:{hash} |
| L3 vector store | The stored vector, permanent | Qdrant |
| Cache-aside | Hit returns, miss embeds and stores | the flow |
| Hit rate | The fraction served from cache | cost lever |

---

## Alphabetical Glossary

### Cache key

**Definition:** The identity of a cached embedding: model plus content
hash. The model is in the key because a different model produces a
different vector.

**Example:**
```python
f"embedding:{model}:{sha256(normalize(text))}"
```

**Related concepts:** Content hash

---

### Cache-aside

**Definition:** The flow: hash the text, check the cache, return on a hit,
embed and store on a miss.

**Example:**
```python
# GET key -> HIT return | MISS -> embed -> SET -> return
```

**Related concepts:** Cache key

---

### Content hash

**Definition:** SHA-256 of the normalized text. The same text produces the
same hash and the same key.

**Example:**
```python
sha256(normalize(text))
```

**Related concepts:** Cache key

---

### Hit rate

**Definition:** The fraction of embedding requests served from cache. The
cost lever — a high rate means few API calls.

**Example:**
```python
# 80% of requests never reach the API
```

**Related concepts:** Cache-aside

---

### L1 memory

**Definition:** Process memory: the fastest layer, lost on restart.

**Example:**
```python
# a dict in the process
```

**Related concepts:** L2 Redis, L3 vector store

---

### L2 Redis

**Definition:** The Redis layer: fast, survives restarts, TTL-bounded.

**Example:**
```python
# SET embedding:{hash} vector EX 86400
```

**Related concepts:** L1 memory

---

### L3 vector store

**Definition:** The stored vector in Qdrant: the permanent cache. A stored
point never needs re-embedding.

**Example:**
```python
# the point's vector is the cache
```

**Related concepts:** L2 Redis

---

## Related Concepts

- **Batch processing**: cached texts skip the batch (topic 02)
- **Redis caching**: the L2 layer (redis-cache 01)
- **Quality evaluation**: cached embeddings are consistent (topic 04)

## Key Takeaways

1. The key carries the model and the content hash.
2. Layers: memory, Redis, the vector store.
3. Cache-aside: hit returns, miss embeds and stores.
4. The key invalidates on model or content change.
5. The hit rate is the cost lever.