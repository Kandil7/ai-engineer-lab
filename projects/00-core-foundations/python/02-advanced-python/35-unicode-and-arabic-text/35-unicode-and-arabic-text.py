"""
Unicode and Arabic Text - Advanced Python Exercises
====================================================
Topics: code points vs bytes, encodings, normalization (NFC/NFKC),
Arabic presentation forms, diacritics (tashkeel), Arabic-Indic digits,
bidirectional text, collation, robust batch text import.

Why this matters for AI engineering:
    An Arabic RAG pipeline (Athar-style) lives or dies on text hygiene.
    The same verse can arrive in 4 different byte encodings, with or
    without diacritics, with lam-alef as one ligature code point or two
    letters, with Arabic-Indic or ASCII digits. If you do not normalize
    at ingestion, search misses documents that ARE there, dedup fails,
    and embeddings for "the same" text differ. This file builds the
    Unicode mental model and the importer pattern that fails LOUDLY on
    a broken record instead of silently corrupting the index.

Environment note:
    Pure standard library (unicodedata). Nothing here crashes on a
    missing dependency.

Run:      python 35-unicode-and-arabic-text.py
Verify:   python 35-unicode-and-arabic-text.py --verify
Reference: https://docs.python.org/3/library/unicodedata.html
"""

from __future__ import annotations

import sys
import tempfile
import unicodedata

# Windows consoles default to a legacy codepage (cp1252/cp1256) that cannot
# encode Arabic. A Unicode lesson must fix its own output boundary first.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    _reconfigure(encoding="utf-8", errors="replace")
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

# ============================================================
# 1. Code points vs bytes - the foundational distinction
# ============================================================
# A Python str is a sequence of CODE POINTS (numbers), not bytes.
# Encoding is the translation from code points to bytes. Every "mojibake"
# bug is an encoding step done wrong or assumed.

print("=" * 60)
print("1. Code points vs bytes")
print("=" * 60)

word = "سلام"  # salaam - peace
print(f"str:      {word!r}")
print(f"len(str): {len(word)} characters")
for ch in word:
    print(f"  {ch}  U+{ord(ch):04X}  {unicodedata.name(ch, '?')}")

utf8_bytes = word.encode("utf-8")
print(f"utf-8 bytes: {utf8_bytes!r}  ({len(utf8_bytes)} bytes)")
# Arabic letters encode to 2 bytes each in UTF-8; ASCII to 1; emoji to 4.
print(f"emoji '🙂' encodes to {len('🙂'.encode('utf-8'))} bytes")
print()

# ============================================================
# 2. Encoding and decoding - and why silent failure is the enemy
# ============================================================
# decode(errors="strict") raises UnicodeDecodeError: GOOD. A clear error
# at ingestion beats U+FFFD replacement characters polluting your index.
# errors="replace" hides corruption; use it only for display, never for
# data you will store or search.

print("=" * 60)
print("2. Encoding errors: fail loudly vs corrupt silently")
print("=" * 60)

# Real mojibake: UTF-8 bytes of "سلام" decoded as Windows-1256 (Arabic Windows)
good_bytes = "سلام".encode("utf-8")
mojibake = good_bytes.decode("windows-1256")
print(f"correct decode : {'سلام'}")
print(f"mojibake       : {mojibake!r}   <- what cp1256 sees")

try:
    b"\xff\xfe invalid".decode("utf-8")  # type: ignore[union-attr]
except UnicodeDecodeError as exc:
    print(f"strict decode  : raises UnicodeDecodeError: {exc}")
    print(f"  start={exc.start} end={exc.end} reason={exc.reason}")

print(f"replace decode : {b'\xff\xfe'.decode('utf-8', errors='replace')!r}")
print("  -> U+FFFD garbage. Never store this. Fail and quarantine instead.")
print()

# ============================================================
# 3. Normalization - the same text, four encodings
# ============================================================
# Unicode defines equivalence classes. NFC composes, NFD decomposes,
# NFKC/NFKD also fold compatibility forms (ligatures, presentation forms).
# Rule: normalize ONCE at ingestion (NFC for storage, NFKC for search keys)
# and never compare raw strings from different sources.

print("=" * 60)
print("3. Normalization forms")
print("=" * 60)

s_decomposed = "مُحَمَّد"  # already composed here, but sources differ
nfc = unicodedata.normalize("NFC", s_decomposed)
nfd = unicodedata.normalize("NFD", s_decomposed)
print(f"NFC == NFD? {nfc == nfd}  (same text, different code point order)")
print(f"NFC len={len(nfc)}, NFD len={len(nfd)}  (NFD splits base+mark)")
print(f"is_normalized NFC: {unicodedata.is_normalized('NFC', nfc)}")
print()

# ============================================================
# 4. Arabic presentation forms - the legacy-encoding trap
# ============================================================
# Old Arabic encodings (and some PDFs/websites) emit PRESENTATION FORMS
# (U+FB50-U+FDFF, U+FE70-U+FEFF): pre-shaped ligature glyphs like the
# lam-alef ligature. NFKC folds them back to standard letters.

print("=" * 60)
print("4. Presentation forms and lam-alef")
print("=" * 60)

lam_alef_standard = "لا"  # U+0644 U+0627 (two code points)
lam_alef_presentation = "\ufefb"  # LAM WITH ALEF ISOLATED FORM (one code point)
print(f"standard     : {lam_alef_standard!r} len={len(lam_alef_standard)}")
print(f"presentation : {lam_alef_presentation!r} len={len(lam_alef_presentation)}")
print(f"equal?       : {lam_alef_standard == lam_alef_presentation}")
folded = unicodedata.normalize("NFKC", lam_alef_presentation)
print(f"NFKC folded  : {folded!r}  equal now: {folded == lam_alef_standard}")
print()

# ============================================================
# 5. Diacritics (tashkeel) - search key vs display text
# ============================================================
# Harakat U+064B-U+0652 (fatha, damma, kasra, sukun, shadda, tanwin) and
# the superscript alef U+0670 are MARKS layered on base letters. For
# search you strip them; for display and for tajweed-aware use you keep
# them. Store both: display_text (verbatim) and search_key (normalized).

HARAKAT = set(range(0x064B, 0x0653)) | {0x0670}


def strip_harakat(text: str) -> str:
    """Remove Arabic diacritics, keep base letters."""
    return "".join(ch for ch in text if ord(ch) not in HARAKAT)


def arabic_search_key(text: str) -> str:
    """Canonical key for Arabic search/dedup.

    Steps: NFKC (fold presentation forms) -> strip harakat ->
    unify hamza carriers (أ إ آ -> ا) -> unify alef maqsura (ى -> ي) ->
    unify ta marbuta (ة -> ه) -> NFC.
    """
    text = unicodedata.normalize("NFKC", text)
    text = strip_harakat(text)
    text = text.replace("\u0623", "\u0627").replace("\u0625", "\u0627")
    text = text.replace("\u0622", "\u0627")
    text = text.replace("\u0649", "\u064a")
    text = text.replace("\u0629", "\u0647")
    return unicodedata.normalize("NFC", text)


print("=" * 60)
print("5. Diacritics: display vs search")
print("=" * 60)

diacritized = "مُحَمَّد"
plain = "محمد"
print(f"diacritized : {diacritized!r} (len={len(diacritized)})")
print(f"stripped    : {strip_harakat(diacritized)!r}")
print(f"search hit  : {arabic_search_key(diacritized) == arabic_search_key(plain)}")
print(f"raw compare : {diacritized == plain}  <- why raw comparison fails")
print()

# ============================================================
# 6. Arabic-Indic digits - page numbers and verse numbers
# ============================================================
# Sources mix ٠١٢٣ (U+0660-U+0669), ۰۱۲۳ (Persian U+06F0-U+06F9) and
# 0123. int() rejects Arabic-Indic digits; isdigit() accepts them. Fold
# everything to ASCII at ingestion.

ARABIC_INDIC = {0x0660 + i: str(i) for i in range(10)}
EXTENDED_ARABIC_INDIC = {0x06F0 + i: str(i) for i in range(10)}
DIGIT_FOLD = str.maketrans({**ARABIC_INDIC, **EXTENDED_ARABIC_INDIC})


def fold_digits(text: str) -> str:
    """Map Arabic-Indic and Persian digits to ASCII digits."""
    return text.translate(DIGIT_FOLD)


print("=" * 60)
print("6. Digit folding")
print("=" * 60)

page_ar = "صفحة ١٢٣"
page_fa = "صفحه ۴۵۶"
print(f"{page_ar!r} -> {fold_digits(page_ar)!r}")
print(f"{page_fa!r} -> {fold_digits(page_fa)!r}")
print(f"int('٣') raises: ", end="")
try:
    int("٣")
except ValueError as exc:
    print(f"ValueError: {exc}")
print(f"after fold  : int('٣'.translate(DIGIT_FOLD)) = {int('٣'.translate(DIGIT_FOLD))}")
print()

# ============================================================
# 7. Bidirectional text - base direction matters
# ============================================================
# Arabic runs right-to-left but embeds numbers/Latin left-to-right.
# Python does not reorder for you: the terminal/HTML renderer does,
# using the FIRST strong character or an explicit base direction.
# When mixing Arabic with Latin/numbers in UI strings, wrap with
# Unicode bidi isolates (U+2066..U+2069) to stop the run from leaking.

print("=" * 60)
print("7. Bidirectional classes")
print("=" * 60)

for ch in "لا3A":
    print(f"  {ch}  U+{ord(ch):04X}  bidi={unicodedata.bidirectional(ch)}")

LRI, PDI = "\u2066", "\u2069"
mixed = f"النتيجة: {LRI}accuracy=0.93{PDI} على الاختبار"
print(f"isolated mixed string: {mixed}")
print()

# ============================================================
# 8. Collation - code point order is NOT alphabetical order
# ============================================================
# sorted() uses code points. Hamza carriers (أ إ آ) sort BEFORE ا and
# ta marbuta (ة) sorts between ب and ت, both wrong for Arabic
# dictionaries. For real collation use a locale library (PyICU); for
# search keys the normalization above is enough.

print("=" * 60)
print("8. Sorting Arabic")
print("=" * 60)

names = ["أحمد", "ابراهيم", "بلال", "ثابت"]
print(f"code point sort : {sorted(names)}")
print(f"search-key sort : {sorted(names, key=arabic_search_key)}")
print("  (أحمد and ابراهيم now group under ا, as a dictionary would)")
print()

# ============================================================
# 9. The batch importer - bounded memory, loud failure
# ============================================================
# Mastery criterion from the skills map: read a large Arabic corpus in
# batches with bounded memory, and fail with a CLEAR message on a broken
# record (bad encoding, missing field) instead of corrupting the index.


@dataclass
class TextRecord:
    record_id: str
    book: str
    page: int
    text: str
    search_key: str


class ImportRecordError(ValueError):
    """A record is structurally broken; carries its location for the log."""

    def __init__(self, line_no: int, reason: str) -> None:
        super().__init__(f"line {line_no}: {reason}")
        self.line_no = line_no


def parse_record(line: str, line_no: int) -> TextRecord:
    """Parse one JSONL line into a normalized TextRecord."""
    import json

    try:
        obj = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ImportRecordError(line_no, f"invalid JSON: {exc.msg}") from exc
    if not isinstance(obj, dict):
        raise ImportRecordError(line_no, f"expected object, got {type(obj).__name__}")
    missing = [k for k in ("id", "book", "page", "text") if k not in obj]
    if missing:
        raise ImportRecordError(line_no, f"missing fields: {', '.join(missing)}")
    text = obj["text"]
    if not isinstance(text, str) or not text.strip():
        raise ImportRecordError(line_no, "text is empty or not a string")
    try:
        page = int(fold_digits(str(obj["page"])))
    except ValueError as exc:
        raise ImportRecordError(line_no, f"page not an integer: {obj['page']!r}") from exc
    return TextRecord(
        record_id=str(obj["id"]),
        book=str(obj["book"]),
        page=page,
        text=unicodedata.normalize("NFC", text),
        search_key=arabic_search_key(text),
    )


def read_batches(
    path: Path, batch_size: int = 100, on_error: object | None = None
) -> Iterator[tuple[int, list[TextRecord]]]:
    """Yield (start_line, batch) reading the file lazily, line by line.

    Memory stays O(batch_size) regardless of file size. Failure policy:
      on_error=None (default) -> a broken record raises ImportRecordError
                                 (fail loudly, abort the run).
      on_error=callable       -> the callable receives the error and the
                                 record is skipped (quarantine policy).
    """
    batch: list[TextRecord] = []
    start_line = 1
    with open(path, encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                batch.append(parse_record(line, line_no))
            except ImportRecordError as exc:
                if on_error is None:
                    raise
                on_error(exc)  # type: ignore[operator]
                continue
            if len(batch) >= batch_size:
                yield start_line, batch
                batch = []
                start_line = line_no + 1
    if batch:
        yield start_line, batch


def demo_importer() -> None:
    """Import a synthetic corpus in batches; quarantine one broken record."""
    import json
    import tempfile

    records = [
        {"id": str(i), "book": "كتاب الأصول", "page": i, "text": f"نص عربي رقم {i} ۞"}
        for i in range(1, 251)
    ]
    records[122] = {"id": "123", "book": "كتاب الأصول"}  # broken: no text/page
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "corpus.jsonl"
        with open(path, "w", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

        imported = 0
        quarantined: list[str] = []
        for _start_line, batch in read_batches(
            path, batch_size=50, on_error=lambda e: quarantined.append(str(e))
        ):
            imported += len(batch)
        print(f"  batches imported : {imported} records (memory = one batch)")
        print(f"  quarantined      : {quarantined}")
        # second pass: default fail-loud policy aborts the run at the bad line
        aborted: list[str] = []
        try:
            for _s, _b in read_batches(path, batch_size=50):
                pass
        except ImportRecordError as exc:
            aborted.append(str(exc))
        print(f"  fail-loud abort  : {aborted}")
        assert imported == 249, "one broken record must be excluded"
        assert len(quarantined) == 1 and "line 123" in quarantined[0]
        assert len(aborted) == 1 and "line 123" in aborted[0]
        print("  [ok] bounded-memory import with loud, located failure")


print("=" * 60)
print("9. Batch importer demo")
print("=" * 60)
demo_importer()
print()

# ============================================================
# 10. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = [
        (
            "lam-alef presentation folds to standard",
            unicodedata.normalize("NFKC", "\ufefb") == "لا",
        ),
        ("harakat stripped", strip_harakat("مُحَمَّد") == "محمد"),
        (
            "search key unifies hamza/maqsura/ta-marbuta",
            arabic_search_key("أَحْمَد") == arabic_search_key("احمد")
            and arabic_search_key("على") == arabic_search_key("علي")
            and arabic_search_key("مدرسة") == arabic_search_key("مدرسه"),
        ),
        ("digits fold", fold_digits("١٢٣٤٥") == "12345" and fold_digits("۴۵") == "45"),
        ("NFC idempotent", unicodedata.normalize("NFC", "سلام") == "سلام"),
        (
            "bidi classes present",
            unicodedata.bidirectional("ا") == "AL" and unicodedata.bidirectional("3") == "EN",
        ),
        ("importer fails loudly", _importer_fails_loudly()),
    ]
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


def _importer_fails_loudly() -> bool:
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bad.jsonl"
        path.write_text(
            json.dumps({"id": "1", "book": "b", "page": 1, "text": "نص"}, ensure_ascii=False)
            + "\n"
            + "{not json}\n",
            encoding="utf-8",
        )
        try:
            list(read_batches(path))
        except ImportRecordError as exc:
            return "line 2" in str(exc) and "invalid JSON" in str(exc)
        return False


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("=" * 60)
    print("Verification (python 35-unicode-and-arabic-text.py --verify):")
    _verify()
