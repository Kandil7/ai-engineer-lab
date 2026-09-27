"""
Applied ML — 04: Rules vs Models and Error Analysis
====================================================
Topics: the rule baseline, the rules-vs-model decision, and the error
        analysis loop.

Why this matters:
    Not every problem needs a model. This exercise builds a rule baseline,
    compares it to a model, and runs the error analysis loop on failures.

Run:      python 04-rules-vs-models-error-analysis.py
Verify:   python 04-rules-vs-models-error-analysis.py --verify
"""

from __future__ import annotations

import sys

try:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HOW_WORDS = {"كيف", "ما هو", "لماذا", "كيفية"}
WHO_WORDS = {"من", "أين", "متى"}


def rule_classify(q: str) -> str:
    """Keyword rule baseline for question-type classification."""
    if any(w in q for w in HOW_WORDS):
        return "how"
    if any(w in q for w in WHO_WORDS):
        return "who"
    return "other"


def model_classify(q: str) -> str:
    """A 'model' that is deliberately worse than the rule on this data:
    it only catches 'كيف' and misses the other how-words."""
    if "كيف" in q:
        return "how"
    return "other"


def precision_recall(
    preds: list[str], actuals: list[str], cls: str
) -> tuple[float, float]:
    tp = sum(1 for p, a in zip(preds, actuals) if p == cls and a == cls)
    fp = sum(1 for p, a in zip(preds, actuals) if p == cls and a != cls)
    fn = sum(1 for p, a in zip(preds, actuals) if p != cls and a == cls)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r


def main() -> None:
    questions = [
        "كيف أتعلم البرمجة",  # how
        "ما هو الذكاء الاصطناعي",  # how
        "لماذا السماء زرقاء",  # how
        "من هو العالم",  # who
        "أين تقع القاهرة",  # who
        "متى بدأت الحرب",  # who
    ]
    actuals = ["how", "how", "how", "who", "who", "who"]

    rule_preds = [rule_classify(q) for q in questions]
    model_preds = [model_classify(q) for q in questions]

    rule_p, rule_r = precision_recall(rule_preds, actuals, "how")
    model_p, model_r = precision_recall(model_preds, actuals, "how")

    # The rule beats the model on recall: it catches all how-words.
    assert rule_r > model_r, "the rule catches more how-questions"
    assert rule_p >= model_p

    # Error analysis: the model's HOW-class failures cluster on the missed
    # how-words ('ما هو', 'لماذا'). The who-questions are a separate cluster.
    how_failures = [
        q for q, p, a in zip(questions, model_preds, actuals) if p != a and a == "how"
    ]
    assert all(any(w in f for w in ["ما هو", "لماذا"]) for f in how_failures), (
        "how-class failures cluster on the missed how-words"
    )
    assert how_failures == ["ما هو الذكاء الاصطناعي", "لماذا السماء زرقاء"]

    print(f"rule:  precision={rule_p:.2f} recall={rule_r:.2f}")
    print(f"model: precision={model_p:.2f} recall={model_r:.2f}")
    print(f"model how-class failures cluster on: {how_failures}")
    print(
        "conclusion: the rule is better here — the model is not earning its complexity"
    )
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
