# DS-Algo 04: Sorting and Searching — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Timsort | The built-in sort, O(n log n) | a.sort() |
| Binary search | Halving the range, O(log n) | sorted data only |
| Linear search | Scanning every element, O(n) | any data |
| bisect | The built-in binary search | bisect_left |
| Sort once | O(n log n) paid once, O(log n) searches | many lookups |
| Off-by-one | The binary search bounds bug | lo <= hi |
| Insertion point | Where an element belongs | bisect_left |

---

## Alphabetical Glossary

### Binary search

**Definition:** Halving the range toward the target each step. O(log n),
but requires sorted data.

**Example:**
```python
lo, hi = 0, len(a) - 1
while lo <= hi:
    mid = (lo + hi) // 2
```

**Related concepts:** Linear search, Timsort

---

### bisect

**Definition:** The built-in binary search. `bisect_left` finds the
insertion point in O(log n).

**Example:**
```python
import bisect

bisect.bisect_left(a, target)
```

**Related concepts:** Binary search

---

### Insertion point

**Definition:** The position where an element belongs in a sorted
sequence. Found by bisect in O(log n).

**Example:**
```python
bisect.bisect_left([1, 3, 5], 4)  # 1
```

**Related concepts:** bisect

---

### Linear search

**Definition:** Scanning every element until the target is found. O(n),
works on any data.

**Example:**
```python
target in a  # O(n)
```

**Related concepts:** Binary search

---

### Off-by-one

**Definition:** The binary search bounds bug. The loop condition `lo <= hi`
and the mid adjustment must be exact.

**Example:**
```python
# lo = mid + 1 or hi = mid - 1, never lo = mid
```

**Related concepts:** Binary search

---

### Sort once

**Definition:** Paying O(n log n) once so many searches cost O(log n)
each. The justification for sorting.

**Example:**
```python
a.sort()  # once
# then binary search many times
```

**Related concepts:** Timsort, Binary search

---

### Timsort

**Definition:** The built-in sort: O(n log n) worst case, O(n) on
nearly-sorted input.

**Example:**
```python
a.sort()
```

**Related concepts:** Binary search

---

## Related Concepts

- **Arrays**: sorting and searching operate on arrays (topic 01)
- **Hash maps**: the O(1) alternative to binary search (topic 02)
- **Recursion**: merge sort is recursive (topic 03)

## Key Takeaways

1. The built-in sort is O(n log n).
2. Sorting enables O(log n) binary search.
3. Binary search halves the range each step.
4. Sort once, search many times.
5. Use the built-ins.