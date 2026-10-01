# GenAI 07: Chunking Strategies — Quiz

> **Topic Overview**: Splitting documents for retrieval — fixed, recursive, and structure-aware.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why chunk at all?**
- A) To reduce storage
- B) Retrieval and context need passages, not whole documents
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Chunks are the retrievable unit.</details>

### Question 2 — Easy
**What is fixed-size chunking?**
- A) Splitting by meaning
- B) Splitting every N tokens/characters, often with overlap
- C) Splitting by page
- D) Not splitting

<details><summary>Reveal Answer</summary>**B.** Simple and structure-blind.</details>

### Question 3 — Medium
**What is the risk of chunks that are too small?**
- A) Too much memory
- B) Lost context; a claim split across chunks is unretrievable
- C) Slow search
- D) No risk

<details><summary>Reveal Answer</summary>**B.** Small chunks lose coherence.</details>

### Question 4 — Medium
**What is the risk of chunks that are too large?**
- A) Lost context
- B) Diluted relevance and wasted context budget
- C) Fast search
- D) No risk

<details><summary>Reveal Answer</summary>**B.** Large chunks dilute the signal.</details>

### Question 5 — Medium
**Why does chunking need to be measured?**
- A) It is obvious
- B) Strategy affects recall; the golden set decides
- C) For speed
- D) It does not

<details><summary>Reveal Answer</summary>**B.** Chunking is an evaluation variable.</details>

### Question 6 — Hard
**Why is structure-aware chunking better for code or books?**
- A) It is faster
- B) Boundaries follow natural units (functions, verses), so chunks are coherent
- C) It is cheaper
- D) It is not

<details><summary>Reveal Answer</summary>**B.** Natural boundaries preserve meaning.</details>

### Question 7 — Hard
**Why carry provenance on every chunk?**
- A) For storage
- B) So citations resolve to the exact source location
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** A chunk without origin cannot be cited.</details>

### Question 8 — Hard
**A retrieval change lowers recall. Could chunking be the cause?**
- A) No
- B) Yes; chunking determines what is retrievable, so it must be a controlled variable
- C) Only for code
- D) No

<details><summary>Reveal Answer</summary>**B.** Chunking is upstream of retrieval quality.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can design chunking. |
| 5-6 | Review size tradeoffs. |
| < 5 | Re-read the lecture. |
