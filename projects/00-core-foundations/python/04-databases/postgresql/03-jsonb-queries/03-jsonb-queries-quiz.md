# PostgreSQL 03: JSONB Queries — Quiz

> **Topic Overview**: Extraction, containment, `json` vs `jsonb`, and GIN.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `->` return?**
- A) Text
- B) `jsonb`, chainable for deeper access
- C) An integer
- D) A boolean

<details><summary>Reveal Answer</summary>**B.** Still JSON.</details>

### Question 2 — Easy
**What does `->>` return?**
- A) `jsonb`
- B) Text, terminal for comparisons
- C) An array
- D) A path

<details><summary>Reveal Answer</summary>**B.** Extract as text.</details>

### Question 3 — Medium
**Why does `meta -> 'language' = 'python'` never match?**
- A) Wrong key
- B) The left side is `jsonb`, the right is text; types differ
- C) Slow
- D) Missing index

<details><summary>Reveal Answer</summary>**B.** The #1 JSONB bug.</details>

### Question 4 — Medium
**What does `@>` test?**
- A) Equality
- B) Containment: the document holds the given structure
- C) Existence
- D) Type

<details><summary>Reveal Answer</summary>**B.** Structure containment.</details>

### Question 5 — Medium
**Why is `jsonb` preferred to `json`?**
- A) Smaller
- B) Parsed binary: normalized and indexable instead of reparsed per read
- C) Faster writes
- D) Preserves whitespace

<details><summary>Reveal Answer</summary>**B.** Parsed and indexed.</details>

### Question 6 — Hard
**What does a GIN index accelerate?**
- A) Joins
- B) `@>`, `?`, and other containment/existence queries
- C) Sorting
- D) Aggregates

<details><summary>Reveal Answer</summary>**B.** The fast path.</details>

### Question 7 — Hard
**How do you prove the GIN index is used?**
- A) Timing only
- B) `EXPLAIN` showing a bitmap index scan on it
- C) Row counts
- D) Trust

<details><summary>Reveal Answer</summary>**B.** Plan proof.</details>

### Question 8 — Hard
**Why should join keys stay out of JSONB?**
- A) They cannot be stored
- B) Relational joins on extracted values are slow and unenforced
- C) Size
- D) Types

<details><summary>Reveal Answer</summary>**B.** Relations belong in columns.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You query JSONB well. |
| 5-6 | Review extraction types and containment. |
| < 5 | Re-read the lecture. |
