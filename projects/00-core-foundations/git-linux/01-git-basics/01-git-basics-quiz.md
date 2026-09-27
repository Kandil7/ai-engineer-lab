# Git-Linux 01: Git Basics — Quiz

> **Topic Overview**: The three areas, staging, and the commit.

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

**What are the three areas?**

- A) Local, remote, cloud
- B) Working tree, index, HEAD
- C) Staging, commit, push
- D) Add, commit, log

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Working tree (disk), index (staged), HEAD (last commit).

</details>

---

### Question 2 — Easy

**What does `git add` do?**

- A) Commits changes
- B) Moves changes from working tree to index
- C) Pushes changes
- D) Deletes changes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: `git add` stages changes.

</details>

---

### Question 3 — Easy

**What does `git commit` do?**

- A) Moves the index to HEAD
- B) Stages changes
- C) Pushes changes
- D) Shows history

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The commit records the staged snapshot.

</details>

---

### Question 4 — Medium

**What is the commit hash?**

- A) The message
- B) The commit's identity
- C) The author
- D) The date

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The hash addresses the history.

</details>

---

### Question 5 — Medium

**What does .gitignore do?**

- A) Deletes files
- B) Excludes files from the repository
- C) Commits files
- D) Stages files

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Secrets, artifacts, and large assets stay out.

</details>

---

### Question 6 — Medium

**A secret committed once is:**

- A) Removed by deletion
- B) In the history forever
- C) Cached
- D) Ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Deleting the file does not remove it from history.

</details>

---

### Question 7 — Medium

**Blind `git add -A` is:**

- A) Recommended
- B) A mistake
- C) Required
- D) Fast

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Staging is deliberate; only intended files are committed.

</details>

---

### Question 8 — Hard

**A clear commit message is:**

- A) Vague
- B) Imperative, concise, and specific
- C) Long
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The message documents what changed and why.

</details>

---

### Question 9 — Hard

**`git status` shows:**

- A) Only committed files
- B) The state of the three areas
- C) Only remote state
- D) Only the log

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Modified, staged, and untracked files.

</details>

---

### Question 10 — Hard**

**The roadmap's rule about secrets is:**

- A) Commit them
- B) Never commit them
- C) Cache them
- D) Encrypt them

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Secrets never enter the history.

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
| 9-10 | Expert | Ready for branching |
| 7-8 | Proficient | Review the three areas |
| 5-6 | Developing | Re-study staging |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Branching and Merging](02-branching-merging-quiz.md)