"""
Arabic NLP — 01: Arabic Text Fundamentals
==========================================
Topics: script, Unicode normalization (NFC/NFD), diacritic stripping,
        encoding round-trip, the two-text discipline.

Why this matters:
    Every Arabic retrieval failure traces to a text-handling bug: mojibake
    from a wrong encoding, diacritics breaking exact matches, or
    normalization altering the quote the user sees. This exercise builds
    the primitives and proves them with asserts.

Run:      python 01-arabic-text-fundamentals.py
Verify:   python 01-arabic-text-fundamentals.py --verify
"""

from __future__ import annotations

import io
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SAMPLE = "قالَ اللهُ تعالى في كتابه العزيز"
DIACRITIC = "\u064e"  # fatha


def strip_tashkeel(text: str) -> str:
    """Remove combining marks (diacritics) from Arabic text."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def normalize_nfc(text: str) -> str:
    """Compose to NFC for consistent storage."""
    return unicodedata.normalize("NFC", text)


def roundtrip_utf8(text: str) -> bool:
    """Encode then decode UTF-8; True if the text survives intact."""
    return text.encode("utf-8").decode("utf-8") == text


def is_arabic(text: str) -> bool:
    """True if the text contains Arabic-script characters (U+0600-U+06FF)."""
    return any("\u0600" <= c <= "\u06ff" for c in text)


def main() -> None:
    stripped = strip_tashkeel(SAMPLE)
    print(f"original: {SAMPLE}")
    print(f"stripped: {stripped}")

    assert strip_tashkeel("كَتَبَ") == "كتب"
    assert normalize_nfc("كَتَبَ") == "كَتَبَ"
    assert roundtrip_utf8(SAMPLE)
    assert is_arabic(SAMPLE)
    assert not is_arabic("hello")
    assert unicodedata.category(DIACRITIC) == "Mn"
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
