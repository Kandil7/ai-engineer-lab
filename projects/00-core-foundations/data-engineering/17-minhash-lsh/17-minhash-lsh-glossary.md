# Data Engineering 17: MinHash LSH — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Shingle | Overlapping k-gram piece of a passage | char 5-grams |
| Shingling | Turning text into a shingle set | sliding window |
| k | Shingle length, the granularity knob | k = 5 |
| Jaccard similarity | Overlap over union of two sets | 0.85 near-dupe |
| MinHash | Signature scheme estimating Jaccard | 128 minima |
| Signature | Ordered list of permutation minima | length 128 |
| Permutation | One seeded hash function over shingles | perm 7 of 128 |
| Seed | Fixed value making signatures deterministic | seed 42 |
| LSH | Banding trick surfacing likely pairs | shared band |
| Band | One horizontal slice of a signature | band 3 of 32 |
| Row | One signature position inside a band | 4 rows per band |
| S-curve | Candidate probability versus similarity | steep near 0.4 |
| Threshold | Similarity at the S-curve middle | ~0.4 at 32x4 |
| num_perm | Signature length, bands times rows | 128 = 32 x 4 |
| Candidate pair | Pair sharing one full band | (d1, d2) |
| Labelled pair set | Fixture corpus with known pairs | 1 near-dupe |
| Precision | Flagged pairs that are real dupes | 2 of 3 |
| Recall | Real dupes the pass flagged | 1 of 1 |
| Near-duplicate | Similar but not identical content | one word changed |
| Boilerplate | Template text with small variants | dated notice |
| Reprint | Same text reissued with corrections | new edition |
| Two-pass dedup | Exact pass first, approximate second | hash then LSH |
| Dedup ratio | Rows removed over rows before | 0.40 removed |
| datasketch | Production MinHash LSH library | MinHashLSH |

---

## Alphabetical Glossary

### Band

**Definition:** One horizontal slice of a signature; a pair matching fully in any band becomes a candidate. **Example:** band 3 of 32 with 4 rows.

### Boilerplate

**Definition:** Template text repeated with small variants like dates or names; the top near-dupe source. **Example:** the same notice reissued monthly.

### Candidate pair

**Definition:** A pair sharing at least one full LSH band, owed a full Jaccard comparison. **Example:** (d1, d2) sharing band 11.

### datasketch

**Definition:** The production MinHash LSH library; the migration target this topic prepares for. **Example:** MinHashLSH with threshold and num_perm.

### Dedup ratio

**Definition:** Rows removed divided by rows before; the headline metric of a dedup run. **Example:** 5 rows to 3 is 0.40 removed.

### Jaccard similarity

**Definition:** Overlap size over union size of two shingle sets; the slope hashing cannot give. **Example:** 0.9 for a one-word variant.

### k

**Definition:** Shingle length; small k over-matches, large k under-matches. **Example:** character k = 5 as the starting point.

### Labelled pair set

**Definition:** A fixture corpus with known dupe and non-dupe pairs for measuring precision and recall. **Example:** one planted near-dupe plus unrelated passages.

### LSH

**Definition:** Locality-sensitive hashing; banding that surfaces likely-similar pairs without all-pairs comparison. **Example:** 32 bands catching (d1, d2).

### MinHash

**Definition:** A signature scheme whose agreement fraction estimates Jaccard similarity. **Example:** 128 permutation minima per passage.

### Near-duplicate

**Definition:** Content similar but not identical; invisible to exact hashing, visible to shingles. **Example:** a reprint with one word changed.

### num_perm

**Definition:** The signature length; must equal bands times rows for the LSH mapping to hold. **Example:** 128 = 32 bands x 4 rows.

### Permutation

**Definition:** One seeded hash function whose minimum over the shingle set is one signature slot. **Example:** perm 7 of 128.

### Precision

**Definition:** Flagged pairs that are real dupes; low precision drowns reviewers in false pairs. **Example:** 2 true of 3 flagged.

### Recall

**Definition:** Real dupes the pass flagged; low recall leaves near-dupes degrading retrieval. **Example:** the planted pair found.

### Reprint

**Definition:** The same text reissued across editions with small corrections; hashes differ, content matches. **Example:** a corrected second edition page.

### Row

**Definition:** One signature position inside a band; more rows per band raise the threshold. **Example:** 4 rows per band.

### S-curve

**Definition:** The candidate-probability curve over similarity: flat, steep, flat; the steep middle is the threshold. **Example:** steep near 0.4 for 32x4.

### Seed

**Definition:** The fixed value deriving every permutation; determinism for reproducible verifies. **Example:** seed 42 for all 128 perms.

### Shingle

**Definition:** One overlapping k-gram piece; the unit of approximate comparison. **Example:** a 5-character slice.

### Shingling

**Definition:** Turning a passage into its shingle set with a sliding window. **Example:** windowing a normalized passage at k = 5.

### Signature

**Definition:** The ordered list of permutation minima standing in for the full shingle set. **Example:** 128 integers per passage.

### Threshold

**Definition:** The similarity at the S-curve middle; corpus-specific and re-measured, never copied. **Example:** ~0.4 for 32 bands of 4 rows.

### Two-pass dedup

**Definition:** Exact hashing first for byte-identical rows, MinHash second for the survivors. **Example:** hash removes d3, LSH merges d2.

---

## Related Concepts

- **Exact dedup**: the first pass this topic runs before MinHash (topic 05)
- **Review queue**: LSH candidates feed human review, never auto-delete (topic 05)
- **Normalization**: runs before shingling so variants compare fairly

## Key Takeaways

1. Shingles turn the hash cliff into a measurable slope.
2. Seeded MinHash signatures estimate Jaccard deterministically.
3. Bands times rows place the threshold; the threshold is re-measured per corpus.
4. Precision and recall on labelled pairs judge every dedup pass.
