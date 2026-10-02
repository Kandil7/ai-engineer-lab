# SQL SQLite 07: Order By — Quiz

> **Topic Overview**: Direction, multi-column sorts, NULLs, and stable pages.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you sort descending?**
- A) `SORT BY x DOWN`
- B) `ORDER BY x DESC`
- C) `ORDER x -`
- D) `REVERSE x`

<details><summary>Reveal Answer</summary>**B.** `DESC`.</details>

### Question 2 — Easy
**Can directions mix across columns?**
- A) No
- B) Yes, direction is per column
- C) Only two columns
- D) Only ascending first

<details><summary>Reveal Answer</summary>**B.** Per-column direction.</details>

### Question 3 — Medium
**Why end a sort with a unique key?**
- A) Style
- B) To make the order fully deterministic when earlier keys tie
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Tiebreaker.</details>

### Question 4 — Medium
**Where do NULLs sort by default?**
- A) Always last
- B) Engine-dependent; state `NULLS FIRST/LAST` when it matters
- C) They error
- D) They are dropped

<details><summary>Reveal Answer</summary>**B.** Explicit placement.</details>

### Question 5 — Medium
**Why does pagination need `ORDER BY`?**
- A) Style
- B) Without it, pages overlap and skip rows
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Order is the page.</details>

### Question 6 — Hard
**What is wrong with `ORDER BY 2`?**
- A) Nothing
- B) Positional references break when the select list changes
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Name columns.</details>

### Question 7 — Hard
**How can an index serve `ORDER BY`?**
- A) It cannot
- B) A matching composite index returns rows in order, skipping the sort
- C) It caches
- D) It sorts twice

<details><summary>Reveal Answer</summary>**B.** Order from the index.</details>

### Question 8 — Hard
**Why is unordered output worse than random?**
- A) It is not
- B) It looks stable until the plan changes, then silently shifts
- C) It is slow
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Arbitrary, not random.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You sort deterministically. |
| 5-6 | Review tiebreakers and NULLs. |
| < 5 | Re-read the lecture. |
