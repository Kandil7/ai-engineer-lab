"""
DS-Algo — 01: Arrays and Strings
================================
Topics: indexing, slicing, the two-pointer pattern, and string building.

Why this matters:
    Arrays and strings are the most common data structures. This exercise
    applies the two-pointer pattern and the join discipline.

Run:      python 01-arrays-strings.py
Verify:   python 01-arrays-strings.py --verify
"""

from __future__ import annotations

import sys


def reverse_in_place(a: list[int]) -> list[int]:
    """Two pointers scan from both ends toward the middle."""
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i, j = i + 1, j - 1
    return a


def build_string(words: list[str]) -> str:
    """Join is O(n); a loop of concatenation is O(n^2)."""
    return " ".join(words)


def main() -> None:
    # Two-pointer reverse works in place.
    assert reverse_in_place([1, 2, 3, 4]) == [4, 3, 2, 1]
    assert reverse_in_place([1]) == [1], "single element"
    assert reverse_in_place([]) == [], "empty input"

    # Indexing is O(1); slicing copies a range.
    a = [10, 20, 30, 40]
    assert a[0] == 10
    assert a[1:3] == [20, 30]

    # String building uses join, not a concatenation loop.
    assert build_string(["a", "b", "c"]) == "a b c"

    print("two-pointer reverse works in place, including edge cases")
    print("indexing is O(1); slicing copies a range")
    print("string building uses join, not a concatenation loop")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
