# FastAPI 42: Security Testing — Quiz

> **Topic Overview**: Auth bypass matrices, fuzzing, scans, and threat models.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the auth bypass matrix?**
- A) A password list
- B) Every protected route tested as anonymous, wrong user, and wrong role
- C) A firewall
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Enumerate access cases.</details>

### Question 2 — Easy
**What finds crashes at boundaries?**
- A) Unit tests
- B) Fuzzing with malformed, huge, or hostile inputs
- C) Reviews
- D) Logs

<details><summary>Reveal Answer</summary>**B.** Adversarial inputs.</details>

### Question 3 — Medium
**What do static and dependency scans catch?**
- A) Runtime bugs
- B) Known-vulnerable patterns and packages before deploy
- C) Logic errors
- D) Performance

<details><summary>Reveal Answer</summary>**B.** Shift-left scanning.</details>

### Question 4 — Medium
**What does threat-modeling an endpoint produce?**
- A) Code
- B) The assets, actors, abuse paths, and mitigations for one route
- C) Logs
- D) Metrics

<details><summary>Reveal Answer</summary>**B.** Focused risk list.</details>

### Question 5 — Medium
**Why test IDOR explicitly?**
- A) Style
- B) Sequential or guessable ids let one user reach another's records
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Object-level access.</details>

### Question 6 — Hard
**Why are scanners insufficient alone?**
- A) They are slow
- B) They find known patterns, not business-logic flaws like broken authorization
- C) They cache
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Logic needs reasoning.</details>

### Question 7 — Hard
**What makes a good security regression test?**
- A) Speed
- B) A failing request that stays failing: exploit pinned as a test
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Pin every bug forever.</details>

### Question 8 — Hard
**When do you rerun the security suite?**
- A) Yearly
- B) On every auth, dependency, or exposed-route change, not just releases
- C) Never
- D) On cache changes

<details><summary>Reveal Answer</summary>**B.** Change-triggered.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You test security deliberately. |
| 5-6 | Review bypass matrices and fuzzing. |
| < 5 | Re-read the lecture. |
