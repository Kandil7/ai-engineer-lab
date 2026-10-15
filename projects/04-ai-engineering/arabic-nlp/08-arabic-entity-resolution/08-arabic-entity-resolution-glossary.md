# Arabic NLP 08: Arabic Entity Resolution — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Blocking | Pre-filtering records into shared-key buckets so only plausible pairs get compared | trigram key `author\|tri\|حمد` |
| Blocking recall | Fraction of gold positive pairs that shared at least one blocking key | 0.50 = half the true pairs unreachable |
| Canonization | Assigning one permanent canonical id per resolved cluster | cluster → ULID |
| Conflict veto | Metadata contradiction that forbids auto-merge regardless of string score | death years 50 AH apart |
| Damerau-Levenshtein | Edit distance including adjacent transpositions | محمّد ↔ محمد = 1 edit |
| Digit folding | Mapping Arabic-Indic digits to ASCII in the index copy | ١٤٤٥ → 1445 |
| Display form | The verbatim observed string, kept for display and citation | محمَّد بن ... |
| Gold pair set | Labelled record pairs: same entity or not | 100 same + 100 different |
| Homonym | Identical names belonging to different people | محمد بن عبد الله (d. 150 vs d. 200) |
| Jaro-Winkler | Prefix-weighted similarity for personal names | JW(MARTHA, MARHTA) = 0.961 |
| Kunya | Teknonym: أبو/أم + firstborn's name | أبو عبد الله |
| Laqab | Epithet or title attached to a name | الواقدي |
| Merge candidate | A scored pair with a decision, emitted before any write | score 0.90, review |
| Nasab | Patronymic chain: bin / ibn links | محمد بن أحمد بن إسماعيل |
| Nisba | Origin/adjective name suffix | البغدادي |
| Review band | Score interval routed to human review, never auto-merged | 0.55 ≤ score < 0.85 |
| Ta marbuta folding | ة → ه applied only in fuzzy keys, not the index copy | مدرسة ≠ مدرسه in index |
| Tombstone | Status marking a merged-away record; never deleted | status: tombstoned |
| Two-text discipline | Every record keeps original + normalized copies | Athar `original`/`searchable` |
| ULID | Time-sortable 26-char identifier used for canonical ids | 01JB7K... |

---

## Alphabetical Glossary

### Alias

**Definition:** Any recorded surface form of an entity other than (or
including) its preferred display form. Every observed spelling is preserved;
aliases are additive, never replacements.

**Example:**
```python
# canonical author: محمد بن إسماعيل البخاري
aliases = ("الإمام البخاري", "محمَّد بن إسماعيل البخاري")
```

**Related concepts:** Alias table, Display form, Two-text discipline

---

### Alias table

**Definition:** The store mapping one canonical entity id to every observed
surface form, each stamped with the normalizer version that produced its
normalized key. It is what makes merges reversible and old ids resolvable.

**Example:**
```python
@dataclass(frozen=True)
class Alias:
    entity_id: str
    surface: str  # observed, never mutated
    normalized: str  # derived matching key
    normalizer_version: str  # "ar-er-norm-1.0"
```

**Related concepts:** Canonization, EntityId, Normalizer version

---

### Audit trail

**Definition:** Append-only history of every MergeCandidate and
MergeDecision: scores, evidence, decision, actor, timestamp. A reversal is a
new superseding row, never an edit.

**Example:**
```python
# decision: merged | rejected | deferred, with decided_by and reason
MergeDecision(
    decision="merged",
    decided_by="auto-v1",
    score=0.91,
    reason="exact after normalization",
)
```

**Related concepts:** Merge decision, Reversibility, Tombstone

---

### Auto-merge

**Definition:** System-executed merge applied when score ≥ AUTO threshold
(0.85 in the exercise) and no veto fired. Only band allowed to write
without a human.

**Example:**
```python
# كتاب الإيمان vs كتاب الايمان -> score 1.0 -> auto-merge
```

**Related concepts:** Conflict veto, Review band, Threshold study

---

### Blocking

**Definition:** Candidate generation by grouping records under shared keys
so only plausible pairs are compared. Replaces the O(n²) all-pairs cross
product.

**Example:**
```text
all-pairs: 10,000 records -> ~50,000,000 comparisons
blocking:  shared trigram/bucket keys -> a few thousand comparisons
```

**Related concepts:** Blocking key, Blocking recall, Sorted neighborhood

---

### Blocking key

**Definition:** A string under which records are co-bucketed. The exercise
emits category-scoped character trigrams plus a length-bucket key
(category + initial letter + length // 4) for every record form.

**Example:**
```python
keys = {"author|tri|حمد", "author|fl|م|5", ...}
```

**Related concepts:** Blocking, Blocking recall, Transliteration blocking

---

### Blocking recall

**Definition:** Of all gold-positive pairs, the fraction that share at least
one blocking key. A hard ceiling on end-to-end merge recall: ungenerated
pairs can never merge.

**Example:**
```text
blocking recall = 2/4 = 0.50   # BAD pack: transliteration pair unreachable
```

**Related concepts:** Blocking key, Gold pair set, Merge recall

---

### Canonization

**Definition:** Assigning each resolved cluster one permanent canonical
identifier, retiring member ids into the alias table. No member id is
rewritten or deleted.

**Example:**
```python
canonical = canonize(candidates)  # au-1 and au-2 -> one ULID
```

**Related concepts:** Alias table, ULID, No destructive updates

---

### Character n-gram Jaccard

**Definition:** Set overlap of character bigrams (or n-grams) between two
strings; robust to insertions and reordering that break edit distance.

**Example:**
```python
char_ngram_jaccard("الإيمان", "الإيمان") == 1.0
```

**Related concepts:** Damerau-Levenshtein, Match signals, Jaro-Winkler

---

### Conflict veto

**Definition:** A rule that forbids auto-merge when metadata contradicts —
years too far apart, or differing context (publisher, madhhab). Policy, not
evidence: it outranks the score.

**Example:**
```text
محمد بن عبد الله (d.150) vs محمد بن عبد الله (d.200)
score 0.90, veto=year-conflict -> review, never auto-merge
```

**Related concepts:** Homonym, Review band, Context agreement

---

### Context agreement

**Definition:** Signal measuring consistency of non-name metadata — era,
publisher, madhhab, edition. Contributes positively when consistent and
triggers the veto when contradictory.

**Example:**
```python
ctx, veto = context_signal(e1, e2)  # (0.0, "year-conflict")
```

**Related concepts:** Conflict veto, Digit/date agreement, Match signals

---

### Damerau-Levenshtein

**Definition:** Edit distance over insertions, deletions, substitutions, and
adjacent transpositions, normalized by the longer string's length.

**Example:**
```python
damerau_levenshtein("AB", "BA") == 1  # one transposition
damerau_levenshtein_sim("كتاب", "كتاب") == 1.0
```

**Related concepts:** Character n-gram Jaccard, Match signals

---

### Digit folding

**Definition:** Mapping Arabic-Indic (٠-٩) and Extended Arabic-Indic (۰-۹)
digits to ASCII inside the index copy so years, volumes, and page numbers
compare equal.

**Example:**
```python
normalize_ar("١٤٤٥") == normalize_ar("1445")  # True
```

**Related concepts:** Normalizer version, Two-text discipline, NFC

---

### Display form

**Definition:** The verbatim observed string kept on the record for display
and citation. Never normalized, never overwritten; the matching key lives in
a separate derived field.

**Example:**
```python
Entity(display="محمَّد بن إسماعيل البخاري", ...)  # tashkeel preserved
```

**Related concepts:** Two-text discipline, Alias, Tashkeel

---

### EntityId

**Definition:** The stable, opaque identifier of one canonical entity.
Non-empty, never reused, carries no semantic fields; granted at canonization
as a ULID or UUIDv7.

**Example:**
```python
@dataclass(frozen=True)
class EntityId:
    value: str  # "01JB7K3M9Q..."  (ULID)
```

**Related concepts:** Canonization, ULID, UUIDv7

---

### Gold pair set

**Definition:** Labelled record pairs (same entity / different entities)
used to tune weights, set thresholds, and compute merge precision, recall,
and F1. Split by record, not by pair, to avoid leakage.

**Example:**
```python
PairLabel(
    "h-1",
    "h-2",
    same=False,
    category="narrator",
    note="homonyms: identical names, 50 years apart",
)
```

**Related concepts:** Blocking recall, Threshold study, Merge precision

---

### Homonym

**Definition:** Two or more different people sharing a name. The corpus's
most dangerous false-merge case; handled by the conflict veto and the review
band, never by string score alone.

**Example:**
```text
محمد بن عبد الله, death 150 AH   vs   محمد بن عبد الله, death 200 AH
naive pipeline: merged (wrong)   governed: review (correct)
```

**Related concepts:** Conflict veto, Content safety, Merge precision

---

### Jaro-Winkler

**Definition:** Jaro similarity plus a prefix bonus (up to 4 shared
leading characters), tuned for personal names where the distinguishing
material sits at the end of the string.

**Example:**
```python
jaro_winkler("MARTHA", "MARHTA")  # 0.9611111 (locked by assertion)
jaro_winkler("محمد", "محمد") == 1.0
```

**Related concepts:** Match signals, Damerau-Levenshtein, Threshold study

---

### Kunya

**Definition:** Teknonym — أبو (or أم) plus the name of one's firstborn —
used as a primary name form. A record may carry kunya only, making it hard
to match against an ism-only record.

**Example:**
```text
"أبو بكر أحمد بن علي الرازي"  vs  "الحافظ الرازي"
```

**Related concepts:** Laqab, Nasab, Nisba, Stacked name forms

---

### Laqab

**Definition:** An epithet or family title attached to the name, often the
only form a brief source records.

**Example:**
```text
الواقدي, الظاهري, الغزالي
```

**Related concepts:** Kunya, Nisba, Stacked name forms

---

### Length bucket key

**Definition:** Blocking key from initial character plus length // 4,
grouping short-name variants that trigram keys would over-share across the
corpus.

**Example:**
```python
# "محمد" -> author|fl|م|1 ; first char + bucket scoping
```

**Related concepts:** Blocking key, Sorted neighborhood

---

### Match signals

**Definition:** The independent evidence features a pair's score combines:
exact-normalized, n-gram Jaccard, Damerau-Levenshtein, Jaro-Winkler,
token-set overlap, alias agreement, digit/date agreement, context
agreement.

**Example:**
```python
signals = (
    ("exact", 1.0),
    ("fuzzy", 0.977),
    ("token", 0.5),
    ("alias", 1.0),
    ("context", 1.0),
)
```

**Related concepts:** Scoring model, Conflict veto, Threshold study

---

### Merge candidate

**Definition:** The immutable scored-pair object the pipeline emits before
any write: ids, category, score, decision, veto, per-signal evidence. The
unit reviewers act on.

**Example:**
```python
MergeCandidate(
    left_id="h-1", right_id="h-2", score=0.9, decision="review", veto="year-conflict"
)
```

**Related concepts:** Merge decision, Review band, Tombstone

---

### Merge decision

**Definition:** The append-only record of a decision (merged, rejected, or
deferred) with actor, timestamp, reason, and the score at decision time.
Reversal writes a new superseding decision.

**Example:**
```python
MergeDecision(
    decision="rejected",
    decided_by="reviewer-7",
    reason="distinct scholars, different eras",
)
```

**Related concepts:** Audit trail, Reversibility, Tombstone

---

### Nasab

**Definition:** The patronymic chain (bin / ibn X bin Y) linking a person
to ancestors. Often recorded to different depths by different sources, so
two records of one man share only its head or tail.

**Example:**
```text
محمد بن إسماعيل بن إبراهيم الجعفي
```

**Related concepts:** Kunya, Laqab, Nisba, Stacked name forms

---

### Nisba

**Definition:** Origin adjective (city, tribe, or family) suffixed to the
name; frequently dropped in short references.

**Example:**
```text
البغدادي, الشافعي, الذهلي
```

**Related concepts:** Kunya, Laqab, Nasab

---

### Normalizer version

**Definition:** The version string stamping every normalized key with the
rule set that produced it. Changing rules bumps the version and re-derives
keys; generations are never mixed inside one index.

**Example:**
```python
NORMALIZER_VERSION = "ar-er-norm-1.0"
```

**Related concepts:** Alias table, Digit folding, Idempotence

---

### Review band

**Definition:** The score interval (0.55 ≤ score < 0.85) whose candidates
are queued for human adjudication. Also holds vetoed pairs scoring above
AUTO — evidence says similar, policy says ask a human.

**Example:**
```text
score 0.90 + veto -> still review; the veto outranks the score
```

**Related concepts:** Auto-merge, Conflict veto, Human-in-the-loop

---

### Sorted neighborhood

**Definition:** Classical blocking: sort records by normalized key, slide a
window of width w, compare only within-window records. Simple, but one
stray character moves a record across the entire sort.

**Example:**
```text
sorted keys: [البخاري, البخاري, الذهلي, الذهلي]
window w=2 -> compare (1,2), (2,3), (3,4) only
```

**Related concepts:** Blocking, Blocking key

---

### Stacked name forms

**Definition:** The combinatorics of kunya, ism, nasab, laqab, and nisba:
sources record arbitrary subsets, so identity must be judged across every
subset, not one canonical rendering.

**Example:**
```text
"أبو عبد الله محمد بن أحمد الواقدي البغدادي"
   kunya   ism+nasab    laqab   nisba
```

**Related concepts:** Kunya, Laqab, Nasab, Nisba, Homonym

---

### Ta marbuta folding

**Definition:** ة → ه applied only when generating fuzzy candidate keys —
never in the index copy, where it would merge genuinely distinct words.

**Example:**
```python
assert normalize_ar("مدرسة") != normalize_ar("مدرسه")  # index copy
# fold_ta_marbuta=True exists for fuzzy keys only
```

**Related concepts:** False match, Two-text discipline, Normalizer version

---

### Tashkeel (index copy)

**Definition:** Diacritics stripped from the matching key but preserved in
the display form, so محمَّد and محمد collide for matching while citation
text stays verbatim.

**Example:**
```python
assert normalize_ar("محمد") == normalize_ar("محمَّد")  # index key
# display="محمَّد بن ..." is stored untouched
```

**Related concepts:** Display form, Two-text discipline, Shadda

---

### Threshold study

**Definition:** The sweep of weights and cutoffs against a gold pair set
that justifies the shipped operating point. Ships as evidence, not as a gut
feeling; re-run whenever config changes.

**Example:**
```text
AUTO sweep 0.60 -> 0.95; plot precision/recall; pick precision-first
```

**Related concepts:** Gold pair set, Review band, Merge precision

---

### Tombstone

**Definition:** Status marking a merged-away or rejected record instead of
deleting it; points at the survivor so foreign keys and audits keep
resolving.

**Example:**
```python
# status: tombstoned, survivor: <canonical ULID>  (row still exists)
```

**Related concepts:** Audit trail, Reversibility, No destructive updates

---

### Transliteration blocking

**Definition:** Blocking keys derived from Latin transliterations (or a
transliteration of the Arabic) so Arabic and Latin records of one person
can become candidates. Without it, script-mixed pairs are unreachable.

**Example:**
```text
"ابن تيمية" vs "Ibn Taymiyyah"  -> no shared trigram -> blocking miss
fix direction: Buckwalter or Latin alias keys
```

**Related concepts:** Blocking recall, Alias, Latin/Arabic mixing

---

### Two-text discipline

**Definition:** Every record (and every Athar passage) carries both the
verbatim original and the derived normalized form. The original is for
display and citation; the normalized copy is for matching.

**Example:**
```python
# athar-lab contracts: Passage.original + Passage.searchable
```

**Related concepts:** Display form, Normalizer version, Athar

---

### ULID

**Definition:** 26-character Crockford base32 identifier: 48-bit
millisecond timestamp + 80 random bits. Lexicographically sortable and
offline-generable — the exercise's canonical-id choice.

**Example:**
```python
value = (ms << 80) | uuid4().int & ((1 << 80) - 1)  # then base32
```

**Related concepts:** Canonization, UUIDv7, EntityId

---

### UUIDv7

**Definition:** RFC 9562 time-ordered UUID: 6-bit version, 48-bit
timestamp, 74 random bits. The standards-track alternative to ULID for
canonical entity ids.

**Example:**
```text
0190c9f2-6b3a-7c1d-8e4f-...   (timestamp prefix sorts by creation)
```

**Related concepts:** Canonization, ULID, EntityId

---

## Related Concepts

- **Normalization and tokenization**: the two-text discipline and false-match
  tables this pipeline reuses (arabic-nlp 02).
- **Retrieval evaluation**: golden-set methodology reused for end-to-end
  hit-rate measurement (arabic-nlp 07).
- **Athar contracts**: `Document` stable book identity and `Passage`
  original/searchable pairs (`projects/04-ai-engineering/athar-lab/contracts.py`).
- **Knowledge graph construction**: downstream consumer that requires
  canonical ids before drawing citation edges (next lecture).

## Key Takeaways

1. Identity comes from weighted evidence plus vetoes, never from the
   display string.
2. Blocking is a measured recall filter; report its recall next to merge
   recall.
3. Normalization is dual-copy and versioned; ة folding stays fuzzy-only.
4. Canonization mints sortable offline ids and preserves every observed
   form in the alias table.
5. Merges are reversible by design: tombstones, alias maps, append-only
   decisions.
6. Homonyms are held for human review; the tooling never adjudicates
   scholarly positions, only record identity.
