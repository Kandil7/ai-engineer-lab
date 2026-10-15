# Arabic NLP 08: Arabic Entity Resolution

## Topic Overview

Entity resolution is the task of deciding which records refer to the same
real-world thing. In an Islamic-knowledge corpus the same scholar appears as
"kunya-only", "ism + nisba", "laqab + teknonym", fully diacritized, undiacritized,
Latin-transliterated, or spelled with a different alef. The same book appears
under title variants, edition statements with Arabic-Indic digits, and publisher
short forms. Until those records are resolved to one canonical entity, every
citation graph, isnad chain, and "works by this author" query built on top of
them is built on sand.

This lecture teaches entity resolution as an engineering pipeline: a versioned
normalizer that never mutates the display copy, blocking that replaces the
O(n²) cross product with measured-recall candidate generation, a weighted
scoring model over several match signals, a review band with a human in the
loop, canonization with reversible merges, and evaluation against a labelled
pair set. It is in the Arabic module because every stage has Arabic-specific
failure modes that a Latin-script tutorial never mentions.

The pipeline is implemented end to end in the companion exercise
`08-arabic-entity-resolution.py`, whose GOOD pack must score zero findings and
whose BAD pack must surface every planted pathology.

**Duration:** 4-5 hours
**Difficulty:** Advanced
**Prerequisites:** Arabic NLP 01 (text fundamentals), Arabic NLP 02
(normalization and the two-text discipline), Arabic NLP 07 (evaluation
methodology), basic Python dataclasses

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** why Arabic script, name structures, and digit systems make
   string equality an unusable identity test.
2. **Design** a versioned normalization stage that keeps the original text
   intact and produces a reproducible matching key.
3. **Build** blocking keys (trigram, length bucket, initial letter) that cut
   the pair space while measuring the recall they lose.
4. **Compute** character n-gram Jaccard, Damerau-Levenshtein, and
   Jaro-Winkler similarity and say which name pathology each one handles.
5. **Tune** a weighted scoring model and its thresholds on a labelled pair
   set, choosing precision over recall where a false merge is costlier.
6. **Canonize** resolved entities with ULID or UUIDv7 identifiers and an
   alias table that preserves every observed form.
7. **Route** low-confidence merges through a human review band with tombstones
   and a full audit trail instead of destructive updates.
8. **Measure** merge precision, recall, and F1 per entity category, plus
   blocking recall and end-to-end retrieval hit rate.
9. **Specify** the Author, Book, Alias, EntityId, MergeCandidate, and
   MergeDecision domain model with stated invariants.
10. **Justify** a phased rollout (authors and books first) and the content
    safety rules for a corpus of named scholars.

---

## Key Concepts

### 1. Why Arabic Makes Entity Resolution Hard

Entity resolution on English text is mostly a spelling problem. On Arabic
scholarly text it is a script problem, a naming-system problem, a numeral
problem, and a homonym problem at once:

| Difficulty | Example | What breaks |
|---|---|---|
| Alef variants | إيمان vs ايمان vs آيمان | Exact string match misses one spelling |
| Missing diacritics | محمَّد vs محمد | Same name, two byte sequences |
| Tatweel decoration | كتـــاب vs كتاب | Decorative glyph pollutes the key |
| Latin/Arabic mixing | ابن تيمية vs Ibn Taymiyyah | No shared characters at all |
| Arabic-Indic digits | ١٤٤٥ vs 1445 | Page, volume, and year fields disagree |
| Space placement | عبدالرحمن vs عبد الرحمن | Same name, different token count |
| Homonyms | محمد بن عبد الله (d. 150 AH) vs the same name (d. 200 AH) | String equality is *right* and the merge is *wrong* |

**Name anatomy.** Arabic personal names stack four independent name parts,
any of which a source may omit:

```
            "أبو عبد الله محمد بن أحمد بن إسماعيل الواقدي البغدادي"
             |_______| |_____________________| |________________|
               kunya            ism (with nasab)    nisba / laqab

  kunya  — teknonym:  أبو عبد الله        (honorific by firstborn)
  ism    — given name: محمد بن أحمد ...   (may include full nasab chain)
  laqab  — epithet:   الواقدي             (family or descriptive title)
  nisba  — origin:    البغدادي            (place/tribe attribution)
```

Two sources describing the same man may record disjoint subsets: one keeps
kunya + ism, another keeps ism + nisba, a third keeps only the laqab. The
"stacked name forms" problem is that identity must be judged over every
*subset* of the stack, not over one canonical rendering.

**The homonym problem is the hard core.** In a corpus spanning twelve
centuries of scholars, the same short name recurs across generations,
madhhabs, and regions. A pipeline that merges on name equality will silently
fuse different people. A pipeline that refuses to merge anything uncertain
leaves the corpus fragmented. The rest of this lecture is the design that
navigates between those two failure modes, with the cost asymmetry in
section 5 deciding where the line falls.

### 2. Normalization for Matching

**The two-copy rule.** Every record keeps two texts, exactly as the Athar
contracts enforce for passages: `display` (the verbatim observed form, with
diacritics and odd spellings) and `normalized` (the derived matching key).
Athar's `Passage` carries `original` and `searchable` for the same reason
(`projects/04-ai-engineering/athar-lab/contracts.py`). Nothing ever
overwrites the original; the normalized copy is always re-derivable.

**Version the normalizer.** The normalized key is meaningless without the
rules that produced it, so every stored key carries a normalizer version:

```python
NORMALIZER_VERSION = "ar-er-norm-1.0"


@dataclass(frozen=True)
class Alias:
    entity_id: str
    surface: str  # observed form, never mutated
    normalized: str  # derived key
    normalizer_version: str
```

Changing a rule (say, folding ة → ه into the index copy) produces keys that
are not comparable with the old ones: bump the version and re-derive, never
mix generations inside one index.

**The rule table.** The matching normalizer applies orthographic unification
only:

| Rule | Example | Applied to | Why |
|---|---|---|---|
| Alef variants → ا | أ إ آ ٱ → ا | index copy | Orthographic, not lexical |
| ى → ي | على → علي (key) | index copy | Alef maqsura and ya unify in keys |
| ة → ه | مدرسة → مدرسه | **fuzzy keys only** | Distinct words collide if folded in the index copy |
| Tashkeel stripped | محمَّد → محمد | index copy | Display copy keeps tashkeel |
| Tatweel removed | كتـــاب → كتاب | index copy | Purely decorative |
| NFC | decomposed ↔ precomposed | both | Same characters, one byte form |
| Digit folding | ١٤٤٥ → 1445 | index copy | Years, pages, volumes must compare |

Two deliberate asymmetries:

- **Tashkeel is stripped from the index copy but preserved for display.**
  Name matching must not care about vowel marks — محمَّد and محمد are the
  same man. Citation display must show the source exactly — that is the
  two-text discipline from Arabic NLP 02.
- **ة → ه is fuzzy-only.** Folding it in the index copy merges genuinely
  distinct words (the lecture-02 false-match table). It belongs in a relaxed
  key used to *generate candidates*, not in the equality key used to score
  them.

**Idempotence is a test, not a hope.** Normalizing twice must equal
normalizing once; the exercise asserts this on a diacritized probe string.
A non-idempotent normalizer silently corrupts re-indexing runs.

### 3. Blocking and Candidate Generation

**Never all-pairs.** Comparing every record with every other record costs
n(n-1)/2 comparisons: 10,000 records → ~50 million pairwise scores, each
running three string similarities over several name forms.

```
all-pairs (n = 10,000)                blocking (same corpus)

   e1 ─ e2 ─ e3 ─ ...                    key "author|tri|حمد"
   │ ╲  │ ╱  │                           ├─ au-17  (محمد بن ...)
   │  ╲ │ ╱   │                          ├─ au-42  (محمَّد بن ...)
   │   ╳│╱    │   50,000,000 pairs       └─ au-3   (أحمد بن حنبل)
   │  ╱ │╲    │                          key "author|tri|الب"
   │ ╱  │ ╲   │                          ├─ au-17  (... البخاري)
   e9  e8  e7                            └─ au-91  (... البلخي)
   n(n-1)/2                              only intra-key pairs get compared
```

**Blocking = grouping by keys shared by any same-entity pair.** The exercise
uses three key families, emitted for every form of every record:

1. **Character trigram keys** — `category|tri|حمد`-style keys over the
   collapsed normalized form. Robust to spelling noise: any two spellings of
   one name share most trigrams.
2. **Length + initial-letter keys** — `category|fl|م|5`: first character plus
   a length bucket (length // 4). Cheap bucketing that catches
   short-name variants trigrams would over-share.
3. **Category scoping** — every key carries the category (author, book,
   narrator). Authors never block with books; cross-category comparison is
   not entity resolution, it is a type error.

**Sorted neighborhood** is the classical alternative: sort records by a
normalized key and slide a window of width w over the sorted list, comparing
only records within the window. It is simple and preserves ordering-based
recall, but a single wildcard character moves a record across the whole sort.
The exercise's key-inverted index is the usual production choice; sorted
neighborhood appears here because you should know it exists.

**Blocking recall must be measured, not assumed.** Blocking is a recall
filter: if two same-entity records never share a key, no downstream matcher
can save them. Define:

```
blocking recall = gold pairs that share >= 1 blocking key
                  -----------------------------------------
                        all gold positive pairs
```

Report it next to merge precision/recall. The exercise's BAD pack plants an
Arabic-vs-Latin transliteration pair that shares no trigram — blocking
recall drops to 0.50 and the audit prints it as a `blocking miss`. The fix
direction (transliteration keys, alias-derived keys) is a design change, and
the point is that the pipeline *reports* the gap instead of hiding it behind
a good-looking merge metric.

### 4. Match Signals

No single signal decides identity. The scoring model collects independent
evidence, and each signal in the exercise exists because of a named Arabic
pathology:

| Signal | Definition | Pathology it catches |
|---|---|---|
| Exact-normalized | Some form pair equal after normalization (or space collapse) | Alef/diacritic/digit variants of one form |
| Char n-gram Jaccard | Jaccard of character bigram sets | Insertions and reordering that ruin edit distance |
| Damerau-Levenshtein | Edit distance + adjacent transpositions, normalized by length | Short names with one wrong/reordered letter |
| Jaro-Winkler | Common-prefix-weighted similarity | Personal names sharing a long prefix (محمد بن ...) |
| Token-set overlap | Jaccard over whitespace tokens | Partial-name records (kunya vs full nasab) |
| Alias agreement | Any recorded form of one record equals any form of the other | Different *records* of one person, linked by alias tables |
| Digit/date agreement | Shared digit runs: years, volumes, editions | ١٤٤٥ vs 1445; edition statements |
| Context agreement | Era, publisher, madhhab consistency | Homonyms: identical names, contradictory metadata |

**Character n-gram Jaccard** — set overlap of character bigrams:

```python
def char_ngram_jaccard(a: str, b: str, n: int = 2) -> float:
    ga = {a[i : i + n] for i in range(max(len(a) - n + 1, 1))}
    gb = {b[i : i + n] for i in range(max(len(b) - n + 1, 1))}
    return len(ga & gb) / len(ga | gb)
```

**Damerau-Levenshtein** adds adjacent transpositions to the three classical
edits, so محمّد-style letter swaps cost 1, not 2. Normalize by the longer
string's length so 1 edit in a 4-letter name weighs more than 1 in a
40-letter nasab chain.

**Jaro-Winkler** boosts strings by shared prefix length (up to 4 chars).
It was designed for personal names and behaves well on محمد بن ... records
where the distinguishing material sits at the *end* of the string — exactly
where edit distance and n-gram overlap weaken. The exercise's reference
assertion locks it to the published value: Jaro-Winkler(MARTHA, MARHTA) =
0.9611111, and identical strings must score exactly 1.0.

**Alias agreement** is the signal that makes resolution *transitive in
practice*: record A's display equals record B's alias, even though the two
displays are unrelated. In the GOOD pack, `محمد بن إسماعيل البخاري` and
`الإمام الجعفي` share the alias form that links them.

**Context agreement** carries the veto, not just a bonus (section 5): era
(death year), publisher, and madhhab metadata can *contradict*, and a
contradiction outranks string similarity.

### 5. Scoring and Thresholds

**Weighted evidence.** Each signal contributes its weight; the sum is the
pair's score:

```python
score = 0.30 * exact + 0.35 * fuzzy + 0.15 * token + 0.10 * alias + 0.10 * context
# fuzzy = 0.4*ngram + 0.3*DL + 0.3*JW over the best-matching form pair
```

These weights are not universal constants. They are the object you tune on
a **labelled pair set**: gold pairs (same entity) and sampled non-pairs
(different entities), ideally stratified per category. Sweep weights and
thresholds, plot precision/recall, pick the operating point.

**Three bands, two thresholds:**

| Score | Decision | Who acts |
|---|---|---|
| ≥ 0.85 (AUTO) and no veto | auto-merge | System, logged |
| 0.55 (REVIEW) to 0.85 | review | Human, in the merge queue |
| below 0.55 | no-merge | Nobody; stays a distinct record |

**The asymmetry argument.** A missed merge leaves two records; retrieval
returns slightly duplicated results, and a human can still find the material.
A false merge *fuses two different people or works into one*: every citation,
isnad edge, and book attribution attached to either record is now wrong, and
the corruption propagates into the knowledge graph where it becomes invisible
to downstream consumers. The cost ratio is not symmetric, so the operating
point sits on the high-precision side:

```
        precision
        1.0 ┤······················×
            │                 ×
        0.9 ┤             ×
            │          ·  ← operating point: precision-first
        0.8 ┤        ·
            │      ·                recall
        0.6 ┤   ·                 → 0.5: some gold pairs deferred
            │ ·                   → 0.9: most merged, some wrongly
        0.4 ×
            └────────────────────────────
```

Missing merges is a recall problem you measure and burn down (better
blocking keys, alias capture). Wrong merges are a correctness incident you
have to unwind. Spend precision where corruption is costly.

**The conflict veto.** A high string score never auto-merges across a
metadata contradiction. Two records both named `محمد بن عبد الله` with
death years 50 years apart score 0.90 on strings alone — the veto holds them
in the review band, where a human decides whether they are a homonym pair.
The exercise proves this: the naive baseline (strings only) merges them; the
governed pipeline holds them.

### 6. Canonization: Canonical IDs and the Alias Table

Resolution produces **clusters**; canonization gives each cluster one
permanent identifier and never forgets where it came from.

**ID choice — ULID or UUIDv7, not UUIDv4 and not database sequences:**

| Option | Sortable | Offline | Opaque | Verdict |
|---|---|---|---|---|
| ULID | Yes (time-prefixed, 48-bit ms) | Yes | Yes | Good default; 26-char Crockford base32 |
| UUIDv7 | Yes (time-prefixed) | Yes | Yes | Also good; RFC 9562 standard form |
| UUIDv4 | No (random) | Yes | Yes | Sorts poorly in indexes |
| DB sequence | Yes | **No** (needs the DB) | No (leaks counts) | Breaks offline ingestion and shard merges |

Sortable matters because merges and index rebuilds iterate clusters in
creation order; offline generation matters because Athar-style ingestion
runs in batch jobs that must not serialize on an id allocator. The exercise
implements ULID directly (timestamp << 80 | random, base32).

**The alias table preserves every observed form:**

```
canonical: 01JB7K... (ULID)          ← one row per cluster
  ├── alias: محمد بن إسماعيل البخاري  (surface, normalized, norm-version)
  ├── alias: الإمام البخاري
  ├── alias: محمَّد بن إسماعيل البخاري
  └── alias: au-1, au-2               ← retired record ids, also aliases
```

**No destructive updates.** Merging cluster B into cluster A never deletes
B's row or rewrites references in place. B becomes an alias of A's canonical
id: every stored foreign key that pointed at B still resolves (through the
alias map) to A. Queries deduplicate by canonical id; the display shows the
preferred surface form but citations keep the surface the *source* used.

### 7. Merge with Review

**MergeCandidate is the unit of work.** The scoring stage never touches
entities; it emits candidates:

```python
@dataclass(frozen=True)
class MergeCandidate:
    left_id: str
    right_id: str
    category: str
    score: float
    decision: str  # "auto-merge" | "review" | "no-merge"
    veto: str | None  # "year-conflict" | "context-conflict"
    signals: tuple[tuple[str, float], ...]  # evidence, for the reviewer
```

The reviewer sees the score *and* the evidence behind it — a queue that
shows only a number teaches reviewers to click through.

**Human-in-the-loop below the confidence band.** Anything in the review
band, and anything vetoed despite a high score, goes to a queue. Decisions
are recorded, not remembered:

```python
@dataclass(frozen=True)
class MergeDecision:
    candidate: MergeDecision ids...
    decision: str          # "merged" | "rejected" | "deferred"
    decided_by: str        # reviewer id or "auto-v1"
    decided_at: str        # ISO timestamp
    reason: str            # human note or veto reason
    score: float           # score at decision time
```

**Tombstone, not delete.** A rejected or merged-away record is marked
`status: "tombstoned"` with a pointer to its survivor. Consumers filter
tombstones; the row remains for audit and for un-merging.

**Audit trail and reversibility.** Every merge writes: the candidate, the
scores, the decision, the actor, the timestamp. Reversal is the *same
machinery backwards* — split the cluster, restore the tombstone, keep the
original merge decision record with `superseded_by`. If the threshold study
was wrong, you can unwind a thousand merges without a restore-from-backup
disaster.

### 8. Evaluation

**The labelled pair set is the instrument.** Sample record pairs, label them
same/different (two annotators on the homonym-prone strata, disagreements
adjudicated). Split by *record*, not by pair, so the same record does not
leak across train and test.

**Report merge quality per category.** Predicted merge = auto-merge
decisions; the review band counts as *deferred*, not as correct:

| Category | Precision | Recall | F1 | What each number guards |
|---|---|---|---|---|
| Authors | P = TP/(TP+FP) | R = TP/(TP+FN) | harmonic mean | Fused scholars vs fragmented bibliography |
| Books | ... | ... | ... | Fused titles vs duplicate editions |
| Narrators | ... | ... | ... | Fused transmitters vs broken isnad chains |

Aggregate F1 hides category failure: narrator precision is the number that
protects hadith attribution, so it gets its own threshold.

**Blocking recall is reported alongside.** Recall computed after blocking
conflates two failures (never generated vs generated-but-scored-low). Report
both, exactly as the exercise prints blocking recall next to per-category
metrics.

**End-to-end effect on retrieval hit rate.** Merge quality is a means; the
user-visible measure is whether retrieval improves:

```
hit rate before resolution: query "شروح صحيح البخاري"
  → top-5 scattered across 3 duplicate book records
hit rate after resolution: one canonical book row collects all editions,
  citations and "related works" edges land in one place
```

Define hit@5 over the golden query set from Arabic NLP 07, measure before
and after resolution, and require the delta to be positive. That number is
what justifies the pipeline to anyone who asks why records needed merging.

### 9. Domain Model

Six types, with invariants that tests enforce — an invariant violation is a
corruption bug, not a cosmetic one (the same stance as Athar's mandatory
`book_id` and `page`):

```python
@dataclass(frozen=True)
class EntityId:
    value: str  # ULID or UUIDv7; never reused, never rewritten
    # INVARIANT: non-empty; opaque (no semantic fields encoded)


@dataclass(frozen=True)
class Author:
    entity_id: EntityId
    display: str  # preferred surface form
    aliases: tuple[str, ...]  # every other observed form
    era: tuple[int, int] | None  # birth/death years AH, if known
    # INVARIANT: display non-empty; aliases unique; era ordered if present


@dataclass(frozen=True)
class Book:
    entity_id: EntityId
    display: str
    aliases: tuple[str, ...]
    author_id: EntityId | None  # points at a CANONICAL author id
    # INVARIANT: author_id, if set, resolves through the alias map to a
    #            non-tombstoned author


@dataclass(frozen=True)
class Alias:
    entity_id: EntityId
    surface: str  # observed, verbatim
    normalized: str  # derived
    normalizer_version: str  # which rules produced `normalized`
    # INVARIANT: (surface, normalizer_version) stored once per entity;
    #            surface is never modified after insert
```

`MergeCandidate` and `MergeDecision` were defined in section 7. Their
invariants:

- **MergeCandidate**: immutable; produced by scoring only; a pair appears at
  most once per pipeline run.
- **MergeDecision**: append-only; a reversal is a new decision that
  supersedes the old one — rows are never edited in place.

The identity invariant ties it together: **an entity's canonical id is
stable for life; its surfaces are mutable observations keyed by normalizer
version.** Identity is durable, spelling is data.

### 10. Phased Rollout

Resolve in this order, and justify each step by blast radius:

**Phase 1 — authors and books.** They have the richest alias evidence
(title variants, kunya/laqab forms, publisher statements), the easiest
labels (bibliographic data settles disputes), and the most direct
user-visible payoff (every "works by X" and citation query). The two-text
discipline and `Document`/`Passage` contracts in
`projects/04-ai-engineering/athar-lab/README.md` already give books stable
identity; resolution extends it.

**Phase 2 — isnad narrators.** Transmitters are the hardest homonym
problem in the corpus: short names recur across generations, and a wrong
merge corrupts hadith attribution. This phase waits for phase 1 precisely
because the human reviewers now have a working queue, and because narrator
resolution leans on resolved authors and books for context agreement
(a narrator's era is anchored by the works he transmits).

**Phase 3 — terminology.** Technical terms (fiqh vocabulary, sect names)
are not personal identity; homonymy is expected and *legitimate* (two
meanings of one term must stay distinct). Resolution here is
sense-differentiation, not identity, and it reuses the machinery only after
the identity phases are trustworthy.

Skipping to phase 2 first inverts the risk order: you would hand the
riskiest merges to the least-tested reviewer workflow.

### 11. Downstream: Resolution Before the Knowledge Graph

A knowledge or citation graph is built from *edges between canonical
entities*: book cites book, author writes book, narrator transmits from
narrator. Those edges are only as good as the node identity underneath.

```
unresolved corpus:                       resolved corpus:

  [كتاب الإيمان]──┐                       [كتاب الإيمان ◆ canonical]
  [كتاب الايمان]──┼─? same book?            ▲            │
  [الإيمان (طبعة ١٤٤٥)]──┘                 │            ▼ cites
                                     [author ▲] ── [other book ▲]

edges duplicated, lost, or wrongly drawn    one node, edges land correctly
```

What breaks if you skip resolution:

- **Citation edges split** across duplicate nodes, so no book looks cited
  and no scholar looks authoritative.
- **Citation edges wrongly fuse** when a homonym merge puts two authors'
  bibliographies together — a scholarly claim gets attributed to the wrong
  person.
- **Isnad chains break** at each duplicate narrator, or worse, close a false
  loop through a homonym merge.
- **Retrieval deduplication fails**: top-k fills with variants of one
  document, suppressing genuinely different evidence.

Resolution is therefore a *precondition* of graph construction, not a
cleanup pass after it.

### 12. Anti-Patterns

1. **Merging on the display string.** Normalized equality is one signal, not
   a verdict. It scores the BAD pack's homonyms as perfect matches; only the
   metadata veto stops the merge.
2. **Auto-merge without a threshold study.** Weights and cutoffs guessed
   from a demo, never measured against labelled pairs. Ship the sweep, not
   the gut feel.
3. **Destroying the losing record.** `DELETE` on merge loses provenance,
   breaks foreign keys, and makes un-merge impossible. Tombstone instead.
4. **Conflating homonyms.** Same name, different people — the failure mode
   this corpus has most and forgives least. Conflict vetoes and the review
   band exist for it.
5. **Letting blocking recall go unmeasured.** A perfect matcher over an
   incomplete candidate set has a recall ceiling nobody notices.
6. **Cross-category matching.** Comparing an author against a book because
   their strings look alike is a schema error, not a merge.
7. **Silent threshold changes.** Moving AUTO from 0.85 to 0.80 re-labels
   historical decisions as auto-approved. Version the threshold config and
   re-run evaluation on every change.

### 13. Content Safety for the Islamic Scholarly Corpus

This corpus is about named scholars with documented, often *differing*
positions. Resolution touches that directly, so the rules are hard
constraints, not preferences:

- **Same-name scholars are never silently conflated.** If two records share
  a name and their eras conflict, the only valid outcomes are `review` or
  `no-merge`. Auto-merge is forbidden by the veto, and the veto cannot be
  disabled by a config flag.
- **Differing scholarly positions must not be fused into one voice.** A
  merge asserts "these records are the same entity". It never asserts that
  two attributed positions agree, and no downstream summary may present a
  merged cluster as a single position without the sources behind it.
- **No religious rulings in the tooling.** The pipeline adjudicates record
  identity from bibliographic evidence only. Whether a position is correct
  is out of scope by design; the system does not evaluate, rank, or rule on
  matters of fiqh or aqidah.
- **Cite sources for claims.** Every assertion about a scholar in stored
  metadata carries its source reference (book, page, edition), consistent
  with how the corpus itself works. An identity decision's audit record is
  a bibliographic argument, or it is not a decision.
- **Prefer deferral over confidence.** When the evidence is genuinely
  ambiguous — two plausible identifications in the literature — the correct
  pipeline output is `review` with both readings recorded, not a coin-flip
  merge.

---

## Common Mistakes to Avoid

❌ Merging on the display string — normalized equality treats the BAD pack's
two `محمد بن عبد الله` homonyms as identical.
✅ Score multiple signals, and let year/context contradictions veto a merge
regardless of string score.

❌ Overwriting the original text with the normalized form.
✅ Keep display and normalized as two fields; the alias table stores the
observed surface forever (Athar's two-text discipline).

❌ Folding ة → ه into the index copy because lecture 02 "mentioned it".
✅ Use ta-marbuta folding only in fuzzy candidate keys; the exercise asserts
`مدرسة != مدرسه` in the index copy.

❌ Running all-pairs comparison over the corpus.
✅ Block by trigram, length bucket, and initial letter — and publish blocking
recall beside merge recall.

❌ Tuning weights in your head and shipping the thresholds.
✅ Sweep weights on a labelled pair set; check the precision/recall curve;
pick the precision-first operating point.

❌ Auto-merging everything above 0.55 to "improve recall".
✅ Three bands: auto-merge (high, veto-free), review (human), no-merge.
Recall is recovered with better blocking and aliases, not with a looser
merge.

❌ Deleting the losing record at merge time.
✅ Tombstone with a survivor pointer; reversal is a new decision, never an
edit.

❌ Reporting one aggregate F1 for all entity types.
✅ Per-category metrics; narrator precision guards hadith attribution and
deserves its own gate.

❌ Measuring merge quality only.
✅ Also measure end-to-end retrieval hit rate on the golden query set — the
number that justifies the pipeline.

❌ Letting a threshold or normalizer change go out without re-running
evaluation.
✅ Both are versioned config; a change re-derives keys and re-runs the gold
pair set before merge authority is restored.

---

## Best Practices

1. **Version everything that touches identity:** normalizer version, weights,
   thresholds, blocking-key schema. Each is part of the corpus version.
2. **Emit candidates, never mutate records, in the scoring stage.** All
   writes happen through MergeDecision, append-only.
3. **Put the veto above the score.** Conflict rules are policy; scores are
   evidence. Policy wins.
4. **Give the reviewer evidence, not just a number.** Show the winning form
   pair and per-signal contributions with every queue item.
5. **Sample gold pairs from production traffic**, not just from easy cases —
   the homonym stratum is where labels earn their keep.
6. **Keep blocking keys deterministic and cheap to recompute**; they are
   rebuilt on every re-index.
7. **Make the demo packs CI-checked.** The GOOD pack must produce zero
   findings and the BAD pack must surface each planted pathology — either
   drifting is a regression.
8. **Design for un-merge from day one.** Tombstones, alias maps, and
   decision history cost little now and are unbuildable later.
9. **Scope comparisons by category.** The schema should make cross-category
   pairs unrepresentable, not merely discouraged.
10. **Document each identity decision like an ADR**: evidence, decision,
    reviewer, date — because a citation graph is a scholarly artifact.

---

## Practice Exercises

1. **Normalizer regression suite.** Take the eight variant pairs from
   section 2 and assert both directions: what must equal, and what must not
   (ة folding). Run the suite against the exercise's `normalize_ar`.
2. **Blocking recall audit.** On a 500-record sample, build a gold set of
   50 positive pairs, compute blocking recall for trigram-only vs
   trigram + length-bucket keys, and report which key family each miss
   needs.
3. **Threshold sweep.** Generate 200 labelled pairs (100 same, 100
   different). Sweep AUTO in 0.05 steps, plot precision/recall, and write
   one paragraph justifying your operating point using the asymmetry
   argument.
4. **Homonym case study.** Find two same-name scholars in the corpus with
   distinguishable eras. Verify the naive baseline merges them and the
   governed pipeline vetoes them; attach both outputs to your notes.
5. **Transliteration keys.** Add an Arabic → Buckwalter (or simple Latin)
   blocking key to the exercise and re-measure the BAD pack's blocking
   recall. What new false-candidate load does it add?
6. **Un-merge drill.** Given a MergeDecision history, implement `undo(id)`
   as a new superseding decision and prove the tombstone restores and both
   former cluster members resolve to distinct canonical ids again.

---

## Summary

1. Arabic entity resolution is hard for stacked names, script variants,
   diacritics, transliteration, digits, and homonyms — string equality is
   one signal, never the verdict.
2. Normalization is versioned, idempotent, and dual-copy: display keeps the
   observed text, the index copy unifies orthography, and ة folding stays
   fuzzy-only.
3. Blocking replaces all-pairs with key-generated candidates, and blocking
   recall is measured next to merge recall because a missed candidate is an
   invisible recall ceiling.
4. Scoring combines exact, fuzzy (n-gram Jaccard, Damerau-Levenshtein,
   Jaro-Winkler), token, alias, and context signals — with conflict vetoes
   outranking scores.
5. Thresholds come from a labelled pair set; the precision-first operating
   point reflects the asymmetry that a false merge corrupts a citation graph
   while a missed merge merely duplicates a record.
6. Canonization mints a ULID/UUIDv7 per cluster, preserves every observed
   form in the alias table, and never destructively updates.
7. Review, tombstones, and append-only MergeDecision history make every
   merge reversible and auditable.
8. Evaluate per category (authors, books, narrators) plus end-to-end
   retrieval hit rate, and roll out in blast-radius order: authors and books
   first, then isnad narrators, then terminology.
9. For the Islamic scholarly corpus, same-name scholars are never silently
   conflated, the tooling makes no religious rulings, and identity claims
   carry bibliographic sources.

**Next lecture:** Arabic NLP 09 (planned): building the citation and isnad
graph over resolved entities — turning canonical ids and alias tables into
edges, and measuring what resolution bought the graph.

## Further Reading / Connections

- `projects/04-ai-engineering/athar-lab/README.md` and `contracts.py` — the
  two-text discipline and stable `book_id` identity this pipeline extends.
- `projects/04-ai-engineering/arabic-nlp/02-arabic-normalization-tokenization/`
  — the normalization decisions (shadda, false matches) this lecture builds on.
- `projects/04-ai-engineering/arabic-nlp/07-arabic-mrr-evaluation/` — the
  golden-set methodology reused here for hit-rate measurement.
- `registries/knowledge-registry.yaml` — `arabic-nlp.*` nodes; this topic
  continues the track after `arabic-nlp.mrr-evaluation`.
- `learning-sources/source-index.md` anchors `source-index#16`
  (Hugging Face NLP course) and `source-index#28` (Chip Huyen, *AI
  Engineering*) for dataset/evaluation background.
