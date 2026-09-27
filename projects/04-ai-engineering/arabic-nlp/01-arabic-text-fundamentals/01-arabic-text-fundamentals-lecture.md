# Arabic NLP 01: Arabic Text Fundamentals

## 🎯 Topic Overview

Arabic is not "English with different letters." It is a morphologically rich
language where a single word carries the meaning of a whole English clause,
written in a script that drops short vowels, joins letters, and reorders
visually. Every downstream failure in Arabic retrieval and generation —
missing matches, broken quotes, wrong answers — traces back to a
misunderstanding of one of these fundamentals. This lecture builds the
foundation: script, Unicode, morphology, and the two-text discipline that
protects the user's quote.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the Arabic script: right-to-left, cursive joining, contextual letter forms
2. Distinguish the 28 letters from the 3 short vowels and the diacritics that mark them
3. Explain why Arabic is morphologically rich and what that costs retrieval
4. Handle Arabic in Python: Unicode normalization, NFC/NFD, and encoding traps
5. Apply the two-text discipline: original for display, normalized for search

---

## 1. The Script

Arabic writes right to left, joins most letters within a word, and gives each
letter up to four forms (isolated, initial, medial, final) depending on
position. Six letters never join to the following one, which is why the same
word can look different at a glance. The alphabet has 28 letters; the three
short vowels (a, i, u) are written as diacritics above or below letters and
are usually omitted in running text.

```python
# The same letter in its four forms (beh):
# isolated ب  initial بـ  medial ـبـ  final ـب
```

## 2. Diacritics and the Two Texts

Full diacritization (tashkeel) marks every short vowel; most modern text is
undiacritized, which means the reader (and the model) must infer vowels from
context. This is the root of Arabic ambiguity: the same letters can be read
multiple ways. The practical consequence for a knowledge system is the
**two-text discipline**: keep the original text exactly as the source wrote
it for display and citation, and derive a normalized search text (strip
diacritics, normalize hamza forms) for matching. Never let normalization
change what the user sees quoted.

```python
# display_text:  "قالَ اللهُ تعالى"   (as written, with diacritics)
# search_text:   "قال الله تعالى"     (normalized, for matching)
```

## 3. Morphology: The Retrieval Cost

Arabic builds words from triliteral roots with templates: كَتَبَ (he wrote),
يَكْتُبُ (he writes), كِتَاب (book), مَكْتَب (office), كَاتِب (writer) all
share the root k-t-b. A query for "كتب" must match "الكتاب" and "مكتبة" —
exact string matching fails immediately. This is why Arabic retrieval needs
stemming or root-aware matching, and why naive tokenization (split on
whitespace) produces poor recall. The lesson: plan for morphology at the
indexing stage, not as a retrieval afterthought.

## 4. Unicode in Python

```python
import unicodedata

# Normalize to NFC (composed) for consistent storage
text = unicodedata.normalize("NFC", "السلام عليكم")


# Strip diacritics for the search text
def strip_tashkeel(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
```

Arabic letters are in the U+0600–U+06FF block; combining marks are category
`Mn`. The classic encoding trap is a file read as Windows-1256 that should be
UTF-8 — the bytes decode to mojibake and every downstream match silently
fails. Always declare encoding on file reads and verify with a round-trip
test.

## 5. The Two-Text Discipline in Practice

Store both texts on every passage: `original` (verbatim, for display and
citation) and `searchable` (normalized, for indexing). The search index
operates on `searchable`; the answer cites `original`. This single decision
prevents the most common Arabic RAG bug: a user asks a question, the system
retrieves the right passage, then displays a normalized, diacritic-stripped
quote that no longer matches what the book actually says.

## Common Mistakes

- Reading Arabic files without declaring UTF-8, producing silent mojibake.
- Normalizing the display text and breaking the user's quote.
- Splitting on whitespace and expecting morphology to take care of itself.
- Forgetting that Arabic is right-to-left when building UIs or string slicing.

## Key Takeaways

1. Arabic is morphologically rich and script-complex; plan for both.
2. Keep original and normalized texts separate, always.
3. Normalize to NFC; strip diacritics only for the search text.
4. Declare UTF-8 on every file read; test the round-trip.