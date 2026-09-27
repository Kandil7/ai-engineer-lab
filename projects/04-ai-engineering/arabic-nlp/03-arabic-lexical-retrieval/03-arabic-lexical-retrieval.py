"""
Arabic NLP â€” 03: Lexical Retrieval (BM25 and Inverted Index)
=============================================================
Topics: inverted index, BM25 scoring, Arabic normalization inside the
        index, recall@k measurement and stage diagnosis.

Why this matters:
    Lexical search is the first arm of hybrid retrieval. It matches exact
    terms and names that embeddings blur â€” and it inherits the quality of
    the normalization and tokenization pipeline.

Run:      python 03-arabic-lexical-retrieval.py
Verify:   python 03-arabic-lexical-retrieval.py --verify
"""

from __future__ import annotations

import math
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import unicodedata
from collections import defaultdict

PREFIXES = ("Ø§Ù„", "ÙˆØ§Ù„", "Ø¨Ø§Ù„", "ÙƒØ§Ù„", "Ù„Ù„")


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("Ø£", "Ø§").replace("Ø¥", "Ø§").replace("Ø¢", "Ø§")
    text = text.replace("Ø¤", "Ùˆ").replace("Ø¦", "ÙŠ")
    return text


def light_stem(word: str) -> str:
    for p in PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            return word[len(p) :]
    return word


def tokenize(text: str) -> list[str]:
    return [light_stem(w) for w in normalize_arabic(text).split()]


def build_index(passages: list[str]) -> tuple[dict[str, list[int]], dict[str, int]]:
    index: dict[str, list[int]] = defaultdict(list)
    df: dict[str, int] = defaultdict(int)
    for doc_id, text in enumerate(passages):
        for term in set(tokenize(text)):
            index[term].append(doc_id)
            df[term] += 1
    return dict(index), dict(df)


def bm25(
    query: str,
    passages: list[str],
    index: dict,
    df: dict,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[tuple[int, float]]:
    N = len(passages)
    avg_len = sum(len(tokenize(p)) for p in passages) / max(1, N)
    q_terms = tokenize(query)
    scores: list[float] = [0.0] * N
    for doc_id, text in enumerate(passages):
        doc_terms = tokenize(text)
        doc_len = len(doc_terms)
        for term in q_terms:
            tf = doc_terms.count(term)
            if tf == 0:
                continue
            idf = math.log(1 + (N - df.get(term, 0) + 0.5) / (df.get(term, 0) + 0.5))
            tf_norm = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_len / avg_len))
            scores[doc_id] += idf * tf_norm
    ranked = sorted(range(N), key=lambda i: scores[i], reverse=True)
    return [(i, scores[i]) for i in ranked]


def recall_at_k(query: str, passages: list[str], relevant: set[int], k: int) -> float:
    ranked = bm25(query, passages, *build_index(passages))
    top = {doc_id for doc_id, _ in ranked[:k]}
    return len(top & relevant) / max(1, len(relevant))


def main() -> None:
    passages = [
        "Ø§Ù„ÙƒØªØ§Ø¨ Ø¹Ù„Ù‰ Ø§Ù„Ù…ÙƒØªØ¨ ÙÙŠ Ø§Ù„Ø¨ÙŠØª",
        "Ø§Ù„Ù…ÙƒØªØ¨Ø© Ù…ÙØªÙˆØ­Ø© Ø§Ù„ÙŠÙˆÙ… Ù„Ù„Ø·Ù„Ø§Ø¨",
        "Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§ Ø¬Ø¯ÙŠØ¯Ø§ Ø¹Ù† Ø§Ù„Ø¹Ù„Ù…",
        "Ø§Ù„Ø¨ÙŠØª ÙƒØ¨ÙŠØ± ÙˆÙˆØ§Ø³Ø¹",
    ]
    relevant = {2}  # the passage about the writer writing a book

    r = recall_at_k("Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§", passages, relevant, k=2)
    print(f"recall@2 for 'Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§': {r:.2f}")
    assert r == 1.0, "normalized+stemmed index should retrieve the writer passage"

    ranked = bm25("Ø§Ù„ÙƒØªØ§Ø¨", passages, *build_index(passages))
    top_doc = ranked[0][0]
    print(f"top doc for 'Ø§Ù„ÙƒØªØ§Ø¨': {top_doc}")
    assert top_doc == 0, "the book-on-desk passage should rank first"
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
