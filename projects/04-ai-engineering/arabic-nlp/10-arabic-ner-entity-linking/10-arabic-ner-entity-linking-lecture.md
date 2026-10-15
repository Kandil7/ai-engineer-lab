# Arabic NLP 10: Arabic NER and Entity Linking

## Topic Overview

A retrieval system that cannot name what it found cannot answer a question
about it. Named-entity recognition (NER) locates the spans that carry
identity — a scholar, a book, a narrator, a Quran verse — and entity
linking resolves each span to a stable ID in a knowledge base. Arabic makes
both halves unusually hard: names fuse with proclitics, the script carries
no capitalization, a single common word can be a person or a preposition,
and the same scholar appears under a kunya, a nasab, a title, or a Latin
transliteration. Every downstream stage — retrieval ranking, citation,
provenance — inherits whatever the detector and linker got wrong, and a
span-level mistake is invisible to a token-level metric.

This lecture treats NER and linking as an engineering pipeline: a
gazetteer-and-rules baseline that must be measured before any model claim,
a clitic-aware detector whose spans always map back to the verbatim
string, a scored linker with AUTO/REVIEW/ABSTAIN bands that never invents
an ID, an entity-level evaluator that refuses to hide behind token
averages, and a config auditor whose GOOD pack scores zero findings while
the BAD pack surfaces all eight planted pathologies (NER001-NER008). The
pipeline is deliberately complementary to Arabic NLP 08: 08 owns
resolution, merging, and the canonization model (`EntityId`); this topic
owns detection and the act of linking a fresh mention *into* that canon.

The pipeline is implemented end to end in the companion exercise
`10-arabic-ner-entity-linking.py`: an offset-mapped normalizer, a
longest-window gazetteer detector with clitic repair, nasab and Quran
reference rules, a Jaro-Winkler linker banded into AUTO/REVIEW/ABSTAIN,
an entity-level evaluator, and the NER001-NER008 auditor. On the built-in
held-out set the GOOD pack reaches entity F1 0.970 (16 true positives,
0 false positives, 1 honest false negative) while the BAD pack drops to
0.909 and triggers every rule. The exercise's own demo output, with the
three linking bands visible on real Arabic text:

```
--- link decisions (GOOD pipeline) ---
  text: قال الشافعي في كتاب الأم.
    AUTO    score=1.00  canon=person:shafii        'الشافعي'
  text: قال الإمام الشافعي في كتبه.
    AUTO    score=1.00  canon=person:shafii        'الشافعي'
    REVIEW  score=0.57  canon=person:shafii        'الإمام الشافعي'
  text: روى ابن الجوزي من طريق هشام بن عروة.
    AUTO    score=1.00  canon=person:hisham-bin-urwa  'هشام بن عروة'
    ABSTAIN score=0.49  canon=-                    'ابن الجوزي'
  text: Ibn Taymiyyah rejected the appeal.
    AUTO    score=1.00  canon=person:ibn-taymiyyah 'ibn taymiyyah'
  text: ومن آيات الكرسي في سورة البقرة، الآية ٢٥٥.
    AUTO    score=1.00  canon=quran:2:255          'سورة البقرة، الاية 255'
```

Every band appears at least once: AUTO on exact matches, REVIEW on the
title-extended outer phrase, ABSTAIN on the unseen nasab. The lecture
explains each transition; the exercise makes each one testable.

**Duration:** 4-5 hours
**Difficulty:** Advanced
**Prerequisites:** Arabic NLP 01 (text fundamentals), Arabic NLP 02
(normalization and the two-text discipline), Arabic NLP 09 (clitics and
surface variation), Arabic NLP 08 (entity resolution and the canon),
basic Python dataclasses

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Separate** detection from linking, and explain why a correct span
   with a minted ID still breaks a knowledge base.
2. **Build** a gazetteer baseline with longest-window matching, and
   measure it before claiming any model improvement (NER001).
3. **Reconstruct** spans across clitic boundaries so a proclitic-attached
   name (لابن تيمية) yields the entity core, not the fused token (NER006).
4. **Guard** an ambiguity-prone gazetteer entry (مالك) behind a context
   cue, and measure the false positives the guard prevents (NER007).
5. **Score** candidate links with string similarity plus token overlap,
   and band them into AUTO, REVIEW, and ABSTAIN without force-linking
   (NER008).
6. **Evaluate** at the entity level with exact span+type matching, and
   show the gap to token-level F1 that hides span errors (NER003).
7. **Justify** every auto-link threshold with a labelled pair study
   instead of a round number (NER002).
8. **Parse** Quran references as structured (surah, ayah) pairs validated
   against a surah table, never as free text (NER005).
9. **Route** every resolved mention to an external canon ID and refuse to
   mint local identifiers (NER004).
10. **Audit** an NER-and-linking pipeline against the NER001-NER008
    catalog and state what each finding costs downstream.

---

## Key Concepts

### 1. Detection, Linking, and the Canon Boundary

NER answers *where*; entity linking answers *which*. The two stages have
different failure modes and different owners:

| Stage | Question | Output | Failure mode |
|---|---|---|---|
| Detection | Which character spans carry identity? | `Span(start, end, type)` | Missed or over-long span |
| Linking | Which knowledge-base entity is this? | `EntityId` + score + band | Wrong ID, forced link |
| Resolution (topic 08) | Are these two records the same entity? | Merge decision | Over-merge, under-merge |

The boundary with Arabic NLP 08 is deliberate. Topic 08 taught how to
compare two *known* records, score them, and merge them under a canonical
`EntityId`. This topic never re-litigates that decision: when the linker
scores a mention against the gazetteer, the winning `entity_id` is looked
up from the existing canon — the linker does not mint, derive, or invent
one. A pipeline that mints local IDs (`mint:person:shafii`) produces
output that cannot be joined to the resolution layer, the alias table, or
any downstream citation. That is the NER004 error, and it is an error
severity because it breaks identity integrity, not just ranking quality.

The division of labor, stated as a contract:

| Concern | Arabic NLP 08 (resolution) | Arabic NLP 10 (detection + linking) |
|---|---|---|
| Input | Two known entity records | Raw text with unknown spans |
| Question | Are these the same entity? | Where is an entity, and which one? |
| Output | Merge decision + `EntityId` | `Span` + scored `LinkDecision` |
| Score | Pair similarity (agreement, veto) | Link score (form sim + overlap) |
| Thresholds | AUTO 0.85 / REVIEW 0.55 (merge bands) | AUTO 0.85 / REVIEW 0.55 (link bands) |
| Failure | Over-merge, under-merge | Missed span, wrong ID, forced link |
| Owns the canon? | **Yes** — produces it | **No** — consumes it |

The shared threshold numbers (0.85 / 0.55) are not a coincidence: both
stages make the same kind of decision — confident auto, uncertain review,
refuse — and a single risk posture across the pipeline keeps the human
review queue consistent. What differs is the *direction*: 08 merges two
records into one ID; 10 resolves one mention into an existing ID.

```
    raw text ──► normalize (working copy) ──► detect spans
                                                  │
                    ┌─────────────────────────────┘
                    ▼
              gazetteer + rules ──► mention (span + surface + norm)
                                          │
                    ┌─────────────────────┘
                    ▼
              block candidates ──► score ──► band (auto/review/abstain)
                                                    │
                            ┌───────────────────────┘
                            ▼
                    canon lookup ──► EntityId (never minted)
```

The exercise keeps the two-text discipline from Athar and topics 02/09:
the raw string is never rewritten. Detection runs on a working copy whose
every character carries a map back to the raw offsets, so a matched span
converts to a display-faithful slice of the original. This matters most
for Quranic text and citations, where a normalized-only span would be
unciteable.

### 2. The Arabic Detection Challenge

A Latin NER tutorial assumes whitespace words and capitalization as a
free signal. Arabic removes both advantages and adds three new problems:

**Clitic fusion.** The whitespace token is a morpheme chain. A name can
hide behind a single proclitic:

```
              لَابْنِ تَيْمِيَةِ   (li-ibn Taymiyyah, "to/for Ibn Taymiyyah")
              ┌──────────────────┐
              │  ل  ابن  تيمية   │   segments after clitic repair
              └──────────────────┘
               │   │      │
               │   │      └── entity core (matches gazetteer form ابن تيمية)
               │   └── the nasab particle (part of the name)
               └── proclitic: preposition ل, stripped, NOT part of the span
```

The exercise's held-out document d10 contains كتاب الإيمان **لابن
تيمية** — the book-title entity is clean, but the scholar appears as the
fused token لابن. A detector that only matches whole tokens never sees
ابن تيمية. The exercise strips known proclitics from the first token of a
window and enclitics from the last, then requires the remainder to match
a gazetteer form exactly. The gazetteer *is* the over-stripping guard:
والده would strip to هده, which matches nothing, so nothing is emitted.
When clitic repair is disabled the held-out span is lost — that is the
NER006 warning, and the audit message cites the exact count of
clitic-dependent gold spans it dropped.

The prefix and suffix lists are deliberately small and closed:

| Direction | Strips (longest first) | Guard |
|---|---|---|
| Proclitic (first token) | بال كال فال لل ال و ف ب ك ل | remainder must hit gazetteer exactly |
| Enclitic (last token) | ها هم هن كم نا هما ه ي ك | same |

`MIN_REST = 2`, not 3: the nasab particle ابن is itself only two
characters, and لابن تيمية must be able to reach it. Raising the floor
to 3 would silently disable clitic repair for every ابن-name — a
regression the held-out set would catch as a new false negative.

**No capitalization.** Latin NER uses capitalization as a strong prior.
Arabic script has none, so مالك in مالك الأمر ("the owner of the matter")
and مالك in عن مالك (the narrator Malik ibn Anas) are orthographically
identical. The exercise's gazetteer marks مالك as `ambiguous` and requires
the preceding token to be one of its context cues — here the isnad
preposition عن. Document d7 places مالك after الكتاب:, the guard holds,
and no span is emitted. Disabling the guard is the NER007 warning; the
audit cites the count of common-word false positives the disabled guard
admitted.

**Surface variation and nesting.** The same scholar appears as الشافعي,
محمد بن مسلم, أبو عبد الله محمد بن مسلم, or Ibn Taymiyyah. A title
prefix produces a nested outer span: قال **الإمام الشافعي** carries both
the inner mention الشافعي and the outer phrase الإمام الشافعي. The
exercise emits both, scores the outer phrase against the same canon entry,
and lands it in the REVIEW band (0.57 in the demo) — high enough to be
useful, low enough to demand a human. Emitting only the inner span would
score detection well while losing the title context a reader needs.

### 3. The Gazetteer Baseline, Measured

The first rule of an NER project is not "use a transformer." It is: know
what a gazetteer already gets you. The exercise ships a small gazetteer
of normalized surface forms mapped to canonical IDs, matched by
longest-window, left-to-right scan. Windows run from `MAX_WINDOW` tokens
down to one; the first exact (or clitic-repaired) hit wins, and matching
advances past the covered region.

A gazetteer baseline is cheap, deterministic, auditable, and — on a
closed domain like an isnad chain — often shockingly strong. It is also
brittle: any name not in the list is invisible. The exercise makes this
honest. Document d11 contains the narrator **قتادة**, which the gazetteer
deliberately omits. The detector misses it, the gold annotation includes
it, and the GOOD pack's recall is 0.941 rather than a suspicious 1.000.
That single false negative is the price of a transparent baseline, and
the lecture keeps it rather than padding the gazetteer to make the number
look better.

The measured baseline is what makes a model claim meaningful. NER001
fires when a config asserts a model F1 (e.g., `arabert-f1-0.94`) without
having measured the gazetteer baseline it supposedly improves on. Without
that number there is no way to attribute the delta: the "improvement" may
be the gazetteer doing the work. The GOOD pack records the claim *and*
sets `baseline_measured=True`; the BAD pack claims and measures nothing.

The exercise's gazetteer is small on purpose — it is a teaching artifact,
not a production KB — but every entry is a real classical name or text:

| Canonical ID | Type | Forms (normalized) | Notes |
|---|---|---|---|
| person:shafii | Person | الشافعي، شافعي | matched at AUTO |
| person:ahmad-ibn-hanbal | Person | أحمد بن حنبل | 2-token nasab |
| person:yahya-bin-main | Person | يحيى بن معين | 2-token nasab |
| person:muhammad-bin-muslim | Person | محمد بن مسلم، أبو عبد الله محمد بن مسلم | kunya + short form |
| person:zuhayr-bin-harb | Person | زهير بن حرب | 2-token nasab |
| person:ibn-taymiyyah | Person | ابن تيمية، Ibn Taymiyyah | Arabic + Latin |
| person:hisham-bin-urwa | Person | هشام بن عروة | 2-token nasab |
| person:malik | Person | مالك | **ambiguous**; cue: عن |
| person:ans-bin-malik | Person | أنس بن مالك | 2-token nasab |
| book:iman | Book | كتاب الإيمان | 2-token title |
| madhhab:shafii | Madhhab | الشافعية | school of law |
| (canon) quran:2:255 | QuranVerse | — | resolved via surah table |

The narrator **قتادة** is deliberately absent. Document d11 contains it,
the gold annotation includes it, and the detector misses it. That single
false negative is what keeps the GOOD pack's recall at 0.941 instead of a
suspicious 1.000 — the honest cost of a measured baseline.

### 4. Sequence Labeling and the Offset Problem

A neural Arabic NER tagger typically fine-tunes a pretrained encoder
(AraBERT, CAMeL-BERT, or a multilingual baseline) with a BIO (or BILOU)
label head. The Arabic-specific problem is **alignment**: the model's
subword tokenizer splits a word into fragments, and the tagger emits one
label per subword. Reconstructing a character span from subword labels
requires a mapping from subword index back to character offset, and
Arabic's clitic fusion means a single "word" the annotator saw as one
span may be three subwords with different labels.

Two engineering rules keep this honest:

1. The model runs on the **working copy**, never the raw string. The
   offset map from §1 converts subword ranges back to raw spans.
2. The **gazetteer baseline is measured first**. A model is adopted only
   if its entity-level F1 beats the measured baseline on a held-out set,
   and the comparison is recorded. This is the NER001 discipline expressed
   as a process, not a comment.

The offset map is the mechanism that makes rule 1 safe. A worked example:

```
raw:      بِسْمِ ٱللَّهِ   (with tashkeel and wasla, for display)
          0 1 2 3 4 5 6 ...   raw indices

working:  بسم الله            (tashkeel stripped, wasla folded)
          0 1 2 3 4 5         working-copy indices
map:      [0, 1, 2, 6, 7, 8]  map[i] = raw index of working char i
                ↑     ↑
                │     └── working index 3 ('ا') maps to raw index 6 (ٱ)
                └── working index 2 ('م') maps to raw index 3 (م, before sukun)
```

A match on working-copy `[0, 6)` converts to raw `[0, 9)` — the full
diacritized phrase — so the emitted span can be sliced from the verbatim
original and cited. An off-by-one in the map produces a span that is
correct at the token level and total-miss at the entity level, which is
why the exercise's evaluator is exact and why its self-checks assert the
map round-trips.

The exercise does not ship a neural tagger — it is stdlib-only and
deterministic — but every offset, span, and evaluation primitive it
implements is exactly what a tagger's output must pass through before it
can be linked or cited.

### 5. Candidate Blocking and Link Scoring

Linking every detected mention against every gazetteer entry is wasteful
and, on a large canon, impossible. **Blocking** narrows the candidate set
cheaply: the exercise keeps candidates of the same entity type that share
at least one character trigram with any form of the mention. This is
recall-oriented; precision is the scorer's job.

The score combines two signals:

```
score = 0.7 * best_form_similarity + 0.3 * token_overlap
best_form_similarity = 1.0            if an exact normalized form match
                     = 0.5 * trigram_jaccard + 0.5 * jaro_winkler otherwise
```

Exact normalized matches score 1.0 and land in AUTO. Fuzzy matches
balance character-level similarity (Jaro-Winkler, prefix-boosted) against
word-level overlap. The prefix boost is deliberately a *component*, not
the decision: Arabic name pairs concentrate their similarity on shared
heads (ابن, أبو, al-), so a string score alone would auto-link ابن
الجوزي to ابن تيمية. A worked calculation for the unseen nasab:

```
mention:  "ابن الجوزي"        (detected by the nasab regex rule)
candidate: person:ibn-taymiyyah, form "ابن تيمية"

trigram Jaccard:  shared {ابن, ب ن, ن } / union ≈ 3/12 = 0.25
Jaro-Winkler:     shared prefix "ابن " (4 chars) boosts to ≈ 0.62
best_form_sim:    0.5 * 0.25 + 0.5 * 0.62 = 0.435
token_overlap:    {ابن, الجوزي} ∩ {ابن, تيمية} = {ابن} → 2*1/(2+2) = 0.50

score = 0.7 * 0.435 + 0.3 * 0.50 = 0.455  (demo run: 0.49)
        ─────────────────────────   ──────
        below the 0.55 review floor → ABSTAIN (GOOD pack)
```

The demo's exact output is 0.49 — the small difference from the hand
calculation comes from the precise trigram set and Jaro-Winkler
transposition count, but the conclusion is the same: the score is below
the floor, and the GOOD pack abstains. The BAD pack, with abstention
disabled, force-links it — the NER008 error.

**Three bands, never two.** AUTO (score ≥ 0.85) links to the canon ID.
REVIEW (0.55–0.85) links but flags for a human. Below the floor the
pipeline **abstains**: no ID, no guess. Disabling abstention is the
NER008 error; the audit cites how many spans were force-linked below the
floor. A system that links every span looks complete and is quietly
wrong — the wrong ID is worse than no ID, because it poisons every
citation and every merge that downstream trusts.

The band thresholds are not universal constants. The exercise uses 0.85
and 0.55 because they produce a useful demo split on the held-out set;
a production system would set them from a labelled pair study (§7). What
*is* constant is the three-band structure: a two-band system (link or
nothing) forces every uncertain mention into a wrong decision, and a
one-band system (always link) is the NER008 defect by construction.

### 6. Entity-Level Evaluation

Token-level F1 averages over BIO tags and is the default in most
toolchains. It hides the errors that matter. A detector that gets every
token right but merges two adjacent entities into one span scores
perfectly at the token level and fails at the span level; a linker that
emits an over-long span covering a title and a name inflates token recall
while breaking the citation.

The exercise evaluates **entity-level**: a prediction is a true positive
only if its `(start, end, type)` triple exactly matches a gold triple.
Token-level metrics are computed alongside, per document, so the two can
be compared. The audit's NER003 exhibit is precisely that gap — in the
BAD pack, entity F1 is 0.909 while token F1 is 0.985. A pipeline
reporting only the token number would look near-perfect while dropping a
clitic-attached span and admitting a common-word false positive.

Both levels are computed **per document and then pooled**. Scoring spans
from one document against another's gold is a silent bug the exercise
guards against by keying every span set on its document ID. The held-out
set is eleven documents, each chosen to exercise a specific failure mode:

| Doc | Text (abbreviated) | Gold spans | Exercises |
|---|---|---|---|
| d1 | وعند أحمد بن حنبل، وعن يحيى بن معين | 2 Person | multi-token nasab, clitic و |
| d2 | قال الإمام الشافعي في كتبه | 2 Person (inner + outer) | title extension, nesting |
| d3 | روى أبو عبد الله محمد بن مسلم عن زهير بن حرب | 2 Person | kunya (6-token window) |
| d4 | Among the later authors, Ibn Taymiyyah ... | 1 Person | Latin transliteration |
| d5 | ... سورة البقرة، الآية ٢٥٥ | 1 QuranVerse | Arabic-digit reference |
| d6 | وورد في 2:255 أثر قديم | 1 QuranVerse | ASCII reference |
| d7 | وفي مقدمة الكتاب: مالك الأمر | (none) | ambiguity guard holds |
| d8 | روى ابن الجوزي ... هشام بن عروة | 2 Person | nasab rule + abstain |
| d9 | ومذهب الشافعية ... | 1 Madhhab | school of law |
| d10 | كتاب الإيمان لابن تيمية | 1 Book + 1 Person | clitic repair (لابن) |
| d11 | أحمد بن حنبل، عن قتادة، عن أنس بن مالك | 3 Person | honest FN (قتادة) |

The GOOD pack's aggregate over this set: entity P/R/F1 =
1.000/0.941/0.970 (tp=16, fp=0, fn=1). The single false negative is
قتادة in d11 — the deliberate gazetteer gap from §3. The BAD pack drops
to entity F1 0.909 while token F1 reads 0.985; that gap is the NER003
exhibit.

### 7. Thresholds, Pair Studies, and the Abstention Floor

The AUTO threshold (0.85) and the REVIEW floor (0.55) look like round
numbers because they start that way. Shipping them unexamined is the
NER002 warning: an auto-link threshold without a **labelled pair study**
has unmeasured precision. A pair study samples pairs the threshold would
auto-link, has them judged same-entity / not-same by a human, and reports
the precision the threshold actually delivers. Only then is the number
defensible.

The exercise models this as a governance flag (`threshold_study`). The
GOOD pack sets it; the BAD pack does not, and the audit fires. The
deeper lesson is that the bands encode a **risk posture**: AUTO trades
reviewer time for the risk of a silent wrong link; ABSTAIN trades
completeness for correctness. Choosing where the bands sit is a product
decision, but choosing to *measure* them is an engineering obligation.

### 8. Quran References as Structured Data

A Quran citation is not free text. سورة البقرة، الآية ٢٥٥ and 2:255 and
البقرة: ٢٥٥ all denote the same verse, and a knowledge base that stores
the surface string cannot join them, cannot validate them, and cannot
detect an impossible citation. The exercise parses three surface variants
into a `(surah, ayah)` pair and validates it against a small surah table
(name → number → ayah count). In **reference-parse** mode an out-of-range
ayah (2:999) is rejected; in **free-text** mode any integers pass. That
mode is the NER005 error, because an unvalidated reference is how
impossible citations leak into an Islamic corpus — and a fabricated
citation in this domain is a correctness bug, not a ranking miss.

Validated references resolve to a canonical ID (`quran:2:255`) looked up
in the canon. The exercise's `CANON_QURAN_IDS` holds the verse the
held-out set cites; the linker refuses to mint a Quran ID and abstains
when the parsed pair is not in the canon.

### 9. The NER001-NER008 Audit Catalog

The auditor reads a declarative config and the run's statistics, and emits
one finding per violated rule. Severity separates identity/reference
integrity (error) from silent quality loss (warning):

| Code | Severity | Defect |
|---|---|---|
| NER001 | warning | Model claim with no measured gazetteer baseline |
| NER002 | warning | Auto-link threshold with no labelled pair study |
| NER003 | warning | Evaluation at token level only, not entity level |
| NER004 | error | Linker mints local IDs instead of the external canon |
| NER005 | error | Quran reference parsed as free text, no surah validation |
| NER006 | warning | Clitic-attached entities unsegmented; repair disabled |
| NER007 | warning | Gazetteer ambiguity guard disabled; common words may match |
| NER008 | error | Abstention disabled; every span is force-linked |

Each finding message cites the run exhibit that proves it: NER003 names
the entity-vs-token F1 gap, NER006 counts the clitic-dependent gold spans
it dropped, NER007 counts the guard-attributable false positives, NER008
counts the force-linked spans. A finding without evidence is a vibe; the
exercise refuses to emit one.

The BAD pack plants exactly one instance of each rule and must surface
all eight. The GOOD pack sets every field to its governed value and must
surface **zero**. That asymmetry — eight versus zero — is the exercise's
definition of a configured pipeline.

A full audit walk-through, using the exercise's actual output:

```
--- BAD pack findings (NER001-NER008) ---
  [WARNING] NER001 (line 1063): model claim 'arabert-f1-0.94' has no
            measured gazetteer baseline; an ungated model change cannot
            be attributed
  [WARNING] NER002 (line 1066): auto_threshold=0.85 ships without a
            labelled pair study; AUTO band precision is unmeasured
  [WARNING] NER003 (line 1062): metric='token' hides span errors:
            entity F1 0.909 vs token F1 0.985
  [ERROR  ] NER004 (line 1068): id_source='mint' breaks the join into
            topic 08's canon IDs
  [ERROR  ] NER005 (line 1069): quran_mode='free-text' accepts
            out-of-range ayahs (e.g., 2:999) into the knowledge base
  [WARNING] NER006 (line 1070): clitic_repair=False drops 1 gold
            span(s) that only a stripped proclitic reveals (e.g., لابن
            تيمية)
  [WARNING] NER007 (line 1071): gazetteer_guard=False admits 1
            common-word false positive(s) (e.g., مالك as 'owner')
  [ERROR  ] NER008 (line 1067): allow_abstain=False force-linked 1
            span(s) below the review floor
```

Three design choices in this output are worth naming:

1. **Line numbers are resolved from marker comments, not hard-coded.**
   Each BAD-pack field carries a `# NERxxx:` comment, and the auditor
   scans the file's own source for that marker. A finding that points at
   the wrong line is worse than no finding, and hard-coded line numbers
   drift the moment anyone edits the config.

2. **Every message cites a run exhibit, not a rule restatement.** NER003
   names the two F1 numbers; NER006 names the dropped-span count; NER007
   names the FP count; NER008 names the force-link count. A finding
   without evidence cannot be triaged — it is a vibe, not a signal.

3. **Severity separates integrity from quality.** NER004, NER005, and
   NER008 are errors because they break identity or reference integrity
   in ways downstream consumers cannot detect. NER001, NER002, NER003,
   NER006, and NER007 are warnings: silent quality loss or a governance
   gap that degrades the pipeline without corrupting its output IDs.

### 10. Islamic-Content Safety

Three rules bound what this pipeline may assert in an Islamic-knowledge
corpus, mirroring the safety section of Arabic NLP 09:

1. **Never conflate same-name scholars.** Two scholars sharing a name are
   two entities with two canon IDs. The ambiguity guard (§2) exists
   partly for this reason; when it cannot disambiguate, the pipeline
   abstains rather than guessing.
2. **Never adjudicate a reading or a ruling.** The detector flags
   spans and scores links; it never decides which scholar is correct or
   which position is sound. Grade and authenticity metadata are
   *inherited* from the source record, never invented by the linker.
3. **Never fabricate a citation.** The Quran reference parser validates
   against the surah table precisely so that an impossible verse cannot
   enter the canon. A span that parses to an out-of-range ayah is
   rejected, not softened.

These are not retrofits. They are why abstention exists, why the canon ID
is external, and why NER005 and NER008 are error-severity findings.

A concrete example of rule 1 in action. Two historical figures share the
name محمد: the Prophet and any of dozens of later scholars also named
محمد. A gazetteer that collapses them under one ID produces a knowledge
base where a hadith narration and a fiqh opinion are attributed to the
same "entity" — a conflation that is not merely a retrieval error but a
scholarly one. The exercise's gazetteer sidesteps this by never listing a
bare محمد: only compound forms (محمد بن مسلم) and contextualized surfaces
(Ibn Taymiyyah) are entries. When the detector cannot distinguish two
same-name figures, it abstains, and a human with the source's metadata
resolves it. The metadata (grade, authenticity, century) is *inherited*
from the source record — the linker never invents it, because inventing
a grade is fabricating a scholarly judgment.

Rule 3 deserves the same precision. The exercise's surah table is a
subset (الفاتحة، البقرة، آل عمران، يوسف، الحجرات، الملك), but the
*mechanism* is general: a reference that parses to an impossible
(surah, ayah) pair is rejected before it reaches the canon. In a
production Islamic corpus this gate would sit at ingestion, not at query
time — an impossible verse that has already entered the knowledge base
will be cited, ranked, and repeated before anyone notices. The exercise
models the gate at the parser level so the self-check can assert both
outcomes: `validate=True` rejects 2:999, `validate=False` accepts it,
and the GOOD/BAD config pair makes the choice auditable.

---

## Common Mistakes to Avoid

**Skipping the baseline.** Fine-tuning AraBERT before measuring what a
gazetteer already achieves wastes days and makes the model's contribution
unattributable. Measure the baseline first; adopt the model only on a
recorded entity-level delta (NER001).

**Evaluating at the token level and stopping.** Token F1 looks great
while spans are over-long, entities are merged, and clitics are dropped.
Always report entity-level exact-match F1 beside it, and show the gap
(NER003).

**Force-linking every mention.** A pipeline with no abstention band looks
complete and is quietly wrong. ابن الجوزي is not in the canon; the
correct output is no ID, not a guess at ابن تيمية (NER008).

**Minting IDs.** `mint:person:shafii` cannot be joined to topic 08's
resolution output or to any citation. The linker's only legitimate ID
source is the external canon (NER004).

**Storing the surface string as the Quran reference.** Without a parsed
(surah, ayah) pair validated against the table, you cannot join,
deduplicate, or validate citations — and an impossible ayah slips
through (NER005).

**Matching whole tokens only.** لابن تيمية never matches as a whole
token. Strip known clitics, require the remainder to hit the gazetteer
exactly, and keep the span on the entity core (NER006).

**Leaving the ambiguity guard off.** مالك matches everywhere and pollutes
the output with common-word false positives. Mark ambiguous entries,
require a context cue, and measure what the guard prevents (NER007).

**Choosing 0.85 because it looks reasonable.** An unjustified auto-link
threshold has unmeasured precision. Run a labelled pair study; record the
number the threshold actually delivers (NER002).

---

## Best Practices

1. **Measure the gazetteer baseline before any model claim.** Record the
   entity-level F1 the baseline achieves on the held-out set; a model is
   adopted only on a recorded delta (NER001).
2. **Keep the two-text discipline.** Detection runs on a working copy
   whose offsets map back to the verbatim raw string. A span that cannot
   be sliced from the original cannot be cited.
3. **Emit the entity core across clitics.** Strip known proclitics and
   enclitics, require an exact gazetteer hit on the remainder, and place
   the span on the core — never on the fused token (NER006).
4. **Guard ambiguous entries behind context cues.** Mark common-word
   names, require a cue token (e.g., the isnad preposition عن), and
   count the false positives the guard prevents (NER007).
5. **Band links into AUTO / REVIEW / ABSTAIN.** Below the review floor
   the pipeline abstains. A wrong ID is worse than no ID (NER008).
6. **Evaluate at the entity level, per document, then pool.** Report
   exact span+type F1 beside token F1 and show the gap (NER003).
7. **Justify thresholds with a labelled pair study.** Sample the pairs a
   threshold would auto-link, judge them, and record the delivered
   precision (NER002).
8. **Parse Quran references into (surah, ayah) and validate.** Reject
   out-of-range ayahs; resolve the pair to a canon ID looked up, never
   minted (NER004, NER005).
9. **Make every audit finding cite its exhibit.** NER006 names the
   dropped-span count; NER007 names the FP count; NER008 names the
   force-link count. A finding without evidence is not a finding.
10. **Refuse to adjudicate.** The pipeline flags, scores, and links; it
    never decides a scholarly question or invents a grade. Metadata is
    inherited from the source, never fabricated.

---

## Practice Exercises

1. **Extend the gazetteer.** Add the narrator قتادة (single-token,
   Person) to the exercise's gazetteer. Re-run the held-out evaluation
   and confirm recall rises from 0.941 to 1.000. Then remove one *other*
   entry and observe the new false negative. Which is the better
   production posture: a complete-but-unmeasured gazetteer or a measured
   one with known gaps?

2. **Move the REVIEW floor.** Lower `REVIEW_FLOOR` from 0.55 to 0.45 and
   re-run the demo. Does ابن الجوزي (0.49) now land in REVIEW instead of
   ABSTAIN? Write the labelled pair study you would need before shipping
   the new floor (NER002).

3. **Add a title.** Add الربيع to `TITLES` and construct a held-out
   document containing قال الربيع بن سليمان عن الشافعي. Verify the outer
   span الربيع بن سليمان ... wait — the title rule extends a *match*
   preceded by a title token; add الربيع بن سليمان as a gazetteer form
   and confirm the nested outer span appears and lands in REVIEW or
   AUTO.

4. **Break the offset map.** Deliberately return a working-copy offset
   that is off by one from `normalize_with_map`, run the held-out set,
   and observe the exact-match evaluator report a false negative on a
   span that is "almost right." Explain why an off-by-one span is worse
   at the entity level than at the token level.

5. **Design NER009.** Propose a ninth audit rule for a defect the
   catalog does not cover — for example, a gazetteer entry whose forms
   were never normalized with the stamped `NORMALIZER_VERSION`. State the
   severity, the exhibit the message must cite, and the GOOD-pack field
   that would silence it.

---

## Summary

Arabic NER and entity linking are one pipeline with two failure surfaces:
detection must find the span across clitics, missing capitalization, and
common-word ambiguity; linking must resolve that span to an external canon
ID without minting, force-linking, or guessing. The engineering discipline
is the same one every other stage of this track has taught: measure the
baseline before claiming a model improvement (NER001), justify thresholds
with data (NER002), evaluate where the errors actually live — the entity
level (NER003) — and never break identity or reference integrity (NER004,
NER005). The exercise's GOOD pack scores zero findings and entity F1
0.970; its BAD pack triggers all eight rules and drops to 0.909. That
asymmetry is the definition of a configured pipeline, and it is the gate
this topic leaves you with.

**Next lecture:** [11 - Arabic Dialect Identification](../11-arabic-dialect-identification/) (planned) — variety detection as a routing decision, building on the variety policy from Arabic NLP 09.

---

## Further Reading / Connections

- **Arabic NLP 08** — entity resolution, merging, and the `EntityId`
  canon this topic links into.
- **Arabic NLP 09** — clitics, surface variation, and the two-text
  discipline the detector reuses.
- **Athar Lab** (`projects/04-ai-engineering/athar-lab/`) — the
  Islamic-knowledge domain whose entity inventory (scholars, narrators,
  books, isnads, Quran verses) this pipeline is built to serve.
- **`learning-sources/source-index.md`** — Hugging Face NLP course
  (`#16`) for the sequence-labeling and offset-alignment methodology;
  Chip Huyen's *AI Engineering* (`#28`) for evaluation and RAG-pipeline
  framing.
