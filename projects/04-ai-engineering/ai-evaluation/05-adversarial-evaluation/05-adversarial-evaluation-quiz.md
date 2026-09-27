# AI Evaluation 05: Adversarial Evaluation — Quiz

> **Topic Overview**: Prompt injection, data poisoning, and grading
> resistance.

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

**What is prompt injection?**

- A) A cache miss
- B) An instruction smuggled into input to override the system
- C) A model upgrade
- D) A query error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Injection tries to override the system prompt.

</details>

---

### Question 2 — Easy

**Where can injection arrive in RAG?**

- A) Only the query
- B) The query or the retrieved content
- C) Only the cache
- D) Only the database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A retrieved passage can carry an injected instruction.

</details>

---

### Question 3 — Easy

**What is data poisoning?**

- A) Corrupting the corpus to repeat bad content
- B) Caching bad answers
- C) A slow query
- D) A model error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Poisoned passages get retrieved and repeated.

</details>

---

### Question 4 — Medium

**The defense against data poisoning is:**

- A) A bigger cache
- B) Provenance and source trust
- C) A faster model
- D) More queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Only vetted sources enter the corpus; every passage carries its source.

</details>

---

### Question 5 — Medium

**The adversarial test set is:**

- A) A sample of traffic
- B) A fixed collection of attack inputs
- C) The training data
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each entry records the attack, expected behavior, and pass condition.

</details>

---

### Question 6 — Medium

**Resistance is graded:**

- A) On a scale
- B) Binary per attack
- C) By speed
- D) By cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Resisted or not; the resistance rate is the fraction resisted.

</details>

---

### Question 7 — Medium

**A system resisting 90% of the adversarial set is:**

- A) Done
- B) Not done; the remaining 10% is next
- C) Broken
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The remaining attacks are the next work items.

</details>

---

### Question 8 — Hard

**Why test retrieved-content injection?**

- A) It is faster
- B) Query-only testing misses attacks hidden in passages
- C) It is required
- D) It reduces queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The attack can hide in retrieved text, not just the query.

</details>

---

### Question 9 — Hard

**Adversarial testing runs:**

- A) Once
- B) In CI like the golden set
- C) Only on weekends
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every prompt, guardrail, or ingestion change re-runs the set.

</details>

---

### Question 10 — Hard**

**A change that fixes a golden-set metric but opens an injection hole is:**

- A) An improvement
- B) A regression
- C) A cache win
- D) Neutral

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Quality and resistance both gate; a hole is a regression.

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
| 9-10 | Expert | Ready for eval in CI |
| 7-8 | Proficient | Review poisoning |
| 5-6 | Developing | Re-study injection |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - LLM-as-Judge](04-llm-as-judge-quiz.md) | **Next**: [06 - Eval in CI](06-eval-in-ci-quiz.md)