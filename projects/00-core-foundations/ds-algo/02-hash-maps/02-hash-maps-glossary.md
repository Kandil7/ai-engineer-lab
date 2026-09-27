# DS-Algo 02: Hash Maps — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hash map | Key-value store with O(1) average lookup | dict |
| Hash function | Maps a key to a bucket | hash(key) |
| Collision | Two keys in the same bucket | bucket scan |
| Set | Keys with no values, membership tests | dedup |
| Counter | A map from item to count | counts[x] |
| Two-sum | The complement-in-map pattern | one pass O(n) |
| Unhashable | Cannot be a key (mutable) | list |

---

## Alphabetical Glossary

### Collision

**Definition:** Two keys hashing to the same bucket. The bucket stores
both; the lookup scans it. Rare with a good hash; pathological hashes
degrade to O(n).

**Example:**
```python
# two keys, one bucket -> the lookup scans the bucket
```

**Related concepts:** Hash function

---

### Counter

**Definition:** A map from item to count. Counting in one pass.

**Example:**
```python
counts[x] = counts.get(x, 0) + 1
```

**Related concepts:** Hash map

---

### Hash function

**Definition:** Maps a key to a bucket. The lookup computes the hash and
goes straight to the bucket.

**Example:**
```python
hash("a")  # -> a bucket index
```

**Related concepts:** Collision

---

### Hash map

**Definition:** A key-value store with O(1) average lookup. The workhorse
for counting, deduplication, and membership.

**Example:**
```python
d = {"a": 1, "b": 2}
```

**Related concepts:** Hash function, Set

---

### Set

**Definition:** A hash map with no values. Membership tests and
deduplication.

**Example:**
```python
seen = set(items)
```

**Related concepts:** Hash map

---

### Two-sum

**Definition:** The canonical pattern: for each element, check whether its
complement is in the map. One pass, O(n).

**Example:**
```python
if target - x in seen:
    return [seen[target - x], i]
```

**Related concepts:** Hash map

---

### Unhashable

**Definition:** Cannot be a key because it is mutable. Lists and dicts are
unhashable; tuples and strings are hashable.

**Example:**
```python
# d[[1, 2]] = 3  # TypeError: unhashable
```

**Related concepts:** Hash map

---

## Related Concepts

- **Arrays**: the alternative for ordered access (topic 01)
- **Recursion**: memoization uses hash maps (topic 03)
- **Sorting**: the alternative for finding pairs (topic 04)

## Key Takeaways

1. Hash maps give O(1) average lookup.
2. Collisions are rare with a good hash.
3. Counting and deduplication are one-pass.
4. A set for membership; a map for values.
5. Two-sum is the canonical hash-map pattern.