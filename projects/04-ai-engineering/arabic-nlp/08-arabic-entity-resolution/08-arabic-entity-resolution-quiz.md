# Arabic NLP 08: Arabic Entity Resolution — Quiz

> **Topic Overview**: Normalization for matching, blocking, fuzzy similarity,
> weighted scoring with conflict vetoes, canonization, merge-with-review, and
> gold-pair evaluation for the Arabic scholarly corpus.

---

## Questions

### Question 1

**Difficulty:** Easy

**Which normalization rule is applied only to fuzzy candidate keys, never to
the index copy?**

- A) Alef variants folded to ا
- B) ة folded to ه
- C) Tashkeel stripped
- D) Digits folded to ASCII

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Folding ة to ه in the index copy merges distinct words, so
it belongs in relaxed fuzzy keys only. The exercise asserts
`normalize_ar("مدرسة") != normalize_ar("مدرسه")` — the index copy keeps ة
and ه distinct.

</details>

---

### Question 2

**Difficulty:** Easy

**Under the two-text discipline, where do diacritics (tashkeel) survive?**

- A) Nowhere — they are always deleted
- B) In the display/original copy only
- C) In the normalized key only
- D) In blocking keys only

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The display copy keeps the verbatim form with tashkeel;
the index copy strips it so محمَّد and محمد collide for matching.

</details>

---

### Question 3

**Difficulty:** Easy

**Blocking exists to replace:**

- A) Fuzzy similarity with exact match
- B) The O(n²) all-pairs comparison with key-grouped candidates
- C) Human review with automatic merging
- D) The alias table with a lookup index

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: 10,000 records imply ~50 million all-pairs scores. Blocking
compares only records sharing a trigram or bucket key.

</details>

---

### Question 4

**Difficulty:** Easy

**A homonym is:**

- A) A name written in two scripts
- B) Two different people sharing the same name
- C) A book with two title variants
- D) A record missing its death year

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Identical names across different people are the corpus's
most dangerous false-merge case — string equality is correct and the merge
is still wrong.

</details>

---

### Question 5

**Difficulty:** Medium

**After normalization, which pair keys as EQUAL in the index copy?**

- A) مدرسة and مدرسه
- B) كتاب الإيمان and كتاب الايمان
- C) الشافعي and محمد بن إدريس الشافعي
- D) محمد بن عبد الله (d. 150) and محمد بن عبد الله (d. 200)

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Alef variants (أ here) fold to ا, so the two spellings
normalize identically. A fails because ة does not fold; C differs in tokens;
D is equal but is a different pair problem (homonyms).

</details>

---

### Question 6

**Difficulty:** Medium

**Blocking recall of 0.50 means:**

- A) Half the auto-merges are wrong
- B) Half of the true pairs never share a blocking key
- C) Reviewers reject half the candidates
- D) The thresholds are 0.50

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Blocking recall is a ceiling on merge recall: pairs never
generated as candidates can never merge, no matter how good the scorer is.

</details>

---

### Question 7

**Difficulty:** Medium

**Jaro-Winkler is the right similarity for personal names because it:**

- A) Ignores the end of the string
- B) Rewards a shared prefix, where names often agree before they differ
- C) Compares character trigram sets
- D) Counts only transpositions

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: محمد بن ... records share a long prefix and differ at the
end; the Winkler prefix bonus keeps those pairs above threshold where pure
edit distance weakens.

</details>

---

### Question 8

**Difficulty:** Medium

**Why must every normalized key carry a normalizer version?**

- A) For faster string comparison
- B) Because keys from different rule sets are not comparable
- C) To satisfy the ULID specification
- D) Because display text embeds the version

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Changing a folding rule produces keys that cannot be mixed
with old ones. Bump the version and re-derive; never mix generations in one
index.

</details>

---

### Question 9

**Difficulty:** Medium

**The conflict veto fires when:**

- A) The score is below 0.55
- B) Two records disagree on year or context despite high string similarity
- C) A reviewer rejects a candidate
- D) Blocking generates too many pairs

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Policy outranks evidence: identical names with death years
50 years apart are held for review even at score 0.90 — they are probably
homonyms.

</details>

---

### Question 10

**Difficulty:** Medium

**Which identifier is recommended for canonical entity ids, and why?**

- A) UUIDv4 — it is standard
- B) Database sequence — it is simplest
- C) ULID or UUIDv7 — time-sortable and offline-generable
- D) The normalized name — it is meaningful

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Sortable ids keep merge/rebuild iteration ordered; offline
generation lets batch ingestion mint ids without an allocator. UUIDv4 sorts
poorly; DB sequences break offline and sharded runs.

</details>

---

### Question 11

**Difficulty:** Hard

**Why does the scoring model sit on the high-precision side of the
precision/recall curve?**

- A) Recall is impossible to measure
- B) A false merge corrupts a citation graph; a missed merge only
  duplicates a record
- C) Reviewers prefer precision
- D) Fuzzy similarity is biased toward recall

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The asymmetry is the whole argument: fused records poison
every citation and attribution downstream, while two unfused records merely
fragment retrieval. Recall is recovered with better blocking and aliases.

</details>

---

### Question 12

**Difficulty:** Hard

**A pair scores 0.90 but carries a year-conflict veto. Its correct
destination is:**

- A) Auto-merge — 0.90 exceeds AUTO
- B) No-merge — the veto is fatal
- C) The review band — a human adjudicates the contradiction
- D) Deletion of one record

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Vetoed pairs never auto-merge, but a 0.90 score plus
conflicting years is exactly the ambiguity a reviewer must see — probably a
homonym, possibly one record with a typo'd year.

</details>

---

### Question 13

**Difficulty:** Hard

**Merging two records should:**

- A) Delete the losing row
- B) Rewrite all foreign keys in place
- C) Tombstone the loser and alias its id to the canonical survivor
- D) Overwrite the loser's display with the normalized form

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Tombstones preserve provenance and let old ids resolve
through the alias map; deletion destroys audit history and makes un-merge
impossible.

</details>

---

### Question 14

**Difficulty:** Hard

**Merge evaluation should report:**

- A) One aggregate F1 over all entity types
- B) Precision/recall/F1 per category, plus blocking recall and end-to-end
  retrieval hit rate
- C) Only auto-merge counts
- D) Only reviewer satisfaction

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: An aggregate hides a narrator-precision collapse that
corrupts hadith attribution. Blocking recall separates "never generated"
from "scored too low"; hit rate proves the user-visible payoff.

</details>

---

### Question 15

**Difficulty:** Hard

**Why does isnad-narrator resolution come AFTER authors and books?**

- A) Narrators are less important
- B) Narrators have no aliases
- C) Narrators are the hardest homonym problem, so they need a tested
  review workflow and resolved author/book context first
- D) Arabic names are easier for books

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Phased rollout follows blast radius: books/authors have the
richest alias evidence and easiest labels; narrators wait until the reviewer
queue and context signals are proven.

</details>

---

## Score Tracking

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 15 |
| Correct Answers | 0 |
| Score | 0% |

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Easy |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | C | Medium |
| 11 | B | Hard |
| 12 | C | Hard |
| 13 | C | Hard |
| 14 | B | Hard |
| 15 | C | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 13-15 | Expert | Pipeline design ready — try the threshold-sweep exercise |
| 10-12 | Proficient | Review the veto and canonization sections |
| 7-9 | Developing | Re-read blocking and scoring sections 3-5 |
| 0-6 | Novice | Start from the two-text discipline in arabic-nlp 02 |

---

**Previous**: [07 - MRR Evaluation](07-arabic-mrr-evaluation-quiz.md)
**Next**: 09 (planned) — Citation graph over resolved entities
