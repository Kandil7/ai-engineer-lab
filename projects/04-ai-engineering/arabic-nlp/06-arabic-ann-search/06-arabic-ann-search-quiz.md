# Arabic NLP 06: ANN Search — Quiz

> **Topic Overview**: The recall/speed tradeoff and the index parameters.

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

**Exact search:**

- A) Prunes the search space
- B) Scores every vector
- C) Is fast on large corpora
- D) Is approximate

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Latency grows linearly with the corpus.

</details>

---

### Question 2 — Easy

**ANN trades:**

- A) Speed for recall
- B) A little recall for a lot of speed
- C) Memory for speed
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The index prunes the search space.

</details>

---

### Question 3 — Easy

**HNSW is:**

- A) A cache
- B) A multi-layer graph index
- C) A query
- D) A collection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A query walks the graph toward the nearest vectors.

</details>

---

### Question 4 — Medium

**The recall loss means:**

- A) The search is faster
- B) The true neighbor may be pruned
- C) The index is broken
- D) The corpus is small

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The cost of the speed.

</details>

---

### Question 5 — Medium

**Connectivity controls:**

- A) The corpus size
- B) The graph's branching
- C) The query
- D) The recall loss

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Higher builds a better index but uses more memory.

</details>

---

### Question 6 — Medium

**Exploration controls:**

- A) The graph's branching
- B) The search's thoroughness
- C) The corpus size
- D) The recall loss

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Higher searches more thoroughly but slower.

</details>

---

### Question 7 — Medium

**The parameters are:**

- A) Fixed
- B) The recall/speed dial
- C) Cached
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: More pruning, faster but less accurate.

</details>

---

### Question 8 — Hard

**The index is tuned on:**

- A) The training data
- B) The golden set
- C) The cache
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Measure recall@k and latency, keep the best.

</details>

---

### Question 9 — Hard

**Ignoring the recall loss causes:**

- A) Faster search
- B) Silent degradation
- C) A cache miss
- D) A broken index

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The degradation is invisible without measurement.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for large corpora is:**

- A) Exact search
- B) ANN search
- C) No search
- D) Cached search

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ANN is used for large corpora.

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
| 9-10 | Expert | Ready for MRR evaluation |
| 7-8 | Proficient | Review the parameters |
| 5-6 | Developing | Re-study the tradeoff |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Hybrid Search](05-arabic-hybrid-search-quiz.md) | **Next**: [07 - MRR Evaluation](07-arabic-mrr-evaluation-quiz.md)