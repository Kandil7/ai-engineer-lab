# DS-Algo 01: Arrays and Strings — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Array | A contiguous block addressed by index | a[0] |
| Indexing | O(1) address computation | a[3] |
| Slicing | Copying a range, O(k) | a[1:3] |
| Two-pointer | Scanning from both ends or speeds | reverse |
| Amortized O(1) | Append cost averaged over operations | list.append |
| Immutable | Cannot be modified in place | str |
| Off-by-one | Iterating one past or short | boundary bug |

---

## Alphabetical Glossary

### Amortized O(1)

**Definition:** The cost of an operation averaged over many operations.
Appending to a list is amortized O(1) even though occasional resizes cost
more.

**Example:**
```python
a.append(x)  # amortized O(1)
```

**Related concepts:** Array

---

### Array

**Definition:** A contiguous block of elements addressed by index. Indexing
is O(1) because the address is computed, not searched.

**Example:**
```python
a = [10, 20, 30, 40]
```

**Related concepts:** Indexing, Slicing

---

### Immutable

**Definition:** Cannot be modified in place. Strings are immutable in
Python — every modification creates a new string.

**Example:**
```python
s = s + "x"  # creates a new string, O(n)
```

**Related concepts:** Array

---

### Indexing

**Definition:** Accessing an element by its position. O(1) — the address is
computed.

**Example:**
```python
a[0]  # 10
```

**Related concepts:** Array

---

### Off-by-one

**Definition:** The classic bug of iterating one past the end or stopping
one short. Checked by testing the boundary conditions.

**Example:**
```python
# for i in range(len(a)):  # correct
# for i in range(len(a) + 1):  # off by one
```

**Related concepts:** Array

---

### Slicing

**Definition:** Copying a range of elements. O(k) for a slice of length k.

**Example:**
```python
a[1:3]  # [20, 30]
```

**Related concepts:** Array

---

### Two-pointer

**Definition:** Scanning an array from both ends or at different speeds.
Solves reversing, pair-finding, and deduplication in one pass.

**Example:**
```python
i, j = 0, len(a) - 1
```

**Related concepts:** Array

---

## Related Concepts

- **Hash maps**: the alternative for fast lookups (topic 02)
- **Recursion**: the alternative to iterative scans (topic 03)
- **Sorting**: sorted arrays enable binary search (topic 04)

## Key Takeaways

1. Indexing is O(1); slicing is O(k).
2. Operation costs decide the data structure.
3. Two pointers solve many problems in one pass.
4. Strings are immutable; build with join.
5. Check the boundary conditions explicitly.