# GenAI 09: RAG Baseline — Quiz

> **Topic Overview**: The end-to-end retrieval-augmented generation pipeline.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the stages of a RAG pipeline?**
- A) Train → deploy
- B) Ingest → embed → index → retrieve → generate
- C) Only generate
- D) Only retrieve

<details><summary>Reveal Answer</summary>**B.** Retrieval supplies facts; generation writes the answer.</details>

### Question 2 — Easy
**Why use RAG instead of relying on the model's memory?**
- A) It is faster
- B) It grounds answers in a corpus that can change without retraining
- C) It is cheaper
- D) It is required

<details><summary>Reveal Answer</summary>**B.** RAG is the knowledge path.</details>

### Question 3 — Medium
**What bounds answer quality in RAG?**
- A) The model only
- B) Retrieval recall: a passage never retrieved cannot ground the answer
- C) The prompt only
- D) The cost

<details><summary>Reveal Answer</summary>**B.** Recall is the ceiling.</details>

### Question 4 — Medium
**Why build an eval harness early?**
- A) For speed
- B) Without measurement, a retrieval change is opinion
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Eval-first makes decisions evidence-based.</details>

### Question 5 — Medium
**Why separate retrieval metrics from answer metrics?**
- A) They are the same
- B) A retrieval miss and a generation miss need different fixes
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Diagnose at the stage.</details>

### Question 6 — Hard
**What is the failure mode of a RAG system without abstention?**
- A) Slow answers
- B) It answers out-of-corpus questions confidently
- C) High cost
- D) No failure

<details><summary>Reveal Answer</summary>**B.** Abstention is required for honesty.</details>

### Question 7 — Hard
**Why keep the retrieval `top_k` modest?**
- A) For speed only
- B) The context budget is finite; weak extra passages dilute and cost tokens
- C) For accuracy
- D) It is arbitrary

<details><summary>Reveal Answer</summary>**B.** `top_k` is a candidate count, not a prompt guarantee.</details>

### Question 8 — Hard
**What is the minimal first RAG deliverable?**
- A) A full agent
- B) A working retrieve-then-generate pipeline measured on a small golden set
- C) A fine-tuned model
- D) A dashboard

<details><summary>Reveal Answer</summary>**B.** Start measurable and simple.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand the RAG baseline. |
| 5-6 | Review retrieval-bounds-answer and eval-first. |
| < 5 | Re-read the lecture. |
