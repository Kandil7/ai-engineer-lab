# Arabic NLP 09: Arabic Morphology, Tokenization and Surface Variation — Quiz

> **Topic Overview**: Root-and-pattern morphology, clitic anatomy, conservative
> segmentation, tokenization cost/coverage trade-offs, diacritic handling,
> variety policy, and the MOR001-MOR007 pipeline audit.

---

## Questions

### Question 1

**Difficulty:** Easy

**In the root-and-pattern system, the root ك-ت-ب primarily carries:**

- A) The grammatical tense of the verb
- B) The definiteness of the noun
- C) A semantic field related to writing
- D) The number of the subject

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: The root is the consonantal semantic base. Patterns (wazn)
assign grammatical roles: كَتَبَ (verb), كاتِب (writer), كِتاب (book). Tense
and number are pattern or affix properties, not root properties.

</details>

---

### Question 2

**Difficulty:** Easy

**The word وَالكِتَابِهَا segments (conservatively) into:**

- A) و / ال / كتاب / ها
- B) وا / كتاب / ها
- C) و / ك / تاب / ها
- D) وال / كتابها

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation**: R1 strips the conjunction و, R3 strips the article ال, R5
splits the multi-character enclitic ها. The stem كتاب survives with its
4 characters; no root material is touched.

</details>

---

### Question 3

**Difficulty:** Easy

**Why does the conservative segmenter keep الله whole instead of splitting it
into ال + ...?**

- A) الله is in the composition guard list for bare prepositions
- B) After stripping ال, only 2 characters would remain — below the ≥ 3
  length floor
- C) The shadda blocks prefix stripping
- D) الله is stored in a special lexicon that the segmenter never touches

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The length floor requires ≥ 3 characters to remain after any
article strip. الله minus ال leaves له (2 chars), so R3 refuses. The
composition guard (_COMPOSITION_GUARD) protects لكن, a different trap.

</details>

---

### Question 4

**Difficulty:** Easy

**Under the two-text discipline, where do tashkeel (short vowels) survive?**

- A) In the fuzzy key only
- B) In the segmented copy only
- C) Nowhere — they are always deleted
- D) In the display/original copy, and in working copies only when the
  content class is quranic display

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation**: Display copies keep the observed form verbatim (Quranic text
keeps every mark). Working copies strip combining marks for matching. The
stored-strip mistake is MOR002.

</details>

---

### Question 5

**Difficulty:** Medium

**A full root extractor maps كاتِب (writer), كِتاب (book), and مَكْتَبَة
(library) all to ك-ت-ب. Why is that dangerous for embedding?**

- A) The three words describe different senses; collapsing them destroys
  meaning before the model sees it
- B) The root extraction is too slow for batch pipelines
- C) Roots contain only consonants, so embeddings cannot be computed
- D) The three words are actually three different roots

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation**: Root collapse merges a writer, a book, and a place under one
key. That is the MOR003 pathology: stem feeding embed with no evaluation
gate. Gated expansion on the lexical arm recovers recall without this
collapse.

</details>

---

### Question 6

**Difficulty:** Medium

**The exercise's tokenizer harness reports: word 1.0 tok/word (0% unk),
subword 1.68 (8.6% unk), byte-fallback 8.78 (80.5% byte chars). What does the
subword column's 8.6% unk rate represent?**

- A) A bug in the greedy longest-match loop
- B) Characters the subword vocabulary cannot represent — expected for a
  hand-built vocab, near-zero for a trained BPE
- C) The share of words that are out-of-domain dialect
- D) The byte-inflation factor for Arabic letters

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Unknown-character rate measures vocabulary coverage. The
exercise's curated fragment list is intentionally incomplete; a trained BPE
covers its training distribution. The byte-inflation factor is the 8.78
tok/word column, not the unk rate.

</details>

---

### Question 7

**Difficulty:** Medium

**In the MOR catalog, which findings are severity "error" (data destruction
or double-processing)?**

- A) MOR003, MOR004, MOR005
- B) MOR001, MOR004, MOR007
- C) MOR002, MOR003, MOR006
- D) MOR001, MOR002, MOR006

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation**: Errors are destruction or double-processing: MOR001
(original overwritten), MOR002 (tashkeel stripped from stored content),
MOR006 (segmenter over subword ids). MOR003/004/005/007 are warnings —
silent quality loss or governance gaps.

</details>

---

### Question 8

**Difficulty:** Medium

**The elided-lam fused preposition لل reconstructs as ل + ال + stem. What
orthographic rule does `reconstruct` need for the round trip?**

- A) Strip the alef from every article
- B) When a segment ل is followed by the article ال, join them as لل (the
  alef is re-added)
- C) Always insert a space between preposition and article
- D) Convert ل to lam-gemination before joining

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: ل + ال is written لل in orthography (alef elided after lam).
`reconstruct` applies exactly one rule: buffer ending in ل + ال → لل. Every
other clitic concatenates directly; 18/18 samples round-trip.

</details>

---

### Question 9

**Difficulty:** Medium

**Digit folding (١٤٤٥ → 1445) is applied to:**

- A) The display copy, so citations show ASCII digits
- B) Fuzzy keys only, like ta marbuta folding
- C) The working copy; the display keeps the source digits
- D) Neither copy — digits are left verbatim everywhere

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Digit folding is an index/working-copy rule: edition, page,
and year fields must compare across digit systems. The display copy keeps
what the source wrote. Leaving digits unfolded is MOR007.

</details>

---

### Question 10

**Difficulty:** Medium

**A corpus mixing MSA, classical, Egyptian, Levantine, and Gulf passages
with no variety decision triggers:**

- A) MOR004 — a warning that one tuning knob cannot serve mixed varieties
  without a recorded policy
- B) MOR001 — the originals are considered corrupted
- C) MOR006 — dialect text confuses the segmenter
- D) Nothing; mixed varieties are always safe

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation**: MOR004 fires when dialect_sources has more than one entry
and variety_decision is None. The GOOD pack stamps variety at ingest and
records an explicit, versioned policy (ar-morph-variety-1.0).

</details>

---

### Question 11

**Difficulty:** Hard

**In the GOOD pipeline, where does `stem` sit relative to `embed`, and why?**

- A) Before embed, because embeddings work best on stems
- B) After index, so BM25 sees stems first
- C) Parallel to embed, on a copy of the raw text
- D) After embed, scoped to the lexical arm, behind eval_gate=True —
  embeddings get normalized-but-unstemmed text; stemming's recall gains are
  measured, not assumed

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation**: MOR003 catches stem-before-embed with no gate. The GOOD
pack orders embed on normalized text, then segment/stem serve the lexical
(BM25 expansion) arm. The audit checks declared order and the gate flag.

</details>

---

### Question 12

**Difficulty:** Hard

**The segmenter's reconstructability invariant states:**

- A) reconstruct(segments) == original (byte-identical to display)
- B) reconstruct(segments) == normalized (the working copy), with the single
  ل + ال → لل orthographic rule
- C) reconstruct(segments) == fuzzy_key
- D) reconstruct(segments) is a best-effort string; mismatches are warnings

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Segments are derived from the normalized working copy, so
the round trip targets normalized, not the diacritized original. It is an
assertion, not a warning: 18/18 samples must round-trip or the segmenter
has a bug.

</details>

---

### Question 13

**Difficulty:** Hard

**The invariant "only known clitics may be short; stems keep ≥ 3 chars" is
relaxed for:**

- A) Words starting with الله
- B) Multi-character suffix splits (base ≥ 2)
- C) Unsplit short words — a whole word like مش is a complete lexical item,
  not an extracted stem
- D) Dialect samples only

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: The length rule protects against bad *splits*. A 2-char
word that was never split (the Levantine negator مش) is not an extracted
stem; it passes untouched. The exercise's first run failed precisely until
this distinction was coded.

</details>

---

### Question 14

**Difficulty:** Hard

**A production pipeline swaps a multilingual sentence-transformer for an
English-only model "because it benchmarks better on MTEB." Based on this
lecture, the primary risk is:**

- A) Tokenizer mismatch: Arabic pays the byte-fallback tax (~8.8 tok/word,
  80.5% byte chars), sequences inflate, and quality collapses regardless of
  the English benchmark
- B) The display copy will be overwritten
- C) MOR005 fires automatically
- D) The segmenter will split roots

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation**: The tokenizer is part of the model's contract. An
English-BPE model given Arabic produces the byte-fallback column: every
letter costs 2 byte tokens. Benchmarks on other scripts do not transfer;
measure tokens/word and unk/byte rates on Arabic before swapping.

</details>

---

### Question 15

**Difficulty:** Hard

**Classical Quranic readings can turn on diacritics and particle
segmentation (e.g., الملك / مَلِك variant readings). The pipeline's correct
behavior is:**

- A) Default to the majority reading and store only that segmentation
- B) Strip all diacritics so the ambiguity disappears from the index
- C) Merge both readings into one embedding to maximize recall
- D) Flag that multiple segmentations exist; never adjudicate which reading
  is correct — rulings belong to qualified scholarship, the tooling only
  preserves evidence

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation**: The Islamic-content safety rules: morphological ambiguity is
surfaced, not resolved; display text is evidence and stays verbatim; the
tooling makes no religious rulings. Options A, B, and C each destroy or
falsify the evidence.

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
| 1 | C | Easy |
| 2 | A | Easy |
| 3 | B | Easy |
| 4 | D | Easy |
| 5 | A | Medium |
| 6 | B | Medium |
| 7 | D | Medium |
| 8 | B | Medium |
| 9 | C | Medium |
| 10 | A | Medium |
| 11 | D | Hard |
| 12 | B | Hard |
| 13 | C | Hard |
| 14 | A | Hard |
| 15 | D | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 13-15 | Expert | Pipeline design ready — try the MOR008 design exercise |
| 10-12 | Proficient | Review the stemming gate and tokenizer trade-off sections |
| 7-9 | Developing | Re-read clitic anatomy and the audit catalog (sections 2, 8) |
| 0-6 | Novice | Start from the two-text discipline in arabic-nlp 02 |

---

**Previous**: [08 - Entity Resolution](../08-arabic-entity-resolution/08-arabic-entity-resolution-quiz.md)
**Next**: 10 (planned) — Arabic NER and entity linking
