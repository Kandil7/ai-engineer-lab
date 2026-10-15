# ADR-0012: Choose MinHash LSH for near-duplicate dedup

- **Status:** Proposed
- **Date:** 2026-10-15
- **Deciders:** Repo owner (AI engineer track)
- **Tags:** data-engineering, deduplication, minhash, lsh

## Context

Topic `05-deduplication` covers exact dedup (by key, by content hash) and edit
detection. Real corpora also contain near-duplicates: boilerplate with small
variations, the same passage with different whitespace or diacritics, pages
reprinted across editions. Exact hashing never catches these, and they silently
inflate retrieval indexes. Topic 17 must teach approximate dedup.

## Decision Drivers

- The method must catch near-duplicates with a measurable precision/recall, not
  a vibe ("looks similar").
- `datasketch` is absent on this machine and installs need approval, so the
  teaching implementation must run today with zero installs.
- The production path must still be named, so the teaching code is never
  mistaken for it.

## Options Considered

### Option A — datasketch MinHashLSH

- Pros: the production library; battle-tested LSH index; one import.
- Cons: not installed; adopting it now blocks topic 17 on provisioning; the user
  would learn an API instead of the algorithm.

### Option B — stdlib MinHash signatures plus LSH banding (chosen)

- Pros: zero dependencies (`hashlib` shingles, seeded permutation parameters for
  determinism); teaches the actual algorithm: shingling, signature matrix,
  band-row LSH, Jaccard estimation; precision/recall measurable on a fixture
  corpus with known duplicate pairs.
- Cons: slower than `datasketch` at scale; no persistent index; must carry an
  explicit "not production code" label.

### Option C — embedding-similarity dedup

- Pros: catches paraphrases, not just shingle overlap.
- Cons: needs an embedding model and GPU time; thresholds are uncalibrated without
  a labelled set; massively overkill for boilerplate dedup. Rejected for this
  layer (embeddings belong to retrieval, not to corpus cleaning).

## Decision

Option B for topic 17 and the capstone `dedup.py`: character-shingle MinHash with
LSH banding, deterministic seeds, reporting estimated Jaccard per candidate pair
and a measured dedup ratio (rows before/after) on the fixture corpus. The lecture
maps each piece to its `datasketch` counterpart (`MinHash`, `MinHashLSH`,
`num_perm`, `threshold`) so the production migration is a follow-up, not a
rewrite. Exact dedup from topic 05 stays as the first pass; MinHash is the second.

## Consequences

- Positive: approximate dedup is runnable offline today with honest metrics; the
  two-pass order (exact, then approximate) is explicit and tested.
- Negative: stdlib implementation must not ship to production use; threshold
  tuning is corpus-specific and must be re-measured, never copied.
- Follow-ups / new ADR candidates: a migration ADR if `datasketch` gets adopted
  for corpora above ~1M passages.

## Links

- Related ADRs: ADR-0010 (dependency adoption).
- Related artifacts (reviews, plans, eval reports):
  `projects/00-core-foundations/data-engineering/05-deduplication/`,
  `17-minhash-lsh/`, `capstone` (`dedup.py`, acceptance tests).
