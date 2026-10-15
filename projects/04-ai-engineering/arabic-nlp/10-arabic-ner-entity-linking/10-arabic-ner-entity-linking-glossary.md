# Arabic NLP 10: Arabic NER and Entity Linking — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Abstention | Refusing to link a mention when no candidate clears the review floor | ابن الجوزي → no ID |
| Ambiguity guard | Context-cue requirement on gazetteer entries that double as common words | مالك needs the cue عن |
| Auto band | Score ≥ auto_threshold; the linker links to the canon without review | الشافعي → person:shafii |
| Blocking | Cheap candidate narrowing before scored linking | same type + shared trigram |
| Canon ID | The external, stable entity identifier the linker looks up, never mints | person:shafii, quran:2:255 |
| Clitic repair | Stripping proclitics/enclitics so a fused token matches a gazetteer form | لابن تيمية → ابن تيمية |
| Common-word false positive | A gazetteer hit on a string that is an ordinary word in context | مالك in مالك الأمر |
| Context cue | A preceding token that licenses an ambiguous entry to match | عن before مالik |
| Detection | Locating character spans that carry entity identity | Span(start, end, type) |
| Entity linking | Resolving a detected span to a knowledge-base entity ID | mention → person:shafii |
| Entity-level F1 | Exact span+type match metric; the honest NER score | GOOD pack: 0.970 |
| Gazetteer | List of normalized surface forms mapped to canonical IDs | forms → entity_id |
| Jaccard (trigram) | Character-trigram set similarity used in fuzzy link scoring | 0.5 * jaccard + 0.5 * JW |
| Jaro-Winkler | Prefix-boosted string similarity; a link-score component | shared ابن heads |
| Labelled pair study | Human-judged sample of pairs a threshold would auto-link | justifies the 0.85 number |
| Longest-window match | Greedy left-to-right scan taking the longest gazetteer hit first | أبو عبد الله محمد بن مسلم |
| Minted ID | A locally invented identifier that cannot join the canon (NER004) | mint:person:shafii |
| Nasab | Patronymic construction; pattern rule detects unseen ابن X names | ابن الجوزي (regex) |
| Normalization map | Per-character working-copy → raw-offset map for span reconstruction | offsets[i] = raw index |
| Off-by-one span | A span correct except at one boundary; fails entity exact match | precision 0 at entity level |
| Pair study precision | The auto-link precision a labelled study actually delivers | evidence for NER002 |
| Quran reference parsing | Parsing a citation into a validated (surah, ayah) pair | 2:255 → (2, 255) |
| Reference-parse mode | Validated Quran parsing that rejects out-of-range ayahs | 2:999 rejected |
| Review band | Score between floor and threshold; linked but flagged for a human | outer span at 0.57 |
| Review floor | Minimum score to emit any link decision; below it, abstain | 0.55 |
| Sequence labeling | BIO/BILOU tagging over subwords; needs an offset map back to raw | AraBERT tagger head |
| Span (half-open) | Character interval [start, end) into the raw text | (10, 18, "Person") |
| Surah table | name → (number, ayah count) used to validate Quran references | البقرة → (2, 286) |
| Title extension | Emitting a nested outer span when a match follows a title token | الشافعي → الإمام الشافعي |
| Token-level F1 | Subtoken average metric that hides span errors (NER003) | BAD pack: 0.985 |
| Two-text discipline | Raw original kept verbatim; working copy derived, never the reverse | Athar Passage.original |
| Working copy | Normalized text detection runs on, offset-mapped to raw | ar-ner-norm-1.0 |
| NER001 | Model claim with no measured gazetteer baseline | warning |
| NER002 | Auto-link threshold with no labelled pair study | warning |
| NER003 | Evaluation at token level only | warning |
| NER004 | Linker mints local IDs instead of the canon | error |
| NER005 | Quran reference parsed as free text, no validation | error |
| NER006 | Clitic-attached entities unsegmented | warning |
| NER007 | Ambiguity guard disabled; common words match | warning |
| NER008 | Abstention disabled; every span force-linked | error |

---

## Alphabetical Glossary

### Abstention

**Definition:** The linker's decision to emit no entity ID when no blocked
candidate clears the review floor. Abstention is the correctness-preserving
default: an unlinked mention is a gap a human can fill; a wrong ID is a
defect that propagates into every citation and merge that trusts it.

**Example:**
```python
# GOOD pack: ابن الجوزي scores 0.49, below the 0.55 floor
decision = link_mention(unseen_nasab, gaz, GOOD_PIPELINE)
assert decision.band == "abstain" and decision.entity_id is None
# BAD pack (allow_abstain=False): the same mention is force-linked
```

**Related concepts:** Review floor, NER008, Minted ID

---

### Ambiguity guard

**Definition:** A requirement that an ambiguous gazetteer entry — one whose
single-token form doubles as an ordinary word — match only when the
preceding token is one of its context cues. The guard exists because
Arabic has no capitalization to separate مالك-the-narrator from
مالك-the-word-for-owner.

**Example:**
```python
GazetteerEntry(
    "person:malik",
    "Person",
    _raw_forms("مالك"),
    ambiguous=True,
    common_cues=("", "عن"),  # isnad preposition licenses it
)
# d7 "مالك الأمر": prev token الكتاب is not a cue -> no span (guard holds)
# guard off (NER007): the span leaks in as a common-word false positive
```

**Related concepts:** Context cue, NER007, Common-word false positive

---

### Blocking

**Definition:** The cheap, recall-oriented narrowing of candidate entities
before scored linking. The exercise keeps same-type candidates that share
at least one character trigram with any gazetteer form of the mention.
Blocking never decides; it only shrinks the set the scorer sees.

**Example:**
```python
def block_candidates(mention, gaz):
    m_tri = trigrams(mention.norm)
    # same etype + at least one shared trigram with any form
    ...


# ابن الجوزي blocks against ابن تيمية (shared ابн trigrams) but scores 0.49
```

**Related concepts:** Jaccard (trigram), Candidate, Link scoring

---

### Canon ID

**Definition:** The external, stable identifier for an entity in the
knowledge base — the output of topic 08's resolution layer. The linker's
only legitimate ID source is a canon lookup; minting a local identifier
breaks the join into resolution output, the alias table, and downstream
citation (NER004, error severity).

**Example:**
```python
# GOOD: id_source="canon" -> the winning entry's ID is looked up
assert link_mention(shafii, gaz, GOOD_PIPELINE).entity_id == "person:shafii"
# BAD: id_source="mint" -> "mint:person:shafii" cannot join the canon
```

**Related concepts:** NER004, Entity linking, Minted ID

---

### Clitic repair

**Definition:** Stripping known proclitics from a window's first token and
enclitics from its last, then requiring the remainder to match a gazetteer
form exactly. The span is placed on the entity core, not the fused token.
The gazetteer itself is the over-stripping guard: a stripped remainder
that matches nothing emits nothing.

**Example:**
```python
# d10: كتاب الإيمان لابن تيمية
# repair on: strip ل from لابن -> "ابن تيمية" hits the gazetteer, span on the core
# repair off (NER006): the whole-token window never matches; the span is lost
```

**Related concepts:** NER006, Longest-window match, Proclitic

---

### Common-word false positive

**Definition:** A detection emitted because a gazetteer surface is also an
ordinary word in the observed context. The canonical Arabic example is
مالك: the narrator's name and the word for "owner" are orthographically
identical. The ambiguity guard exists to prevent exactly this class.

**Example:**
```python
# d7 "وفي مقدمة الكتاب: مالك الأمر إلى الله."
# gold: no entity. guard off: مالك matches person:malik -> 1 false positive
# the audit's NER007 message cites this count
```

**Related concepts:** Ambiguity guard, NER007, Context cue

---

### Context cue

**Definition:** A token that, by its presence immediately before an
ambiguous mention, licenses that mention to match. In isnad chains the
preposition عن ("on the authority of") is the strongest cue for a
narrator name; titles (الإمام، الشيخ) cue scholar phrases.

**Example:**
```python
# عن مالك     -> cue present, مالك matches the narrator
# مالك الأمر  -> prev token is not a cue, guard blocks the match
```

**Related concepts:** Ambiguity guard, Context cue, NER007

---

### Detection

**Definition:** Locating the character spans in a text that carry entity
identity, each labeled with an entity type. The exercise emits
`Span(start, end, etype)` over the raw (verbatim) text, reconstructed
through the working copy's normalization map. Detection never assigns an
ID; that is linking's job.

**Example:**
```python
mentions = detect("قال الإمام الشافعي في كتبه.", GOOD_PIPELINE)
# two spans: inner الشافعي and outer الإمام الشافعي, both Person, raw offsets
```

**Related concepts:** Span (half-open), Entity linking, Normalization map

---

### Entity-level F1

**Definition:** The harmonic mean of precision and recall over exact
`(start, end, type)` span matches. A prediction is a true positive only
if its triple exactly equals a gold triple. This is the honest NER metric;
token-level F1 is reported beside it purely to expose the gap (NER003).

**Example:**
```text
GOOD pack held-out: entity P/R/F1 = 1.000/0.941/0.970 (tp=16 fp=0 fn=1)
BAD pack:           entity F1 = 0.909  vs token F1 = 0.985   <- the NER003 gap
```

**Related concepts:** NER003, Token-level F1, Exact span match

---

### Gazetteer

**Definition:** A mapping from normalized surface forms to canonical
entity IDs, used as the detection baseline. The exercise's gazetteer
stores pre-normalized forms so matching never re-normalizes a known
surface, and marks ambiguous entries that require a context cue. It is
cheap, deterministic, and auditable — and blind to any name it does not
list, which is why its baseline is *measured* rather than assumed.

**Example:**
```python
entries = [
    GazetteerEntry("person:shafii", "Person", _raw_forms("الشافعي", "شافعي")),
    GazetteerEntry("book:iman", "Book", _raw_forms("كتاب الإيمان")),
]
```

**Related concepts:** Longest-window match, NER001, Ambiguity guard

---

### Jaro-Winkler

**Definition:** A prefix-boosted string similarity used as one component
of the link score. The boost favors shared heads — which is exactly where
Arabic name pairs concentrate their similarity (ابن، أبو) — so the string
score alone must never drive an auto-link. The exercise weights it at 0.5
beside trigram Jaccard, and the combined form similarity at 0.7 beside
token overlap.

**Example:**
```python
score = 0.7 * best_form_sim + 0.3 * token_overlap
# ابن الجوزي vs ابن تيمية: shared ابن prefix boosts JW, but the total
# lands at 0.49 -> below the floor, the linker abstains
```

**Related concepts:** Link scoring, Review floor, Blocking

---

### Labelled pair study

**Definition:** A human-judged sample of the mention–candidate pairs a
given auto-link threshold would accept, used to measure the precision the
threshold actually delivers. Without one, the AUTO band's precision is
unmeasured and the threshold is a round number (NER002).

**Example:**
```text
Study: sample 200 pairs with score >= 0.85, judge same-entity / not.
Delivered precision: 0.97 -> the 0.85 threshold is defensible.
Record the number; never ship the threshold bare (NER002).
```

**Related concepts:** NER002, Auto band, Review floor

---

### Longest-window match

**Definition:** The gazetteer scan strategy: at each token position, try
windows from `MAX_WINDOW` tokens down to one, take the first exact (or
clitic-repaired) hit, and advance past the covered region. Longest-first
prefers the full kunya over a shorter fragment of it, so
أبو عبد الله محمد بن مسلم wins before محمد بن مسلم can match a sub-span.

**Example:**
```python
for length in range(min(MAX_WINDOW, n - i), 0, -1):
    for variant, v_start in _window_variants(tokens, i, i + length):
        if gaz.get(variant):  # first hit wins
            ...
```

**Related concepts:** Gazetteer, Clitic repair, MAX_WINDOW

---

### Minted ID

**Definition:** A locally invented identifier of the form `mint:...` that
the linker produces instead of looking up the external canon. A minted ID
cannot be joined to topic 08's resolution output, the alias table, or any
downstream citation, so it is an error-severity finding (NER004), not a
style preference.

**Example:**
```python
# BAD pack (id_source="mint"):
assert link_mention(shafii, gaz, BAD_PIPELINE).entity_id == "mint:person:shafii"
# GOOD pack (id_source="canon"): "person:shafii", looked up, never invented
```

**Related concepts:** Canon ID, NER004, Entity linking

---

### Nasab

**Definition:** The Arabic patronymic construction ("X son of Y"). A
nasab name the gazetteer never listed is detected by a regex rule: the
token ابن followed by a non-divine token yields a Person span over the
two-token phrase. The rule detects the span; linking then decides whether
the canon knows it.

**Example:**
```python
# d8 "روى ابن الجوزي من طريق هشام بن عروة."
# ابن الجوزي is unseen: the nasab rule emits the span, the linker abstains
# (score 0.49) because the canon has no such entry
```

**Related concepts:** Detection, Abstention, Link scoring

---

### Normalization map

**Definition:** The per-character list produced alongside the working
copy, where `map[i]` is the raw-text index of working-copy character `i`.
It is what lets a span found on the normalized text be converted back to
a display-faithful slice of the verbatim original — the mechanism that
keeps the two-text discipline intact through detection.

**Example:**
```python
norm, offsets = normalize_with_map("الإمامُ الشّافعيُّ")
assert norm == "الامام الشافعي"
assert raw[offsets[0]] == "ا"  # map points back into the raw text
```

**Related concepts:** Working copy, Two-text discipline, Span reconstruction

---

### Off-by-one span

**Definition:** A detected span that is correct except at one boundary —
one character too long or too short. Token-level F1 barely notices (most
tokens still overlap); entity-level exact match scores it a total miss.
The exercise's evaluator is exact precisely so this class of error cannot
hide.

**Example:**
```text
gold:  (10, 18, "Person")   pred: (10, 19, "Person")
token F1: ~0.94 (one extra token partially covered)
entity-level: fp=1, fn=1   <- a total miss, not a near hit
```

**Related concepts:** Entity-level F1, NER003, Exact span match

---

### Quran reference parsing

**Definition:** Parsing a Quran citation into a structured `(surah,
ayah)` pair and validating it against a surah table (name → number →
ayah count). The exercise accepts three surface variants and, in
reference-parse mode, rejects an out-of-range ayah. The validated pair
resolves to a canon ID (`quran:2:255`) that is looked up, never minted.

**Example:**
```python
assert parse_quran_reference("سورة البقرة، الآية 255", validate=True) == (2, 255)
assert parse_quran_reference("2:999", validate=True) is None  # rejected
assert parse_quran_reference("2:999", validate=False) == (2, 999)  # NER005
```

**Related concepts:** NER005, Surah table, Canon ID

---

### Reference-parse mode

**Definition:** The governed Quran-parsing configuration in which every
citation is validated against the surah table. Its opposite, free-text
mode, accepts any integers and is the NER005 error: an unvalidated
reference is how impossible citations leak into an Islamic corpus.

**Example:**
```python
GOOD: quran_mode="reference-parse"  -> 2:999 rejected, canon ID looked up
BAD:  quran_mode="free-text"        -> 2:999 accepted (NER005, error)
```

**Related concepts:** NER005, Surah table, Quran reference parsing

---

### Review band

**Definition:** The middle linking band: a score between the review floor
and the auto threshold. The mention is linked to the canon ID but flagged
for human confirmation. The exercise's title-extended outer span
(الإمام الشافعي, score 0.57) lands here — useful enough to keep, uncertain
enough to check.

**Example:**
```text
AUTO    score=1.00  canon=person:shafii        'الشافعي'
REVIEW  score=0.57  canon=person:shafii        'الإمام الشافعي'  <- flagged
```

**Related concepts:** Auto band, Review floor, Abstention

---

### Review floor

**Definition:** The minimum link score at which the pipeline emits any
decision at all. Below the floor it abstains. The exercise sets it at
0.55; moving it is a product decision that requires a labelled pair study
to justify (NER002).

**Example:**
```python
REVIEW_FLOOR = 0.55
# ابن الجوزي scores 0.49 -> below the floor -> abstain (GOOD)
# lowering the floor to 0.45 would drag it into REVIEW — measure first
```

**Related concepts:** NER002, Abstention, Labelled pair study

---

### Sequence labeling

**Definition:** The neural NER formulation: a BIO/BILOU tag per subword,
produced by fine-tuning a pretrained encoder (AraBERT, CAMeL-BERT) with a
tagging head. The Arabic-specific difficulty is alignment — mapping
subword labels back to character spans across clitic fusion — which is
why the exercise's offset map is the same primitive a tagger's output
must pass through.

**Example:**
```text
working copy:  لابن تيمية        (one whitespace token)
subwords:      لـ | ابن | تيمية  (B-Person I-Person I-Person)
raw span:      [12, 22)          via the normalization map
```

**Related concepts:** Normalization map, Working copy, NER001

---

### Span (half-open)

**Definition:** A character interval `[start, end)` into the raw text,
labeled with an entity type. Half-open intervals compose without
off-by-one gaps, and the triple `(start, end, type)` is the exact-match
key the entity-level evaluator compares.

**Example:**
```python
Span(start=10, end=18, etype="Person")  # covers raw[10] .. raw[17]
span.key() == (10, 18, "Person")  # the evaluation key
```

**Related concepts:** Entity-level F1, Exact span match, Detection

---

### Surah table

**Definition:** The lookup used to validate Quran references: surah name
→ (number, ayah count). The exercise ships a small subset (الفاتحة،
البقرة، آل عمران، يوسف، الحجرات، الملك). A reference-parse pipeline
rejects any ayah beyond the table's count; a free-text pipeline does not.

**Example:**
```python
SURAHS = {"البقرة": (2, 286), "الفاتحة": (1, 7), ...}
# 2:255 valid (255 <= 286); 2:999 rejected in reference-parse mode
```

**Related concepts:** Quran reference parsing, NER005, Reference-parse mode

---

### Title extension

**Definition:** Emitting a nested outer span when a gazetteer match is
immediately preceded by a title token (الإمام، الشيخ، الحافظ، العلامة).
Both the inner mention and the outer phrase are kept as separate spans;
the outer phrase is scored against the same canon entry and typically
lands in the REVIEW band, preserving the title context a reader needs
without forcing a separate entity.

**Example:**
```text
قال الإمام الشافعي في كتبه.
inner: 'الشافعي'          -> AUTO    score=1.00
outer: 'الإمام الشافعي'   -> REVIEW  score=0.57   <- title extension
```

**Related concepts:** Nested entity, Review band, Detection

---

### Token-level F1

**Definition:** The harmonic mean over whitespace tokens fully contained
in a span. It is reported beside entity-level F1 only to expose the gap:
token averages hide over-long spans, merged entities, and dropped clitics.
The exercise computes it per document, then pools — spans from one doc
are never scored against another's gold.

**Example:**
```text
BAD pack: entity F1 = 0.909  vs  token F1 = 0.985
          ^ the gap is the NER003 exhibit; reporting only 0.985 would lie
```

**Related concepts:** NER003, Entity-level F1, Off-by-one span

---

### Two-text discipline

**Definition:** Every record keeps the verbatim original for display and
citation beside a derived working copy for matching. The detector never
rewrites the raw string; the working copy is re-derivable from it at any
time, and the normalization map is what keeps the two joined. First
taught in Athar's `Passage` contract and Arabic NLP 02; reused here so
every emitted span can be sliced from the original.

**Example:**
```python
raw = "الإمامُ الشّافعيُّ"  # kept verbatim, never mutated
norm, offsets = normalize_with_map(raw)  # derived working copy + map
# detection runs on norm; spans convert back through offsets to raw
```

**Related concepts:** Working copy, Normalization map, Athar

---

### Working copy

**Definition:** The normalized text detection runs on: tashkeel stripped,
alef variants and alef maqsura folded, Arabic-Indic digits folded to
ASCII, tatweel dropped, Latin casefolded, whitespace collapsed — every
character carrying a map back to the raw offsets. Stamped with
`NORMALIZER_VERSION` (`ar-ner-norm-1.0`) so a re-normalization under new
rules is a new, traceable run.

**Example:**
```python
norm, offsets = normalize_with_map("بِسْمِ ٱللَّهِ ٢٥٥")
assert "بسم" in norm and "255" in norm  # display keeps every mark in raw
```

**Related concepts:** Normalization map, Two-text discipline, ar-ner-norm-1.0

---

### NER001 — NER008 (audit catalog)

**Definition:** The eight planted misconfigurations the exercise's auditor
detects. Warnings mark silent quality loss or a governance gap; errors
mark identity or reference integrity broken. Each finding message cites
the run exhibit that proves it, and the GOOD pack must surface zero.

| Code | Severity | Defect | Exhibit cited |
|---|---|---|---|
| NER001 | warning | Model claim, no measured baseline | the unmeasured claim string |
| NER002 | warning | Threshold without a pair study | the bare auto_threshold |
| NER003 | warning | Token-level metric only | entity vs token F1 gap |
| NER004 | error | Minted IDs, not canon | id_source="mint" |
| NER005 | error | Free-text Quran parsing | unvalidated (surah, ayah) |
| NER006 | warning | Clitic repair off | dropped gold-span count |
| NER007 | warning | Ambiguity guard off | common-word FP count |
| NER008 | error | Abstention off | force-linked span count |

**Example:**
```text
[WARNING] NER003: metric='token' hides span errors: entity F1 0.909 vs token F1 0.985
[ERROR  ] NER008: allow_abstain=False force-linked 1 span(s) below the review floor
```

**Related concepts:** Audit, Finding, GOOD pack / BAD pack
