"""
Arabic NLP â€” 05: Hybrid Search and Reranking
============================================
Topics: lexical + dense arms, reciprocal rank fusion (RRF), reranking,
        and measuring hybrid vs single-arm recall@k.

Why this matters:
    Hybrid search is the production Arabic retrieval pattern. This exercise
    builds both arms from topics 03-04, fuses them with RRF, and proves
    hybrid meets or beats either arm alone.

Run:      python 05-arabic-hybrid-search.py
Verify:   python 05-arabic-hybrid-search.py --verify
"""

from __future__ import annotations

import hashlib
import math
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import unicodedata

PREFIXES = ("Ø§Ù„", "ÙˆØ§Ù„", "Ø¨Ø§Ù„", "ÙƒØ§Ù„", "Ù„Ù„")
DIM = 64


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


def embed(text: str, dim: int = DIM) -> list[float]:
    vec = [0.0] * dim
    for token in normalize_arabic(text).split():
        h = hashlib.sha256(token.encode("utf-8")).digest()
        for i in range(dim):
            vec[i] += (h[i % len(h)] / 255.0) - 0.5
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def lexical_rank(query: str, passages: list[str]) -> list[int]:
    q = set(tokenize(query))
    scored = sorted(
        range(len(passages)),
        key=lambda i: len(q & set(tokenize(passages[i]))),
        reverse=True,
    )
    return scored


def dense_rank(query: str, passages: list[str]) -> list[int]:
    q = embed(query)
    return sorted(
        range(len(passages)), key=lambda i: cosine(q, embed(passages[i])), reverse=True
    )


def rrf(rank_lists: list[list[int]], k: int = 60) -> list[int]:
    scores: dict[int, float] = {}
    for ranks in rank_lists:
        for rank, doc in enumerate(ranks, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)


def recall_at_k(ranked: list[int], relevant: set[int], k: int) -> float:
    top = set(ranked[:k])
    return len(top & relevant) / max(1, len(relevant))


def main() -> None:
    passages = [
        "Ø§Ù„ÙƒØªØ§Ø¨ Ø¹Ù„Ù‰ Ø§Ù„Ù…ÙƒØªØ¨ ÙÙŠ Ø§Ù„Ø¨ÙŠØª",
        "Ø§Ù„Ù…ÙƒØªØ¨Ø© Ù…ÙØªÙˆØ­Ø© Ø§Ù„ÙŠÙˆÙ… Ù„Ù„Ø·Ù„Ø§Ø¨",
        "Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§ Ø¬Ø¯ÙŠØ¯Ø§ Ø¹Ù† Ø§Ù„Ø¹Ù„Ù…",
        "Ø§Ù„Ø¨ÙŠØª ÙƒØ¨ÙŠØ± ÙˆÙˆØ§Ø³Ø¹",
    ]
    relevant = {2}

    lex = lexical_rank("Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§", passages)
    dense = dense_rank("Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§", passages)
    hybrid = rrf([lex, dense])

    r_lex = recall_at_k(lex, relevant, k=2)
    r_dense = recall_at_k(dense, relevant, k=2)
    r_hyb = recall_at_k(hybrid, relevant, k=2)
    print(f"lexical recall@2: {r_lex:.2f}")
    print(f"dense   recall@2: {r_dense:.2f}")
    print(f"hybrid  recall@2: {r_hyb:.2f}")

    assert r_hyb >= r_lex and r_hyb >= r_dense, (
        "hybrid must not underperform either arm"
    )
    assert hybrid[0] == 2, "the writer passage should rank first after fusion"
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
