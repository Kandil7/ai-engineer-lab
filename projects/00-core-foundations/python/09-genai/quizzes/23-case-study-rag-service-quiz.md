# GenAI 23: Case Study — RAG Service — Quiz

> **Topic Overview**: Building a RAG service end to end: ingestion, retrieval, deployment, evaluation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the first artifact of a RAG service?**
- A) A UI
- B) A measured retrieval baseline on a golden set
- C) A fine-tuned model
- D) A dashboard

<details><summary>Reveal Answer</summary>**B.** Measure before optimizing.</details>

### Question 2 — Easy
**Why containerize the service?**
- A) For speed
- B) Reproducible deployment of the API and its dependencies
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** The image is the environment.</details>

### Question 3 — Medium
**Why separate ingestion from the request path?**
- A) For cost
- B) Ingestion is slow and belongs in workers; requests must stay short
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Do not block requests on embedding.</details>

### Question 4 — Medium
**What is the service contract?**
- A) The model
- B) A stable request/response shape with citations and errors
- C) The dataset
- D) The GPU

<details><summary>Reveal Answer</summary>**B.** The contract survives model changes.</details>

### Question 5 — Medium
**Why require citations in the response?**
- A) For style
- B) So grounding is verifiable
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Citations make trust checkable.</details>

### Question 6 — Hard
**Why is the index derived and rebuildable?**
- A) To save space
- B) The source of truth is the database; the index can be regenerated
- C) For speed
- D) It is not

<details><summary>Reveal Answer</summary>**B.** Derived stores are recoverable.</details>

### Question 7 — Hard
**What must the deployment include to be recruiter-legible?**
- A) Only the URL
- B) A README with architecture, eval numbers, and cost per query
- C) The source only
- D) The model weights

<details><summary>Reveal Answer</summary>**B.** Legibility is part of the deliverable.</details>

### Question 8 — Hard
**A production regression appears. First move?**
- A) Retrain
- B) Check traces and the eval report to localize retrieval vs generation
- C) Rebuild the index
- D) Add more data

<details><summary>Reveal Answer</summary>**B.** Localize before fixing.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can build a RAG service. |
| 5-6 | Review baseline-first and the contract. |
| < 5 | Re-read the lecture. |
