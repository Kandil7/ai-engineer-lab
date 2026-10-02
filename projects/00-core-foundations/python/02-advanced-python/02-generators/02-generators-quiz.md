# Advanced Python 02: Generators — Quiz

> **Topic Overview**: The iterator protocol, `yield`, delegation, and pipelines.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What two methods make an iterator?**
- A) `__enter__`/`__exit__`
- B) `__iter__`/`__next__`
- C) `__getitem__`/`__len__`
- D) `__call__`/`__init__`

<details><summary>Reveal Answer</summary>**B.** The iterator protocol.</details>

### Question 2 — Easy
**What does `yield` do?**
- A) Ends the function permanently
- B) Produces a value and pauses the function, resuming on the next request
- C) Sorts
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Suspends and resumes.</details>

### Question 3 — Medium
**What is the memory advantage of a generator over a list?**
- A) None
- B) It produces values lazily, so it does not materialise the whole sequence
- C) It is faster always
- D) It stores on disk

<details><summary>Reveal Answer</summary>**B.** O(1) working memory per item.</details>

### Question 4 — Medium
**What does `yield from` do?**
- A) Skips values
- B) Delegates to another iterable, forwarding values (and `send`/`throw`)
- C) Sorts
- D) Closes

<details><summary>Reveal Answer</summary>**B.** Delegation in one statement.</details>

### Question 5 — Medium
**What does `send()` allow?**
- A) Nothing new
- B) Sending a value into the generator at the paused `yield`
- C) Closing the generator
- D) Restarting it

<details><summary>Reveal Answer</summary>**B.** Two-way generators.</details>

### Question 6 — Hard
**Why is a generator exhausted after one full iteration?**
- A) It is a bug
- B) It is a single-use iterator; there is no rewind
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Re-iterating yields nothing.</details>

### Question 7 — Hard
**What does a generator pipeline of three stages cost in memory?**
- A) The full dataset
- B) One item at a time; the stages stream
- C) O(n²)
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Lazy composition.</details>

### Question 8 — Hard
**What does `throw()` do?**
- A) Stops iteration
- B) Raises an exception inside the generator at the paused `yield`
- C) Sends a value
- D) Closes it

<details><summary>Reveal Answer</summary>**B.** Error injection for cleanup protocols.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand generators. |
| 5-6 | Review delegation and generator methods. |
| < 5 | Re-read the lecture. |
