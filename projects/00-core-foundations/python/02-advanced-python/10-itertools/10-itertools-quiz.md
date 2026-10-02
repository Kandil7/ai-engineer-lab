# Advanced Python 10: itertools — Quiz

> **Topic Overview**: Infinite, terminating, and combinatorial iterators as pipelines.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What defines an "infinite" iterator in itertools?**
- A) It loops forever
- B) `count`, `cycle`, `repeat` produce endless values until you stop them
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Must be bounded by `islice`/`takewhile`.</details>

### Question 2 — Easy
**What does `chain` do?**
- A) Sorts
- B) Concatenates iterables into one stream
- C) Groups
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Sequential concatenation.</details>

### Question 3 — Medium
**What does `groupby` require of the input?**
- A) Nothing
- B) It must be sorted by the grouping key
- C) It must be a list
- D) Hashable keys

<details><summary>Reveal Answer</summary>**B.** Otherwise groups split.</details>

### Question 4 — Medium
**What does `islice` do?**
- A) Sorts
- B) Slices an iterator without materialising it
- C) Caches
- D) Groups

<details><summary>Reveal Answer</summary>**B.** Lazy slicing.</details>

### Question 5 — Medium
**What does `product` produce?**
- A) A sum
- B) The Cartesian product of input iterables
- C) A chain
- D) A group

<details><summary>Reveal Answer</summary>**B.** Nested loops as a stream.</details>

### Question 6 — Hard
**Why must `groupby` consumers fully exhaust each group before advancing?**
- A) For speed
- B) Groups are generated lazily; the underlying iterator advances once you move on
- C) They need not
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Lazy group boundaries.</details>

### Question 7 — Hard
**What is a memory risk with `list(combinations(...))`?**
- A) None
- B) The result can be combinatorially huge; keep it as a lazy iterator
- C) It is faster
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Materialising explodes memory.</details>

### Question 8 — Hard
**What does `accumulate` do?**
- A) Sorts
- B) Yields running totals of a binary operation
- C) Groups
- D) Chains

<details><summary>Reveal Answer</summary>**B.** Prefix accumulation.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use itertools well. |
| 5-6 | Review groupby and islice. |
| < 5 | Re-read the lecture. |
