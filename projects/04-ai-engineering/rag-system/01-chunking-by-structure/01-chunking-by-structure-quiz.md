# RAG System 01: Chunking by Source Structure — Quiz

> **Topic Overview**: Structure-aware chunking, the two-text discipline, and
> provenance on chunks.

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

**What is the highest-leverage retrieval decision?**

- A) The model
- B) Chunking
- C) The database
- D) The API

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Chunk size and boundaries bound retrieval quality from both sides.

</details>

---

### Question 2 — Easy

**What is structure-aware chunking?**

- A) Fixed-size splitting
- B) Chunking by the source's natural boundaries
- C) Random splitting
- D) No chunking

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Page, section, and paragraph boundaries preserve meaning.

</details>

---

### Question 3 — Easy

**What does the two-text discipline require per chunk?**

- A) One text
- B) Original for citation, searchable for matching
- C) Only normalized text
- D) Only verbatim text

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The index matches searchable; the answer cites original.

</details>

---

### Question 4 — Medium

**What happens if you normalize the display text?**

- A) Nothing
- B) The quote no longer matches the source
- C) It is faster
- D) It saves space

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Normalization alters the quote — a correctness bug.

</details>

---

### Question 5 — Medium

**Why does every chunk need provenance?**

- A) It is faster
- B) A chunk without provenance cannot be cited honestly
- C) It saves space
- D) It is required by the schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Provenance makes the chunk traceable and citable.

</details>

---

### Question 6 — Medium

**What does chunk_id encode?**

- A) Only the book
- B) book_id, page, and chunk index
- C) Only the page
- D) The text hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: chunk_id like "b1:p7:2" encodes provenance.

</details>

---

### Question 7 — Medium

**How is chunking measured?**

- A) By speed
- B) By recall@k on a labeled set
- C) By file size
- D) By token count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Chunking is evaluated by what retrieval can find.

</details>

---

### Question 8 — Hard

**What is the fallback when a paragraph exceeds the token limit?**

- A) Drop it
- B) Split it further, capped by the limit
- C) Merge it with the next
- D) Skip it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Structure first, size cap as the fallback for oversized units.

</details>

---

### Question 9 — Hard

**For code corpora, what chunking wins?**

- A) Paragraph
- B) AST-aware (syntax boundaries)
- C) Fixed-size
- D) Sentence

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Functions and classes are the complete citable units for code.

</details>

---

### Question 10 — Hard**

**A chunker that gains 5pp recall is:**

- A) Not worth it
- B) Worth its complexity
- C) A mistake
- D) Slower

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Measured recall gains justify the chunker's complexity.

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
| 9-10 | Expert | Ready for retrieval and filters |
| 7-8 | Proficient | Review the two-text discipline |
| 5-6 | Developing | Re-study provenance |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Hard Filters and Retrieval](02-hard-filters-retrieval-quiz.md)