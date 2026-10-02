# Advanced Python 18: Unit Testing — Quiz

> **Topic Overview**: pytest, fixtures, parametrization, and isolated tests.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a unit test?**
- A) A full-system test
- B) A fast, isolated test of one small behavior
- C) A load test
- D) A manual check

<details><summary>Reveal Answer</summary>**B.** Small and isolated.</details>

### Question 2 — Easy
**How does pytest identify tests?**
- A) Any function
- B) Files `test_*.py` and functions named `test_*`
- C) Classes only
- D) Decorators

<details><summary>Reveal Answer</summary>**B.** Naming conventions.</details>

### Question 3 — Medium
**What is a fixture for?**
- A) Caching
- B) Providing shared setup/teardown and injecting it into tests
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Reusable setup.</details>

### Question 4 — Medium
**What does `@pytest.mark.parametrize` do?**
- A) Caches
- B) Runs one test over many input/output cases
- C) Locks
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Table-driven cases.</details>

### Question 5 — Medium
**Why must unit tests avoid network and disk?**
- A) For speed only
- B) I/O makes them slow and flaky; use mocks/fakes for boundaries
- C) It is required
- D) They cannot

<details><summary>Reveal Answer</summary>**B.** Determinism and speed.</details>

### Question 6 — Hard
**What makes a test trustworthy?**
- A) It passes
- B) It fails when the behavior is broken (a test that cannot fail is worthless)
- C) It is long
- D) It mocks everything

<details><summary>Reveal Answer</summary>**B.** Assert real behavior.</details>

### Question 7 — Hard
**Why pin external responses in offline tests?**
- A) For speed
- B) To make the test hermetic and reproducible, independent of the network
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Recorded fixtures.</details>

### Question 8 — Hard
**What is a common pitfall with over-mocking?**
- A) Speed
- B) The test verifies the mock, not the code; the real integration is untested
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Mocks can test nothing real.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write good tests. |
| 5-6 | Review fixtures and parametrize. |
| < 5 | Re-read the lecture. |
