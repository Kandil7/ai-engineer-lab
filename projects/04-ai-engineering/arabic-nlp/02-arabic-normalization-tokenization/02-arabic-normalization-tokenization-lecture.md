# Arabic NLP 02: Arabic Normalization and Tokenization

## Topic Overview

Arabic text processing starts with two operations that determine every
downstream result: normalization and tokenization. Normalization
transforms raw text into a canonical form for comparison; tokenization
splits text into units for analysis. For Arabic, both operations are
harder than for English because of the script's richness: diacritics
(tashkeel), letter variants (alef forms), and morphological complexity
all affect the result.

Getting normalization wrong produces false matches (two different words
normalize to the same form) or false misses (the same word fails to
match because of an unnormalized variant). Getting tokenization wrong
loses information or creates noise. This lecture covers both operations
in depth, with the Arabic-specific decisions that determine quality.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the Arabic writing system features that affect normalization
2. Design a normalization pipeline with explicit decisions
3. Implement the standard normalization steps for Arabic
4. Choose the right tokenization strategy for the task
5. Detect false matches and false misses from over/under-normalization
6. Handle the two-text discipline (original vs normalized)
7. Test normalization quality with known word pairs

## Prerequisites

- Arabic text fundamentals (arabic-nlp 01)
- Basic Python string processing

---

## 1. Why Arabic Normalization Is Hard

### The Arabic writing system

Arabic script has features that make direct string matching unreliable:

| Feature | Example | Effect on matching |
|---------|---------|-------------------|
| Diacritics (tashkeel) | كَتَبَ vs كتب | Same word, different strings |
| Alef variants | أ إ آ ا | Often the same word |
| Ta marbuta vs ha | ة vs ه | Often the same word |
| Alef maqsura vs ya | ى vs ي | Often the same word |
| Shadda (gemination) | رَسُول vs رَسُّول | Meaning changes, but similar |
| Tatweel (kashida) | كـــتـــب | Decorative, not meaningful |

### The core tension

Normalization has two competing goals:

1. **Match aggressively** — "الله" should match "اللَّهَ" and "اللهُ"
2. **Don't over-merge** — "كتب" (he wrote) should NOT match "كُتُب" (books)

Over-normalization merges distinct words. Under-normalization misses
valid matches. The right balance depends on the task:
- **Search/retrieval:** Normalize aggressively (more matches > more precision)
- **Translation/morphology:** Normalize minimally (preserve distinctions)
- **Islamic text:** Normalize moderately (preserve diacritics that change meaning)

---

## 2. The Normalization Pipeline

### Step-by-step

```python
def normalize_arabic(text: str) -> str:
    """Standard Arabic normalization for search/retrieval."""
    # 1. Remove diacritics (tashkeel)
    text = re.sub(r"[\u064B-\u065F\u0670\u0640]", "", text)

    # 2. Unify alef forms
    text = text.replace("أ", "ا")  # أ -> ا
    text = text.replace("إ", "ا")  # إ -> ا
    text = text.replace("آ", "ا")  # آ -> ا

    # 3. Unify ta marbuta and ha
    text = text.replace("ة", "ه")  # ة -> ه

    # 4. Unify alef maqsura and ya
    text = text.replace("ى", "ي")  # ى -> ي

    # 5. Remove tatweel
    text = text.replace("\u0640", "")

    # 6. Remove tatweel and normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
```

### What each step does

| Step | Input | Output | Rationale |
|------|-------|--------|-----------|
| Remove tashkeel | كَتَبَ | كتب | Diacritics are for pronunciation, not identity |
| Unify alef | أُمّ | امّ | Alef variants are orthographic, not semantic |
| Unify ta marbuta | مدرسه | مدرسه | ة and ه often the same word |
| Unify ya | على | علي | ى and ي often the same word |
| Remove tatweel | كـــتـب | كتب | Kashida is decorative |

### What NOT to normalize

| Feature | Why not | Example |
|---------|---------|---------|
| Shadda (gemination) | Changes meaning | رَسُول (messenger) vs رَسُّول (thoroughly sent) |
| Hamza on waw/ya | Preserves meaning | ؤ vs ئ are different letters |
| Quranic pause marks | Part of the text | ۟ ۖ ۗ ۘ |
| Arabic-Indic digits | May be significant | ١٢٣ vs 123 (task-dependent) |

### The moderate normalization for Islamic text

For Islamic text, the recommendation is **moderate normalization**:

```python
def normalize_islamic(text: str) -> str:
    """Moderate normalization: keep meaning-bearing diacritics."""
    # Remove only the most common tashkeel
    text = re.sub(r"[\u064B-\u0650\u0652]", "", text)  # fatha, damma, kasra, sukun
    # Keep shadda (gemination)
    # Unify alef forms
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    # Unify ta marbuta
    text = text.replace("ة", "ه")
    return text
```

The rule: **normalize what is orthographic, preserve what is semantic.**

---

## 3. Tokenization

### What tokenization does

Tokenization splits text into units: words, subwords, or characters. The
unit choice depends on the task.

| Unit | Used for | Example |
|------|----------|---------|
| Word | Lexical retrieval (BM25), keyword search | ["القصر", "جائز", "للمسافر"] |
| Subword | Embeddings, language models | ["الق", "صر", "جا", "ئز"] |
| Character | Spell checking, fuzzy matching | ["ا", "ل", "ق", "ص", "ر"] |

### Arabic word tokenization

Arabic words are space-delimited but carry clitics (prefixes, suffixes)
that merge multiple morphemes into one surface form:

```
Surface: "وَبِالْوَالِدَيْنِ" (and with parents)
Morphemes: وَ + بِ + الْ + والد + ين
```

For lexical retrieval (BM25), word tokenization is usually sufficient.
The clitics come along with the word and the index matches the whole form.

### Arabic subword tokenization

For embeddings and language models, subword tokenizers (BPE, SentencePiece,
WordPiece) handle Arabic's morphological richness by splitting rare words
into known pieces. The tokenizer's vocabulary determines how Arabic text
is represented.

**Critical:** The subword tokenizer must be trained on Arabic text. A
tokenizer trained only on English will split Arabic into meaningless
fragments or represent it as [UNK] tokens.

### Choosing the tokenizer

| Task | Tokenizer | Why |
|------|-----------|-----|
| BM25 / keyword search | Word | Matches user expectations |
| Embeddings | Model's subword | Must match the embedding model |
| Morphological analysis | Morphological analyzer | Handles clitics |
| Translation | SentencePiece / BPE | Handles unknown words |

### Tokenization and the two-text discipline

The searchable text (from the two-text discipline) is what gets tokenized.
The original text is for display only. Tokenization happens on the
normalized form.

```python
# Original: "القَصْرُ جَائِزٌ لِلْمُسَافِرِ"
# Normalized: "القصر جائز للمسافر"
# Tokens (word): ["القصر", "جائز", "للمسافر"]
# Tokens (subword): ["الق", "صر", "جا", "ئز", "لل", "مس", "افر"]
```

---

## 4. False Matches and False Misses

### False matches (over-normalization)

When normalization merges distinct words:

| Word 1 | Word 2 | Normalized to | Problem |
|--------|--------|---------------|---------|
| كتب (he wrote) | كُتُب (books) | كتب | Meaning lost |
| صلاه (prayer) | صلوه (pray!) | صلوه | Imperative vs noun |
| حديث (hadith) | حديت (conversation) | حديث | Different words |

### False misses (under-normalization)

When normalization fails to merge same words:

| Word 1 | Word 2 | Why they don't match |
|--------|--------|---------------------|
| اللهُ | اللَّهَ | Diacritics differ |
| أُمّ | امّ | Alef variant |
| مدرسه | مدرسة | Ta marbuta variant |

### Detecting the problem

Build a test set of word pairs:
- **Should match:** Same word, different surface forms (100 pairs)
- **Should NOT match:** Different words, similar surface forms (100 pairs)

Measure:
- **Match recall:** Of "should match" pairs, how many do match?
- **Match precision:** Of all matches, how many are correct?

The normalization pipeline is balanced when both are high (>95%).

---

## 5. Implementation with Tests

### The normalization function

```python
import re


def normalize_arabic(text: str) -> str:
    # Remove tashkeel
    text = re.sub(r"[\u064B-\u065F\u0670\u0640]", "", text)
    # Unify alef forms
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    # Unify ta marbuta
    text = text.replace("ة", "ه")
    # Unify alef maqsura
    text = text.replace("ى", "ي")
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
```

### The word tokenizer

```python
def tokenize_words(normalized_text: str) -> list[str]:
    """Split into words. Simple space-based for lexical retrieval."""
    return normalized_text.split()
```

### The test suite

```python
def test_normalization():
    # Should match after normalization
    assert normalize_arabic("اللهُ") == normalize_arabic("اللَّهَ")
    assert normalize_arabic("أُمّ") == normalize_arabic("امّ")
    assert normalize_arabic("مدرسه") == normalize_arabic("مدرسة")

    # Should NOT merge (under moderate normalization)
    # Note: aggressive normalization would merge these
    assert normalize_arabic("كتب") != normalize_arabic("كُتُب")  # if we keep kasra


def test_tokenization():
    tokens = tokenize_words("القصر جائز للمسافر")
    assert tokens == ["القصر", "جائز", "للمسافر"]
    assert len(tokens) == 3
```

---

## 6. The Arabic-Specific Decisions

### Decision: which diacritics to remove?

| Choice | Effect | Use when |
|--------|--------|----------|
| Remove ALL tashkeel | Maximum matching | General search |
| Remove all except shadda | Preserves gemination | Islamic text |
| Keep all tashkeel | Exact matching | Text display, linguistic analysis |

### Decision: how to handle Quranic text?

Quranic text has additional markers:
- Sajda marks (۩)
- Pause marks (ۖ ۗ ۘ ۙ ۚ)
- Small marks (ۥ ۦ)

For retrieval: remove these markers.
For display: preserve them.

### Decision: Arabic-Indic digits vs Western digits?

| Context | Choice |
|---------|--------|
| User might type either | Normalize to one form |
| Source has a specific form | Preserve the source form |
| Citations reference page numbers | Normalize (so "12" matches "١٢") |

---

## 7. Quality Metrics for Normalization

### Match rate

What fraction of known-same word pairs match after normalization?

```
Match rate = (pairs that match) / (total should-match pairs)
Target: > 95%
```

### False match rate

What fraction of known-different word pairs incorrectly match?

```
False match rate = (wrong matches) / (total should-NOT-match pairs)
Target: < 5%
```

### Tokenization consistency

Does the same input always produce the same tokens? (Determinism test.)

```
assert tokenize(text) == tokenize(text)  # always true
```

### Vocabulary coverage (for subword)

What fraction of tokens are in the vocabulary (not [UNK])?

```
Coverage = (known tokens) / (total tokens)
Target: > 99%
```

---

## Real-World Application

In a production Arabic RAG system:

1. Source text is ingested with original + normalized forms.
2. The normalized form is tokenized for the search index.
3. User queries are normalized with the same pipeline.
4. The golden set includes Arabic word pairs that test match rate and false-match rate.
5. The normalization pipeline is versioned — a change requires re-indexing.

The normalization version is part of the corpus version. Changing the
normalization invalidates the index and the cache.

---

## Common Mistakes

1. **Normalizing for display** — showing normalized text to the user
   instead of the original with diacritics.

2. **Over-normalization** — removing shadda, merging كتب with كُتُب.
   For Islamic text, shadda is meaning-bearing.

3. **No test set** — never measuring match rate and false-match rate.
   The pipeline might be broken without anyone knowing.

4. **Different normalization for queries and corpus** — query normalized
   one way, corpus another. Matches fail silently.

5. **Ignoring Quranic markers** — leaving pause marks and sajda marks in
   the searchable text creates noise in embeddings.

6. **No versioning** — changing normalization without re-indexing.
   The old and new vectors become incomparable.

7. **Character tokenization for BM25** — splitting into characters
   destroys word-level matching. Use word tokens for lexical search.

---

## Key Takeaways

1. Arabic has features (diacritics, alef forms, ta marbuta) that break
   naive matching.
2. Normalization has a tension: aggressive matching vs preserving
   distinctions.
3. For Islamic text, moderate normalization: keep shadda, unify alef.
4. Tokenization unit depends on the task: words for BM25, subwords for
   embeddings.
5. Test with known word pairs: match rate > 95%, false-match rate < 5%.

---

## Self-Check Questions

1. What are three Arabic writing features that cause false misses?
2. Why should shadda be preserved for Islamic text but removed for
   general search?
3. What is the two-text discipline and how does normalization fit in?
4. How would you measure whether your normalization is over-aggressive?
5. Why must the query and corpus use the same normalization pipeline?

---

## Further Reading / Connections

- **arabic-nlp 01** — Arabic text fundamentals
- **arabic-nlp 03** — Lexical retrieval (BM25) that uses word tokens
- **arabic-nlp 04** — Embeddings that use subword tokens
- **rag-system 01** — The two-text discipline in chunking
- **data-engineering 02** — Schemas for storing original + normalized forms