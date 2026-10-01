# GenAI 18: Caching and Cost — Quiz

> **Topic Overview**: Reducing LLM cost with caches, prompt discipline, and cost tracking.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is semantic caching?**
- A) Exact-match caching
- B) Returning a cached answer for a semantically similar query
- C) Model caching
- D) Disk caching

<details><summary>Reveal Answer</summary>**B.** Similarity, not equality.</details>

### Question 2 — Easy
**Why does a cache reduce cost?**
- A) It changes the model
- B) A hit avoids the paid model call
- C) It compresses data
- D) It does not

<details><summary>Reveal Answer</summary>**B.** Hits serve for free.</details>

### Question 3 — Medium
**What must a cache key include?**
- A) Only the query
- B) The query plus the prompt and corpus versions
- C) The model
- D) The user

<details><summary>Reveal Answer</summary>**B.** A change in any input invalidates.</details>

### Question 4 — Medium
**When should a result never be cached?**
- A) Always
- B) When it is abstained or malformed
- C) When it is correct
- D) Never cache

<details><summary>Reveal Answer</summary>**B.** Bad answers must not be served.</details>

### Question 5 — Medium
**What is cost per useful answer?**
- A) Cost per token
- B) Total cost divided by accepted answers, including retries
- C) The model price
- D) The GPU price

<details><summary>Reveal Answer</summary>**B.** The useful unit is an answer.</details>

### Question 6 — Hard
**What is the semantic-cache threshold tradeoff?**
- A) None
- B) Too low serves wrong answers; too high saves little
- C) It only affects speed
- D) It is arbitrary

<details><summary>Reveal Answer</summary>**B.** A correctness dial as much as a cost dial.</details>

### Question 7 — Hard
**Why is a cache a correctness hazard, not only a saving?**
- A) It is not
- B) A stale or mismatched answer can be served confidently
- C) For speed
- D) It is safe

<details><summary>Reveal Answer</summary>**B.** Version keys and a threshold bound the risk.</details>

### Question 8 — Hard
**A dropping cache hit rate signals what?**
- A) Nothing
- B) A changing corpus, a broken key, or over-aggressive invalidation
- C) Better answers
- D) Lower traffic

<details><summary>Reveal Answer</summary>**B.** The trend surfaces the cause.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can cache and cost-engineer. |
| 5-6 | Review cache keys and thresholds. |
| < 5 | Re-read the lecture. |
