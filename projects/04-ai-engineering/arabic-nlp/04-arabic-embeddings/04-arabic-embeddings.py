"""
Arabic NLP â€” 04: Arabic Embeddings
==================================
Topics: embedding model choice, cosine ranking, dense retrieval, and the
        evaluation protocol that compares the dense arm to the lexical arm.

Why this matters:
    Arabic embedding quality is a measured choice. This exercise builds a
    tiny dense arm with a deterministic hashed embedding (no network, no
    model download) so the protocol is muscle memory before a real model
    is chosen.

Run:      python 04-arabic-embeddings.py
Verify:   python 04-arabic-embeddings.py --verify
"""

from __future__ import annotations

import hashlib
import math
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import unicodedata

DIM = 64


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("Ø£", "Ø§").replace("Ø¥", "Ø§").replace("Ø¢", "Ø§")
    text = text.replace("Ø¤", "Ùˆ").replace("Ø¦", "ÙŠ")
    return text


def embed(text: str, dim: int = DIM) -> list[float]:
    """Deterministic hashed embedding: same text -> same vector."""
    vec = [0.0] * dim
    for token in normalize_arabic(text).split():
        h = hashlib.sha256(token.encode("utf-8")).digest()
        for i in range(dim):
            vec[i] += (h[i % len(h)] / 255.0) - 0.5
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def dense_search(query: str, passages: list[str], k: int) -> list[int]:
    q = embed(query)
    scored = sorted(
        range(len(passages)), key=lambda i: cosine(q, embed(passages[i])), reverse=True
    )
    return scored[:k]


def main() -> None:
    passages = [
        "Ø§Ù„ÙƒØªØ§Ø¨ Ø¹Ù„Ù‰ Ø§Ù„Ù…ÙƒØªØ¨ ÙÙŠ Ø§Ù„Ø¨ÙŠØª",
        "Ø§Ù„Ù…ÙƒØªØ¨Ø© Ù…ÙØªÙˆØ­Ø© Ø§Ù„ÙŠÙˆÙ… Ù„Ù„Ø·Ù„Ø§Ø¨",
        "Ø§Ù„ÙƒØ§ØªØ¨ ÙŠÙƒØªØ¨ ÙƒØªØ§Ø¨Ø§ Ø¬Ø¯ÙŠØ¯Ø§ Ø¹Ù† Ø§Ù„Ø¹Ù„Ù…",
        "Ø§Ù„Ø¨ÙŠØª ÙƒØ¨ÙŠØ± ÙˆÙˆØ§Ø³Ø¹",
    ]

    # Same-token query: dense should find the exact passage.
    top = dense_search("Ø§Ù„ÙƒØªØ§Ø¨", passages, k=1)
    print(f"dense top-1 for 'Ø§Ù„ÙƒØªØ§Ø¨': {top}")
    assert top[0] == 0

    # Paraphrase-ish query: shared token 'Ø§Ù„ÙƒØ§ØªØ¨' should surface passage 2.
    top2 = dense_search("Ø§Ù„ÙƒØ§ØªØ¨", passages, k=1)
    print(f"dense top-1 for 'Ø§Ù„ÙƒØ§ØªØ¨': {top2}")
    assert top2[0] == 2

    # Normalization consistency: diacritized query matches plain passage.
    top3 = dense_search("Ø§Ù„Ù’ÙƒÙØªÙŽØ§Ø¨Ù", passages, k=1)
    print(f"dense top-1 for diacritized 'Ø§Ù„Ù’ÙƒÙØªÙŽØ§Ø¨Ù': {top3}")
    assert top3[0] == 0
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
