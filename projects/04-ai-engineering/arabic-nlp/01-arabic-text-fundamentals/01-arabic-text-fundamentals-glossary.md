# Arabic NLP 01: Arabic Text Fundamentals — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Arabic script | Right-to-left cursive script, 28 letters, contextual forms | ب / بـ / ـبـ / ـب |
| Diacritics (tashkeel) | Marks for short vowels, usually omitted in text | َ ُ ِ |
| Morphology | Root-and-pattern word building (triliteral roots) | ك ت ب → كتب، كتاب |
| NFC / NFD | Unicode normalization forms (composed / decomposed) | storage consistency |
| Combining mark | Unicode category `Mn`; diacritics are combining marks | stripping target |
| Mojibake | Wrong-encoding decode producing garbage text | Windows-1256 vs UTF-8 |
| Two-text discipline | Original for display, normalized for search | quote preservation |

---

## Alphabetical Glossary

### Arabic script

**Definition:** The right-to-left cursive script of Arabic, with 28 letters
that take up to four contextual forms and join within words. Six letters
never join forward.

**Example:**
```python
# ب isolated, بـ initial, ـبـ medial, ـب final
```

**Related concepts:** Diacritics, RTL

---

### Combining mark

**Definition:** A Unicode character (category `Mn`) that modifies a preceding
base letter rather than standing alone. Arabic diacritics are combining
marks; stripping them is the normalization step.

**Example:**
```python
unicodedata.category("َ")  # 'Mn'
```

**Related concepts:** Diacritics, NFC / NFD

---

### Diacritics (tashkeel)

**Definition:** Marks encoding the three short vowels (and other phonetic
features), usually omitted in running text. Their absence creates ambiguity
that context must resolve.

**Example:**
```python
# كَتَبَ (fully diacritized) vs كتب (as usually written)
```

**Related concepts:** Combining mark, Two-text discipline

---

### Mojibake

**Definition:** Text decoded with the wrong encoding, producing garbage.
Arabic read as Windows-1256 when it is UTF-8 is the classic silent failure.

**Example:**
```python
open(path, encoding="utf-8")  # always declare; never guess
```

**Related concepts:** NFC / NFD

---

### Morphology

**Definition:** The root-and-pattern system where triliteral roots combine
with templates to form related words. Why exact string matching fails on
Arabic.

**Example:**
```python
# ك ت ب → كتب، كتاب، مكتبة، كاتب — one root, many words
```

**Related concepts:** Stemming, Tokenization

---

### NFC / NFD

**Definition:** Unicode normalization forms: NFC composes to single code
points, NFD decomposes to base plus combining marks. NFC for storage, NFD
for diacritic stripping.

**Example:**
```python
unicodedata.normalize("NFC", text)  # consistent storage
```

**Related concepts:** Combining mark, Diacritics

---

### Two-text discipline

**Definition:** Storing both the verbatim original (for display and citation)
and a normalized searchable form (for indexing). The quote the user sees is
never altered by normalization.

**Example:**
```python
# original: "قالَ اللهُ"  searchable: "قال الله"
```

**Related concepts:** Diacritics, Normalization

---

## Related Concepts

- **RTL**: right-to-left layout and string handling
- **Stemming**: reducing words to roots for recall (topic 02)
- **Normalization**: the search-side text pipeline (topic 02)

## Key Takeaways

1. Script and morphology shape every Arabic pipeline decision.
2. Two texts: original for the user, normalized for the index.
3. Declare UTF-8; test the round-trip.