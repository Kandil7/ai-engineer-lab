# Data Engineering 18: DVC and Dataset Versioning — Quiz

> **Topic Overview**: Why git fails for datasets, dvc.yaml stages, lock
> pinning, repro semantics, remotes, .dvcignore, and manifest.json.

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

**Why does git fail for datasets?**

- A) It cannot store text
- B) Blob bloat plus no derivation graph
- C) It has no branches
- D) It cannot store YAML

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Committed data bloats history permanently, and git records file states, not how one dataset derived from another.

</details>

---

### Question 2 — Easy

**What four fields does a dvc.yaml stage declare?**

- A) Branch, tag, commit, push
- B) Cmd, deps, outs, params
- C) Input, model, metric, plot
- D) Host, port, user, password

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The command to run, the files it reads, the files it writes, and the parameters affecting output.

</details>

---

### Question 3 — Easy

**What does dvc.lock pin?**

- A) Git branch names
- B) Checksums of every dep and out
- C) Cloud credentials
- D) Quiz answers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: After a run the lock records each path's checksum, so staleness and byte changes are mechanical.

</details>

---

### Question 4 — Medium

**Why must pipeline scripts appear in deps?**

- A) To back them up
- B) So a script change re-triggers the stage
- C) To count lines of code
- D) To satisfy the linter

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Code is an input to the output; a changed script with unchanged data deps must still mark the stage stale.

</details>

---

### Question 5 — Medium

**How does dvc repro decide what to skip?**

- A) Timestamps only
- B) Inputs matching dvc.lock are skipped
- C) It never skips anything
- D) Random sampling

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Stages whose deps and params match the lock are fresh; changed inputs re-run and cascade downstream.

</details>

---

### Question 6 — Medium

**Which remote should come first?**

- A) A cloud bucket
- B) A local path
- C) A public URL
- D) No remote at all

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A local remote needs no credentials or billing, so the full push/pull loop is learnable offline per ADR-0013.

</details>

---

### Question 7 — Medium

**What must manifest.json carry?**

- A) Only row counts
- B) Input checksums, params hash, git sha, row counts, output bytes
- C) Only the git sha
- D) Cloud credentials

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Five fields telling what happened: which inputs, which settings, which commit, how many rows, how many bytes.

</details>

---

### Question 8 — Hard

**The lock answers "which bytes". What does the manifest answer?**

- A) Nothing new
- B) "What happened" — the pipeline story
- C) The cloud bill
- D) The team roster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Row counts and settings tell the story for reviewers; checksums then prove it.

</details>

---

### Question 9 — Hard

**Why is an output missing from dvc.lock a failure?**

- A) It slows the quiz
- B) Unpinned output is untracked data
- C) It breaks YAML parsing
- D) It deletes the file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without a pinned checksum no commit can reproduce or verify those bytes, so the check fails loudly.

</details>

---

### Question 10 — Hard

**The dvc binary is absent. What does the exercise do?**

- A) Simulates dvc commands
- B) Runs structural checks and skips binary checks with an install note
- C) Fails every assert
- D) Installs dvc silently

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fixture checks always run; binary checks gate on shutil.which with a skip naming pip install dvc, per ADR-0010.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Medium |
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
| 9-10 | Expert | Ready for the capstone |
| 7-8 | Proficient | Review repro semantics |
| 5-6 | Developing | Re-study lock vs manifest |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [15 - Storage and Databases](../15-storage-and-databases/)
