# MLops 03: Data Versioning — Quiz

> **Topic Overview**: Versioning datasets so every model run points at a reproducible data snapshot.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**Why version data separately from code?**

- A) Data is too big to commit
- B) The same code on different data is a different experiment
- C) Data is not part of the experiment
- D) To save time

<details><summary>Reveal Answer</summary>

**B.** Data is an experiment input; it must be identified.

</details>

### Question 2 — Easy

**What does a data version identify?**

- A) The file size
- B) A specific snapshot of the dataset
- C) The GPU used
- D) The code branch

<details><summary>Reveal Answer</summary>

**B.** A snapshot, not "whatever is on disk now".

</details>

### Question 3 — Medium

**Why is "the data on the shared drive" not a version?**

- A) It is too slow
- B) It changes over time, so two runs read different data under one name
- C) It is not licensed
- D) It is too small

<details><summary>Reveal Answer</summary>

**B.** Mutability destroys reproducibility.

</details>

### Question 4 — Medium

**What is content-addressing?**

- A) Naming files by date
- B) Identifying a dataset by a hash of its content, so any change yields a new id
- C) Sorting files
- D) Compressing files

<details><summary>Reveal Answer</summary>

**B.** The hash is the immutable identity.

</details>

### Question 5 — Medium

**A model was trained on data v1 and you now serve it. Can you retrain it exactly next year?**

- A) Yes, if code is unchanged
- B) Only if data v1 is still retrievable
- C) Always
- D) Never

<details><summary>Reveal Answer</summary>

**B.** Reproducibility depends on retaining the snapshot.

</details>

### Question 6 — Hard

**What is the migration/rollback concern for a dataset?**

- A) Disk space
- B) A pipeline that consumed v1 must know how to handle v2, and a bad v2 must be revertible
- C) Licensing
- D) GPU cost

<details><summary>Reveal Answer</summary>

**B.** Dataset changes are schema changes for the pipeline.

</details>

### Question 7 — Hard

**How does data versioning connect to RAG index rebuilds?**

- A) It does not
- B) The index is derived from a data version; a new version means a rebuild is a defined operation
- C) The index is the source of truth
- D) Versioning is optional

<details><summary>Reveal Answer</summary>

**B.** Lineage from data version to index makes rebuilds well-defined.

</details>

### Question 8 — Hard

**A training metric dropped. How does data versioning help diagnose?**

- A) It speeds training
- B) It shows whether the data version changed between runs, isolating data from code
- C) It improves accuracy
- D) It reduces cost

<details><summary>Reveal Answer</summary>

**B.** Attributing the change is the point.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can version a dataset. |
| 5-6 | Review snapshot vs mutable data. |
| < 5 | Re-read the lecture. |
