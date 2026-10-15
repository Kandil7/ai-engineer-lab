# Arabic NLP 10: Arabic NER and Entity Linking — Quiz

> **Topic Overview**: Detection vs linking, the gazetteer baseline, clitic
> repair, ambiguity guarding, scored linking with AUTO/REVIEW/ABSTAIN
> bands, entity-level evaluation, Quran reference parsing, and the
> NER001-NER008 pipeline audit.

---

## Questions

### Question 1

**Difficulty:** Easy

**What does entity detection output, and what does entity linking add?**

- A) Detection outputs an entity ID; linking outputs the character span
- B) Detection outputs a typed character span; linking resolves that span
  to a knowledge-base entity ID
- C) Both stages output the same span, and linking only re-ranks it
- D) Detection outputs a token label; linking merges duplicate documents

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Detection answers *where* — a `Span(start, end, type)`
over the raw text. Linking answers *which* — resolving that span to a
canonical entity ID in the knowledge base. They have different failure
modes: a missed span vs a wrong ID.

</details>

---

### Question 2

**Difficulty:** Easy

**Why must the gazetteer baseline be measured before any model-improvement
claim?**

- A) Gazetteers are always more accurate than transformers on Arabic
- B) Without the baseline number, the model's delta cannot be attributed —
  the "improvement" may be the gazetteer doing the work
- C) Transformers refuse to run until a baseline file exists
- D) The baseline is required by the two-text discipline in topic 02

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: NER001 fires when a config claims a model F1 without a
measured gazetteer baseline. Without that reference point there is no way
to know whether the model contributed anything, so the claim is
unattributable. The GOOD pack records the claim and sets
`baseline_measured=True`.

</details>

---

### Question 3

**Difficulty:** Easy

**In the held-out document d10 (كتاب الإيمان لابن تيمية), the scholar
appears fused with the preposition ل. How does the detector recover the
entity core?**

- A) It matches the whole token لابن against the gazetteer
- B) It strips the article ال and matches تيمية
- C) It strips the known proclitic ل, matches the remainder ابن تيمية
  against the gazetteer exactly, and places the span on the core
- D) It tokenizes the preposition away with a morphological analyzer

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: Clitic repair strips known proclitics from the window's
first token and requires the remainder to hit the gazetteer exactly — the
gazetteer itself is the over-stripping guard. The span is placed on the
entity core (ابن تيمية), not the fused token (لابن). With repair off the
span is lost, which is the NER006 warning.

</details>

---

### Question 4

**Difficulty:** Easy

**Why is مالك marked `ambiguous` in the exercise's gazetteer?**

- A) It is spelled two different ways across dialects
- B) It is both a narrator's name and the ordinary word "owner," so it
  matches everywhere without a context cue
- C) It appears in both the Quran and hadith collections
- D) Its normalized form collides with the alef-maqsura fold

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Arabic has no capitalization, so مالك-the-narrator and
مالك-the-word-for-owner are orthographically identical. The entry is marked
ambiguous and requires a preceding context cue (e.g., the isnad
preposition عن) before it may match. Document d7 places it after الكتاب:,
and the guard holds.

</details>

---

### Question 5

**Difficulty:** Medium

**The exercise's link score is `0.7 * best_form_similarity + 0.3 *
token_overlap`. Why is Jaro-Winkler's prefix boost deliberately only a
*component* rather than the whole decision?**

- A) Jaro-Winkler is too slow to compute on large gazetteers
- B) Arabic name pairs concentrate their similarity on shared heads (ابن,
  أبو), so a string score alone would auto-link ابن الجوزي to ابن تيمية
- C) Prefix boosts only work on Latin transliterations
- D) Token overlap is the only signal that matters for Arabic names

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The shared prefix ابن boosts Jaro-Winkler substantially,
but the total score for ابن الجوزي vs ابن تيمية lands at 0.49 — below the
0.55 review floor — precisely because the boost is weighted beside
trigram Jaccard and token overlap rather than driving the decision alone.
The GOOD pack abstains.

</details>

---

### Question 6

**Difficulty:** Medium

**What are the three linking bands, and what does the pipeline do in
each?**

- A) HIGH/MEDIUM/LOW: always links, with decreasing confidence
- B) AUTO/REVIEW/ABSTAIN: links without review, links flagged for a
  human, and emits no ID
- C) PASS/FLAG/DROP: passes to the resolver, flags for merge, or drops the
  mention entirely
- D) MATCH/PARTIAL/NONE: merges, partially merges, or keeps separate

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: AUTO (score ≥ 0.85) links to the canon without review.
REVIEW (0.55–0.85) links but flags for a human. Below the floor the
pipeline abstains — no ID, no guess. The three-band design exists because
a wrong ID is worse than no ID.

</details>

---

### Question 7

**Difficulty:** Medium

**Why is force-linking every span (disabling abstention) an
error-severity finding, NER008?**

- A) It is slow, because every mention must be scored
- B) It produces output that looks complete but is quietly wrong — a wrong
  ID poisons every citation and merge that downstream trusts
- C) It violates the two-text discipline from topic 02
- D) It requires a neural tagger, which the exercise does not ship

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: NER008 is error severity because it breaks identity
integrity, not just ranking. The exercise's BAD pack force-links ابن
الجوزي (score 0.49) to a candidate the canon does not contain, and the
audit cites the count of force-linked spans. A system that links every
span looks complete and is silently untrustworthy.

</details>

---

### Question 8

**Difficulty:** Medium

**The BAD pack reports entity F1 0.909 while token F1 is 0.985. What
does this gap demonstrate?**

- A) The tokenizer is broken and needs re-training
- B) Token-level averages hide the span-level errors (a dropped clitic-attached
  span, a common-word false positive) that entity-level exact match catches
- C) The gazetteer is missing 9% of its entries
- D) The evaluator is double-counting true positives

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Token F1 averages over subtokens and barely notices a
dropped clitic-attached span or an over-long false positive. Entity-level
exact match scores both as total misses. Reporting only the token number
would look near-perfect while the pipeline is losing spans and admitting
false positives — which is exactly the NER003 warning.

</details>

---

### Question 9

**Difficulty:** Medium

**What must justify an auto-link threshold before it ships?**

- A) A round number chosen by convention, like 0.8 or 0.9
- B) A labelled pair study that samples the pairs the threshold would
  auto-link, has them human-judged, and records the delivered precision
- C) The threshold the model's training loss converged on
- D) The threshold used by the most popular NER library

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: NER002 fires when an auto-link threshold ships without a
labelled pair study, because the AUTO band's precision is then unmeasured.
The study samples pairs above the threshold, judges them same-entity /
not-same, and reports the precision the number actually delivers. Only
then is it defensible.

</details>

---

### Question 10

**Difficulty:** Medium

**Why does the exercise evaluate entity-level F1 *per document* and then
pool, rather than pooling all spans first?**

- A) It is faster on large corpora
- B) Spans from one document could otherwise be scored against another
  document's gold, silently corrupting the metrics
- C) Entity-level metrics cannot be computed on more than one document at
  a time
- D) The two-text discipline requires one evaluation pass per document

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: Character offsets are only meaningful within their own
document. Pooling raw span keys across documents lets a span from d1
coincidentally match a gold triple in d7. Keying every span set on its
document ID before comparing prevents that silent bug.

</details>

---

### Question 11

**Difficulty:** Hard

**In reference-parse mode the exercise rejects 2:999 but accepts 2:255.
What is the engineering reason for validating against a surah table, and
why is skipping it an error (NER005) rather than a warning?**

- A) The table is needed to normalize the digits; without it the parse
  crashes
- B) Validation is only cosmetic and NER005 is over-severity
- C) An unvalidated reference is how impossible citations leak into an
  Islamic corpus, and a fabricated citation there is a correctness bug,
  not a ranking miss
- D) The surah table is required by the Athar Passage contract

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: In an Islamic-knowledge corpus a citation that points to
a non-existent verse is a correctness failure with domain consequences,
not a retrieval-quality issue. The surah table (name → number → ayah
count) lets the parser reject out-of-range pairs, and the validated pair
resolves to a canon ID that is looked up, never minted. Hence NER005 is
error severity.

</details>

---

### Question 12

**Difficulty:** Hard

**The linker refuses to mint an ID even when the mention scores 1.0
against a gazetteer entry. Why is minting an ID an error (NER004) rather
than a harmless fallback?**

- A) Minted IDs are slower to look up than canon IDs
- B) A locally invented ID cannot be joined to topic 08's resolution
  output, the alias table, or any downstream citation — it breaks the
  identity chain the whole knowledge base depends on
- C) Minted IDs collide with the normalization map's offsets
- D) The canon forbids any identifier that is not a UUID

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The canon ID is the output of the resolution layer. A
minted `mint:person:shafii` is a different identifier for the same
entity, so every merge, alias, and citation keyed on the canon ID will
not find it. The linker's only legitimate ID source is a canon lookup;
when the canon does not contain the entity, the correct output is
abstention, not invention.

</details>

---

### Question 13

**Difficulty:** Hard

**Title extension emits both the inner mention (الشافعي) and the outer
phrase (الإمام الشافعي) as separate spans. Why keep both rather than only
the longer span?**

- A) The evaluator requires exactly two spans per name
- B) The inner span links at AUTO (exact match, 1.00) while the outer
  phrase links at REVIEW (0.57); keeping both preserves the precise
  canon join and the title context a reader needs
- C) The outer phrase is a different entity type and must be scored
  separately
- D) Longer spans always score higher, so both are needed for the
  threshold to fire

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: The inner mention is an exact gazetteer hit and links at
AUTO with full confidence. The outer title phrase is a fuzzier match that
lands in REVIEW — useful, but worth a human glance. Emitting only the
outer span would lose the precise AUTO join; emitting only the inner span
would discard the title context. Both are kept, each banded on its own
score.

</details>

---

### Question 14

**Difficulty:** Hard

**Why is the clitic-stripping remainder required to match a gazetteer
form *exactly*, rather than fuzzily?**

- A) Fuzzy matching is too expensive inside the window loop
- B) Exact matching on the remainder is what makes the gazetteer itself
  the over-stripping guard — والده would strip to هده, match nothing, and
  emit nothing
- C) Fuzzy matching would break the normalization map's offsets
- D) The exercise's gazetteer stores only normalized forms, so fuzzy
  matching is impossible

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation**: If the stripped remainder could fuzzily match anything,
every token would be a candidate and the strip would over-segment
constantly. Requiring an exact gazetteer hit means the strip is
self-limiting: only remainders that are known entity cores produce spans.
والده → هده matches nothing, so nothing is emitted — the guard is the
lexicon itself.

</details>

---

### Question 15

**Difficulty:** Hard

**The GOOD pack reaches entity F1 0.970, not 1.000, because قتادة in d11
is a deliberate false negative. Why does the exercise keep this miss
rather than adding قتادة to the gazetteer?**

- A) قتادة is not a real narrator and should not be in any gazetteer
- B) The gazetteer is already at its maximum size
- C) A measured baseline with a known, honest gap is more trustworthy
  than a padded one that looks perfect; the miss is the price of a
  transparent baseline, and NER001's discipline depends on that honesty
- D) The evaluator cannot score single-token names

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation**: A gazetteer that is quietly complete tells you nothing
about its real coverage; one with a documented gap tells you exactly what
it costs. The exercise keeps قتادة unlisted so recall is honestly 0.941,
not a suspicious 1.000. This is the same discipline as NER001: measure
what you have, state the gap, and improve it deliberately rather than
papering over it.

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
| 3 | C | Easy |
| 4 | B | Easy |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Medium |
| 9 | B | Medium |
| 10 | B | Medium |
| 11 | C | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | B | Hard |
| 15 | C | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 13-15 | Expert | Pipeline design ready — try the NER009 design exercise |
| 10-12 | Proficient | Review the linking bands and entity-level evaluation sections |
| 7-9 | Developing | Re-read clitic repair, the ambiguity guard, and the audit catalog |
| 0-6 | Novice | Start from the two-text discipline in arabic-nlp 02 and the canon model in 08 |

---

**Previous**: [09 - Morphology and Tokenization](../09-arabic-morphology-tokenization/09-arabic-morphology-tokenization-quiz.md)
**Next**: 11 (planned) — Arabic dialect identification
