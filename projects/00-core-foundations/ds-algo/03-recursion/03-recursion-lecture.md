# DS-Algo 03: Recursion

## 🎯 Topic Overview

Recursion solves a problem by solving a smaller version of itself. Every
recursive function has a base case that stops the recursion and a
recursive case that shrinks the problem. This lecture covers the two
cases, the call stack, and the recursion-vs-iteration choice.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write the base case and the recursive case
2. Trace the call stack
3. Explain the stack-depth limit
4. Convert recursion to iteration
5. Use memoization to avoid repeated work

---

## 1. The Two Cases

A recursive function has a base case that returns directly and a recursive
case that calls itself on a smaller input. The base case is the exit; the
recursive case is the progress. A missing base case recurses forever. The
roadmap's exit test: "recursion has a base case."

```python
def factorial(n):
    if n <= 1:
        return 1  # base case
    return n * factorial(n - 1)  # recursive case
```

## 2. The Call Stack

Each recursive call pushes a frame onto the call stack. The stack unwinds
as the base case returns. The depth is the number of nested calls. The
roadmap's exit test: "the call stack is understood."

## 3. The Depth Limit

The call stack has a limit. Deep recursion — thousands of frames — hits
the limit and raises a recursion error. The limit is the reason some
recursion is converted to iteration. The roadmap's exit test: "the
recursion depth is bounded."

## 4. Recursion vs Iteration

Anything recursive can be written iteratively. Iteration avoids the stack
limit but can be less readable. The choice is readability against depth:
recursion for naturally recursive problems, iteration for deep ones.

## 5. Memoization

Recursion can repeat work — Fibonacci recomputes the same values. Memoization
stores results in a hash map so each value is computed once. The roadmap's
exit test: "memoization avoids repeated work."

```python
memo = {}


def fib(n):
    if n in memo:
        return memo[n]
    ...
```

## Common Mistakes

- A missing base case (infinite recursion).
- Recursion too deep (stack overflow).
- No memoization (exponential repeated work).
- Recursion for a problem iteration solves more simply.
- Forgetting the stack unwinds on return.

## Key Takeaways

1. Base case exits; recursive case shrinks.
2. Each call pushes a stack frame.
3. Deep recursion hits the depth limit.
4. Iteration avoids the limit.
5. Memoization removes repeated work.