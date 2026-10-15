# Arabic NLP 09: Arabic Morphology, Tokenization and Surface Variation

## Topic Overview

An Arabic whitespace word is not a word. It is a fusion: proclitics bolt onto
the front, enclitics bolt onto the back, a patterned root sits in the middle,
and the short vowels that disambiguate readings are usually unwritten. A
dialect speaker writes the same concept with different letters than the
standard variety. Every retrieval decision — segment or not, which normalizer,
which tokenizer, which variety — changes recall, token cost, and whether a
quoted passage can still be shown verbatim. Get the layer wrong and every
stage above it inherits a defect it cannot see.

This lecture teaches the word layer as an engineering pipeline: root-and-pattern
morphology, the anatomy of clitic chains, conservative segmentation that never
splits a root, tokenization measured as a cost/coverage trade-off (word vs
subword vs byte-fallback), diacritics treated as signal rather than decoration,
and a variety policy that keeps dialects from silently colliding. Every stage
has Arabic-specific failure modes that a Latin-script tutorial never mentions.

The pipeline is implemented end to end in the companion exercise
`09-arabic-morphology-tokenization.py`: a display-preserving normalizer, a
conservative clitic segmenter, a tokenizer-comparison harness, and a config
auditor whose GOOD pack must score zero findings and whose BAD pack must
surface all seven planted pathologies (MOR001-MOR007).

**Duration:** 4-5 hours
**Difficulty:** Advanced
**Prerequisites:** Arabic NLP 01 (text fundamentals), Arabic NLP 02
(normalization and the two-text discipline), Arabic NLP 03 (lexical
retrieval), basic Python dataclasses

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the root-and-pattern system and why inflection-based intuitions
   from Latin fail on Arabic.
2. **Analyze** an Arabic whitespace word into proclitics, stem, and enclitics,
   naming each fused segment.
3. **Implement** conservative clitic segmentation that keeps roots intact,
   guards lexically fused words, and round-trips losslessly.
4. **Argue** when stemming helps lexical retrieval and when it destroys
   meaning, and gate it behind evaluation instead of shipping it by default.
5. **Measure** tokenization cost: tokens per word, unknown-character rate,
   and byte-fallback rate for word, subword, and byte tokenizers over real
   Arabic text.
6. **Justify** diacritic handling per content class: Quranic text keeps every
   mark, citations keep the source form, matching keys strip tashkeel — never
   the reverse.
7. **Design** a variety policy that stamps each passage with its source
   variety and routes dialect queries through documented expansions.
8. **Audit** an ingestion pipeline against the MOR001-MOR007 catalog and
   say what each finding costs downstream.
9. **Specify** the TextSample, StoredText, Finding, and PipelineConfig domain
   model with stated invariants and a reconstructability guarantee.
10. **Apply** the Islamic-content safety rules: the tooling flags morphological
    ambiguity, never adjudicates a reading.

---

## Key Concepts

### 1. Root-and-Pattern: The Shape of the Lexicon

Arabic words are built from two slots: a consonantal **root** (usually three
consonants carrying a semantic field) and a **pattern** (a vowel/template
skeleton that assigns grammatical meaning). The root ك-ت-ب is "writing-related";
drop it into different patterns and the family emerges:

| Pattern | Word | Role |
|---|---|---|
| فَعَلَ (faʿala) | كَتَبَ | he wrote (verb, past) |
| فَاعِل (fāʿil) | كاتِب | writer (active participle) |
| مَفْعول (mafʿūl) | مَكْتوب | written (passive participle) |
| فِعَال (fiʿāl) | كِتاب | book (noun of instance) |
| فُعُل (fuʿul) | كُتُب | books (broken plural) |
| مَفْعَل (mafʿal) | مَكْتَبَة | library / bookstore |

The same root ك-ت-ب yields a verb, a profession, a product, a physical object,
and a place. Latin morphology mostly *inflects* words (case, tense, number)
without changing the lexeme; Arabic *derives* new lexemes by re-patterning a
root. This is why naive stemming is uniquely dangerous on Arabic: a stemmer
that strips affixes to reach a surface stem does not reach the root, and a
stemmer that reaches the root collapses a writer, a book, and a library into
one key.

**Where morphology is useful and where it is not.** Lexical retrieval over a
classical corpus benefits from connecting كتبَ / كُتُب / كتاب under one
root-based expansion *when the query is about the writing field in general*.
It hurts when the user asked for the plural pattern (a listing of editions)
or the participle (a list of authors). The safe engineering stance, borrowed
from the information-retrieval literature on Arabic stemming (see
`learning-sources/source-index.md` anchor `#16` for the evaluation
methodology), is: morphology generates *expansion candidates* that retrieval
scores; it never rewrites the stored text. The stored text is evidence.

**Light morphology vs full analysis.** A light stemmer strips known prefixes
and suffixes (و، ال، ب، ك، ل، ف، ها، هم، ...) and stops. Full morphological
analysis returns a set of candidate analyses per word (root, pattern, POS,
features) — the job of analyzers like CAMeL Tools or Farasa. The exercise
implements the light end deliberately: it is auditable, deterministic, and
round-trips. Full analysis belongs behind the same two-text discipline: the
analysis is derived metadata, never a replacement for the observed string.

### 2. Anatomy of a Fused Word

The whitespace token in Arabic is a morpheme chain. A single printed word can
carry a conjunction, a preposition, the definite article, a stem, and a
pronoun suffix:

```
                    وَالكِتَابِهَا   (wa-al-kitābihā, "and with their book")
                 ┌───────────────────┐
                 │  و  ال  كتاب  ها   │   segments after conservative split
                 └───────────────────┘
                  │  │    │    │
                  │  │    │    └── enclitic: 3rd-person feminine plural suffix
                  │  │    └─────── stem: the lexical core (root ك-ت-ب)
                  │  └──────────── proclitic: definite article ( fused after ب)
                  └─────────────── proclitic: conjunction و
```

Three families of clitics matter for segmentation:

1. **Conjunction و** ("and") — the single most frequent proclitic in running
   text. وكتابها must be able to find كتابها.
2. **The definite article ال** ("the") — and its *fused* forms with
   prepositions: بِـ + ال = بال, كَـ + ال = كال, فَـ + ال = فال, and the
   elided-lam form ل + ال = لل (the alef is dropped after lam: للمسافر,
   not للمسافر with two alefs). These fusions are orthographic, not optional:
   there is no space between the preposition and the article.
3. **Pronoun suffixes** — ها، هم، هن، هما، كم، كن، نا، كما (multi-character)
   and ه، ي، ك (single-character). They fuse to the *end* of the stem, after
   any article.

Topic 02 stopped at whitespace tokens and left this chain intact. This
lecture's segmenter pulls the chain apart conservatively — because the
decision to segment is a retrieval decision, not a cosmetic one.

### 3. Conservative Segmentation: Precision Over Recall

The exercise's segmenter applies five rules in order (R1-R5), each guarded by
a length floor so that the stem survives:

| Rule | Applies when | Minimum remains | Example |
|---|---|---|---|
| R1: conjunction | word starts with و | ≥ 3 chars | وكتابها → و / كتاب / ها |
| R2: fused preposition + article | starts with بال كال فال | ≥ 3 chars rest | بالكتاب → ب / ال / كتاب |
| R2b: elided lam | starts with لل | ≥ 3 chars rest | للمسافر → ل / ال / مسافر |
| R3: plain article | starts with ال | ≥ 3 chars rest | الكتاب → ال / كتاب |
| R4: bare preposition + multi suffix | ب/ل + her/their/... | suffix is a known multi | بها → ب / ها |
| R5: one pronoun suffix | ends with a suffix | base ≥ 2 (multi) / ≥ 4 (single) | كتابها → كتاب / ها |

The length floors are the heart of the design. They encode four Arabic
lexical traps that every aggressive segmenter steps on:

- **الله** — starting with ال but the rest is only 2 chars; it must never
  become ال + ه (or worse, ال + ل + ه).
- **وجه** ("face"), **علي** ("upon" / a companion's name), **موسى** (Moses) —
  short words whose final letters *look* like pronoun suffixes. The ≥ 4-char
  single-suffix floor keeps them whole.
- **كتب** ("he wrote") — the bare-preposition rule must never fire on a 3-letter
  verb; only multi-character suffix compositions (R4) are allowed for bare
  ب/ل, never bare stripping.
- **لكن** ("but") — a lexically fused word that mimics ل + كن. A guard set
  (`_COMPOSITION_GUARD`) refuses the split.

The invariant the exercise asserts after every split: **only known clitics may
be short; every extracted stem keeps ≥ 3 characters; an unsplit short word
(مش, في, من) is a complete lexical item and passes untouched.** And the
round-trip guarantee: segments re-joined (with one orthographic rule — ل + ال
→ لل) reproduce the normalized string exactly. The exercise proves this on all
18 samples: `display fidelity: 18/18 samples round-trip`.

**What conservative segmentation is not.** It is not a root extractor. It is
not a stemmer. It does not touch pattern vowels because those are gone
(undiacritized text). Its job is to make the *clitic layer* explicit so that
downstream stages — BM25 expansion, embedding, entity matching — can decide
what to do with each morpheme, instead of guessing from a fused string.

### 4. The Stemming Gate: When Roots Help and When They Hurt

Aggressive stemming (LightICEB, ISRI, Tashkeela-style root stripping) collapses
the كتب family to the root ك-ت-ب. That collapse is exactly the false-positive
table from topic 02, one level deeper:

| Surface | Light stem | Full root | Retrieval judgment |
|---|---|---|---|
| كُتُب (books) | كتب | كتب | same field — expansion candidate |
| كِتَاب (book) | كتاب | كتب | same field — expansion candidate |
| كاتِب (writer) | كاتب | كتب | different sense — dangerous to merge |
| مَكْتَبَة (library) | مكتبة | كتب | different sense — dangerous to merge |
| كَتَبَ (he wrote) | كتب | كتب | verb form — BM25 already matches |

A query for "مؤلف الكتب" (author of the books) should *not* retrieve library
pages because مكتبة collapsed into the same key. The exercise plants this
exact failure as **MOR003**: the BAD pipeline runs `stem` before `embed` with
no evaluation gate, and the audit emits

```
[warning] MOR003 line 19: aggressive stem feeds embedding (stem line 19 <
embed line 21) with no evaluation gate; meaning the model's needs may be
destroyed (كتب/كُتُب/كِتَاب collapse)
```

The GOOD pipeline puts `stem` *after* `embed`, scoped to the lexical arm
(BM25 candidate expansion) where its recall gains can be measured against a
golden set (Arabic NLP 07's methodology), and leaves the embedding arm on
normalized-but-unstemmed text. The rule: **stemming ships behind an evaluation
gate, or it does not ship.** The gate is a boolean in `PipelineConfig`
(`eval_gate: True`); the audit checks the flag, not the model quality — the
audit can't see your metrics, only whether you declared that you measured.

### 5. Tokenization as a Retrieval Decision

Topic 02 introduced word vs subword at the concept level. This lecture
measures it. The exercise ships a three-tokenizer harness over the same
18-sample corpus (40 whitespace words after normalization):

```
=== tokenizer comparison over 18 texts (40 words) ===
  tokenizer           tokens  tok/word  unk chars  byte chars
  word-whitespace         40       1.0       0.0%        0.0%
  subword-greedy          67      1.68       8.6%        0.0%
  byte-fallback          351      8.78       0.0%       80.5%
```

Read the table as a three-way trade-off:

- **Word (whitespace)**: 1.0 tokens per word, zero unknowns — but the
  vocabulary is the corpus's own word list. Any unseen spelling is `<unk>`,
  and morphology variants never share parameters. Fine for BM25 over a
  fixed corpus; unusable as a neural model's input vocabulary.
- **Subword (greedy over a fragment vocab)**: 1.68 tokens per word is the
  realistic inflation factor for BPE/Unigram on Arabic (published AraBERT
  figures run in the same band; cite your model's tokenizer, don't guess).
  The 8.6% unknown characters here come from the exercise's *hand-built*
  fragment vocab — a trained BPE covers its training distribution instead.
  The point transfers: **your subword vocabulary is part of your model's
  contract; never swap tokenizers under a saved model.**
- **Byte-fallback**: 8.78 tokens per word and 80.5% of characters paid as
  raw UTF-8 bytes. This is the honest simulation of a model with no Arabic
  coverage (an English BPE given Arabic): every Arabic letter costs 2 byte
  tokens, sequences blow up, attention spreads over padding, and generation
  must stitch letters back into codepoints. If your model card doesn't list
  Arabic in its supported scripts, this table is your forecast.

The pipeline consequence is **MOR006**: running the model's subword tokenizer
and then a clitic segmenter over the *token ids* is double segmentation. The
segmenter was written for characters; feeding it token ids makes it "split"
the model's own vocabulary units. The BAD pack plants the reversed order
(`subword_tokenize` at line 15, `segment` consuming `subword_tokens` at line
17) and the audit reports

```
[error] MOR006 line 17: clitic segmenter consumes subword tokens from an
earlier stage; segmenting token ids is double segmentation and splits the
model's own vocabulary units
```

The GOOD pack orders the stages so the segmenter reads *normalized text* and
the model's tokenizer runs on its own input, each once.

### 6. Diacritics Are Signal, Not Decoration

Tashkeel (فَتْحَة، ضَمَّة، كَسْرَة، سُكُون، شَدَّة، تَنْوِين) disappears in
most modern printing — and its absence is itself information. The engineering
stance has three parts:

**1. Strip tashkeel from the working copy, never from the stored original.**
This is the two-text discipline from topic 02, re-stated at the morphological
level because diacritics here carry *morphological* content: shadda (شَدَّة)
marks gemination, which separates مضارع from ماضي in some verbs and doubles
roots; tanween marks indefinite case. Stripping them from a stored Quranic or
citation string is unrecoverable. The exercise's normalizer strips combining
marks (Unicode category `Mn`) from the derived copy only; the audit rule
**MOR002** fires when `tashkeel_target="stored"` and the pipeline stores
quranic or citation content:

```
[error] MOR002 line 13: tashkeel stripped from stored citation, quranic
content (sample: quranic); the original reading cannot be reconstructed
from the index
```

**2. Quranic text keeps every mark in display.** The exercise's probe string
`بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ` normalizes to
`بسم الله الرحمن الرحيم` for matching while the original stays byte-identical.
Note the wasla (ٱ) and superscript alef (ٰ): both are handled (wasla folds to
alef in the working copy; superscript alef is `Mn` and strips). The display
copy is the evidence; the working copy is an index artifact.

**3. Partial diacritization is a matching problem, not a data-quality
problem.** A corpus where 5% of tokens carry tashkeel will have two byte
sequences for the same name (محمَّد vs محمد). Topic 02 solved this with
normalization. This lecture adds the retrieval angle: for BM25, strip tashkeel
in the *index keys*; for citation display, show what the source wrote; for
Quranic search, keep a *diacritized key column* as well, because a search for
بِسْمِ should rank the basmala higher than undiacritized prose that happens
to contain the letters. The choice is content-class dependent, and the
`PipelineConfig.stored_content` tuple declares which classes the pipeline
holds — the audit can then reason about what stripping costs.

### 7. Surface Variation Across Time and Space

Arabic is a dialect continuum with a standard written register (MSA) layered
on classical Arabic, plus centuries of orthographic drift. The exercise's
sample corpus spans five varieties on purpose:

| Variety | Sample | Surface cue |
|---|---|---|
| MSA | كتاب الإيمان | standard spelling, alef hamza variants |
| Classical | بسم الله الرحمن الرحيم | Quranic orthography, wasla |
| Egyptian | عايز أروح المدرسة بكرة | عايز for "want", بكرة for "tomorrow" |
| Levantine | مش رايح المدرسة اليوم | مش negator (2 chars — the segmenter's unsplit-short-word case) |
| Gulf | وين بتروحون اليوم؟ | وين for "where", plural verb form |

Three engineering consequences, each with an audit rule:

**a) Dialect spellings diverge at the character level.** Egyptian orthography
often writes أ as ى (the alef maqsura glyph in final position where MSA
writes ء or أ); Levantine drops final ta marbuta in speech-writing; Gulf
retains patterns MSA simplified. The normalizer's alef and maqsura folds
(topic 02) absorb much of this — but not all of it. **MOR007** catches the
digit half of the problem: Arabic-Indic (١٤٤٥) and Extended (۱۴۴۵) digits
left unfolded never equal their ASCII forms, so edition, page, and year
fields silently never match. The GOOD pack folds digits; the audit checks
the flag.

**b) A mixed-variety corpus without a variety policy is a tuning trap.**
If the index silently mixes MSA, classical, and five dialects, an MSA-tuned
embedding model under-serves dialect queries and a dialect-tuned expansion
map over-serves classical text. **MOR004** fires when `variety_decision` is
`None` and more than one variety is present:

```
[warning] MOR004 line 23: corpus mixes varieties (classical, egyptian, gulf,
levantine, msa) but no variety decision is recorded; MSA-heavy and dialect
queries cannot both be tuned
```

The GOOD pack stamps every passage with its source variety at ingest and
records an explicit policy: queries default to msa+classical; dialect queries
route through a documented expansion map; sources never mix silently. The
policy string lives in the config (`ar-morph-variety-1.0` in the exercise)
and is versioned like the normalizer.

**c) The normalizer itself is generation-stamped.** Changing a folding rule
produces keys that are not comparable with the old ones. **MOR005** fires
when the index stores keys with no normalizer version recorded. The version
string (`NORMALIZER_VERSION = "ar-morph-norm-1.0"`) rides with every stored
text; re-derivation is a versioned migration, never an in-place edit.

### 8. The Pipeline Audit: MOR001-MOR007

The exercise's auditor inspects a declarative `PipelineConfig` — steps with
explicit `input_source`, plus flags for original-keeping, tashkeel target,
evaluation gate, variety policy, normalizer version, and digit folding. The
full catalog:

| Code | Severity | Fires when | Downstream cost |
|---|---|---|---|
| MOR001 | error | normalizer overwrites the stored original | display form destroyed; citations can't show source verbatim |
| MOR002 | error | tashkeel stripped from stored quranic/citation | original reading unrecoverable |
| MOR003 | warning | stem feeds embed with no eval gate | meaning collapsed before the model sees it |
| MOR004 | warning | mixed varieties, no variety decision | one tuning knob can't serve all |
| MOR005 | warning | index keys carry no normalizer version | rule change silently mixes key generations |
| MOR006 | error | segmenter consumes subword token ids | double segmentation corrupts model vocabulary |
| MOR007 | warning | digits not folded | ١٤٤٥ never equals 1445 |

Severity policy: **errors** are data destruction or double-processing (the
stored evidence is gone, or a stage ran twice on the wrong input); **warnings**
are silent quality loss or governance gaps (the pipeline runs, but something
downstream will be measurably worse). The audit's contract with CI: the BAD
pack must surface every code (exactly one finding per rule — the exercise
asserts `len(bad_findings) == len(RULE_CATALOG)`), and the GOOD pack must
produce zero findings. Either drifting is a regression.

The BAD pack's seven findings, as the exercise prints them:

```
=== BAD pack: pipeline audit ===
  [error] MOR001 line 13: normalizer overwrites the stored original...
  [error] MOR002 line 13: tashkeel stripped from stored citation, quranic...
  [warning] MOR003 line 19: aggressive stem feeds embedding...
  [warning] MOR004 line 23: corpus mixes varieties...but no variety decision...
  [warning] MOR005 line 23: index stores keys without normalizer version...
  [error] MOR006 line 17: clitic segmenter consumes subword tokens...
  [warning] MOR007 line 13: digits not folded...
  findings: 7 (errors: 3, warnings: 4)

=== GOOD pack: pipeline audit ===
  findings: 0 (errors: 0, warnings: 0)
GOOD pack clean
```

The GOOD pack is not a fantasy pipeline: it uses the same corpus and the same
stages, ordered so that embed reads normalized text, subword tokenization
runs on its own input, the segmenter and the (gated) stem serve the lexical
arm only, and the index records the normalizer version. What separates GOOD
from BAD is declared order and declared policy — which is exactly what an
auditor can check without loading a model.

**Stage order, side by side.** The two packs declare the same six stages;
the arrows show what each stage *consumes* (the `input_source` the audit
reads). Left: every arrow the audit condemns. Right: the order it accepts.

```
BAD pack                                   GOOD pack

 load ──► text                            load ──► text
              │                                    │
              ▼                                    ▼
        normalize ──► normalized            normalize ──► normalized
              │                                    │
              │ (original destroyed: MOR001)       ├──► embed ──► vectors
              ▼                                    │
        subword_tokenize ──► token ids             ├──► subword_tokenize
              │                                    │         (own input, once)
              ▼                                    │
        segment ◄── consumes token ids             ├──► segment ◄── normalized text
              │         (MOR006)                   │
              ▼                                    ▼
        stem ──► stems ──► embed            stem ──► stems   (lexical arm,
              │         (MOR003: no gate)             after embed, gated)
              ▼                                    │
        index ◄── keys, no version           index ◄── keys + normalizer version
                 (MOR005)                            + variety stamp + folded digits
```

The left column's damage is cumulative: the original is gone before any
downstream stage could preserve it, the segmenter has been handed vocabulary
ids instead of text, and the stemmer's collapse feeds the embedding with no
measurement in between. The right column's cost is one extra column of
storage (the original) and one boolean (`eval_gate`) that CI can check.

### 9. Domain Model

Four types carry the layer, with invariants the exercise's self-checks
enforce:

```python
@dataclass(frozen=True)
class TextSample:
    sample_id: str
    raw: str  # verbatim display form; never mutated
    kind: str  # "lexical" | "citation" | "quranic" | "query"
    variety: str  # "msa" | "classical" | "egyptian" | "levantine" | "gulf"
    note: str = ""


@dataclass(frozen=True)
class StoredText:
    original: str  # byte-identical to TextSample.raw
    normalized: str  # derived; re-normalizing original reproduces it
    words: tuple[str, ...]  # whitespace split of normalized
    segments: tuple[tuple[str, ...], ...]  # per-word clitic segments
    normalizer_version: str  # which rules produced normalized
    variety: str  # stamped at ingest


@dataclass(frozen=True)
class Finding:
    severity: str  # "error" | "warning"
    code: str  # "MOR001".."MOR007"
    line: int  # 1-based line in the pipeline config listing
    message: str


@dataclass(frozen=True)
class PipelineConfig:
    name: str
    steps: tuple[PipelineStep, ...]  # each with input_source declared
    keep_original: bool
    tashkeel_target: str  # "working-copy" | "stored"
    stored_content: tuple[str, ...]
    eval_gate: bool
    dialect_sources: tuple[str, ...]
    variety_decision: str | None
    record_normalizer_version: bool
    fold_digits: bool
```

The invariants, stated as assertions in the exercise:

- `original` is byte-identical to the observed input (MOR001 holds by
  construction: `store_text` copies the raw string first and never touches it).
- Re-normalizing `original` reproduces `normalized` (idempotence, topic 02).
- `reconstruct(segments) == normalized` for every stored text — segmentation
  is lossless, or it is a bug.
- Every extracted stem (in a split) keeps ≥ 3 characters; unsplit short words
  pass untouched.
- `NORMALIZER_VERSION` rides with every StoredText; changing a rule bumps it.

The identity invariant of topic 08 (canonical id stable for life, surfaces
mutable) meets this layer here: a surface form is a `TextSample.raw`; its
matching key is a versioned `StoredText.normalized`; the two are never the
same column.

### 10. Islamic-Content Safety

This layer sits directly under Quranic and hadith display, so the rules are
hard constraints:

- **Quranic orthography is evidence.** The exercise keeps the basmala probe
  byte-identical in `original` while normalizing a working copy. A pipeline
  that stores the stripped form loses the reading.
- **Morphological ambiguity is flagged, not adjudicated.** Classical readings
  turn on diacritics and particle segmentation (e.g., الملك / مَلِك variant
  readings in al-Fatiha). The tooling may *surface* that two segmentations
  exist; it never rules on which reading is correct. Rulings belong to
  qualified human scholarship, not to a tokenization library.
- **Citation fidelity is non-negotiable.** A stored passage must be showable
  verbatim. Every audit error (MOR001, MOR002, MOR006) exists because its
  violation destroys verbatim display or corrupts the model's input.
- **No linguistic claims in the pipeline.** The segmenter's conservative
  guards (الله, وجه, علي, موسى) are orthographic safety rails, not statements
  about the words' meanings or about any school's position.

---

## Common Mistakes to Avoid

❌ Overwriting the display copy with the normalized form "to save a column."
✅ Two columns, always: `original` is evidence; `normalized` is derived.
Athar's `Passage.original` / `Passage.searchable` enforce the same split
(`projects/04-ai-engineering/athar-lab/contracts.py`).

❌ Letting the segmenter split الله into ال + ل + ه because "it starts with
ال".
✅ Length floors: ≥ 3 characters must remain after any article strip.
الله stays whole; the exercise asserts it.

❌ Bare-stripping a preposition: كتاب → ك + تاب.
✅ Never split a root. Only multi-suffix compositions (R4) may touch bare
ب/ل, and short-base suffix splits are refused (عليه, كتبه stay whole).

❌ Shipping an aggressive stemmer into the embedding pipeline because "stemming
improves recall".
✅ Gate it: `stem` serves the lexical arm, after `embed`, behind
`eval_gate=True`. The audit (MOR003) checks the declared order, not the
model's soul.

❌ Swapping a model's tokenizer for "a better" one under a saved checkpoint.
✅ The tokenizer is part of the model's contract. Re-train or re-fine-tune;
never swap. The byte-fallback column is what a mismatched script pays.

❌ Stripping tashkeel from stored Quranic or citation text because "users
search undiacritized".
✅ Search undiacritized *keys*; display the source. MOR002 exists to catch
the stored-strip mistake.

❌ Leaving Arabic-Indic digits as-is because "the model handles them".
✅ Fold ١٤٤٥ → 1445 in working copies (MOR007); edition, page, and year
fields must compare across digit systems.

❌ Silently mixing MSA, classical, and dialect passages with one untuned
configuration.
✅ Stamp variety at ingest; record a variety decision; route dialect queries
through a documented expansion map (MOR004).

❌ Changing a normalization rule and re-indexing in place.
✅ Bump `NORMALIZER_VERSION`; re-derive as a migration; never mix key
generations in one index (MOR005).

❌ Running the segmenter over the model's subword token ids because "the
stages are both called tokenization".
✅ Segment characters, then tokenize. Each stage reads its declared input
once (MOR006 checks `input_source`, not stage names).

❌ Hoping the segmenter round-trips because "it looked right in the demo".
✅ Assert `reconstruct(segments) == normalized` over every sample. The
exercise runs it on 18/18 samples; yours must too.

---

## Best Practices

1. **Keep the original immutable and the working copy versioned.** Every
   derived string carries the normalizer version that produced it; the
   original is never rewritten (MOR001's whole catalog).
2. **Segment conservatively; expand aggressively at query time.** A
   precision-first segmenter plus query-time expansion recovers recall without
   corrupting stored evidence.
3. **Length-floor every split.** ≥ 3 characters must remain after a proclitic
   strip; ≥ 4 before a single-char enclitic on a short base. The floors are
   where the Arabic-specific traps live (الله, وجه, علي, موسى).
4. **Assert losslessness.** `reconstruct(segments) == normalized` is a
   one-line test that catches every silent segmentation bug.
5. **Measure tokenization before choosing it.** tokens/word, unk-rate,
   byte-fallback-rate — three numbers, one table, the trade-off made visible.
6. **Treat the tokenizer as model contract.** Version it with the checkpoint;
   a mismatch is a deployment incident, not a refactor.
7. **Strip tashkeel by content class, not globally.** Quranic display: keep
   all marks. Matching keys: strip. Citation display: source form. Declare
   the policy; let the audit check the declaration (MOR002).
8. **Stamp variety at ingest and version the variety policy** like the
   normalizer (MOR004, MOR005). Silent mixing is how MSA-tuned systems
   fail dialect users.
9. **Put the segmenter and stemmer on the lexical arm, after embedding.**
   Embeddings want normalized-but-unstemmed text; BM25 wants expansion.
   The GOOD pack's step order is the reference.
10. **Make the audit CI-checked.** BAD pack must surface every rule; GOOD
    pack must stay at zero findings. Drift in either direction is a
    regression, caught before a human notices missing recall.

---

## Practice Exercises

1. **Segmenter guard suite.** Add three words to `check_segmenter`: a Gulf
   clitic chain, an Egyptian negative, and a classical citation with wasla.
   Assert each round-trips through `reconstruct` and that no root is split.
2. **Tokenizer sweep on a real corpus.** Feed 500 Athar passages through the
   exercise's tokenizer harness. Report tokens/word and unk-rate for the
   whitespace, subword, and byte tokenizers. Which model family does each
   column predict?
3. **MOR003 gate study.** Take a 200-query golden set (Arabic NLP 07's
   format). Measure hit@5 with (a) no stemming, (b) ungated LightICEB before
   embedding, (c) gated expansion after BM25. Write one paragraph choosing
   the operating point.
4. **Variety expansion map.** Document five dialect→MSA query expansions
   (Egyptian عايز→يريد, Levantine مش→لا/ليس, Gulf وين→أين, ...). Plug them
   into the GOOD pipeline's `variety_decision` string and re-run the audit.
5. **Diacritic-aware Quranic keys.** Extend `StoredText` with an optional
   diacritized key column for `kind=="quranic"` samples. Prove the basmala
   probe matches an exact-diacritic query higher than undiacritized prose.
6. **MOR008 design.** Invent an eighth audit rule for a failure this catalog
   misses (e.g., "subword vocab not versioned with checkpoint"). State its
   severity, its trigger condition, and the BAD-pack step list that plants it.

---

## Summary

1. Arabic words are root-and-pattern derivations wrapped in clitic chains;
   Latin inflection intuitions fail at both ends.
2. The whitespace word fuses conjunctions, articles, prepositions, stems,
   and pronoun suffixes — segmentation is a retrieval decision, not cosmetics.
3. Conservative segmentation keeps roots intact with length floors and guard
   sets; it round-trips losslessly and never strips a bare preposition.
4. Aggressive stemming collapses writer/book/library into one key; ship it
   only behind an evaluation gate and only on the lexical arm.
5. Tokenization is a measurable trade-off: word (1.0 tok/word, no
   generalization), subword (~1.7, the model's contract), byte-fallback
   (8.8, the no-Arabic-coverage tax).
6. Diacritics are signal: strip them from working copies, keep them in stored
   Quranic and citation text, and let the audit catch the stored-strip
   mistake (MOR002).
7. Mixed-variety corpora need a stamped variety policy and a versioned
   normalizer; silent mixing and unversioned keys are MOR004/MOR005.
8. The MOR001-MOR007 audit checks declared order and declared policy without
   loading a model; CI keeps BAD at seven findings and GOOD at zero.
9. The domain model (TextSample, StoredText, Finding, PipelineConfig) makes
   immutability, idempotence, and reconstructability testable invariants.
10. For Islamic content, orthographic safety rails protect evidence; the
    tooling flags ambiguity and never adjudicates a reading.

**Next lecture:** Arabic NLP 10: Arabic NER and entity linking — the
name-level half of the surface-variation problem, building on this lecture's
variety policy and topic 08's resolution machinery.

## Further Reading / Connections

- `projects/04-ai-engineering/athar-lab/contracts.py` and `README.md` —
  the two-text discipline (`Passage.original` / `Passage.searchable`) this
  layer implements for word-level text.
- `projects/04-ai-engineering/athar-lab/src/ingestion/extract/camel_tools.py`
  — full morphological analysis (CAMeL Tools) as the production counterpart
  to this lecture's conservative segmenter.
- `projects/04-ai-engineering/arabic-nlp/02-arabic-normalization-tokenization/`
  — the normalization decisions (shadda, false matches, digit folding) this
  lecture builds on and measures.
- `projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/` —
  where the surface forms resolved in this lecture feed the identity pipeline.
- `registries/knowledge-registry.yaml` — `arabic-nlp.*` nodes; this topic
  continues the track after `arabic-nlp.entity-resolution`.
- `learning-sources/source-index.md` anchors `source-index#16` (Hugging Face
  NLP course) and `source-index#28` (Chip Huyen, *AI Engineering*) for
  evaluation and tokenization background.
