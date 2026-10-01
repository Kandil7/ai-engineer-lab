# GenAI 08: Document Processing — Quiz

> **Topic Overview**: Parsing, cleaning, and normalizing source documents before indexing.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why is document processing a separate step?**
- A) For speed
- B) Raw sources are messy; parsing and cleaning precede indexing
- C) For storage
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Garbage in, garbage out.</details>

### Question 2 — Easy
**What does encoding handling protect against?**
- A) Slow reads
- B) Silent mojibake that corrupts text and matches
- C) High cost
- D) Large files

<details><summary>Reveal Answer</summary>**B.** Wrong encoding silently breaks everything downstream.</details>

### Question 3 — Medium
**Why normalize text before indexing?**
- A) For style
- B) So diacritics/variants do not split matches
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Normalization is a matching concern.</details>

### Question 4 — Medium
**What is the two-text discipline?**
- A) Two languages
- B) Keep the verbatim original for display and a normalized form for search
- C) Two files per page
- D) Two models

<details><summary>Reveal Answer</summary>**B.** Display fidelity plus search recall.</details>

### Question 5 — Medium
**How should a corrupt document be handled?**
- A) Silently dropped
- B) Quarantined and logged, not passed silently
- C) Indexed anyway
- D) Ignored

<details><summary>Reveal Answer</summary>**B.** Failures must be visible.</details>

### Question 6 — Hard
**Why track rejected and missing document counts?**
- A) For storage
- B) So a silent partial ingest is a number, not a surprise later
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Counts make loss loud.</details>

### Question 7 — Hard
**Why is normalization lossy, and where is it applied?**
- A) It is not lossy
- B) It removes information; apply it only to the searchable text, never the display text
- C) Apply it everywhere
- D) Never apply it

<details><summary>Reveal Answer</summary>**B.** Keep display verbatim.</details>

### Question 8 — Hard
**How does document processing connect to retrieval recall?**
- A) It does not
- B) Unparsed or mis-encoded text is unretrievable, so processing bounds recall
- C) Only for code
- D) No

<details><summary>Reveal Answer</summary>**B.** Recall starts at ingestion.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can process documents. |
| 5-6 | Review encoding and normalization. |
| < 5 | Re-read the lecture. |
