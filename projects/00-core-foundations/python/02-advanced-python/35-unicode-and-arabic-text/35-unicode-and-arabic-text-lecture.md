# Advanced Python Lecture 35: Unicode and Arabic Text Processing

## Topic Overview

Unicode is the difference between a search index that finds the verse the user is looking for and one that misses it while staring at it. An Arabic RAG pipeline receives the same text in many disguises: precomposed or decomposed characters, lam-alef as one ligature or two letters, with or without harakat, Arabic-Indic or ASCII digits, UTF-8 or Windows-1256 bytes. Each disguise is byte-different but semantically identical. Compare raw strings and search fails; index raw text and duplicates multiply. This lecture builds the code-point mental model, the Arabic-specific normalization stack, and the batch importer that fails loudly on a corrupt record instead of quietly poisoning the index.

The theme: **normalize once at ingestion, store verbatim and searchable forms side by side, and never let a bad record through silently.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish code points, code units, and bytes, and predict UTF-8 sizes.
2. Choose the right decoding error policy: `strict` for storage, `replace` only for display.
3. Explain NFC/NFD/NFKC/NFKD and pick the right form for storage vs search.
4. Fold Arabic presentation forms and lam-alef ligatures back to standard letters.
5. Separate diacritics handling for display text vs search keys.
6. Fold Arabic-Indic and Persian digits to ASCII at ingestion.
7. Handle bidirectional runs in mixed Arabic/Latin UI strings.
8. Explain why code-point sort order is wrong for Arabic and what to do instead.
9. Build a bounded-memory batch importer with located, clear failure messages.

---

## Prerequisites

| Need | Where |
|---|---|
| Strings and encoding basics | Phase 1 `basics/10-strings` |
| Generators and iterators | `02-generators-lecture.md` |
| Exceptions and custom errors | `47-exceptions-advanced-lecture.md` |
| Dataclasses | `06-dataclasses-lecture.md` |

---

## 1. Code points, code units, bytes

A Python `str` is a sequence of **code points** (abstract characters), not bytes. `len("سلام") == 4` counts code points. Encoding converts code points to bytes; UTF-8 uses 1 byte for ASCII, 2 for most Arabic, 3 for many CJK, 4 for emoji. The naive `len(text) == len(text.encode("utf-8"))` check only holds for pure ASCII.

```python
word = "سلام"
len(word)  # 4 code points
len(word.encode("utf-8"))  # 8 bytes (2 per Arabic letter)
len("🙂".encode("utf-8"))  # 4 bytes
```

For AI work this matters twice: tokenizers and embedding models consume decoded text (code points), while file sizes, network payloads, and DB column byte limits are measured in bytes. A `VARCHAR(255)` in Postgres holds 255 *characters*; a MySQL `VARCHAR(255)` in an old utf8 charset held 255 *3-byte units* and mangled emoji. Know which layer you are quoting.

**Rule:** decode at the boundary (read as `str` immediately with an explicit encoding), work in `str` everywhere inside the program, encode only at output boundaries.

## 2. Decoding errors: fail loudly, never corrupt silently

When bytes do not decode, Python offers error handlers. `errors="strict"` (the default) raises `UnicodeDecodeError` with the offset and reason. `errors="replace"` substitutes U+FFFD and moves on. `errors="backslashreplace"` is safe for logs.

For **storage and indexing** there is exactly one correct policy: `strict`. A U+FFFD in your index is permanent garbage — search for the original string and it is gone; embeddings of corrupted text cluster wrong. The cost of a caught exception at ingestion is one quarantined record with a line number; the cost of silent corruption is an unexplainable retrieval miss weeks later.

```python
b"\xff\xfe".decode("utf-8")  # UnicodeDecodeError: start, end, reason
b"\xff\xfe".decode("utf-8", errors="replace")  # '\ufffd\ufffd' — hidden damage
```

The companion bug is **mojibake from mismatched assumptions**: UTF-8 bytes decoded as Windows-1256 (legacy Arabic Windows codepage) or Latin-1 produce plausible-looking garbage — Arabic letters that are *wrong* Arabic letters. Detect it at ingestion: a decode that succeeds under a legacy codepage but yields characters in the wrong frequency profile is a red flag. Simplest guard: **declare and verify encodings explicitly** — `open(path, encoding="utf-8")` always, and if a source claims a legacy encoding, convert at the boundary and log the conversion.

Windows Python reads files in the locale encoding (often cp1252/cp1256) when `encoding` is omitted. In a mixed Linux/Windows pipeline that is an automatic mojibake factory. Never omit `encoding=` in code that will run on more than one machine.

**BOM:** some exporters prefix UTF-8 with a byte-order mark (`EF BB BF`). Read those with `encoding="utf-8-sig"`, which strips a BOM if present and is otherwise identical to `utf-8`.

## 3. Normalization forms

Unicode defines several ways to encode "the same" text. The four forms matter only as pairs:

| Form | Meaning | Use |
|---|---|---|
| **NFC** | composed (base+mark fused where possible) | **storage** — canonical, compact |
| **NFD** | decomposed (marks split out) | linguistic processing (tajweed rules, diacritic QA) |
| **NFKC** | NFC + compatibility folding | **search keys** — folds ligatures, presentation forms |
| **NFKD** | NFD + compatibility folding | rarely needed directly |

```python
unicodedata.normalize("NFC", s)  # storage
unicodedata.normalize("NFKC", s)  # search keys
```

Two sources sending "the same" Arabic word may send NFC bytes (base letter + fused mark) or NFD (base, mark, mark). `==` says they differ. Normalize once at ingestion and the problem disappears forever. `unicodedata.is_normalized("NFC", s)` lets you assert a field is already canonical before indexing.

Do **not** normalize inside hot loops repeatedly. Normalize at the boundary, store the result.

## 4. Presentation forms and lam-alef

Old Arabic encodings and many PDF/web exporters emit **presentation forms** (U+FB50–U+FDFF, U+FE70–U+FEFF): pre-shaped glyph variants for positional forms and ligatures. The classic case is the lam-alef ligature: `لا` is two code points in standard text (U+0644 U+0627), but one code point (U+FEFB) in presentation form. Compare raw strings and "the same" phrase never matches.

NFKC folds all of these back to standard letters:

```python
unicodedata.normalize("NFKC", "\ufefb") == "لا"  # True
```

This is why NFKC is the right form for **search keys**: it is the only form that makes legacy-fed text and clean text equal. Keep the original (NFC) text for display and citation; build the search key with NFKC.

## 5. Diacritics: display text vs search keys

Arabic harakat (fatha U+064B, damma, kasra, sukun, shadda, tanwin) and the superscript alef (U+0670) are combining marks layered on base letters. Two consequences:

1. **Search:** users type `محمد` and expect to match `مُحَمَّد`. Strip harakat in the search key; keep them in the stored text.
2. **Storage:** `len` and tokenization behave differently on diacritized text — the display string is longer in code points than the plain one.

The search-key pipeline for Arabic, applied in order:

1. NFKC (fold presentation forms and compatibility variants)
2. strip harakat
3. unify hamza carriers: أ إ آ → ا
4. unify alef maqsura: ى → ي
5. unify ta marbuta: ة → ه (for search only; the display text keeps ة)
6. NFC

Steps 3–5 are the "fuzzy" fold that makes search recall high. They are wrong for *display* — never show a user the folded string. Store `text` (verbatim, NFC) and `search_key` (folded) as separate fields; index embeddings on whichever your retrieval experiments show works better (usually the folded key).

```python
arabic_search_key("مُحَمَّد") == arabic_search_key("محمد")  # True
arabic_search_key("أَحْمَد") == arabic_search_key("احمد")  # True
arabic_search_key("مدرسة") == arabic_search_key("مدرسه")  # True
```

## 6. Digits

Sources mix `٠١٢٣٤٥٦٧٨٩` (Arabic-Indic, U+0660–U+0669), `۰۱۲۳۴۵۶۷۸۹` (Extended/Persian, U+06F0–U+06F9) and ASCII `0123`. Python's `int()` only accepts ASCII digits even though `str.isdigit()` returns True for all three families. Page numbers, volume numbers, and verse numbers arrive in all forms.

Fold at ingestion with a translation table:

```python
DIGIT_FOLD = str.maketrans(
    {0x0660 + i: str(i) for i in range(10)} | {0x06F0 + i: str(i) for i in range(10)}
)
page = int(obj["page"].translate(DIGIT_FOLD))
```

Do this **before** validation, so `page` is always an ASCII string and downstream integer parsing is trivial.

## 7. Bidirectional text

Arabic runs right-to-left; numbers and Latin runs inside it go left-to-right. Python does not reorder strings — the terminal, HTML engine, or UI toolkit does, using the Unicode bidirectional algorithm and a base direction (usually inferred from the first strong character, or declared explicitly in HTML with `dir="rtl"`).

When building mixed strings like `النتيجة: accuracy=0.93 على الاختبار`, wrap the Latin/number run in **bidi isolates** (LRI U+2066 … PDI U+2069) so its direction cannot leak into the Arabic run. This is a display concern only — the underlying code points are correct either way — but an un-isolated number can visually reattach to the wrong Arabic word and produce a *wrong-looking* UI.

`unicodedata.bidirectional(ch)` returns the class (`AL` for Arabic letters, `EN` for digits, `L` for Latin) if you need to reason about runs programmatically.

## 8. Collation

`sorted()` compares code points. In code-point order, hamza carriers (أ U+0623, إ U+0625, آ U+0622) sort *before* ا (U+0627), and ة (U+0629) sorts between ب and ت — both wrong for dictionary order, where أ groups with ا and ة groups with ه. Presentation forms sort in an entirely different range.

For Arabic dictionary collation use a real collation library (PyICU with the `ar` locale). For search keys the normalization fold above is sufficient: after folding, `arabic_search_key("أحمد")` and `arabic_search_key("ابراهيم")` share the leading ا and sort adjacently.

Never ship a user-facing "sort by title" in Arabic using plain `sorted()` and never claim it is alphabetical.

## 9. The batch importer pattern

The mastery target from the skills map: *process a large file with bounded memory and fail with a clear message on a corrupt record*. The shape:

1. **Stream, never slurp.** `for line in fh` is a generator; memory stays O(batch) regardless of file size.
2. **Parse into a validated record** at the boundary. Parse errors become a typed `ImportRecordError` that carries the **line number** and the **reason**.
3. **Normalize inside the parser** (NFC for `text`, folded key for `search_key`, digits folded for `page`) so downstream code never sees raw input.
4. **The caller decides the failure policy** — abort the run, or quarantine the record and continue. The parser never decides silently.
5. **Locate every failure.** `line 123: missing fields: text, page` is actionable; `ValueError` is not.

What "clear message" means in practice: the operator reading the log must be able to fix the source data without running a debugger — record identifier, location, reason, and (for encoding errors) the byte offset.

```python
class ImportRecordError(ValueError):
    def __init__(self, line_no: int, reason: str) -> None:
        super().__init__(f"line {line_no}: {reason}")
        self.line_no = line_no
```

Batches let the next stage (embedding, DB insert) amortize I/O — but the batch is the *unit of work*, not the unit of memory. Never build a list of the whole corpus first "to count it"; count while streaming.

## 10. Best-practice checklist

| Practice | Why |
|---|---|
| `open(..., encoding="utf-8")` everywhere | locale default differs per machine |
| `errors="strict"` on storage paths | U+FFFD in an index is permanent damage |
| NFC at ingestion for stored text | one canonical form ends class of bugs |
| NFKC + fold for search keys | matches what users actually type |
| Keep verbatim text alongside search key | citations must show the original |
| Fold digits before validation | one integer path downstream |
| Wrap Latin/numbers in bidi isolates in mixed UI | correct display order |
| Errors carry line/record location | quarantining beats restarting blind |
| Normalize once at boundary, not in loops | normalization is not free |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `==` between text from two sources fails | normalize both to NFC first |
| Search misses a phrase you can see on screen | build the key with NFKC + harakat strip |
| `int("٣")` raises ValueError | fold digits to ASCII before parsing |
| Mojibake in Windows logs | pass `encoding="utf-8"` explicitly |
| Displayed text shows folded letters (ه instead of ة) | fold only the search key, never display text |
| Sort order looks random to Arabic readers | fold + real collation; never raw `sorted()` |
| Whole corpus in memory | stream with generators and batches |
| Importer logs `ValueError` with no location | custom error carrying line number |

---

## Mastery Check

You can claim this topic when you can:

1. Process a multi-million-line Arabic JSONL corpus with memory that never exceeds a few batches.
2. One corrupt record produces one error naming the line number and reason; valid records are unaffected.
3. Search for `محمد` finds records stored as `مُحَمَّد` and `محمّد`.
4. Two sources that disagree on normalization and digit style deduplicate to one record.
5. You can explain to a colleague why the stored text keeps harakat while the search key strips them.

---

## Next Steps

- Apply the importer pattern to a real corpus in `02-advanced-python/challenges/`.
- Wire the search key into retrieval in `09-genai/09-rag-baseline.py`.
- Review exception design in `47-exceptions-advanced-lecture.md`.
