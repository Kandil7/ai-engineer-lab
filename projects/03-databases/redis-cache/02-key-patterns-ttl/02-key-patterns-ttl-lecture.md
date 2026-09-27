# Redis 02: Key Patterns and TTL

## 🎯 Topic Overview

A key is the cache's address. The key pattern encodes what the entry is;
the TTL bounds how long it lives. This lecture covers key naming, the TTL
per data type, and eviction.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design key patterns that encode the entry's identity
2. Set TTLs per data type
3. Explain eviction when memory is full
4. Avoid key collisions
5. Use namespaces to separate data types

---

## 1. Key Patterns

A key is a string that identifies an entry. The pattern encodes the
identity: `user:123`, `session:abc`, `rate:1.2.3.4:login`. The colon
separates the namespace from the id. A consistent pattern makes keys
predictable and debuggable. The roadmap's exit test: "keys follow a
consistent pattern."

```
user:{id}        session:{id}        rate:{ip}:{endpoint}
```

## 2. TTL per Data Type

Each data type has its own TTL. A user profile can live 30 minutes; a
session lives 24 hours; a rate-limit counter lives 1 minute. The TTL is
the staleness contract, set per type. The roadmap's exit test: "TTLs are
set per data type."

## 3. Eviction

When memory is full, Redis evicts entries. The eviction policy decides
which: least recently used, least frequently used, or no eviction (errors
on writes). The policy is chosen for the workload. The roadmap's exit
test: "the eviction policy is chosen deliberately."

## 4. Key Collisions

A key collision happens when two data types share a key. `user:123` and
`session:123` are different namespaces, so no collision. A flat key space
collides. The namespace is the collision guard.

## 5. Namespaces

Namespaces separate data types: `user:`, `session:`, `rate:`. A namespace
is a prefix that groups related keys. Namespaces make keys debuggable and
collision-free. The roadmap's exit test: "data types are namespaced."

## Common Mistakes

- Flat key space (collisions).
- One TTL for all data.
- No eviction policy (writes fail when full).
- Keys without a namespace.
- Inconsistent key patterns.

## Key Takeaways

1. The key pattern encodes the entry's identity.
2. TTL is set per data type.
3. Eviction policy is chosen deliberately.
4. Namespaces prevent collisions.
5. Consistent patterns make keys debuggable.