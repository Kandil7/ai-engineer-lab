# DS-Algo 01: Arrays and Strings

## Topic Overview

Arrays and strings are the most common data structures in practice, and the operations on them are
the ones you will write most often. The difference between using them well and badly is almost always
a complexity question: the same task can be linear or quadratic depending on whether you understand
what indexing, slicing, and string building actually cost.

This lecture covers indexing and slicing, the cost of common operations, the two-pointer pattern, the
list-versus-string choice, and the boundary conditions where off-by-one bugs live. It is the foundation
for every later data-structure topic, because most of them are built from arrays.

The practical skill is estimating the cost of an operation before writing it, so that the quadratic
version is not chosen by accident.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Index and slice arrays and strings correctly.
2. Analyze the cost of common operations.
3. Apply the two-pointer pattern.
4. Choose between lists and strings for a task.
5. Handle the boundary conditions that cause off-by-one bugs.
6. Estimate an operation's cost before writing it.

## Prerequisites

- Basic Python lists and strings.
- The idea of Big-O as growth rate.

---

## 1. Indexing and Slicing

### Indexing is O(1)

An array is a contiguous block of elements addressed by index. Indexing computes the address
directly, so it is O(1):

```python
a = [10, 20, 30, 40]
a[0]  # 10, O(1)
```

### Slicing is O(k)

A slice copies a range, so it costs the length of the slice:

```python
a[1:3]  # [20, 30], O(k) for k = 2
```

The copy is the subtle part: a slice is a new list, not a view. A loop that slices repeatedly copies
repeatedly, which turns an O(n) task into O(n^2).

### The exit test

The roadmap's exit test is that indexing and slicing are used correctly, which means knowing when a
slice copies and choosing indexing when a copy is not needed.

## 2. Operation Costs

### The costs

- **Append** to the end of a list is amortized O(1).
- **Insert at the front** is O(n), because every element shifts.
- **Search** an unsorted array is O(n); a sorted array is O(log n) with binary search (DS-Algo 04).
- **Membership** in a list is O(n); in a set it is O(1) (DS-Algo 02).

### Why the cost model decides

The cost model decides the data structure. Inserting at the front of a large list is the wrong
structure for a queue (use a deque); membership in a large list is the wrong structure for counting
(use a set or dict). Choosing by cost is the core skill.

### Estimating before writing

Estimate the cost before writing the loop. If the loop does an O(n) operation n times, it is O(n^2),
and that is usually a bug, not a feature.

## 3. The Two-Pointer Pattern

### The pattern

Two pointers scan an array from both ends or at different speeds. The pattern solves many problems in
one pass:

```python
def reverse_in_place(a: list[int]) -> list[int]:
    """Two pointers scan from both ends toward the middle."""
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i, j = i + 1, j - 1
    return a
```

### Why it works

The two pointers move toward each other, and the work is done when they meet. In-place reversal,
finding a pair that sums to a target in a sorted array, and removing duplicates all fall to this
pattern in O(n) instead of O(n^2).

### The exit test

The roadmap's exit test is that the two-pointer pattern is used. Recognizing when a problem has a
two-pointer solution is the skill; it converts a nested loop into a single pass.

## 4. Lists Versus Strings

### Strings are immutable

Strings are immutable in Python: every modification creates a new string, O(n) per operation. This
makes building a string in a loop O(n^2):

```python
# O(n^2): each += copies the whole string
s = ""
for w in words:
    s += w

# O(n): join builds once
s = " ".join(words)
```

### The fix

Collect into a list and join once. The join is O(n) because it computes the total length and builds
the result once, instead of copying a growing string each iteration.

### The exit test

The roadmap's exit test is that string building uses join. It is a small habit with a large effect on
loops that build text, which is common in parsing and report generation.

## 5. Off-by-One Errors

### The classic bug

Iterating one past the end or stopping one short. Off-by-one errors come from not being precise about
which indices are inclusive.

### The boundary conditions

The discipline is to check the boundaries explicitly:

- **Empty input:** the loop must not run, and the function must return something sensible.
- **Single element:** the loop must handle the case where the two pointers are equal or adjacent.
- **First and last index:** the endpoints must be included or excluded deliberately, not by accident.

### Testing the boundaries

Test empty, single-element, and endpoint cases for every array function. Most array bugs are boundary
bugs, and they are the cheapest to catch.

## 6. The Exercise

### What it models

The exercise implements two-pointer reversal, indexing and slicing, and join-based string building,
with assertions for the boundary cases:

```python
assert reverse_in_place([1, 2, 3, 4]) == [4, 3, 2, 1]
assert reverse_in_place([1]) == [1], "single element"
assert reverse_in_place([]) == [], "empty input"
assert build_string(["a", "b", "c"]) == "a b c"
```

### The lesson

The boundary assertions are the point: reversal works on the empty and single-element cases because
the loop condition (`i < j`) handles them without a special case.

## Real-World Application

- Reversing or partitioning a list in place with two pointers for an O(n) pass.
- Building report text with `join` instead of a concatenation loop.
- Choosing a deque over a list when the task inserts at the front.
- Testing array functions on empty and single-element input before trusting them.

## Common Mistakes

1. **Inserting at the front of a large list.** O(n) shift; use a deque.
2. **Building strings in a loop.** O(n^2); use `join`.
3. **Off-by-one in the loop bounds.** Endpoints wrong.
4. **Forgetting the empty-input case.** The function crashes or misbehaves.
5. **Slicing when indexing suffices.** An unnecessary copy.
6. **Membership in a list.** O(n); use a set.

## Key Takeaways

1. Indexing is O(1); slicing is O(k) because it copies.
2. Operation costs decide the data structure; estimate before writing the loop.
3. Two pointers solve many array problems in one pass.
4. Strings are immutable; build with `join`, not a loop.
5. Check the boundary conditions (empty, single, endpoints) for every array function.

## Self-Check Questions

1. Why is a slice O(k) rather than O(1)?
2. Why is inserting at the front of a list O(n), and what structure avoids it?
3. Give a problem the two-pointer pattern solves in one pass.
4. Why is building a string in a loop O(n^2), and what replaces it?
5. Which boundary cases should every array function handle?

## Further Reading / Connections

- DS-Algo 02 (hash maps) and 04 (sorting and searching) — the structures and algorithms built on arrays.
- `projects/00-core-foundations/python/06-data-structures-algorithms/` — the full DSA curriculum.
- `docs/reference/python-clean-code-checklist.md` — the Pythonic idioms.
