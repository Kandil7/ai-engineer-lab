# Arabic NLP 01: Arabic Text Fundamentals

## Topic Overview

Arabic is not "English with different letters." It is a morphologically rich language
where a single word can carry the meaning of a whole English clause, written in a script
that writes right to left, joins letters contextually, drops short vowels, and reorders
visually. Nearly every downstream failure in Arabic retrieval and generation, from missing
matches to broken quotes to confident wrong answers, traces back to misunderstanding one of
these fundamentals.

This lecture builds the foundation: the script, the diacritic system, why morphology is a
retrieval problem rather than a detail, how Arabic behaves in Python's Unicode model, and
the two-text discipline that protects the user's quote. It is the first lecture in the
Arabic module because every later topic (tokenization, lexical retrieval, embeddings,
hybrid search, evaluation) assumes this material.

None of it is exotic to a computer. All of it is easy to get wrong silently, which is why
the exercises prove each primitive with an assertion rather than trusting that it works.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Describe the Arabic script: right-to-left direction, cursive joining, contextual letter
   forms, and the 28 letters.
2. Distinguish the letters from the three short vowels and the diacritics that mark them.
3. Explain why Arabic is morphologically rich and what that costs retrieval.
4. Handle Arabic text in Python: NFC/NFD normalization, diacritic stripping, and the
   category-`Mn` test.
5. Apply the two-text discipline: `original` for display, `searchable` for matching.
6. Detect the encoding traps that produce silent mojibake.

## Prerequisites

- Basic Python strings and Unicode awareness.
- The idea of a "combining mark" as a character that modifies the previous one.

---

## 1. The Arabic Script

### Direction and joining

Arabic writes right to left. Most letters connect to the letters around them, and each
letter can take up to four shapes depending on its position: isolated, initial, medial, and
final. Six letters (the "non-joining" letters) never connect to the following letter, which
is why a word can appear to break in the middle:

```text
# The letter beh (ب) in its four positional forms:
# isolated ب, initial بـ, medial ـبـ, final ـب
```

The positional forms are different code points in some scripts; in Arabic they are the same
code point rendered differently by the font based on context. This matters because string
comparison operates on code points, not on glyphs, so `<text>`-level comparison is
code-point comparison, which is usually what you want.

### The letters and the vowels

The alphabet has 28 letters. The three short vowels (a, i, u) are not separate letters;
they are diacritics written above or below a letter. In normal running text they are
omitted, and the reader infers them from context. This omission is the root of much Arabic
ambiguity: the same letters can be read several ways.

### Hamza and the alef variants

The hamza (ء) and its carrier forms (أ, إ, آ) are a frequent source of mismatch. The same
word may be written with أ in one source and ا in another. Left unnormalized, these
variants split an index for no retrieval benefit. The later topics normalize them
deliberately; this lecture exposes why they exist.

## 2. Diacritics and Undiacritized Text

### Tashkeel

Full diacritization (tashkeel) marks every short vowel and other features. Most modern
text, and most of a large corpus, is undiacritized. A golden-set query may be
diacritized while the passage is not, or the reverse, so exact string matching fails on
what a human reads as the same word.

### Combining marks

Diacritics are Unicode combining marks in the category `Mn` (nonspacing mark). That is the
key fact: you can identify and remove them programmatically by category, without hardcoding
a list:

```python
import unicodedata


def strip_tashkeel(text: str) -> str:
    """Remove combining marks (diacritics) from Arabic text."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
```

Decomposing to NFD first separates every combining mark so the category filter can remove
it; the result is the undiacritized skeleton.

### Tatweel

Tatweel (ـ, U+0640) is a decorative elongation character with no phonetic value, sometimes
inserted for justification. It must be stripped for matching, or a word padded with tatweel
will not match its plain form.

## 3. Morphology: The Retrieval Cost

### Roots and patterns

Arabic builds words from triliteral roots with templates. The root k-t-b (ك ت ب) underlies:

| Word | Meaning |
| --- | --- |
| كَتَبَ | he wrote |
| يَكْتُبُ | he writes |
| كِتَاب | book |
| مَكْتَب | office, desk |
| مَكْتَبَة | library |
| كَاتِب | writer |

### Why this breaks exact matching

A user searching for "كتاب" (book) expects to find "الكتاب" (the book), "كتب" (books), and
perhaps "مكتبة" (library). Exact string matching finds none of these because they are
different strings. This is why Arabic retrieval needs stemming or root-aware matching, and
why naive whitespace tokenization produces poor recall.

### The lesson

Plan for morphology at the indexing stage. Stemming, root extraction, or careful
normalization chosen during ingestion is a retrieval design decision, not an afterthought.
The later topics (03, 04) build the lexical and dense arms that address it.

## 4. Unicode in Python

### Normalization forms

Unicode offers two canonical forms: NFC (composed) and NFD (decomposed). For storage,
normalize to NFC so the same logical text has one byte representation:

```python
def normalize_nfc(text: str) -> str:
    """Compose to NFC for consistent storage."""
    return unicodedata.normalize("NFC", text)
```

For diacritic stripping, decompose to NFD first. The two are used together: strip on NFD,
then recompose to NFC for storage.

### The Arabic block and the category test

Arabic letters occupy the U+0600 to U+06FF block. A quick script check:

```python
def is_arabic(text: str) -> bool:
    """True if the text contains Arabic-script characters (U+0600-U+06FF)."""
    return any("\u0600" <= c <= "\u06ff" for c in text)
```

This is coarse (Arabic letters also appear in presentation forms and extensions) but it is
enough to catch the common "did I load the right file" mistake.

## 5. The Two-Text Discipline

### The rule

Store two texts on every passage:

- `original`: the text exactly as the source wrote it, used for display and citation.
- `searchable`: the normalized text (diacritics stripped, hamza unified, tatweel removed),
  used for indexing and matching.

```python
# display_text:  "مَا الْكِتَابُ الْمُقَرَّرُ فِي الْمَدْرَسَةِ"   (as written)
# search_text:   "ما الكتاب المقرر في المدرسة"                    (normalized)
```

### Why both

The search index operates on `searchable` so that diacritized and undiacritized forms
match. The answer cites `original` so the user sees precisely what the book says. This one
decision prevents the most common Arabic RAG bug: the system retrieves the right passage
and then displays a normalized, diacritic-stripped quote that no longer matches the source.

### Never normalize the display text

Normalization is lossy by design. Applying it to what the user sees corrupts the quote and
breaks citation fidelity (AI Evaluation 02). The discipline is asymmetric on purpose: lossy
transformation for matching, verbatim preservation for display.

## 6. Encoding Traps and the Round-Trip Test

### The classic trap

A file that is UTF-8 but read as Windows-1256 (or vice versa) decodes to mojibake. The
bytes are intact; the interpretation is wrong. Every downstream match silently fails,
because the query and the passage are mojibake in different ways, or the same way but
compared as garbage.

### The round-trip test

Encode then decode, and assert the text survives:

```python
def roundtrip_utf8(text: str) -> bool:
    """Encode then decode UTF-8; True if the text survives intact."""
    return text.encode("utf-8").decode("utf-8") == text
```

A round-trip success is necessary but not sufficient; it does not catch mojibake that was
already decoded wrong before it reached you. Combine it with declaring the encoding on every
file read and checking for the Arabic block where Arabic is expected.

### Declare encoding always

Never rely on a platform default. Open files with an explicit `encoding="utf-8"`. On
Windows especially, the default is not UTF-8 and the failure is silent.

## 7. Why This Is the Foundation of Athar

Every Athar passage carries an `original` and a `searchable` form drawn from these
primitives. The contracts (`SourceLocation`, `Document`, `Passage`) enforce the two-text
discipline from the first line of code, and the by-book evaluation split assumes passages
are independent once normalized. Get the fundamentals right here and the retrieval topics
build cleanly; get them wrong and every later metric measures a text-handling bug.

## Real-World Application

- Normalizing a diacritized Quranic passage for search while displaying the diacritized
  original in the citation.
- Stripping tatweel from a justified book page so its words match the index.
- Unifying hamza variants so أ and ا do not split the inverted index.
- Running the round-trip test after every corpus load to catch an encoding regression.

## Common Mistakes

1. **Reading Arabic files without declaring UTF-8.** Silent mojibake, silent mismatches.
2. **Normalizing the display text.** The user's quote no longer matches the source.
3. **Splitting on whitespace and ignoring morphology.** Poor recall on inflected queries.
4. **Stripping diacritics with a hardcoded list.** Misses marks; use the `Mn` category.
5. **Forgetting tatweel.** Padded words never match their plain form.
6. **Assuming NFC and NFD are interchangeable.** Mixed forms compare unequal.
7. **Ignoring direction and positional forms when building UIs.** Display bugs that look
   like data bugs.

## Key Takeaways

1. Arabic is script-complex and morphologically rich; plan for both at indexing time.
2. Diacritics are combining marks in category `Mn`; strip them on NFD for the search text.
3. Keep `original` and `searchable` separate, always; never normalize the display text.
4. Normalize to NFC for storage; unify hamza variants; strip tatweel.
5. Declare UTF-8 on every read and test the round-trip; encoding bugs are silent.

## Self-Check Questions

1. Why are positional letter forms not a string-comparison hazard, while hamza variants
   are?
2. What Unicode category identifies a diacritic, and how is that used to strip it?
3. Why does exact string matching fail on the Arabic root k-t-b, and where is the fix
   applied?
4. Give the two texts a passage must store and one thing each is used for.
5. Why is the UTF-8 round-trip test necessary but not sufficient?

## Further Reading / Connections

- Arabic NLP 02 (normalization and tokenization) — the pipeline that formalizes stripping
  and tokenization.
- Arabic NLP 03 and 04 — the lexical and dense arms that consume the searchable text.
- `docs/learning/deep-dives/athar-retrieval-deep-dive.md` — the two-text discipline in the
  real system.
- `projects/04-ai-engineering/athar-lab/contracts.py` — the contracts that enforce it.
