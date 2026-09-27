# Git-Linux 02: Branching and Merging — Quiz

> **Topic Overview**: Branches, merges, conflicts, and history discipline.

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

**What is a branch?**

- A) A copy of all files
- B) A movable pointer to a commit
- C) A remote
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Creating a branch does not copy files.

</details>

---

### Question 2 — Easy

**What does merging do?**

- A) Deletes a branch
- B) Brings a branch's commits into another
- C) Creates a remote
- D) Caches files

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The merge is where the feature joins the main line.

</details>

---

### Question 3 — Easy

**A fast-forward merge happens when:**

- A) Branches diverged
- B) Branches have not diverged
- C) There is a conflict
- D) The remote is ahead

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The pointer moves forward with no divergence.

</details>

---

### Question 4 — Medium

**A conflict happens when:**

- A) Two branches change different lines
- B) Two branches change the same lines
- C) A branch is deleted
- D) A commit is pushed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Git cannot decide which version is correct.

</details>

---

### Question 5 — Medium

**A conflict is:**

- A) A failure
- B) A signal that two changes touched the same place
- C) A cache miss
- D) An error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The resolution is deliberate, never a blind pick.

</details>

---

### Question 6 — Medium

**Rebase:**

- A) Preserves history as it happened
- B) Rewrites commits as a clean sequence
- C) Deletes commits
- D) Caches commits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rebase makes history linear but rewrites commits.

</details>

---

### Question 7 — Medium

**Never rebase:**

- A) A feature branch
- B) A shared branch
- C) A local branch
- D) A new branch

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rewriting shared history breaks collaborators.

</details>

---

### Question 8 — Hard

**Feature branches should be:**

- A) Long-lived
- B) Short-lived and focused
- C) Never deleted
- D) Shared

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Long lives diverge and conflict.

</details>

---

### Question 9 — Hard

**The main line stays:**

- A) Experimental
- B) Deployable
- C) Empty
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Features merge in when ready.

</details>

---

### Question 10 — Hard**

**The roadmap's rule for history is:**

- A) It can be messy
- B) It is clean and readable
- C) It is optional
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Clean history is the discipline.

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
| 9-10 | Expert | Ready for remotes |
| 7-8 | Proficient | Review conflicts |
| 5-6 | Developing | Re-study merging |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Git Basics](01-git-basics-quiz.md) | **Next**: [03 - Remote Workflows](03-remote-workflows-quiz.md)