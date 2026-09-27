# Unicode and Arabic Text Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Code point | A number assigned to an abstract character (e.g. U+0644 = LAM) |
| Code unit | A bit-chunk in an encoding (UTF-8 byte, UTF-16 16-bit unit) |
| Encoding | Translation between code points and bytes (UTF-8, UTF-16, cp1256) |
| UTF-8 | Variable-length encoding: 1 byte ASCII, 2–4 bytes for the rest |
| BOM | Byte-order mark (U+FEFF) at file start; `utf-8-sig` strips it |
| Mojibake | Readable garbage from decoding bytes in the wrong encoding |
| UnicodeDecodeError | Raised by `errors="strict"` on invalid bytes |
| U+FFFD | Replacement character used by `errors="replace"` |
| NFC | Normalization form: composed (base+mark fused) — storage form |
| NFD | Normalization form: decomposed (marks split out) |
| NFKC | NFC + compatibility folding (ligatures, presentation forms) — search-key form |
| NFKD | NFD + compatibility folding |
| Presentation form | Pre-shaped Arabic glyph variant (U+FB50–FDFF, U+FE70–FEFF) |
| Lam-alef ligature | لا as one code point (U+FEFB) vs two (U+0644 U+0627) |
| Harakat (tashkeel) | Arabic diacritics U+064B–U+0652 plus superscript alef U+0670 |
| Hamza carriers | أ إ آ ؤ ئ — letters whose hamza folds away for search |
| Alef maqsura | ى (U+0649); folds to ي (yaa) in search keys |
| Ta marbuta | ة (U+0629); folds to ه in search keys for recall |
| Arabic-Indic digits | ٠١٢٣ (U+0660–U+0669) |
| Extended Arabic-Indic digits | ۰۱۲۳ (U+06F0–U+06F9) |
| Digit folding | Mapping Arabic-Indic/Persian digits to ASCII `0123` |
| Bidirectional algorithm | Unicode rules reordering RTL/LTR runs for display |
| Bidi isolate | Invisible characters (U+2066–U+2069) containing direction runs |
| Collation | Language-aware sort order (dictionary order for Arabic) |
| Search key | Normalized, folded string used for matching; never displayed |
| Verbatim text | The stored original (NFC) used for display and citation |
| Batch import | Streaming records in fixed-size groups with bounded memory |
| Quarantine | Separating corrupt records for review instead of aborting |
| `str.isdigit()` | True for Arabic-Indic digits too; `int()` accepts ASCII only |

---

## Detailed Definitions

### Code point vs bytes
A `str` is a sequence of code points; `len()` counts them. Bytes only appear after `.encode()`. Arabic letters are 2 bytes in UTF-8, so byte limits and character limits are different numbers — state which one you mean.

### Normalization (NFC / NFD / NFKC / NFKD)
The same text can be stored composed or decomposed. NFC is the compact canonical form for storage; NFKC additionally folds compatibility variants (ligatures, presentation forms) and is the right form for search keys. Normalize once at ingestion.

### Presentation forms and lam-alef
Legacy Arabic encodings emit positional glyph variants including the lam-alef ligature (U+FEFB) as a single code point. NFKC folds them to standard letters so legacy-fed text matches clean text.

### Harakat (tashkeel)
Combining diacritics over base letters. Keep them in stored/display text (they carry meaning in Qur'anic material); strip them from search keys so unvocalized queries match.

### Hamza / alef maqsura / ta marbuta folding
Search-key steps that unify أ إ آ → ا, ى → ي, ة → ه. They raise recall at the cost of precision; apply to the search key only, never to display text.

### Digit folding
Translating ٠–٩ (U+0660+) and ۰–۹ (U+06F0+) to ASCII before `int()` parsing. `str.isdigit()` accepts all families; `int()` does not.

### Bidirectional text and isolates
Mixed Arabic/Latin strings reorder at render time. Wrapping embedded Latin/number runs in bidi isolates (U+2066…U+2069) prevents wrong visual attachment. Display concern only.

### Collation
Code-point sort ≠ Arabic alphabetical order (hamza carriers and ة land in the wrong place). Use ICU-level collation for user-facing sorts; the folded search key is enough for internal grouping.

### Search key vs verbatim text
Two fields with two jobs: verbatim text (NFC) for display and citation, folded key (NFKC + strip + letter unification + digit folding) for matching and deduplication.

### Batch import with bounded memory
Stream the file line by line, parse and normalize per record, accumulate at most one batch in memory. A corrupt record raises a typed error carrying line number and reason; the caller quarantines or aborts.

### Quarantine
The failure policy for corrupt records: record the error with its location, skip the record, keep importing. Opposite of silent skip and of abort-the-whole-run.
