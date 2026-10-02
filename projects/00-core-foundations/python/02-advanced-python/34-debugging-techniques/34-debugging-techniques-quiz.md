# Advanced Python 34: Debugging Techniques — Quiz

> **Topic Overview**: Tracebacks, assertions, seeds, `faulthandler`, `pdb`, and bisection.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you read a Python traceback?**
- A) Top-down
- B) Bottom-up: the last line names the error and its site; the frames show the path
- C) Ignore it
- D) Middle first

<details><summary>Reveal Answer</summary>**B.** Error type and site at the end.</details>

### Question 2 — Easy
**What does `traceback.format_exc()` give you?**
- A) A cache
- B) The traceback as a string you can log
- C) A hash
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Loggable exception text.</details>

### Question 3 — Medium
**How do assertions help debug?**
- A) For speed
- B) They state assumptions; a failure pinpoints the first lie
- C) They cache
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Check invariants early.</details>

### Question 4 — Medium
**How do you debug nondeterminism?**
- A) Retry
- B) Freeze seeds (random, NumPy) and control ordering
- C) Cache
- D) Sort

<details><summary>Reveal Answer</summary>**B.** Make it reproducible.</details>

### Question 5 — Medium
**What does `faulthandler` do for a hang?**
- A) Kills the process
- B) Dumps the Python stack after a timeout, showing where it is stuck
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Stack dump on hang.</details>

### Question 6 — Hard
**What is the hypothesis-driven method?**
- A) Random edits
- B) State a hypothesis, design a test that distinguishes it, gather evidence, iterate
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Evidence, not guessing.</details>

### Question 7 — Hard
**How does bisection help?**
- A) It caches
- B) Binary-search the change history to find the commit that introduced the failure
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Narrow the cause fast.</details>

### Question 8 — Hard
**Why is `breakpoint()` preferable to scattering `print`s?**
- A) It is faster
- B) It pauses with full interactive access to state, no code edits needed
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Inspect without editing.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You debug systematically. |
| 5-6 | Review tracebacks, seeds, and pdb. |
| < 5 | Re-read the lecture. |
