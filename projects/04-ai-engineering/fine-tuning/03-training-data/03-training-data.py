"""
Fine-Tuning — 03: Training Data Preparation
============================================
Topics: quality filtering, deduplication, and the train/eval split.

Why this matters:
    The instruction set decides what the model learns. This exercise
    cleans, deduplicates, and splits a small instruction set.

Run:      python 03-training-data.py
Verify:   python 03-training-data.py --verify
"""

from __future__ import annotations

import sys


def dedupe(examples: list[dict]) -> list[dict]:
    """Remove exact duplicates by normalized instruction."""
    seen: set[str] = set()
    out = []
    for ex in examples:
        key = ex["instruction"].strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(ex)
    return out


def split(examples: list[dict], eval_frac: float) -> tuple[list[dict], list[dict]]:
    """Split by example (not by topic) into train and eval."""
    n_eval = max(1, round(len(examples) * eval_frac))
    return examples[n_eval:], examples[:n_eval]


def main() -> None:
    examples = [
        {"instruction": "ما حكم الصلاة في السفر؟", "answer": "القصر جائز"},
        {"instruction": "ما حكم الصلاة في السفر؟", "answer": "القصر جائز"},  # duplicate
        {"instruction": "ما حكم الجمع بين الصلاتين؟", "answer": "جائز في السفر"},
        {"instruction": "ما حكم صيام رمضان؟", "answer": "فرض على المسلم"},
    ]

    cleaned = dedupe(examples)
    assert len(cleaned) == 3, "exact duplicate removed"

    train, eval_set = split(cleaned, 0.33)
    assert len(eval_set) == 1, "one held-out example"
    assert len(train) == 2
    assert not any(e in train for e in eval_set), "no eval leakage into train"

    # The split is by example: the eval set represents the same distribution.
    assert all("حكم" in e["instruction"] for e in eval_set)

    print(f"deduplicated: {len(examples)} -> {len(cleaned)} examples")
    print(f"split: {len(train)} train, {len(eval_set)} eval, no leakage")
    print("the eval set represents the same distribution as training")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
