# Git-Linux 03: Remote Workflows — Quiz

> **Topic Overview**: Remotes, the push/pull loop, and the PR review gate.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**What is a remote?**

- A) A cache
- B) A named reference to another copy of the repo
- C) A branch
- D) A commit

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The default remote is `origin`.

</details>

---

### Question 2 — Easy

**What does push do?**

- A) Brings commits down
- B) Sends local commits to the remote
- C) Deletes commits
- D) Caches commits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Push sends local commits up.

</details>

---

### Question 3 — Easy

**What does pull do?**

- A) Sends commits up
- B) Brings remote commits down
- C) Deletes commits
- D) Creates a branch

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Pull is the other half of the loop.

</details>

---

### Question 4 — Medium

**A push is rejected when:**

- A) The local is ahead
- B) The remote has commits the local lacks
- C) The branch is new
- D) The cache is cold

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The local must pull and merge first.

</details>

---

### Question 5 — Medium

**Divergence happens when:**

- A) Local and remote are identical
- B) Both have commits the other lacks
- C) The remote is empty
- D) The local is empty

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Pulling merges them.

</details>

---

### Question 6 — Medium

**Divergence is managed by:**

- A) Pushing large
- B) Pulling often and pushing small
- C) Never pulling
- D) Deleting branches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Small, frequent syncs keep divergence small.

</details>

---

### Question 7 — Medium

**A pull request is:**

- A) A cache
- B) The review gate for a branch's changes
- C) A commit
- D) A remote

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The PR is where code is reviewed before merging.

</details>

---

### Question 8 — Hard

**A large divergence is usually caused by:**

- A) Pulling often
- B) A long-lived branch
- C) Small commits
- D) A clean history

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Long-lived branches drift from the main line.

</details>

---

### Question 9 — Hard

**The roadmap's rule about pushing is:**

- A) Never push
- B) Push after meaningful work
- C) Push only at the end
- D) Push secrets

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The remote is the source of truth for collaboration.

</details>

---

### Question 10 — Hard**

**The remote is the source of truth for:**

- A) Local work
- B) Collaboration
- C) Caching
- D) Secrets

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The local is the working copy.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for the Linux shell |
| 7-8 | Proficient | Review divergence |
| 5-6 | Developing | Re-study push/pull |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Branching](02-branching-merging-quiz.md) | **Next**: [04 - Linux Command Line](04-linux-command-line-quiz.md)