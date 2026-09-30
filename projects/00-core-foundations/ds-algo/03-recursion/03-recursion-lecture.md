# DS-Algo 03: Recursion

## Topic Overview

Recursion solves a problem by solving a smaller version of itself. Every recursive function has a base
case that stops the recursion and a recursive case that shrinks the problem, and every recursive
function's behavior can be understood by tracing the call stack. It is the natural way to express
tree-shaped problems and a common source of two bugs: the missing base case and the repeated work.

This lecture covers the two cases, the call stack, the depth limit, the recursion-versus-iteration
choice, and memoization as the fix for exponential repeated work.

The practical skill is recognizing when recursion is the clear expression of a problem (trees, divide
and conquer, backtracking) and when iteration is safer (deep or flat problems), and knowing that
memoization turns an exponential recursion into a linear one.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write the base case and the recursive case.
2. Trace the call stack of a recursive function.
3. Explain the stack-depth limit and why it bounds recursion.
4. Convert recursion to iteration when depth is a risk.
5. Use memoization to remove repeated work.
6. Choose recursion or iteration for a given problem.

## Prerequisites

- DS-Algo 02 (hash maps) for the memoization store.

---

## 1. The Two Cases

### The base case

The base case returns directly without recursing. It is the exit condition, and it is what stops the
recursion:

```python
def factorial(n: int) -> int:
    if n <= 1:
        return 1  # base case
    return n * factorial(n - 1)  # recursive case
```

### The recursive case

The recursive case calls the function on a smaller input, making progress toward the base case. A
recursive case that does not shrink the problem recurses forever.

### The missing base case

A missing or unreachable base case is the classic recursion bug: the function recurses until the stack
overflows. Every recursive function needs a base case that is actually reachable for every valid input.

## 2. The Call Stack

### Frames

Each recursive call pushes a frame onto the call stack. The stack unwinds as the base case returns:

```text
factorial(3)
  factorial(2)
    factorial(1) -> returns 1
  returns 2 * 1 = 2
returns 3 * 2 = 6
```

### Why trace it

Tracing the stack turns recursion from magic into a sequence of calls and returns. When a recursive
function misbehaves, the trace is how you find which call returned the wrong value.

### The unwinding

The results are computed on the way back up: the base case returns a value, and each frame combines
it. Understanding the unwinding is what makes a recursive function predictable.

## 3. The Depth Limit

### What it is

The call stack has a limit. Deep recursion, thousands of frames, hits the limit and raises a recursion
error:

```python
# Python's default recursion limit is around 1000 frames
```

### Why it bounds recursion

Every frame consumes stack memory, so unbounded recursion is unbounded memory. The limit is a
protection, and it is why recursion is not the right tool for a flat problem with a large n.

### The exit test

The roadmap's exit test is that the recursion depth is bounded. For a problem that could be deep
(a long list, a deep tree), bound the depth or use iteration.

## 4. Recursion Versus Iteration

### The equivalence

Anything recursive can be written iteratively:

```python
def factorial_iter(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

### The tradeoff

Iteration avoids the stack limit and is often faster; recursion is more readable for naturally
recursive problems (trees, divide and conquer, backtracking). Choose by the problem's shape and the
depth it might reach.

### The rule

Recursion for tree-shaped and divide-and-conquer problems; iteration for flat problems or when depth
is a risk. The choice is readability against depth.

## 5. Memoization

### The problem

Recursion can repeat work. Naive Fibonacci recomputes the same values exponentially:

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)  # O(2^n): recomputes
```

Every node in the recursion tree recomputes its subtree, so the same value is computed many times.

### The fix

Memoization stores each result in a map so it is computed once:

```python
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
```

The memo (a hash map, DS-Algo 02) turns the exponential recursion into a linear one.

### Why it works

The overlapping subproblems are computed once and reused. This is the same idea as caching in a
pipeline (RAG System 06): recognize repeated work and store the result.

## 6. The Exercise

### What it models

The exercise implements factorial (the two cases), memoized Fibonacci, and an assertion that
memoization keeps the computation fast:

```python
assert factorial(0) == 1
assert factorial(5) == 120
assert fib_memo(10) == 55
assert fib_memo(30) == 832040, "memoization keeps it fast"
```

### The lesson

`fib_memo(30)` is instant with memoization and impractically slow without it. The assertion makes the
difference concrete: same result, radically different cost.

## Real-World Application

- Walking a tree structure (an AST, a filesystem) where recursion is the natural expression.
- Divide-and-conquer algorithms (merge sort, DS-Algo 04) that split and recurse.
- Memoizing overlapping subproblems to turn exponential recursion into linear.
- Converting a deep recursion to iteration when the depth would overflow the stack.

## Common Mistakes

1. **A missing base case.** Infinite recursion and a stack overflow.
2. **Recursion too deep.** The depth limit is hit.
3. **No memoization.** Exponential repeated work.
4. **Recursion for a flat problem.** Iteration is clearer and safer.
5. **Forgetting the stack unwinds on return.** Misreading the result order.
6. **A recursive case that does not shrink the input.** No progress to the base case.

## Key Takeaways

1. The base case exits; the recursive case shrinks the problem.
2. Each call pushes a frame; results are combined on the way back up.
3. Deep recursion hits the stack-depth limit, which bounds recursion.
4. Iteration avoids the limit; choose by the problem's shape and depth.
5. Memoization removes repeated work, turning exponential recursion into linear.

## Self-Check Questions

1. What two cases does every recursive function need, and what is the bug if one is missing?
2. Describe the call stack for a small recursive call.
3. Why does the stack-depth limit bound recursion, and when do you use iteration instead?
4. Why is naive Fibonacci exponential, and how does memoization fix it?
5. When is recursion the clearer choice over iteration?

## Further Reading / Connections

- DS-Algo 04 (sorting and searching) — merge sort and binary search, both recursive.
- DS-Algo 02 (hash maps) — the memoization store.
- RAG System 06 (caching) — the same repeated-work idea at the system level.
- `projects/00-core-foundations/python/06-data-structures-algorithms/` — the full DSA curriculum.
