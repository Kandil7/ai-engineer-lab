"""
Arabic NLP — 02: Normalization and Tokenization
================================================
Topics: normalization pipeline, hamza unification, tatweel removal,
        whitespace vs light-stemming tokenization, recall@k comparison.

Why this matters:
    Normalization decides what "the same" means; tokenization decides what
    the index can match. Both are measured choices, not taste.

Run:      python 02-arabic-normalization-tokenization.py
Verify:   python 02-arabic-normalization-tokenization.py --verify
"""

from __future__ import annotations

import io
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PREFIXES = ("ال", "وال", "بال", "كال", "لل")


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ؤ", "و").replace("ئ", "ي")
    return text


def light_stem(word: str) -> str:
    for p in PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            return word[len(p) :]
    return word


def tokenize_whitespace(text: str) -> list[str]:
    return normalize_arabic(text).split()


def tokenize_light_stem(text: str) -> list[str]:
    return [light_stem(w) for w in tokenize_whitespace(text)]


def recall_at_k(query_tokens: set[str], passages: list[list[str]], k: int) -> float:
    hits = 0
    for tokens in passages:
        if query_tokens & set(tokens):
            hits += 1
    return hits / max(1, min(k, len(passages)))


def main() -> None:
    assert normalize_arabic("أَلْكِتَابُ") == "الكتاب"
    assert normalize_arabic("مُؤْمِن") == "مومن"
    assert light_stem("الكتاب") == "كتاب"
    assert light_stem("والكتاب") == "كتاب"
    assert light_stem("كتاب") == "كتاب"

    corpus = [
        tokenize_whitespace("الكتاب على المكتب"),
        tokenize_whitespace("المكتبة مفتوحة اليوم"),
        tokenize_whitespace("الكاتب يكتب كتابا"),
    ]
    stemmed = [tokenize_light_stem(" ".join(p)) for p in corpus]

    query = {"كتب"}
    r_ws = recall_at_k(query, corpus, k=3)
    r_stem = recall_at_k(query, stemmed, k=3)
    print(f"whitespace recall@3: {r_ws:.2f}")
    print(f"light-stem recall@3: {r_stem:.2f}")
    assert r_stem >= r_ws, "stemming should not hurt recall"
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
