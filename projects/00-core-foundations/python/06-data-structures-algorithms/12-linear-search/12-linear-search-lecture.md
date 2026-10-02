# Lecture 12: Linear Search — Data Structures and Algorithms

## Topic Overview

Linear search is the simplest searching algorithm: it checks each element in a collection,
one after another, until it finds the target or runs out of elements. It is the search that
requires no preparation — no sorting, no index, no hashing — and it works on any sequence
you can iterate, including linked lists where random access is impossible.

It matters because it is the baseline every other search is measured against, and because it
is often the *only* correct choice: data that is unsorted, data that changes every query, and
data in a linked list all force a sequential scan. Understanding why it is O(n), and where
that cost can be trimmed, is the foundation for binary search, hash tables, and every
retrieval system you will build later.

What makes it hard is not the loop; it is the arithmetic of its cost and the constant
factors. Off-by-one bounds, an early exit that is wrong on unsorted data, and a sentinel that
mutates and fails to restore an array are the real pitfalls. This lecture builds the simple
version first, then the variants that shave comparisons, and states clearly when each is safe.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement basic linear search and return `-1` (not `None`) on a miss.
2. State best, average, and worst-case time and the O(1) space cost.
3. Write a sentinel search that removes the bounds check and correctly restores the array.
4. Apply an early-exit scan safely on sorted data.
5. Find min, max, and all occurrences in a single pass.
6. Search a 2D matrix and a substring using the same sequential idea.
7. Explain when interpolation or ternary search beats plain linear search.

## Prerequisites

- Python lists, `range`, `len`, indexing, and slicing.
- Big-O notation and the difference between time and space complexity (Lecture 01).
- The idea of an in-place mutation and why it can surprise callers.

## 1. Basic Linear Search

The core idea: walk the collection from left to right and compare each element to the target.
Return the index on the first match; return `-1` after the loop ends to signal absence.

```python
def linear_search(arr, target):
    """Search for target in array. Returns index or -1."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


arr = [10, 23, 45, 70, 11, 15]
print(linear_search(arr, 70))  # 3
print(linear_search(arr, 99))  # -1
```

**Analogy.** Looking for a name on an unsorted guest list by reading it top to bottom. There
is no shortcut; you must read until you find it or reach the end.

**When it fails.** It cannot exploit order. On a sorted million-element array, a scan still
checks every element on a miss, where binary search would need about twenty comparisons. It
also cannot be parallelised simply in Python because the loop is sequential.

**Exit-test connection.** The return convention (`-1` for absence) and the single-pass shape
are exactly what the other search routines in this module reuse.

## 2. Best, Average, and Worst Cases

Linear search is O(n) in time and O(1) in extra space. The three cases differ by where the
target sits:

| Case | Scenario | Comparisons | Time |
|------|----------|-------------|------|
| Best | target is the first element | 1 | O(1) |
| Average | target is somewhere in the middle | ~n/2 | O(n) |
| Worst | target is last or absent | n | O(n) |

The important detail is that the **worst case of a miss is a full scan**. Any "not found"
answer costs the maximum, which is why callers who only need existence should prefer a set or
a hash map when they can afford the memory.

**When it fails.** Quoting "O(n/2)" as if it were a different complexity class — constants are
dropped, so the average is still O(n).

## 3. Sentinel Linear Search

Each iteration of the basic loop performs two comparisons: `i < n` and `arr[i] == target`. The
sentinel technique removes the bounds check by placing the target in the last slot as a guard,
then scanning without a bound and restoring the slot afterward.

```python
def sentinel_search(arr, target):
    """Linear search with sentinel - eliminates boundary check."""
    n = len(arr)
    last = arr[n - 1]
    arr[n - 1] = target  # place sentinel

    i = 0
    while arr[i] != target:  # no i < n check needed
        i += 1

    arr[n - 1] = last  # restore the original element

    if i < n - 1 or arr[n - 1] == target:
        return i
    return -1
```

The final condition resolves the ambiguity: if the loop stopped because the sentinel itself
was the target, the element may or may not have existed before the last slot, so we check.

**When it fails.** If the function raises before the restore line, the caller's array is left
mutated — a silent data-corruption bug. In Python, the `while` loop is slower than the C-level
iteration of the basic version, so the "optimization" often does not win in practice; measure
before adopting it. This is a classic case where the textbook saving is real in C and marginal
in Python.

## 4. Early Exit on Sorted Data

If the data is sorted, a scan can stop as soon as it passes the target, because no later
element can be smaller.

```python
def linear_search_sorted(arr, target):
    """Optimized for sorted arrays - stop early."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            return -1  # passed the target; impossible to find
    return -1


sorted_arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(linear_search_sorted(sorted_arr, 23))  # 5
print(linear_search_sorted(sorted_arr, 10))  # -1, stops at 12
```

**When it fails.** Applying this to an unsorted array returns `-1` for elements that are
present but out of order. Guard it with a sortedness assertion or a comment, so no caller
reuses it on arbitrary input.

## 5. Finding Min, Max, and All Occurrences

The same single-pass shape answers questions that are not equality searches.

```python
def find_min_max(arr):
    """Find both min and max in one pass. O(n)."""
    if not arr:
        return None, None
    if len(arr) == 1:
        return arr[0], arr[0]

    min_val, max_val = (arr[0], arr[1]) if arr[0] < arr[1] else (arr[1], arr[0])

    for i in range(2, len(arr), 2):
        if i + 1 < len(arr):
            local_min, local_max = min(arr[i], arr[i + 1]), max(arr[i], arr[i + 1])
        else:
            local_min = local_max = arr[i]
        min_val, max_val = min(min_val, local_min), max(max_val, local_max)

    return min_val, max_val


def find_all_occurrences(arr, target):
    """Find every index of target. O(n)."""
    return [i for i, val in enumerate(arr) if val == target]
```

Pairing elements (compare two at a time, then compare the smaller to the running min and the
larger to the running max) reduces comparisons from `2n` to about `3n/2` — the standard
tournament bound.

**When it fails.** Iterating `arr` while another thread or the same function mutates it can
skip elements. Sort or copy first when mutation is possible.

## 6. Searching 2D Arrays and Strings

A nested loop scans a matrix in O(m·n). If rows and columns are each sorted, starting at the
top-right corner and walking down or left finds the target in O(m + n).

```python
def search_2d_sorted(matrix, target):
    """Row- and column-sorted matrix. O(m + n)."""
    if not matrix:
        return None
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1  # top-right corner

    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return (row, col)
        elif matrix[row][col] > target:
            col -= 1  # too big: move left
        else:
            row += 1  # too small: move down
    return None
```

Substring search is the same sequential idea with a slice comparison: O(n·m) because each of
the `n - m + 1` alignments may compare up to `m` characters.

**When it fails.** Slicing `text[i:i+m]` allocates a new string each iteration; for large
texts prefer `str.find` or an algorithm like KMP. Interpolation search assumes a *uniform*
distribution; on skewed data its estimate can be worse than binary search.

## 7. Interpolation and Ternary Search

Plain linear search ignores value. Interpolation search estimates the target's position from
its value and the range, giving O(log log n) on uniformly distributed data. Ternary search
splits the range into three instead of two.

```python
def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high and arr[low] <= target <= arr[high]:
        if low == high:
            return low if arr[low] == target else -1
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1


def ternary_search(arr, target):
    """Divide into three parts. O(log3 n)."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3
        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2
        if target < arr[mid1]:
            high = mid1 - 1
        elif target > arr[mid2]:
            low = mid2 + 1
        else:
            low, high = mid1 + 1, mid2 - 1
    return -1
```

Both require a sorted array; on unsorted data they are incorrect, not merely slow. Ternary
search does the same asymptotic work as binary search (log base 3) while making more
comparisons per step, so binary search is usually preferred for arrays.

**When it fails.** Interpolation search divides by `arr[high] - arr[low]`; if all values are
equal, this divides by zero. Guard with the `low == high` and range check shown above.

## Real-World Application

Linear search is the workhorse where order is unavailable or rebuilding is too costly:
streaming logs scanned for an event id, a linked list of tool results scanned for a name,
a small configuration list checked on every request. The min/max single-pass appears in
metrics aggregation and in normalisation routines. Interpolation-style estimation appears in
index statistics, where a database estimates a row's location from a key's value before
reading. In the DevMate retrieval path, exact metadata filters fall back to sequential
filtering when no index covers the field — knowing the cost tells you when that is acceptable
and when it must become an indexed lookup.

## Common Mistakes to Avoid

1. **Returning `None` instead of `-1`.** Callers check `result == -1`; pick one convention and
   keep it across the module.
2. **Off-by-one bounds.** `range(len(arr) - 1)` skips the last element. Use `range(len(arr))`.
3. **Using early-exit on unsorted data.** It reports "not found" for values present out of
   order.
4. **Forgetting to restore the sentinel.** A raised exception leaves the array mutated.
5. **Assuming sentinel search is faster in Python.** The interpreter loop usually loses to the
   built-in C iteration of the basic scan.
6. **Dividing by zero in interpolation search.** Equal values at the ends break the estimate.
7. **Slicing huge strings in a loop.** Each slice allocates; use `str.find`.

## Key Takeaways

- Linear search is O(n) time, O(1) space, and works on any iterable, sorted or not.
- Best case is O(1); the worst case for an absent target is a full scan.
- The sentinel trick removes the bounds check but risks leaving the array mutated.
- Sorted data enables an early exit that halves average work but must never be used on
  unsorted input.
- Prefer a set, hash map, or binary search when their preconditions hold.

## Self-Check Questions

1. Why is the average case O(n) and not O(n/2)?
2. What two comparisons does the sentinel version remove, and what does it cost in safety?
3. On a sorted array, how many elements can the early-exit version check on a miss?
4. Why does the min/max tournament use about 3n/2 comparisons instead of 2n?
5. When is interpolation search a poor choice?
6. What happens if `13-...` callers pass an unsorted array to `linear_search_sorted`?

## Further Reading / Connections

- **Next:** Lecture 13, Binary Search — the O(log n) alternative once data is sorted.
- **Related:** Lecture 06, Hash Tables — O(1) average lookup at the cost of memory.
- **Related:** Lecture 05, Linked Lists — linear search is the only option without random
  access.
- **Exercise:** `12-linear-search.py` implements every variant above; run it and compare the
  timings table it prints.
