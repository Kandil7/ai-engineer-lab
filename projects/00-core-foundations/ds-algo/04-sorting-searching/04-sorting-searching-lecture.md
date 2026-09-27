# DS-Algo 04: Sorting and Searching

## 🎯 Topic Overview

Sorting orders data; searching finds data. The two are linked: a sorted
array enables binary search, which is exponentially faster than linear
search. This lecture covers the sort costs, binary search, and when
sorting is worth it.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Compare the common sort costs
2. Explain why sorting enables binary search
3. Implement binary search
4. Choose between linear and binary search
5. Use the built-in sort

---

## 1. The Sort Costs

The common sorts: O(n log n) for the good ones (merge, quick, the built-in
Timsort), O(n^2) for the simple ones (bubble, insertion). The built-in
sort is Timsort — O(n log n) worst case, O(n) on nearly-sorted input. The
roadmap's exit test: "the built-in sort is used."

```python
a.sort()  # Timsort, O(n log n)
```

## 2. Sorting Enables Binary Search

A sorted array can be searched in O(log n) by halving the range each step.
An unsorted array requires O(n) linear search. Sorting once costs O(n log
n); many searches then cost O(log n) each. The roadmap's exit test:
"binary search is used on sorted data."

## 3. Binary Search

Binary search compares the middle element, then halves the range toward
the target. Each step eliminates half the remaining elements. The
roadmap's exit test: "binary search is implemented correctly."

```python
def binary_search(a, target):
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

## 4. Linear vs Binary

Linear search is O(n) and works on any data. Binary search is O(log n)
but requires sorted data. The choice: sort once and search many times, or
search rarely on unsorted data. The roadmap's exit test: "the right
search is chosen."

## 5. The Built-In Tools

Python's sort and bisect handle the mechanics. `bisect_left` finds the
insertion point in O(log n). The discipline is to use the built-ins and
reserve hand-rolled sorts for learning.

## Common Mistakes

- Binary search on unsorted data (wrong results).
- Hand-rolling a sort when the built-in exists.
- Off-by-one in the binary search bounds.
- Sorting when linear search suffices.
- Forgetting the empty-input case.

## Key Takeaways

1. The built-in sort is O(n log n).
2. Sorting enables O(log n) binary search.
3. Binary search halves the range each step.
4. Sort once, search many times.
5. Use the built-ins.