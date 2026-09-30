# DS-Algo 02: Hash Maps

## Topic Overview

A hash map stores key-value pairs with O(1) average lookup, and it is the workhorse for counting,
deduplication, membership tests, and the many problems that reduce to "have I seen this before?". It
turns a nested loop into a single pass, which is why it appears in the canonical interview patterns
and in production code constantly.

This lecture covers the hash function, collisions and their cost, counting and deduplication, the
set-versus-map choice, and the two-sum pattern that is the canonical example of the technique.

The core skill is recognizing when a hash map replaces a linear scan. Any time you find yourself
searching a collection repeatedly, the answer is usually to build a map and look up instead.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the O(1) average lookup.
2. Explain collisions and why they rarely matter in practice.
3. Use hash maps for counting and deduplication.
4. Choose between a set and a map.
5. Recognize and apply the two-sum pattern.
6. Explain why hashability constrains the key type.

## Prerequisites

- DS-Algo 01 (arrays and strings) for the cost model.

---

## 1. The Hash Function

### The mechanism

A hash function maps a key to a bucket. The lookup computes the hash and goes straight to the bucket,
so it is O(1) on average:

```python
d = {"a": 1, "b": 2}
d["a"]  # 1, O(1) average
```

### Why average

The O(1) is an average, not a guarantee. It holds when the hash spreads keys evenly and the table is
not too full. A pathological hash degrades the map to O(n), because every key lands in one bucket
(Data Engineering 05 hashes for a different purpose, content identity, but the hashing idea is shared).

### Hashability

Keys must be hashable, which means immutable in practice: strings, numbers, and tuples of hashable
values work; lists and dicts do not. A mutable key's hash could change, which would make it
unfindable.

## 2. Collisions

### What they are

Two keys can hash to the same bucket, which is a collision. The bucket stores both, and the lookup
scans the bucket. With a good hash and enough buckets, collisions are rare and the average stays O(1).

### Why they rarely matter

Python's dict and set use a good hash and resize as they fill, so collisions are handled without the
caller noticing. The practical consequence is that you can assume O(1) average and not worry about the
collision mechanics unless you are designing a hash table.

### The pathological case

A hash that maps every key to one bucket degrades the map to O(n) per lookup, which is the worst case.
It is rare in practice for well-chosen keys and worth knowing as the theoretical floor.

## 3. Counting and Deduplication

### Counting

A counter is a map from item to count, built in one pass:

```python
def count(items: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return counts
```

The `get(x, 0) + 1` idiom is the standard counting pattern; `collections.Counter` does the same.

### Deduplication

A set (a map with no values) deduplicates in one pass:

```python
assert set(["a", "b", "a"]) == {"a", "b"}
```

### Why one pass

Counting and deduplication are one pass because the hash map remembers what it has seen. The naive
alternative (nested loops comparing each item to every other) is O(n^2), which the map removes.

## 4. Set Versus Map

### The choice

- A **set** stores keys with no values, for membership and deduplication.
- A **map** stores key-value pairs, for counting and association.

### Why it matters

Using a map when a set suffices wastes memory and suggests a value you do not use. Using a set when a
value must be associated forces a second structure. The right structure is the one that matches the
task: membership, set; association, map.

### Membership

Membership in a list is O(n); membership in a set is O(1). The difference is the difference between a
fast pipeline and a slow one, because membership tests are everywhere.

## 5. The Two-Sum Pattern

### The problem

Given a list and a target, find the two elements that sum to the target. The naive solution is a
nested loop, O(n^2).

### The hash-map solution

For each element, check whether its complement is already in the map, then store the element:

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """For each element, check whether its complement is in the map."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None
```

One pass, O(n). The map remembers what was seen so the complement check is O(1).

### Why it generalizes

Two-sum is the canonical "have I seen the complement?" pattern. Many problems reduce to it: pair
matching, substring with a property, grouping by a computed key. Recognizing the pattern is the skill.

## 6. The Exercise

### What it models

The exercise implements two-sum, counting, and deduplication, with assertions for the found, not-found,
and duplicate cases:

```python
assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([1, 2, 3], 99) is None, "no pair -> None"
assert count(["a", "b", "a", "c", "a"]) == {"a": 3, "b": 1, "c": 1}
assert set(["a", "b", "a"]) == {"a", "b"}
```

### The lesson

The not-found case (`None`) is as important as the found case: the function must signal absence, not
return a misleading pair.

## Real-World Application

- Counting query-term frequencies for an inverted index (Arabic NLP 03).
- Deduplicating passages by content hash (Data Engineering 05).
- Membership tests over a large set of ids instead of scanning a list.
- Grouping results by a computed key for aggregation.

## Common Mistakes

1. **Using a list for membership tests.** O(n); use a set.
2. **A map when a set suffices.** Wasted memory and a misleading value.
3. **Ignoring the collision cost.** Usually fine, but know the worst case.
4. **Mutable keys.** Unhashable and unfindable after mutation.
5. **Forgetting the complement check in two-sum.** The pattern collapses.
6. **Not handling the not-found case.** Returns a misleading result.

## Key Takeaways

1. Hash maps give O(1) average lookup; the cost is average, not guaranteed.
2. Collisions are rare with a good hash and handled transparently.
3. Counting and deduplication are one pass because the map remembers.
4. A set for membership; a map for association.
5. Two-sum is the canonical hash-map pattern: check the complement, then store.

## Self-Check Questions

1. Why is the hash-map lookup O(1) average rather than O(1) guaranteed?
2. Why must keys be hashable, and what does that forbid?
3. When should you use a set rather than a map?
4. Why is two-sum O(n) with a map and O(n^2) without?
5. Give a production task that is a two-sum-style complement lookup.

## Further Reading / Connections

- DS-Algo 01 (arrays and strings) and 04 (sorting and searching) — the surrounding structures.
- Data Engineering 05 (deduplication) — content hashing in a pipeline.
- Arabic NLP 03 (lexical retrieval) — counting term frequencies for an index.
- `projects/00-core-foundations/python/06-data-structures-algorithms/` — the full DSA curriculum.
