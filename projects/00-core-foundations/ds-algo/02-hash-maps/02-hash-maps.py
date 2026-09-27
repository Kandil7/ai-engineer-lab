"""
DS-Algo — 02: Hash Maps
=======================
Topics: O(1) lookups, counting, deduplication, and the two-sum pattern.

Why this matters:
    Hash maps are the workhorse for counting, deduplication, and
    membership. This exercise applies the two-sum pattern.

Run:      python 02-hash-maps.py
Verify:   python 02-hash-maps.py --verify
"""

from __future__ import annotations

import sys


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """For each element, check whether its complement is in the map."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None


def count(items: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return counts


def main() -> None:
    # Two-sum finds the pair in one pass.
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([1, 2, 3], 99) is None, "no pair -> None"

    # Counting is one pass.
    assert count(["a", "b", "a", "c", "a"]) == {"a": 3, "b": 1, "c": 1}

    # A set deduplicates.
    assert set(["a", "b", "a"]) == {"a", "b"}

    print("two-sum finds the pair in one pass, O(n)")
    print("counting is one pass with a hash map")
    print("a set deduplicates")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
