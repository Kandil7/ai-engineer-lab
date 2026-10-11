"""
GenAI - 18: Caching and Cost
============================
Topics: exact and semantic caching, prompt caching, batching, model
routing by task difficulty, cost per conversation, measured savings.

Why this matters for AI/backend engineering:
    LLM bills scale with tokens, and most production traffic is
    repeated questions. Caching turns repeat queries into cache hits,
    routing sends easy tasks to cheap models, and both are measurable
    savings - the unit an engineer can report.

Run:      python 18-caching-and-cost.py
Verify:   python 18-caching-and-cost.py --verify
Reference: https://platform.openai.com/docs/guides/prompt-caching
"""

from __future__ import annotations

import math
import sys
import zlib
from dataclasses import dataclass, field


# ============================================================
# 1. Exact Cache
# ============================================================
# Identical questions get identical answers, stored in a dict.


class ExactCache:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> str | None:
        if key in self._store:
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return None

    def put(self, key: str, value: str) -> None:
        self._store[key] = value

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


# Example 1: exact caching
cache = ExactCache()
cache.put("what is python?", "a language")
cache.get("what is python?")
cache.get("what is python?")
cache.get("what is rust?")
print("Example 1: exact cache")
print(f"  hit rate: {cache.hit_rate():.0%}")
assert cache.hit_rate() == 2 / 3

# ============================================================
# 2. Semantic Cache
# ============================================================
# Similar questions should also hit. Embed both sides and match on
# cosine similarity above a threshold.


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def toy_embed(text: str, dim: int = 32) -> list[float]:
    """Word-level bag embedding - distinct topics get distinct vectors."""
    vec = [0.0] * dim
    for word in text.lower().split():
        vec[zlib.crc32(word.encode("utf-8")) % dim] += 1.0
    return vec


class SemanticCache:
    def __init__(self, threshold: float = 0.3) -> None:
        # Word-bag embedding: synonyms don't overlap, so the threshold can
        # be low (related questions share multiple words). A production
        # system would use a real embedding model with a higher bar.
        self._entries: list[tuple[list[float], str]] = []
        self.threshold = threshold
        self.hits = 0
        self.misses = 0

    def get(self, query: str) -> str | None:
        qv = toy_embed(query)
        for vec, answer in self._entries:
            if cosine_similarity(qv, vec) >= self.threshold:
                self.hits += 1
                return answer
        self.misses += 1
        return None

    def put(self, query: str, answer: str) -> None:
        self._entries.append((toy_embed(query), answer))


# Example 2: semantic cache
scache = SemanticCache(threshold=0.4)
scache.put("how do I reset my password?", "go to settings")
hit = scache.get("how to reset password?")
print("\nExample 2: semantic cache")
print(f"  similar question -> {'HIT: ' + hit if hit else 'miss'}")
assert hit == "go to settings"

# ============================================================
# 3. Model Routing by Task Difficulty
# ============================================================
# Easy tasks go to a cheap model; hard tasks to an expensive one.
# Routing halves the average cost without losing quality.


@dataclass
class Router:
    easy_model: str = "haiku"
    hard_model: str = "opus"
    easy_cost: float = 0.25  # $/1M tokens
    hard_cost: float = 15.0  # $/1M tokens
    easy_cutoff: float = 0.5  # difficulty threshold

    def route(self, difficulty: float) -> str:
        return self.easy_model if difficulty <= self.easy_cutoff else self.hard_model

    def call_cost(self, difficulty: float, tokens: int) -> float:
        price = self.easy_cost if self.route(difficulty) == self.easy_model else self.hard_cost
        return tokens / 1_000_000 * price


# Example 3: routing economics
router = Router()
print("\nExample 3: model routing")
print(f"  difficulty 0.2 -> {router.route(0.2)}  (${router.call_cost(0.2, 1000):.5f})")
print(f"  difficulty 0.9 -> {router.route(0.9)}  (${router.call_cost(0.9, 1000):.4f})")
assert router.route(0.2) == "haiku" and router.route(0.9) == "opus"

# ============================================================
# 4. Prompt Caching (System Prompt Prefixes)
# ============================================================
# Long stable prefixes (system prompt + instructions) can be cached by
# the provider: repeated prefix tokens are billed at a discount.


def prefix_cache_cost(
    system_tokens: int, total_tokens: int, price: float, cache_discount: float = 0.5
) -> float:
    """Cost with the stable prefix charged at a discount."""
    uncached = total_tokens - system_tokens
    return (system_tokens * price * cache_discount + uncached * price) / 1_000_000


# Example 4: prompt caching savings
full = prefix_cache_cost(20_000, 30_000, 3.0, cache_discount=0.5)
no_cache = 30_000 / 1_000_000 * 3.0
print("\nExample 4: prompt caching")
print(f"  with prefix cache: ${full:.3f} vs without: ${no_cache:.3f}")
assert full < no_cache, "cached prefix costs less"


# ============================================================
# 5. Cost Per Conversation
# ============================================================
@dataclass
class ConversationBudget:
    turns: int
    tokens_per_turn: int
    price: float
    cache: ExactCache = field(default_factory=ExactCache)

    def estimated_cost(self) -> float:
        return self.turns * self.tokens_per_turn / 1_000_000 * self.price

    def cost_with_cache(self, repeat_fraction: float) -> float:
        fresh = (1 - repeat_fraction) * self.estimated_cost()
        cached = repeat_fraction * self.estimated_cost() * 0.1  # cache hit ~10% of cost
        return fresh + cached


# Example 5: conversation cost with cache
budget = ConversationBudget(turns=20, tokens_per_turn=1500, price=3.0)
base = budget.estimated_cost()
with_cache = budget.cost_with_cache(repeat_fraction=0.4)
print("\nExample 5: cost per conversation")
print(f"  no cache: ${base:.3f}  |  40% repeat traffic + cache: ${with_cache:.3f}")
assert with_cache < base, "cache cuts conversation cost"


# ============================================================
# Production Pattern
# ============================================================
def estimate_monthly_savings(queries_per_day: int, cost_per_query: float, hit_rate: float) -> float:
    """Dollar savings from caching over a month."""
    return queries_per_day * 30 * cost_per_query * hit_rate


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: caching per-user answers globally (PII cross-bleed)
# MISTAKE: exact-only cache - similar questions miss
# MISTAKE: routing every task to the big model "to be safe"
# MISTAKE: no hit-rate metric - cache exists but nobody knows if it works


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    c = ExactCache()
    c.put("a", "1")
    assert c.get("a") == "1" and c.get("b") is None
    assert c.hit_rate() == 0.5

    s = SemanticCache(threshold=0.5)
    s.put("reset my password", "settings")
    assert s.get("reset the password") == "settings", "similar query hits"
    assert s.get("what is the weather") is None, "unrelated misses"

    r = Router(easy_cost=1.0, hard_cost=10.0)
    assert r.route(0.1) == "haiku" and r.route(0.9) == "opus"
    assert r.call_cost(0.1, 1000) == 0.001
    assert r.call_cost(0.9, 1000) == 0.01

    assert prefix_cache_cost(10_000, 20_000, 10.0, 0.5) < 20_000 / 1e6 * 10.0

    b = ConversationBudget(10, 1000, 1.0)
    assert abs(b.estimated_cost() - 0.01) < 1e-9
    assert b.cost_with_cache(0.5) < b.estimated_cost()

    assert estimate_monthly_savings(1000, 0.001, 0.3) == 1000 * 30 * 0.001 * 0.3
    print("[OK] 18-caching-and-cost: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Exact + semantic caches turn repeat traffic into hits.")
        print("2. Route easy tasks to cheap models.")
        print("3. Prompt caching discounts stable prefixes; measure savings.")
        _verify()
