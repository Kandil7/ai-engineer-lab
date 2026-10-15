# Data Engineering 17: MinHash LSH — Quiz

> **Topic Overview**: Shingling, MinHash signatures, LSH banding, and
> precision/recall on a labelled pair set.

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

**Which near-dupe shape dominates Arabic corpora?**

- A) Identical re-uploads
- B) Whitespace and diacritic differences
- C) Schema violations
- D) Random ids

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Extra spaces, missing hamzas, and added or stripped vocalization marks make one passage hash as two.

</details>

---

### Question 2 — Easy

**Why does a one-word change defeat content hashing?**

- A) The hash input grows
- B) The hash is a cliff: any change flips the digest
- C) The key changes
- D) The row moves

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A cryptographic hash avalanches on any change, so near-identical passages get unrelated digests.

</details>

---

### Question 3 — Easy

**What does shingling convert the hash cliff into?**

- A) A slope: Jaccard similarity over shared pieces
- B) A key
- C) A timestamp
- D) An index

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Overlapping k-grams let a one-word variant keep almost all its pieces, giving a graded similarity.

</details>

---

### Question 4 — Medium

**What breaks when shingle k is too small?**

- A) Nothing
- B) Unrelated passages share many generic pieces and all look similar
- C) Hashing slows down
- D) Keys collide

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tiny shingles are generic, so unrelated texts overlap heavily and precision collapses.

</details>

---

### Question 5 — Medium

**What does one MinHash minimum estimate, and why?**

- A) Length, by counting shingles
- B) Jaccard: two sets share a minimum exactly when the lowest-hash shingle sits in their overlap
- C) Edit distance, by alignment
- D) Threshold, by banding

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The shared-minimum event has probability equal to Jaccard; many seeded perms turn votes into an estimate.

</details>

---

### Question 6 — Medium

**Why must MinHash permutations be seeded?**

- A) For speed
- B) So the same input always yields the same signature and verifies reproduce
- C) For smaller hashes
- D) To skip banding

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Unseeded randomness breaks reproducibility: re-ingest would produce different pairs and --verify would flake.

</details>

---

### Question 7 — Medium

**How do bands and rows move the LSH threshold?**

- A) They do not move it
- B) More bands lower it (more chances to match); more rows raise it (each band harder to match)
- C) More bands raise it; more rows lower it
- D) Only the seed moves it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Bands add match chances (recall up); rows harden each band (precision up); together they place the S-curve middle.

</details>

---

### Question 8 — Hard

**What is the correct two-pass order, and why?**

- A) LSH first, it is faster
- B) Exact hashing first, then MinHash on survivors, so similarity work is never wasted on exact dupes
- C) Either order, identical cost
- D) MinHash only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Content hashes remove byte-identical rows cheaply; the expensive similarity pass runs only where hashing cannot decide.

</details>

---

### Question 9 — Hard

**A threshold tuned on news boilerplate misfires on hadith chains. Why?**

- A) Thresholds are corpus-specific: distinct narrations can share long spans
- B) Hashing is broken there
- C) Seeds expire
- D) Bands overflow

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Every corpus re-measures precision and recall on its own labelled pairs; a copied threshold is an untested assumption.

</details>

---

### Question 10 — Hard

**What maps the teaching code to datasketch?**

- A) Nothing maps
- B) Shingle sets to MinHash, bands and rows to MinHashLSH threshold with num_perm
- C) Seeds to timestamps
- D) Pairs to keys

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The lecture maps each piece so migration is configuration: threshold is the S-curve middle, num_perm equals bands times rows.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | A | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | A | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for the capstone dedup |
| 7-8 | Proficient | Review LSH banding |
| 5-6 | Developing | Re-study shingling and MinHash |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Deduplication](../05-deduplication/05-deduplication-quiz.md) | **Next**: Capstone dedup
