# Arabic NLP 02: Normalization and Tokenization — Quiz

> **Topic Overview**: The normalization pipeline and tokenization strategies
> for Arabic, and how to measure the choice.

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

**What is the first step in the Arabic normalization pipeline?**

- A) Remove tatweel
- B) Normalize to NFD and strip combining marks
- C) Unify hamza forms
- D) Split on whitespace

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Decompose to NFD first so diacritics become separate combining marks, then strip them. Order matters.

</details>

---

### Question 2 — Easy

**What does hamza normalization do?**

- A) Removes all hamza letters
- B) Unifies hamza carrier forms (أ إ آ) to bare alif
- C) Adds diacritics
- D) Converts to English

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Unifying carriers to bare alif lets a query with أ match text with ا or إ.

</details>

---

### Question 3 — Easy

**What is tatweel (ـ)?**

- A) A vowel
- B) A length-extension mark with no meaning
- C) A punctuation mark
- D) A letter

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tatweel extends letter shapes for calligraphy and carries no meaning; it is removed in normalization.

</details>

---

### Question 4 — Medium

**Why does whitespace tokenization fail on Arabic?**

- A) Arabic has no spaces
- B) Morphology fragments related words across tokens
- C) Arabic is right to left
- D) Whitespace is not a valid separator

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Related words (كتب، كتاب، مكتبة) share roots but not tokens, so whitespace splitting misses morphological variants.

</details>

---

### Question 5 — Medium

**What is light stemming?**

- A) Full root analysis
- B) Stripping common affixes like ال، و، ب
- C) Removing all prefixes
- D) Converting to roots

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Light stemming strips common prefixes without full morphological analysis — the pragmatic middle ground.

</details>

---

### Question 6 — Medium

**What is the trade in hamza normalization?**

- A) Speed vs memory
- B) Recall vs the ability to distinguish أ from ا
- C) Precision vs latency
- D) Storage vs cost

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Unifying hamza gains recall but loses the distinction between أ and ا — a loss that matters in proper names and Quranic text.

</details>

---

### Question 7 — Medium

**Which metric decides a tokenization choice?**

- A) Latency
- B) Recall@k on a labeled set
- C) Code size
- D) Token count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tokenizers are compared by recall@k on query-to-passage pairs, never by taste.

</details>

---

### Question 8 — Hard

**What is the correct pipeline order?**

- A) Recompose, strip, decompose
- B) Decompose, strip combining marks, recompose, unify hamza, remove tatweel
- C) Unify hamza, decompose, strip
- D) Remove tatweel, recompose, strip

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Decompose first so marks are separable, strip, recompose, then unify hamza and remove tatweel.

</details>

---

### Question 9 — Hard

**Which corpus should NOT use aggressive hamza normalization?**

- A) Modern news articles
- B) Quranic text
- C) Technical documentation
- D) Social media

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Quranic text distinguishes أ from ا meaningfully; aggressive unification loses that distinction.

</details>

---

### Question 10 — Hard

**What does the two-text discipline require of normalization?**

- A) Normalize both texts identically
- B) Normalize only the searchable text, keep the original verbatim
- C) Normalize only the display text
- D) Skip normalization entirely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The searchable text is normalized for matching; the original stays verbatim for display and citation.

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
| 9-10 | Expert | Ready for retrieval topics |
| 7-8 | Proficient | Review the pipeline order |
| 5-6 | Developing | Re-study normalization |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Text Fundamentals](01-arabic-text-fundamentals-quiz.md) | **Next**: [03 - Lexical Retrieval](03-arabic-lexical-retrieval-quiz.md)