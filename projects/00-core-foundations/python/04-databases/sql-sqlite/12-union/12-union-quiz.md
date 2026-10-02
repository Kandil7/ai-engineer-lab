# SQL SQLite 12: Union — Quiz

> **Topic Overview**: Stacking result sets, `ALL`, and set difference.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `UNION` combine?**
- A) Tables side by side
- B) Result sets vertically, removing duplicates
- C) Databases
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Stacked results.</details>

### Question 2 — Easy
**What does `UNION ALL` skip?**
- A) Sorting
- B) The dedup pass, keeping duplicates and running faster
- C) The second query
- D) Aliases

<details><summary>Reveal Answer</summary>**B.** No dedup.</details>

### Question 3 — Medium
**When is `ALL` strictly better?**
- A) Never
- B) When branches cannot overlap, so dedup is pure cost
- C) Always
- D) For small sets

<details><summary>Reveal Answer</summary>**B.** Disjoint branches.</details>

### Question 4 — Medium
**What does `EXCEPT` return?**
- A) Overlap
- B) Rows in the first query but not the second
- C) The union
- D) An error

<details><summary>Reveal Answer</summary>**B.** Set difference.</details>

### Question 5 — Medium
**What must branches align on?**
- A) Names
- B) Column count and compatible types
- C) Order
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Shape compatibility.</details>

### Question 6 — Hard
**Where does `ORDER BY` go in a union?**
- A) In each branch
- B) Once, at the end, over the combined result
- C) Nowhere
- D) In the first branch

<details><summary>Reveal Answer</summary>**B.** Final ordering.</details>

### Question 7 — Hard
**Whose column names appear in the output?**
- A) The last branch
- B) The first branch
- C) Aliases always
- D) None

<details><summary>Reveal Answer</summary>**B.** First branch names.</details>

### Question 8 — Hard
**How do you find signups who never purchased?**
- A) `INNER JOIN`
- B) `signups EXCEPT purchasers` on the id
- C) `UNION`
- D) `GROUP BY`

<details><summary>Reveal Answer</summary>**B.** Difference query.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You combine sets correctly. |
| 5-6 | Review `ALL`, `EXCEPT`, and alignment. |
| < 5 | Re-read the lecture. |
