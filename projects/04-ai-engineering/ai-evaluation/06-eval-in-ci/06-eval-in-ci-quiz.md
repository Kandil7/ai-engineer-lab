# AI Evaluation 06: Eval in CI — Quiz

> **Topic Overview**: The eval harness, thresholds from a baseline, and the
> verdict.

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

**What is the eval harness?**

- A) A cache
- B) One deterministic command running all eval sets
- C) A database
- D) A model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Same code, same sets, same thresholds, same verdict.

</details>

---

### Question 2 — Easy

**Where do thresholds come from?**

- A) A guess
- B) A baseline run
- C) The cache
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The baseline is captured once, reviewed, then enforced.

</details>

---

### Question 3 — Easy

**A metric below its floor:**

- A) Passes
- B) Fails the build
- C) Is cached
- D) Is ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The threshold is the gate.

</details>

---

### Question 4 — Medium

**A change is judged:**

- A) In isolation
- B) Against the baseline
- C) By the cache
- D) By the model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A new chunker scoring 0.9 is good only if the baseline was lower.

</details>

---

### Question 5 — Medium

**What is the delta?**

- A) The cache size
- B) Current metric minus baseline
- C) The model size
- D) The query count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The delta shows the change's effect.

</details>

---

### Question 6 — Medium

**The eval report shows:**

- A) Only the current metrics
- B) Metric, baseline, current, delta, verdict
- C) Only the baseline
- D) Only the verdicts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The full table makes regressions visible at a glance.

</details>

---

### Question 7 — Medium

**An evaluation that never runs is:**

- A) A gate
- B) A document
- C) A cache
- D) A model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without execution there is no enforcement.

</details>

---

### Question 8 — Hard

**Which changes re-run the harness?**

- A) Only prompt changes
- B) Prompt, retriever, chunker, or guardrail changes
- C) Only retriever changes
- D) Only UI changes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Anything that can move the metrics re-runs the harness.

</details>

---

### Question 9 — Hard

**A change improving one metric and degrading another is:**

- A) Hidden
- B) A tradeoff made explicitly, with the report as evidence
- C) A cache win
- D) Ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The report makes the tradeoff explicit.

</details>

---

### Question 10 — Hard**

**Thresholds without a baseline are:**

- A) Enforced
- B) Guesses
- C) Cached
- D) Reports

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A floor needs a measured starting point.

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
| 9-10 | Expert | Stage 10 evaluation complete |
| 7-8 | Proficient | Review the baseline |
| 5-6 | Developing | Re-study thresholds |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Adversarial Evaluation](05-adversarial-evaluation-quiz.md)