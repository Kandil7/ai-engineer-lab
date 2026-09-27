# DS-Algo 01: Arrays and Strings

## 🎯 Topic Overview

Arrays and strings are the most common data structures in practice. This
lecture covers indexing, slicing, the two-pointer pattern, and the
complexity of common operations.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Index and slice arrays and strings
2. Analyze the cost of common operations
3. Use the two-pointer pattern
4. Choose between lists and strings
5. Avoid the common off-by-one errors

---

## 1. Indexing and Slicing

An array is a contiguous block of elements addressed by index. Indexing is
O(1) — the address is computed, not searched. Slicing copies a range,
which is O(k) for a slice of length k. The roadmap's exit test: "indexing
and slicing are used correctly."

```python
a = [10, 20, 30, 40]
a[0]  # 10, O(1)
a[1:3]  # [20, 30], O(k)
```

## 2. Operation Costs

Appending to a list is amortized O(1); inserting at the front is O(n)
because every element shifts. Searching an unsorted array is O(n); a
sorted array can be searched in O(log n) with binary search. The cost
model decides the data structure.

## 3. The Two-Pointer Pattern

Two pointers scan an array from both ends or at different speeds. The
pattern solves many problems in one pass: reversing, finding pairs,
removing duplicates. The roadmap's exit test: "the two-pointer pattern is
used."

```python
def reverse(a):
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i, j = i + 1, j - 1
```

## 4. Lists vs Strings

Strings are immutable in Python — every modification creates a new string,
O(n) per operation. Building a string in a loop is O(n^2); joining a list
is O(n). The roadmap's exit test: "string building uses join."

## 5. Off-by-One Errors

The classic bug: iterating one past the end or stopping one short. The
discipline is to check the boundary conditions explicitly — empty input,
single element, and the last index.

## Common Mistakes

- Inserting at the front of a large list (O(n) shift).
- Building strings in a loop (O(n^2)).
- Off-by-one in the loop bounds.
- Forgetting the empty-input case.
- Slicing when indexing suffices.

## Key Takeaways

1. Indexing is O(1); slicing is O(k).
2. Operation costs decide the data structure.
3. Two pointers solve many problems in one pass.
4. Strings are immutable; build with join.
5. Check the boundary conditions explicitly.