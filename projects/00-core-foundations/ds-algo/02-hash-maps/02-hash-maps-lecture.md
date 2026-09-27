# DS-Algo 02: Hash Maps

## 🎯 Topic Overview

A hash map stores key-value pairs with O(1) average lookup. It is the
workhorse for counting, deduplication, and membership tests. This lecture
covers the hash function, collisions, and the patterns that use hash maps.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the O(1) average lookup
2. Explain collisions and their cost
3. Use hash maps for counting and deduplication
4. Choose between a set and a map
5. Recognize the two-sum pattern

---

## 1. The Hash Function

A hash function maps a key to a bucket. The lookup computes the hash and
goes straight to the bucket — O(1) on average. The roadmap's exit test:
"hash maps are used for O(1) lookups."

```python
d = {"a": 1, "b": 2}
d["a"]  # 1, O(1) average
```

## 2. Collisions

Two keys can hash to the same bucket — a collision. The bucket stores
both; the lookup scans the bucket. With a good hash and enough buckets,
collisions are rare and the average stays O(1). A pathological hash
degrades the map to O(n).

## 3. Counting and Deduplication

Hash maps count occurrences and remove duplicates in one pass. A counter
is a map from item to count; a set is a map with no values. The roadmap's
exit test: "counting and deduplication use hash maps."

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

## 4. Set vs Map

A set stores keys with no values — membership tests. A map stores
key-value pairs. A set is the right tool when only membership matters; a
map when a value must be associated. The roadmap's exit test: "the right
structure is chosen."

## 5. The Two-Sum Pattern

The classic pattern: for each element, check whether its complement is in
the map. One pass, O(n). The roadmap's exit test: "the two-sum pattern is
recognized."

```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

## Common Mistakes

- Using a list for membership tests (O(n)).
- A map when a set suffices.
- Ignoring the collision cost.
- Mutable keys (unhashable).
- Forgetting the complement check.

## Key Takeaways

1. Hash maps give O(1) average lookup.
2. Collisions are rare with a good hash.
3. Counting and deduplication are one-pass.
4. A set for membership; a map for values.
5. Two-sum is the canonical hash-map pattern.