# DS-Algo 03: Recursion — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Base case | Returns directly, stops recursion | n <= 1 |
| Recursive case | Calls itself on a smaller input | n * factorial(n-1) |
| Call stack | The frames of nested calls | unwinds on return |
| Depth limit | The stack's maximum depth | recursion error |
| Memoization | Storing results to avoid repeated work | fib memo |
| Iteration | The loop alternative to recursion | avoids the limit |
| Stack overflow | Too many nested frames | deep recursion |

---

## Alphabetical Glossary

### Base case

**Definition:** The case that returns directly, stopping the recursion. The
exit. A missing base case recurses forever.

**Example:**
```python
if n <= 1:
    return 1
```

**Related concepts:** Recursive case

---

### Call stack

**Definition:** The frames of nested calls. Each call pushes a frame; the
stack unwinds as the base case returns.

**Example:**
```python
# factorial(3) -> factorial(2) -> factorial(1) -> unwind
```

**Related concepts:** Depth limit

---

### Depth limit

**Definition:** The call stack's maximum depth. Deep recursion hits it and
raises a recursion error.

**Example:**
```python
# RecursionError: maximum recursion depth exceeded
```

**Related concepts:** Call stack

---

### Iteration

**Definition:** The loop alternative to recursion. Avoids the stack limit
but can be less readable.

**Example:**
```python
for i in range(1, n + 1):
    result *= i
```

**Related concepts:** Recursive case

---

### Memoization

**Definition:** Storing computed results in a hash map so each value is
computed once. Removes exponential repeated work.

**Example:**
```python
if n in memo:
    return memo[n]
```

**Related concepts:** Recursive case

---

### Recursive case

**Definition:** The case that calls itself on a smaller input. The
progress toward the base case.

**Example:**
```python
return n * factorial(n - 1)
```

**Related concepts:** Base case

---

### Stack overflow

**Definition:** Too many nested frames exceeding the depth limit. The
failure of unbounded recursion.

**Example:**
```python
# deep recursion -> RecursionError
```

**Related concepts:** Depth limit

---

## Related Concepts

- **Arrays**: recursion often processes arrays (topic 01)
- **Hash maps**: memoization uses hash maps (topic 02)
- **Sorting**: merge sort is recursive (topic 04)

## Key Takeaways

1. Base case exits; recursive case shrinks.
2. Each call pushes a stack frame.
3. Deep recursion hits the depth limit.
4. Iteration avoids the limit.
5. Memoization removes repeated work.