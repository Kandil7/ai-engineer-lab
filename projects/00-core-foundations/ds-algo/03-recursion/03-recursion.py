"""
DS-Algo — 03: Recursion
=======================
Topics: the base case, the recursive case, and memoization.

Why this matters:
    Recursion solves a problem by solving a smaller version of itself.
    This exercise writes the two cases and memoizes Fibonacci.

Run:      python 03-recursion.py
Verify:   python 03-recursion.py --verify
"""

from __future__ import annotations

import sys


def factorial(n: int) -> int:
    if n <= 1:
        return 1  # base case
    return n * factorial(n - 1)  # recursive case


def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """Memoized Fibonacci: each value is computed once."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def main() -> None:
    # The base case stops the recursion.
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

    # Memoized Fibonacci is linear, not exponential.
    assert fib_memo(10) == 55
    assert fib_memo(30) == 832040, "memoization keeps it fast"

    # The call stack unwinds: factorial(3) = 3 * 2 * 1.
    assert factorial(3) == 6

    print("base case stops the recursion; recursive case shrinks")
    print("memoized Fibonacci is linear, not exponential")
    print("the call stack unwinds as the base case returns")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
