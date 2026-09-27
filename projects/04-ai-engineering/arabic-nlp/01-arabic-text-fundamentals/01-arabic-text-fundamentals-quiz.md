# Arabic NLP 01: Arabic Text Fundamentals — Quiz

> **Topic Overview**: Arabic script, Unicode normalization, diacritics, and
> the two-text discipline. This quiz verifies you can handle Arabic text in
> Python without corrupting it.

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

**How many letters does the Arabic alphabet have?**

- A) 26
- B) 28
- C) 30
- D) 32

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Arabic has 28 letters. The three short vowels are diacritics, not letters.

</details>

---

### Question 2 — Easy

**What is the primary purpose of the two-text discipline?**

- A) To save storage space
- B) To keep the original text for display while using a normalized form for search
- C) To translate Arabic to English
- D) To remove all diacritics permanently

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The original text is preserved verbatim for display and citation; a normalized form is derived for matching. Normalization never alters what the user sees quoted.

</details>

---

### Question 3 — Easy

**Which Unicode normalization form should you use for consistent storage?**

- A) NFD
- B) NFC
- C) NFKC
- D) Any of them

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: NFC composes characters to single code points, giving consistent storage. NFD decomposes and is used when stripping diacritics.

</details>

---

### Question 4 — Medium

**What Unicode category do Arabic diacritics belong to?**

- A) Ll
- B) Nd
- C) Mn
- D) Po

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Diacritics are combining marks, category `Mn`. Stripping them is the standard normalization step.

</details>

---

### Question 5 — Medium

**Why does exact string matching fail on Arabic retrieval?**

- A) Arabic has too many letters
- B) Morphology builds many words from one root
- C) Arabic is written right to left
- D) Diacritics are always present

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Triliteral roots generate many related words (كتب، كتاب، مكتبة). Exact matching misses these morphological variants.

</details>

---

### Question 6 — Medium

**What is the classic Arabic encoding trap?**

- A) Using UTF-16 instead of UTF-8
- B) Reading a UTF-8 file as Windows-1256, producing mojibake
- C) Using NFC instead of NFD
- D) Declaring encoding on file reads

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Wrong-encoding decode silently corrupts text. Always declare UTF-8 and verify with a round-trip test.

</details>

---

### Question 7 — Medium

**Which letters never join to the following letter in Arabic?**

- A) All 28 letters
- B) Six specific letters
- C) Only the vowels
- D) None

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Six letters (و ز ر ذ د ا) never join forward, which is why words can look disconnected.

</details>

---

### Question 8 — Hard

**What is the correct way to strip diacritics in Python?**

- A) `text.replace("َ", "")`
- B) Normalize to NFD, then remove all `Mn` characters
- C) Normalize to NFC, then remove all letters
- D) Encode to UTF-8 and back

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: NFD decomposes diacritics into combining marks (category `Mn`), which are then filtered out. Replacing individual marks is fragile.

</details>

---

### Question 9 — Hard

**Which of these words shares the root with كَتَبَ?**

- A) سَلَام
- B) مَكْتَب
- C) قَلَم
- D) بَاب

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: مَكْتَب (office) shares the k-t-b root with كَتَبَ (he wrote). This is the morphological link retrieval must exploit.

</details>

---

### Question 10 — Hard

**What is the consequence of normalizing the display text?**

- A) Faster search
- B) The user's quote no longer matches the source
- C) Better storage
- D) No consequence

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If normalization alters the displayed quote, the citation no longer matches the source text — a correctness bug, not a cosmetic one.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | C | Medium |
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
| 9-10 | Expert | Ready for normalization and retrieval topics |
| 7-8 | Proficient | Review the two-text discipline |
| 5-6 | Developing | Re-study Unicode handling |
| 0-4 | Novice | Restart the fundamentals lecture |

---

**Next**: [02 - Normalization and Tokenization](02-arabic-normalization-tokenization-quiz.md)