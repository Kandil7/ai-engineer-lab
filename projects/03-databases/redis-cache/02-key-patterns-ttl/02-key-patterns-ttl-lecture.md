# Redis 02: Key Patterns and TTL

## Topic Overview

A key is the cache's address, and its pattern encodes what the entry is. A consistent key pattern makes
the cache predictable and debuggable; an inconsistent one makes it a mystery. The TTL, set per data
type, bounds how long each entry lives and therefore how stale the cache can be.

This lecture covers key naming, namespaces that prevent collisions, the TTL per data type, and the
eviction policy that decides what happens when memory fills.

The core insight is that the key is a design artifact, not a string you make up at the call site. A
namespaced pattern and a per-type TTL are what make a cache maintainable, and both are decided when the
cache is designed, not when it is used.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design key patterns that encode an entry's identity.
2. Use namespaces to prevent collisions.
3. Set TTLs per data type.
4. Explain the eviction policy.
5. Keep key patterns consistent across the codebase.
6. Explain why TTL is the staleness contract.

## Prerequisites

- Redis 01 (cache strategies) for the cache this keys.

---

## 1. Key Patterns

### The pattern

A key is a string that identifies an entry, and its pattern encodes the identity:

```text
user:{id}        session:{id}        rate:{ip}:{endpoint}
```

The colon separates the namespace from the id. A consistent pattern makes keys predictable and
debuggable, and it makes a key recognizable when you see one in a log.

### Why consistency

An inconsistent key space (sometimes `user:123`, sometimes `user-123`) produces cache misses because
the same logical entry maps to different keys, and it makes debugging painful because the key cannot be
predicted. The pattern is a contract for the cache.

### The exit test

The roadmap's exit test is that keys follow a consistent pattern, which means a reader can predict the
key from the identity.

## 2. Namespaces

### What they do

Namespaces separate data types: `user:`, `session:`, `rate:`. They are prefixes that group related keys:

```python
assert key("user", "123") != key("session", "123"), "namespaces prevent collisions"
```

### Why they matter

`user:123` and `session:123` are different entries; without the namespace they would collide, and one
data type would overwrite the other. The namespace is the collision guard.

### The exit test

The roadmap's exit test is that data types are namespaced, which is what keeps distinct data from
sharing an address.

## 3. TTL per Data Type

### The idea

Each data type has its own TTL, set to its staleness tolerance:

```python
assert ttl_for("user") == 1800  # 30 minutes
assert ttl_for("session") == 86400  # 24 hours
assert ttl_for("rate") == 60  # 1 minute
```

A user profile tolerates 30 minutes of staleness; a rate-limit counter is meaningless after a minute.

### Why per type

One TTL for all data means some entries expire too soon (extra misses) and some too late (stale reads).
The TTL per type encodes the actual tolerance, which is a product decision.

### The exit test

The roadmap's exit test is that TTLs are set per data type, which is what makes the staleness bound
meaningful.

## 4. Eviction

### What it is

When memory is full, Redis evicts entries according to a policy:

- **LRU (least recently used):** evict the least recently accessed.
- **LFU (least frequently used):** evict the least frequently accessed.
- **noeviction:** reject writes when full.

### Why the policy matters

The policy decides what survives under memory pressure. LRU suits a working-set cache; LFU suits data
with stable popular items; noeviction is right when losing an entry is worse than a failed write.

### The exit test

The roadmap's exit test is that the eviction policy is chosen deliberately, because the default may not
match the workload.

## 5. Key Design as a Contract

### The registry of patterns

The key patterns are documented in one place (a module of `key(namespace, id)` functions), so every
caller uses the same pattern. Scattered string concatenation is how the key space drifts.

### The link to invalidation

A key pattern makes invalidation possible: invalidating `session:abc` requires knowing the key's shape.
A consistent pattern means invalidation can target the right entries.

### The exit test

The roadmap's exit test is that keys are consistent and namespaced, which is what makes invalidation and
debugging possible.

## 6. The Exercise

### What it models

The exercise models namespaced keys and per-type TTLs, and shows that a flat key space collides.

### The assertions

```python
assert user_key != session_key, "namespaces prevent collisions"
assert ttl_for("user") == 1800 and ttl_for("rate") == 60
assert flat_user == flat_session, "flat keys collide"
```

The last assertion makes the collision concrete: a flat key space cannot tell the two data types apart.

## Real-World Application

- Namespacing rate-limit counters as `rate:{ip}:{endpoint}` so two endpoints have separate limits.
- Setting a 24-hour TTL on sessions and a 30-minute TTL on profiles, matching each tolerance.
- Documenting the key patterns in one module so every caller uses the same shape.
- Choosing LRU eviction for a working-set cache.

## Common Mistakes

1. **Flat key space.** Collisions between data types.
2. **One TTL for all data.** Some entries stale, some expire too early.
3. **No eviction policy chosen.** The default may not fit the workload.
4. **Keys without a namespace.** Data types share addresses.
5. **Inconsistent key patterns.** Misses and undebuggable keys.
6. **String concatenation at call sites.** The key space drifts.

## Key Takeaways

1. The key pattern encodes the entry's identity.
2. Namespaces prevent collisions between data types.
3. TTL is set per data type, matching its staleness tolerance.
4. The eviction policy is chosen deliberately.
5. Consistent, documented key patterns make the cache debuggable and invalidatable.

## Self-Check Questions

1. Why does a consistent key pattern matter for debugging and invalidation?
2. Why do namespaces prevent collisions?
3. Why is the TTL set per data type rather than globally?
4. How does the eviction policy decide what survives under memory pressure?
5. Why keep key patterns in one module rather than at call sites?

## Further Reading / Connections

- Redis 01 (cache strategies) and 03 (rate limiting) — the strategies and the counters these keys serve.
- RAG System 06 (caching) — the version-key discipline.
- `docs/cheat-sheets/qdrant.md` — related infrastructure reference.
