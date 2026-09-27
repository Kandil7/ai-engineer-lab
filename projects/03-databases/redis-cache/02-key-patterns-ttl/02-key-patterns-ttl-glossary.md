# Redis 02: Key Patterns and TTL — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Key | The cache's address | user:123 |
| Key pattern | The encoded identity | namespace:id |
| Namespace | The prefix grouping a data type | user:, session: |
| TTL | The staleness bound per data type | 30 min |
| Eviction | Dropping entries when memory is full | LRU |
| Collision | Two data types sharing a key | prevented by namespace |
| Eviction policy | Which entries to drop | LRU, LFU, none |

---

## Alphabetical Glossary

### Collision

**Definition:** Two data types sharing a key. Prevented by namespaces —
`user:123` and `session:123` never collide.

**Example:**
```python
# user:123 vs session:123 -> different namespaces
```

**Related concepts:** Namespace

---

### Eviction

**Definition:** Dropping entries when memory is full. The policy decides
which entries go.

**Example:**
```python
# LRU drops the least recently used entry
```

**Related concepts:** Eviction policy

---

### Eviction policy

**Definition:** The rule for which entries to drop when memory is full:
least recently used, least frequently used, or no eviction.

**Example:**
```python
# maxmemory-policy allkeys-lru
```

**Related concepts:** Eviction

---

### Key

**Definition:** The cache's address: a string identifying an entry. The
pattern encodes the identity.

**Example:**
```python
# "user:123"
```

**Related concepts:** Key pattern

---

### Key pattern

**Definition:** The encoded identity of an entry: namespace:id. Consistent
patterns make keys predictable and debuggable.

**Example:**
```python
# user:{id}, session:{id}, rate:{ip}:{endpoint}
```

**Related concepts:** Key, Namespace

---

### Namespace

**Definition:** The prefix grouping a data type: `user:`, `session:`,
`rate:`. The collision guard.

**Example:**
```python
# "user:" groups all user-profile keys
```

**Related concepts:** Collision, Key pattern

---

### TTL

**Definition:** The staleness bound, set per data type. A profile lives 30
minutes; a session lives 24 hours.

**Example:**
```python
# SET user:123 value EX 1800
```

**Related concepts:** Key pattern

---

## Related Concepts

- **Cache strategies**: TTL bounds the strategy's staleness (topic 01)
- **Rate limiting**: rate keys with short TTLs (topic 03)
- **Pub/Sub**: channels, not keys (topic 04)

## Key Takeaways

1. The key pattern encodes the entry's identity.
2. TTL is set per data type.
3. Eviction policy is chosen deliberately.
4. Namespaces prevent collisions.
5. Consistent patterns make keys debuggable.