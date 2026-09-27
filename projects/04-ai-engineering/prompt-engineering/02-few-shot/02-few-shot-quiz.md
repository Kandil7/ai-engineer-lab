# Prompt Engineering 02: Few-Shot — Quiz

> **Topic Overview**: Example selection and the token cost.

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

**Few-shot examples:**

- A) Replace the task
- B) Demonstrate the pattern
- C) Cache the output
- D) Sort the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model generalizes by imitation.

</details>

---

### Question 2 — Easy

**Examples are chosen to:**

- A) Maximize volume
- B) Cover the pattern
- C) Minimize tokens
- D) Sort the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Two different cases beat five similar ones.

</details>

---

### Question 3 — Easy

**Examples are written in:**

- A) Any format
- B) The exact target format
- C) A cached format
- D) A sorted format

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model imitates the format.

</details>

---

### Question 4 — Medium

**A sloppy example teaches:**

- A) Clean output
- B) Sloppy output
- C) Cached output
- D) Sorted output

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model imitates what it sees.

</details>

---

### Question 5 — Medium

**Every example consumes:**

- A) Cache
- B) Tokens
- C) Memory
- D) Time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The context budget.

</details>

---

### Question 6 — Medium

**Example bias means:**

- A) The model ignores examples
- B) The model over-follows the pattern
- C) The model caches
- D) The model sorts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: All math examples -> math-style answers.

</details>

---

### Question 7 — Medium

**The bias is managed by:**

- A) More examples
- B) Covering the range of inputs
- C) Caching
- D) Sorting

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Pattern coverage.

</details>

---

### Question 8 — Hard

**Zero-shot is:**

- A) The best option
- B) The baseline to compare against
- C) A cache
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Instruction only, no examples.

</details>

---

### Question 9 — Hard

**Few-shot when zero-shot suffices is:**

- A) Correct
- B) A waste of tokens
- C) Required
- D) Faster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The examples add cost without gain.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for examples is:**

- A) They are numerous
- B) They cover the pattern
- C) They are cached
- D) They are short

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Coverage, not volume.

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
| 9-10 | Expert | Ready for chain-of-thought |
| 7-8 | Proficient | Review the cost |
| 5-6 | Developing | Re-study example selection |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Prompt Structure](01-prompt-structure-quiz.md) | **Next**: [03 - Chain-of-Thought](03-chain-of-thought-quiz.md)