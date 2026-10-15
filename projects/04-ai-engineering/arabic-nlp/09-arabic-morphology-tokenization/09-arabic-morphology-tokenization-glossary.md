# Arabic NLP 09: Arabic Morphology, Tokenization and Surface Variation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Alef maqsura | Final ى, visually like ي but historically an alef; folds to ي in keys | موسى → موسى (key) |
| Broken plural | Plural formed by changing the root's internal pattern | كِتاب → كُتُب |
| Byte-fallback | Encoding unknown characters as raw UTF-8 byte tokens | Arabic letter → 2 byte tokens |
| Clitic | Grammatically independent word that fuses orthographically | و، ال، ها |
| Conservative segmentation | Splitting only known clitic boundaries, never roots | وكتابها → و / كتاب / ها |
| Digit folding | Mapping Arabic-Indic and Extended digits to ASCII in working copies | ١٤٤٥ → 1445 |
| Display form | The verbatim observed string, kept for citation and display | بِسْمِ ٱللَّهِ ... |
| Dialect continuum | The span from classical through MSA to regional spoken varieties | Egyptian، Levantine، Gulf |
| Enclitic | Pronoun suffix fused to the end of a stem | كتاب + ها → كتابها |
| Fused preposition | Preposition + article written as one word | بال كال فال لل |
| Gemination | Doubling of a consonant, marked by shadda | محمَّد (shadda on م) |
| Light stemming | Stripping known affixes, stopping before the root | والكتابها → كتاب |
| Morphological analyzer | System returning root, pattern, POS, features per word | CAMeL Tools، Farasa |
| Normalizer version | Stamp on every derived key naming the rules that produced it | ar-morph-norm-1.0 |
| Pattern (wazn) | Vowel/template skeleton assigned to a root | فِعَال → كتاب |
| Pipeline audit | Declarative config checker emitting MOR001-MOR007 findings | GOOD pack: 0 findings |
| Proclitic | Clitic fused to the front of a stem | و (conjunction)، ال (article) |
| Root (jadhr) | Consonantal base carrying a semantic field, usually 3 letters | ك-ت-ب (writing) |
| Round-trip guarantee | Segments re-join to reproduce the normalized string exactly | reconstruct == normalized |
| Shadda | Diacritic marking gemination (doubled consonant) | شَدَّة |
| Subword tokenization | Splitting words into vocabulary fragments (BPE/Unigram) | كتاب → كِ تاب |
| Surface variation | Same concept spelled differently across time, space, and register | محمد / محمَّد / ىحمر |
| Tashkeel | The set of short-vowel and related diacritics | فَتْحَة، ضَمَّة، كَسْرَة |
| Ta marbuta | ة; a noun-final marker that sounds like ه in construct | مدرسة |
| Tatweel | ـ, decorative elongation glyph, often a PDF artifact | كتـــاب |
| Tokenizer contract | The rule that a model's tokenizer is fixed at training time | never swap under a checkpoint |
| Two-text discipline | Every record keeps original + normalized copies | Athar original/searchable |
| Unknown-character rate | Share of characters a vocabulary cannot represent | subword harness: 8.6% |
| Variety decision | Recorded policy for how source varieties are mixed and queried | ar-morph-variety-1.0 |
| Wasla | ٱ, the "connected" alef form in Quranic orthography | ٱللَّه |
| Working copy | The derived, normalized text used for matching and embedding | re-derivable from original |

---

## Alphabetical Glossary

### Alef maqsura

**Definition:** The final letter ى, written like ي but historically derived
from an alef. It appears in classical words (موسى، على، حتى) and, in some
dialect orthographies, replaces ء or أ in final position. It folds to ي in
the working copy; the display copy keeps the observed spelling.

**Example:**
```python
normalize_working_copy("موسى") == normalize_working_copy("موسي")  # True
# display keeps: موسى (the observed form)
```

**Related concepts:** Digit folding, Working copy, Surface variation

---

### Broken plural

**Definition:** A plural formed by changing the *internal* pattern of the
root rather than adding a suffix. Broken plurals are lexically idiosyncratic:
the plural pattern cannot be predicted from the singular, so light stemming
(which only strips affixes) never connects the two forms.

**Example:**
```text
كِتاب (book) → كُتُب (books)     # broken plural: pattern change, no suffix
مُعَلِّم (teacher) → مُعَلِّمُون   # sound plural: suffix added
```

**Related concepts:** Pattern (wazn), Root (jadhr), Light stemming

---

### Byte-fallback

**Definition:** A tokenizer strategy that encodes any character its vocabulary
cannot represent as the character's raw UTF-8 bytes. Arabic letters cost 2
byte tokens each, inflating sequences roughly 8-9x versus whitespace words.
The exercise simulates a model with no Arabic coverage this way.

**Example:**
```
=== tokenizer comparison over 18 texts (40 words) ===
  byte-fallback          351      8.78       0.0%       80.5%
  # 80.5% of characters paid as raw UTF-8 bytes
```

**Related concepts:** Unknown-character rate, Tokenizer contract, Subword
tokenization

---

### Clitic

**Definition:** A word-like element that is grammatically independent but
fused to a host word in writing, with no space separating them. Arabic
clitics include the conjunction و, the definite article ال, prepositions
(ب، ك، ل، ف), and pronoun suffixes (ها، هم، ه، ي، ...).

**Example:**
```text
وكتابها  =  و  +  كتاب  +  ها
(conjunction) (stem) (enclitic)
```

**Related concepts:** Proclitic, Enclitic, Conservative segmentation

---

### Conservative segmentation

**Definition:** Splitting an Arabic word only at known clitic boundaries,
with length floors that keep the stem intact and guard sets that refuse
lexically fused words. Precision over recall: a missed split is recoverable
downstream; a split root is not.

**Example:**
```python
segment_word("والكتابها")  # ("و", "ال", "كتاب", "ها")
segment_word("الله")  # ("الله",) — guard: rest too short after ال
segment_word("كتب")  # ("كتب",)  — root never split
```

**Related concepts:** Root (jadhr), Round-trip guarantee, Light stemming

---

### Digit folding

**Definition:** Mapping Arabic-Indic (٠-٩) and Extended Arabic-Indic (۰-۹)
digits to ASCII (0-9) in the working copy so that edition, page, and year
fields compare across digit systems. The display copy keeps the source digits.

**Example:**
```python
normalize_working_copy("طبعة دار الحديث ١٤٤٥")
# -> "طبعة دار الحديث 1445"  (working copy)
# original keeps: ١٤٤٥
```

**Related concepts:** Working copy, MOR007, Surface variation

---

### Display form

**Definition:** The verbatim observed string, kept for citation and display.
It is never mutated by normalization, segmentation, or stemming. In Athar's
contracts this is `Passage.original`.

**Example:**
```python
@dataclass(frozen=True)
class TextSample:
    raw: str  # display form: بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
```

**Related concepts:** Two-text discipline, Working copy, Display fidelity

---

### Dialect continuum

**Definition:** The span from classical Arabic through Modern Standard
Arabic (MSA) to regional spoken varieties (Egyptian, Levantine, Gulf, ...).
Each point on the continuum has distinct orthography, morphology, and
vocabulary. A mixed-variety corpus needs a recorded variety policy or one
tuning knob cannot serve all users (MOR004).

**Example:**
```text
MSA:         أين تذهب اليوم؟
Levantine:   وين رايح اليوم؟
Egyptian:    هروح فين النهاردة؟
```

**Related concepts:** Variety decision, Surface variation, MOR004

---

### Enclitic

**Definition:** A pronoun suffix fused to the end of a stem. Multi-character
enclitics (ها، هم، هن، هما، كم، كن، نا، كما) may attach to bases of ≥ 2
characters; single-character enclitics (ه، ي، ك) require a base of ≥ 4
characters to avoid false splits on short words.

**Example:**
```python
segment_word("كتابها")  # ("كتاب", "ها")   — multi-suffix, base ≥ 2
segment_word("عليه")  # ("عليه",)        — base would be 2 < 4: refused
```

**Related concepts:** Proclitic, Conservative segmentation

---

### Fused preposition

**Definition:** A preposition written together with the definite article,
with no space: بال (ب + ال), كال (ك + ال), فال (ف + ال), and the elided-lam
form لل (ل + ال, the alef dropped after lam). The segmenter splits each into
preposition + article + stem when ≥ 3 characters remain.

**Example:**
```python
segment_word("بالكتاب")  # ("ب", "ال", "كتاب")
segment_word("للمسافر")  # ("ل", "ال", "مسافر")
```

**Related concepts:** Proclitic, Round-trip guarantee

---

### Gemination

**Definition:** Doubling of a consonant, marked in diacritized text by
shadda (شَّ). Gemination distinguishes verb forms and derived nouns;
stripping shadda from a working copy merges pairs that morphology keeps
apart, which is why the display copy always keeps it.

**Example:**
```text
مُعَلِّم (teacher)  vs  مُعلِم (one who studies)
           ^^^^ shadda marks the doubled ل
```

**Related concepts:** Tashkeel, Shadda, Working copy

---

### Hamza

**Definition:** The glottal stop letter ء, written alone or on an alef
carrier (أ إ آ ٱ) depending on position and orthographic tradition. Alef
variants fold to bare alef in the working copy; the display copy keeps the
observed carrier.

**Example:**
```python
normalize_working_copy("كتاب الإيمان") == normalize_working_copy("كتاب الايمان")
# True in the working copy; display keeps each observed form
```

**Related concepts:** Alef maqsura, Working copy, Normalization

---

### Light stemming

**Definition:** Stripping known prefixes (و، ال، ب، ك، ل، ف) and suffixes
(ها، هم، ...) from a word, stopping before the root. Used for lexical
retrieval expansion, never for rewriting stored text. The exercise's
segmenter is the light end; full morphological analysis returns root,
pattern, and features.

**Example:**
```python
segment_word("والكتابها")  # ("و", "ال", "كتاب", "ها") — not ك-ت-ب
# a light stemmer might yield: كتاب
# a full root extractor would yield: كتب
```

**Related concepts:** Conservative segmentation, Root (jadhr), Morphological
analyzer

---

### Morphological analyzer

**Definition:** A system that returns a set of candidate analyses per word:
root, pattern, part of speech, and morphological features. CAMeL Tools and
Farasa are production analyzers; the exercise implements the light end
(conservative clitic segmentation) because it is auditable and round-trips.

**Example:**
```python
# production: from camel_tools.morphology.analyzer import MorphologicalAnalyzer
# exercise:   segment_word("وكتابها") -> ("و", "كتاب", "ها")
```

**Related concepts:** Light stemming, Root (jadhr), Pattern (wazn)

---

### Normalizer version

**Definition:** A version stamp naming the rules that produced a derived key.
Every StoredText carries it; changing a folding rule bumps the version and
re-derives keys as a migration. Mixing key generations in one index is
MOR005.

**Example:**
```python
NORMALIZER_VERSION = "ar-morph-norm-1.0"
# a rule change produces "ar-morph-norm-1.1" and a re-index
```

**Related concepts:** MOR005, Working copy, Two-text discipline

---

### Pattern (wazn)

**Definition:** The vowel/template skeleton assigned to a root, carrying
grammatical and derivational meaning. The same root in different patterns
yields different lexemes (verb, participle, noun of instance, place).

**Example:**
```text
root ك-ت-ب:
  فِعَال  → كِتاب   (book)
  فَاعِل  → كاتِب   (writer)
  مَفْعَل → مَكْتَبَة (library)
```

**Related concepts:** Root (jadhr), Broken plural, Morphological analyzer

---

### Pipeline audit

**Definition:** A declarative checker that inspects a PipelineConfig (steps,
flags, input sources) and emits MOR001-MOR007 findings without loading a
model. CI contract: the BAD pack must surface every rule; the GOOD pack must
produce zero findings.

**Example:**
```
=== GOOD pack: pipeline audit ===
  findings: 0 (errors: 0, warnings: 0)
GOOD pack clean
```

**Related concepts:** MOR001-MOR007, PipelineConfig, Evaluation gate

---

### Proclitic

**Definition:** A clitic fused to the front of a stem: the conjunction و,
the definite article ال, and fused prepositions (بال كال فال لل). The
segmenter strips one proclitic layer per rule, with length floors.

**Example:**
```python
segment_word("والكتاب")  # ("و", "ال", "كتاب")
# R1 strips و, then R3 strips ال
```

**Related concepts:** Enclitic, Clitic, Conservative segmentation

---

### Root (jadhr)

**Definition:** The consonantal base carrying a semantic field, usually
three consonants. The root is never a segment: splitting a word into root
consonants destroys the surface evidence and confuses derivation with
segmentation.

**Example:**
```text
ك-ت-ب  (writing-related)
ج-ل-س  (sitting-related)
ع-ل-م  (knowledge-related)
```

**Related concepts:** Pattern (wazn), Light stemming, Conservative
segmentation

---

### Round-trip guarantee

**Definition:** The invariant that segments re-joined reproduce the normalized
string exactly. One orthographic rule is needed (ل + ال → لل elision); every
other clitic concatenates directly. The exercise asserts this on all 18
samples.

**Example:**
```python
reconstruct(stored.segments) == stored.normalized  # must be True
# display fidelity: 18/18 samples round-trip
```

**Related concepts:** Conservative segmentation, Display fidelity, Working
copy

---

### Shadda

**Definition:** The diacritic ّ marking gemination (a doubled consonant).
It is Unicode category Mn (nonspacing mark) and strips from working copies;
it survives in display and Quranic text because it distinguishes derived
forms.

**Example:**
```text
مُعَلِّم  (teacher, with shadda on ل)
# strip_tashkeel removes ّ for the working copy; display keeps it
```

**Related concepts:** Gemination, Tashkeel, Working copy

---

### Subword tokenization

**Definition:** Splitting words into vocabulary fragments (BPE, Unigram, or
a curated fragment list). Arabic inflates ~1.7 tokens per whitespace word
under trained subword models. The vocabulary is part of the model's
contract; swapping tokenizers under a saved checkpoint is a deployment
incident.

**Example:**
```
  subword-greedy          67      1.68       8.6%        0.0%
  # 1.68 tokens per word; 8.6% unk from a hand-built vocab
```

**Related concepts:** Tokenizer contract, Unknown-character rate, Byte-fallback

---

### Surface variation

**Definition:** The same concept written differently across time (classical
vs modern), space (dialect orthographies), and register (MSA vs spoken).
Variation is the input to normalization and the reason entity resolution
(topic 08) exists.

**Example:**
```text
محمد / محمَّد / ىمحمد (Egyptian final-alef spelling)
١٤٤٥ / 1445  (digit systems)
```

**Related concepts:** Dialect continuum, Alef maqsura, Digit folding

---

### Tashkeel

**Definition:** The set of short-vowel and related diacritics: fatha,
damma, kasra, sukun, shadda, tanween, and Quranic extras (wasla,
superscript alef). Stripped from working copies; kept in display and
Quranic text.

**Example:**
```python
normalize_working_copy("محمَّد") == "محمد"  # working copy
# original keeps: محمَّد (display)
```

**Related concepts:** Shadda, Working copy, MOR002

---

### Ta marbuta

**Definition:** The letter ة, a noun-final marker that surfaces as ه in
speech. Folding ة → ه in the index copy merges distinct words, so it is
fuzzy-only (topic 02); the working copy keeps ة and ه distinct.

**Example:**
```python
normalize_working_copy("مدرسة") != normalize_working_copy("مدرسه")  # index
normalize_fuzzy_key("مدرسة") == normalize_fuzzy_key("مدرسه")  # fuzzy
```

**Related concepts:** Normalization, Working copy, Fuzzy key

---

### Tatweel

**Definition:** The character ـ (U+0640), used for decorative elongation in
headlines and often a PDF-extraction artifact. Removed from working copies;
it carries no lexical content.

**Example:**
```python
normalize_working_copy("كــتاب") == normalize_working_copy("كتاب")  # True
```

**Related concepts:** Working copy, Normalization

---

### Tokenizer contract

**Definition:** The rule that a model's tokenizer is fixed at training time.
Changing the vocabulary under a saved checkpoint mismatches token ids and
embeddings; the byte-fallback column shows what a script-coverage mismatch
costs. Version the tokenizer with the model.

**Example:**
```text
# a checkpoint trained with tokenizer A cannot silently switch to tokenizer B
# re-train or re-fine-tune; never swap
```

**Related concepts:** Subword tokenization, Byte-fallback, Unknown-character
rate

---

### Two-text discipline

**Definition:** Every record keeps two texts: the display form (verbatim,
never mutated) and the derived working copy (normalized, versioned). The
original is evidence; the working copy is an index artifact. Athar enforces
this with `Passage.original` / `Passage.searchable`.

**Example:**
```python
@dataclass(frozen=True)
class StoredText:
    original: str  # verbatim
    normalized: str  # derived; re-normalizing original reproduces it
```

**Related concepts:** Display form, Working copy, Normalizer version

---

### Unknown-character rate

**Definition:** The share of characters a tokenizer's vocabulary cannot
represent. Zero for word-level (vocabulary is the corpus) and for
byte-fallback (everything is representable as bytes); nonzero for
hand-built subword lists. A trained BPE covers its training distribution.

**Example:**
```
  word-whitespace         40       1.0       0.0%        0.0%
  subword-greedy          67      1.68       8.6%        0.0%
  byte-fallback          351      8.78       0.0%       80.5%
```

**Related concepts:** Subword tokenization, Byte-fallback, Tokenizer contract

---

### Variety decision

**Definition:** A recorded, versioned policy for how source varieties are
stamped, mixed, and queried. Without it, a mixed-variety corpus has no
justified tuning point (MOR004). The GOOD pack stamps variety at ingest and
routes dialect queries through a documented expansion map.

**Example:**
```python
variety_decision = (
    "ar-morph-variety-1.0: every passage is stamped with its source "
    "variety; queries default to msa+classical, dialect queries route "
    "through the documented expansion map; sources never mix silently"
)
```

**Related concepts:** Dialect continuum, MOR004, Surface variation

---

### Wasla

**Definition:** The character ٱ (alef wasla), marking a "connected" alef in
Quranic and classical orthography: the alef is pronounced only when the
word begins an utterance. It folds to bare alef in the working copy; the
display copy keeps the wasla.

**Example:**
```text
بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ   (display, with wasla)
بسم الله الرحمن الرحيم                    (working copy, wasla folded)
```

**Related concepts:** Tashkeel, Working copy, Display form

---

### Working copy

**Definition:** The derived, normalized text used for matching and embedding.
It is re-derivable from the original by a versioned normalizer; it never
overwrites the original; and it is the only text the segmenter and stemmer
touch.

**Example:**
```python
normalized = normalize_working_copy(original)  # derived
segments = segment_text(normalized)  # derived from derived
# original is never mutated (MOR001 holds by construction)
```

**Related concepts:** Two-text discipline, Display form, Normalizer version
