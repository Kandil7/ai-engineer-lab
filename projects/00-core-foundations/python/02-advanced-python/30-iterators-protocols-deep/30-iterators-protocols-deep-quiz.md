# Advanced Python 30: Iterators & Protocols Deep — Quiz

> **Topic Overview**: Dunder protocols, sequence/mapping ABCs, and the data-model contracts.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why does defining `__getitem__` alone make an object iterable?**
- A) It does not
- B) Python falls back to integer indexing until `IndexError`, without `__iter__`
- C) Because of `__len__`
- D) Because of `__contains__`

<details><summary>Reveal Answer</summary>**B.** The legacy iteration fallback.</details>

### Question 2 — Easy
**What is the `__hash__`/`__eq__` contract?**
- A) None
- B) Equal objects must have equal hashes; defining `__eq__` without `__hash__` makes it unhashable
- C) Hashing first
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Invariant for dict/set correctness.</details>

### Question 3 — Medium
**How does `@total_ordering` help?**
- A) Caches
- B) From `__eq__` and one comparison, it derives the rest
- C) Hashes
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Less boilerplate.</details>

### Question 4 — Medium
**What is `__contains__` for?**
- A) Iteration
- B) The `in` operator, letting you override containment cost
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Efficient membership.</details>

### Question 5 — Medium
**What does subclassing `collections.abc.Sequence` give you for free?**
- A) Hashing
- B) Mixin methods (`__contains__`, `__iter__`, `index`, `count`) from `__getitem__`/`__len__`
- C) Sorting
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Protocol mixins.</details>

### Question 6 — Hard
**Difference between `__getattr__` and `__getattribute__`?**
- A) None
- B) `__getattr__` is the fallback on a miss; `__getattribute__` intercepts every access
- C) `__getattr__` is faster
- D) They are opposites

<details><summary>Reveal Answer</summary>**B.** Miss vs all.</details>

### Question 7 — Hard
**Why can an infinite `__getattr__` recurse?**
- A) It cannot
- B) Accessing `self.x` inside it re-triggers `__getattr__` on a miss; use `object.__getattribute__`
- C) Because of `__slots__`
- D) Because of hashing

<details><summary>Reveal Answer</summary>**B.** Guard access.</details>

### Question 8 — Hard
**What does the iterator protocol require to be correct?**
- A) `__iter__` only
- B) `__next__` raising `StopIteration` at the end, and `__iter__` returning self
- C) `__len__`
- D) `__contains__`

<details><summary>Reveal Answer</summary>**B.** Termination contract.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You know the protocols. |
| 5-6 | Review dunder contracts. |
| < 5 | Re-read the lecture. |
