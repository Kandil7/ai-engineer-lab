# Advanced Python 28: Code Quality Tooling — Quiz

> **Topic Overview**: Linters, AST rules, mypy, and CI gating.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the difference between a linter and a formatter?**
- A) None
- B) A linter finds issues; a formatter rewrites layout (e.g. ruff, black)
- C) A formatter finds bugs
- D) A linter rewrites code

<details><summary>Reveal Answer</summary>**B.** Detection vs layout.</details>

### Question 2 — Easy
**What does rule B006 flag?**
- A) Bare except
- B) Mutable default arguments (`def f(x=[])`)
- C) Long lines
- D) Unused imports

<details><summary>Reveal Answer</summary>**B.** Shared-default bug.</details>

### Question 3 — Medium
**Why is a bare `except:` (E722) dangerous?**
- A) It is slow
- B) It catches everything, including `KeyboardInterrupt`/`SystemExit`, hiding real errors
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Catch specific exceptions.</details>

### Question 4 — Medium
**What does cyclomatic complexity (C901) measure?**
- A) Lines
- B) The number of independent paths through a function
- C) Imports
- D) Runtime

<details><summary>Reveal Answer</summary>**B.** Branching complexity.</details>

### Question 5 — Medium
**Why gate lint/type checks in CI?**
- A) For speed
- B) To prevent issues from merging; humans forget, CI does not
- C) To cache
- D) To hash

<details><summary>Reveal Answer</summary>**B.** Automated enforcement.</details>

### Question 6 — Hard
**Why is `# noqa` discipline important?**
- A) It speeds code
- B) Blanket suppressions hide real problems; suppress a specific rule with a reason
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Targeted, justified suppression.</details>

### Question 7 — Hard
**What does mypy add beyond linting?**
- A) Formatting
- B) Static type checking of the annotations
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Type correctness.</details>

### Question 8 — Hard
**Why run a dependency audit?**
- A) For speed
- B) Known-vulnerable packages are a supply-chain risk; audit flags them
- C) To sort
- D) To format

<details><summary>Reveal Answer</summary>**B.** Security of dependencies.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You run a clean toolchain. |
| 5-6 | Review lint rules and CI gating. |
| < 5 | Re-read the lecture. |
