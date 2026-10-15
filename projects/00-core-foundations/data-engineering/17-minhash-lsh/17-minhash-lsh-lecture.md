# Data Engineering 17: MinHash LSH for Near-Duplicate Dedup

## Topic Overview

Exact dedup ends where near-duplicates begin. Topic 05 taught dedup by stable
key and by content hash, and that machinery catches every byte-identical copy.
It catches nothing else: a passage with one changed word has a completely
different hash, so it sails through and is indexed as if it were new.

This lecture extends 05 into approximate dedup: shingling a passage into
overlapping pieces, compressing those pieces into a MinHash signature, banding
signatures with LSH so only plausible pairs are ever compared, and measuring
the result as precision and recall on a labelled pair set. The output is a
review queue, same as in 05, not an automatic delete.

The implementation here is stdlib-only by decision, not by accident. ADR-0012
chose a teaching implementation over the production library, and ADR-0010
records why: `datasketch` is not installed, installs need approval, and the
exercise must run today. The lecture maps every piece to its `datasketch`
counterpart so the production migration is a follow-up, not a rewrite.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Name three near-dupe shapes that exact hashing misses.
2. Shingle a passage and explain the k selection trade-off.
3. Explain how MinHash permutation minima estimate Jaccard similarity.
4. Explain LSH banding: bands, rows, the S-curve, and threshold movement.
5. Measure precision and recall of a dedup pass on a labelled pair set.
6. Run exact dedup first and approximate dedup second, and re-measure the threshold per corpus.

## Prerequisites

- Data Engineering 05 (deduplication) for the exact pass and the review queue.
- Data Engineering 03 (idempotency) for the stable key the first pass uses.

---

## 1. Why Exact Hashing Misses Near-Dupes

### The cliff effect

A cryptographic hash is a cliff: one changed character flips half the bits.
That cliff is exactly what edit detection wants, and exactly what
near-duplicate detection cannot use. Similarity needs a slope, not a cliff.

### Three shapes that slip through

Boilerplate variants are the first shape: the same notice, header, or
template with a date, name, or number changed. The passages are duplicates
for retrieval purposes, but no two hashes match.

Whitespace and diacritic differences are the second shape, and they dominate
Arabic corpora: extra spaces, a missing hamza, tatweel, or vocalization marks
added by one source and stripped by another. The eye sees one passage; the
hash sees two unrelated strings.

Reprints are the third shape: the same text reprinted across editions with
small corrections, a reflowed line, or a changed word. Each reprint is a new
row with a new hash, and the index quietly fills with copies that split
relevance exactly the way 05 describes, except no hash check will flag them.

## 2. Shingling

### The tool

Shingling turns a passage into a set of overlapping character k-grams.
Two passages that differ in one word still share almost all their shingles,
which converts a cliff into a slope:

```python
def shingles(text: str, k: int = 5) -> set[str]:
    text = text.strip()
    if len(text) <= k:
        return {text}
    return {text[i : i + k] for i in range(len(text) - k + 1)}
```

### The k selection trade-off

Small k makes shingles generic: with k at 2 or 3, unrelated passages share
many pieces and every pair looks similar. Large k makes shingles brittle: a
single changed word destroys every shingle covering it, and near-dupes stop
matching. Character 5-grams are the conventional starting point for text,
word shingles suit longer documents, and the choice is validated by
measurement, never by habit. Shingle sets then support Jaccard similarity,
overlap over union: identical passages score 1, near-dupes land high, and
unrelated ones score near 0. That number is the slope hashing could not give.

## 3. MinHash Signatures

Comparing all shingle sets pairwise is quadratic, which dies at corpus scale.
MinHash compresses each set into a short signature that preserves Jaccard, so
most pairs can be skipped without comparison.

### The intuition, not the proof

Hash every shingle with one seeded hash function and keep the minimum value.
Two sets share a minimum exactly when the shingle that hashes lowest sits in
their overlap, and that happens with probability equal to their Jaccard. One
minimum is one noisy vote; repeating with many seeded permutations gives a
signature whose agreement fraction estimates Jaccard within a few points.

### Determinism is a requirement

Every permutation is seeded from a fixed seed, so the same input always
produces the same signature and `--verify` stays reproducible. Randomness
without a seed is a correctness bug here, not a style choice. This hand-rolled
signature is `datasketch.MinHash` with `num_perm` as the signature length:
the teaching code shows the algorithm, the library is what a production
corpus runs, and ADR-0012 keeps the two apart on purpose.

## 4. LSH Banding

Comparing all signatures pairwise is still quadratic, so LSH banding slices
each signature into bands of rows: passages matching completely in at least
one band become candidates, and only candidates pay for a full comparison.

### Bands, rows, and the S-curve

With more bands, a pair gets more chances to match, so recall rises and
precision falls. With more rows per band, each band is harder to match, so
precision rises and recall falls. Plotted against true similarity, the
candidate probability follows an S-curve: flat near zero, steep in the
middle, flat near one. The steep middle is the operating threshold.

### How the threshold moves

Fewer rows per band slides the threshold down and catches looser pairs;
more rows slides it up and keeps only tight pairs. Tuning dedup means moving
this threshold deliberately: 32 bands of 4 rows lands near 0.4 similarity,
which suits short-passage review queues. The number is a starting point for
measurement, not a constant to copy.

Bands and rows are `datasketch.MinHashLSH` with `threshold` and `num_perm`:
the threshold is the S-curve middle and `num_perm` equals bands times rows,
so migration becomes configuration.

## 5. Precision and Recall on a Labelled Pair Set

### Why a labelled set

"This looks like it dedups well" is not a measurement. A fixture corpus with
known pairs, one planted near-dupe, one exact dupe, and unrelated passages,
turns dedup into numbers: of the pairs flagged, how many were real dupes
(precision), and of the real dupes, how many were flagged (recall).

### Reading the two numbers

Low precision fills the review queue with unrelated pairs until reviewers
stop trusting it; low recall leaves near-dupes degrading retrieval. Every
threshold choice is a precision-recall choice, which is why section 4 exists.

### The negative test matters most

05 taught the two-half test, and it applies here: asserting that unrelated
passages are never paired is the half that catches an over-aggressive
threshold. A dedup that flags everything has perfect recall and is useless.

## 6. Two-Pass Order and Threshold Discipline

### Exact first, approximate second

The exact pass from 05 runs first: content hashes remove byte-identical rows
cheaply and deterministically. MinHash runs only on the survivors, so the
expensive similarity machinery never wastes time on pairs hashing already
settles. Reversing the order pays similarity costs for exact dupes.

### The threshold is corpus-specific

A threshold tuned on news boilerplate misfires on hadith chains, where
genuinely distinct narrations share long spans. Every new corpus re-measures
precision and recall on its own labelled pairs and picks its own threshold.
A copied threshold is an untested assumption wearing a number.

LSH output is a candidate list for human review, inheriting the 05 rule:
similarity proposes, a human disposes. Automatic deletion at a similarity
threshold is how distinct content dies.

## Real-World Application

- Catching boilerplate reprints across book editions so the index holds one copy.
- Normalizing whitespace and diacritic variants before shingling Athar passages.
- Turning LSH candidates into a reviewer queue with estimated Jaccard attached.
- Running exact-then-approximate dedup in CI with the dedup ratio reported.

## Common Mistakes

1. **Running MinHash before exact dedup.** Hashing removes exact dupes for free.
2. **Copying a threshold from another corpus.** Thresholds are re-measured per corpus.
3. **Auto-deleting LSH candidates.** Candidates feed a review queue, not a delete job.
4. **Unseeded permutations.** Non-deterministic signatures break reproducibility.
5. **Reporting recall without precision.** A queue full of false pairs trains reviewers to ignore it.

## Key Takeaways

1. Exact hashing misses boilerplate variants, whitespace and diacritic differences, and reprints.
2. Shingling converts the hash cliff into a Jaccard slope; k is a measured trade-off.
3. MinHash signatures estimate Jaccard via seeded permutation minima.
4. LSH banding makes candidates cheap; bands times rows set the S-curve threshold.
5. Exact dedup runs first, MinHash second, and the threshold is re-measured per corpus.

## Self-Check Questions

1. Why does a one-word change defeat content hashing but not shingling?
2. What breaks when k is too small? When k is too large?
3. Why must MinHash permutations be seeded?
4. How do bands and rows move the LSH threshold in opposite directions?
5. Why does the two-pass order put exact dedup before approximate dedup?

## Further Reading / Connections

- Data Engineering 05 (deduplication) — the exact pass and review queue this extends.
- ADR-0012 — the stdlib teaching implementation versus `datasketch` production path.
- ADR-0010 — why this topic stays install-free and dependency honest.
- Arabic NLP 02 (normalization) — the normalization that runs before shingling.
