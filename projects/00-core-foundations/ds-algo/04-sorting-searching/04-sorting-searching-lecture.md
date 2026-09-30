# DS-Algo 04: Sorting and Searching

## Topic Overview

Sorting orders data; searching finds data. The two are linked by a fact worth internalizing: a sorted
array enables binary search, which is exponentially faster than a linear scan. The cost of sorting
once is repaid by every subsequent search, which is why sort-once-search-many is a recurring pattern.

This lecture covers the common sort costs, why sorting enables binary search, how to implement binary
search correctly, the linear-versus-binary choice, and using the built-in tools.

The practical skills are knowing that the built-in sort is the right default, that binary search
requires sorted data and the halving discipline, and that the boundary conditions of binary search are
where its bugs live.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compare the common sort costs.
2. Explain why sorting enables binary search.
3. Implement binary search correctly, including its boundaries.
4. Choose between linear and binary search.
5. Use the built-in sort and `bisect`.
6. Explain when sorting is worth its cost.

## Prerequisites

- DS-Algo 01 (arrays and strings) for the slicing and indexing model.
- DS-Algo 03 (recursion) for the recursive view of the algorithms.

---

## 1. The Sort Costs

### The classes

The common sorts fall into two classes:

- **O(n log n):** merge sort, quicksort (average), and the built-in Timsort.
- **O(n^2):** the simple sorts (bubble, insertion, selection).

### The built-in

Python's built-in sort is Timsort: O(n log n) worst case and O(n) on nearly sorted input. It is the
right default; hand-rolled sorts are for learning, not for production.

```python
b = [5, 3, 9, 1, 7]
b.sort()
assert b == [1, 3, 5, 7, 9]
```

### The exit test

The roadmap's exit test is that the built-in sort is used. It is faster, correct, and maintained; a
hand-rolled sort is a bug waiting to happen.

## 2. Sorting Enables Binary Search

### The link

A sorted array can be searched in O(log n) by halving the range each step. An unsorted array can only
be searched linearly, O(n).

### The math

```text
n = 1,000,000
linear search:  up to 1,000,000 comparisons
binary search:  about 20 comparisons
```

That is the exponential gap: doubling n adds 1 to binary search's steps and doubles linear search's.

### The trade

Sorting once costs O(n log n); many searches then cost O(log n) each. If you search the same data
often, sorting pays for itself quickly. If you search rarely, linear search may be cheaper.

## 3. Binary Search

### The algorithm

Compare the middle element, then halve the range toward the target:

```python
def binary_search(a: list[int], target: int) -> int:
    """Halve the range toward the target. Requires sorted data."""
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### The boundaries

The boundaries are where binary search bugs live:

- `lo <= hi` versus `lo < hi`: the inclusive comparison matters for finding the last element.
- `lo = mid + 1` and `hi = mid - 1`: moving past `mid` avoids an infinite loop.
- The empty input: `lo = 0`, `hi = -1`, so the loop does not run and it returns `-1`.

### The exit test

The roadmap's exit test is that binary search is implemented correctly, which means correct on the
first element, the last element, a missing element, and the empty input.

## 4. Linear Versus Binary

### The choice

- **Linear search** is O(n) and works on any data, sorted or not.
- **Binary search** is O(log n) but requires sorted data.

### The decision

Sort once and search many times, or search rarely on unsorted data. The decision is a cost
calculation, not a preference: estimate the number of searches, compare `n log n + k log n` (sort
then binary) against `k n` (linear each time).

### The precondition

Binary search on unsorted data gives wrong results silently; it does not raise. This is why the
sorted precondition is a contract (Data Engineering 02): the caller must guarantee it, and the
function assumes it.

## 5. The Built-In Tools

### Sort and bisect

Python's sort handles the sorting, and `bisect` handles the binary search:

```python
import bisect
i = bisect.bisect_left(a, target)   # insertion point, O(log n)
```

`bisect_left` finds where a value would be inserted to keep the list sorted, which is the building
block for membership, range queries, and insertion into a sorted list.

### The discipline

Use the built-ins. They are correct, tested, and fast. Reserve hand-rolled sorts and searches for
learning the algorithm, not for shipping.

### The range queries

Once sorted, `bisect` answers range queries (find all elements between x and y) by locating two
insertion points. That is another payoff of the sorted invariant.

## 6. The Exercise

### What it models

The exercise implements binary search with boundary assertions and uses the built-in sort:

```python
assert binary_search(a, 5) == 2
assert binary_search(a, 1) == 0, "first element"
assert binary_search(a, 9) == 4, "last element"
assert binary_search(a, 4) == -1, "missing -> -1"
assert binary_search([], 1) == -1, "empty input"
```

### The lesson

The boundary assertions are the point: the first element, the last element, a missing element, and the
empty input are the cases where binary search bugs surface.

## Real-World Application

- Binary search over a sorted list of ids or timestamps for O(log n) lookup.
- Sorting a result set by relevance once so repeated lookups are cheap.
- Using `bisect` for range queries (all passages between two pages) in a sorted index.
- Choosing linear search when the data is small or searched once.

## Common Mistakes

1. **Binary search on unsorted data.** Silent wrong results.
2. **Hand-rolling a sort when the built-in exists.** Slower and buggier.
3. **Off-by-one in the bounds.** `lo <= hi` and `mid ± 1` must be right.
4. **Sorting when linear search suffices.** The sort cost is not repaid.
5. **Forgetting the empty-input case.** An index error or wrong result.
6. **Assuming binary search raises on unsorted input.** It silently misbehaves.

## Key Takeaways

1. The built-in sort is O(n log n) and is the default; simple sorts are O(n^2) and for learning only.
2. Sorting enables O(log n) binary search, an exponential improvement over linear scan.
3. Binary search's bugs live in its boundaries; test first, last, missing, and empty.
4. Sort once, search many times, or search rarely on unsorted data; the choice is arithmetic.
5. Use the built-in sort and `bisect`; hand-roll only to learn.

## Self-Check Questions

1. Why is the built-in sort the right default over a hand-rolled one?
2. How much faster is binary search than linear search at n = 1,000,000?
3. What are the two boundary conditions in binary search, and what bug does each prevent?
4. When is linear search the better choice despite being O(n)?
5. Why is the sorted precondition a contract, and what happens when it is violated?

## Further Reading / Connections

- DS-Algo 01 (arrays and strings) and 03 (recursion) — the surrounding structures and the recursive sorts.
- `projects/00-core-foundations/python/06-data-structures-algorithms/` — the full DSA curriculum.
- `docs/reference/python-clean-code-checklist.md` — the idiomatic Python.
