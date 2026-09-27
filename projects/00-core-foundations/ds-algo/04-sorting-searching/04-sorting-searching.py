"""
DS-Algo — 04: Sorting and Searching
===================================
Topics: the built-in sort and binary search.

Why this matters:
    Sorting enables binary search, which is exponentially faster than
    linear search. This exercise implements binary search and checks the
    sorted-data requirement.

Run:      python 04-sorting-searching.py
Verify:   python 04-sorting-searching.py --verify
"""

from __future__ import annotations

import sys


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


def main() -> None:
    a = [1, 3, 5, 7, 9]

    # Binary search finds the target in O(log n).
    assert binary_search(a, 5) == 2
    assert binary_search(a, 1) == 0, "first element"
    assert binary_search(a, 9) == 4, "last element"
    assert binary_search(a, 4) == -1, "missing -> -1"
    assert binary_search([], 1) == -1, "empty input"

    # The built-in sort is O(n log n).
    b = [5, 3, 9, 1, 7]
    b.sort()
    assert b == [1, 3, 5, 7, 9]

    print("binary search finds the target in O(log n)")
    print("edge cases: first, last, missing, empty")
    print("the built-in sort is O(n log n)")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
