"""
Applied ML — 05: Baseline Intent Classifier
==========================================
Topics: the non-LLM baseline exit artifact — a rule baseline, a small learned
        model, a leakage-aware split, and an error report.

Why this matters:
    The roadmap's ML exit test is an Arabic intent classifier with a non-LLM
    baseline, a correct (leakage-free) split, and an error report. This script
    is that artifact: it compares a keyword rule against a tiny Naive Bayes
    model on a source-split dataset and prints per-class metrics and the
    misclassifications.

Run:      python 05-baseline-intent-classifier.py
Verify:   python 05-baseline-intent-classifier.py --verify
"""

from __future__ import annotations

import math
import sys
from collections import Counter, defaultdict

_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    _reconfigure(encoding="utf-8", errors="replace")

LABELS = ("how", "who", "other")

# Two rules: a cheap keyword baseline. The model must beat the majority baseline.
RULES: dict[str, tuple[str, ...]] = {
    "how": ("كيف", "كيفية", "ما هو", "ما هي", "لماذا"),
    "who": ("من هو", "من هي", "أين", "متى", "من "),
}


# ── the dataset (text, label, source) ───────────────────────────────
# `source` is the group key: the split must not put one source on both sides.
DATASET: list[tuple[str, str, str]] = [
    ("كيف أتعلم البرمجة", "how", "s1"),
    ("من هو الخوارزمي", "who", "s1"),
    ("اكتب دالة بايثون", "other", "s1"),
    ("ما هو الذكاء الاصطناعي", "how", "s1"),
    ("كيفية عمل المحرك", "how", "s2"),
    ("أين تقع القاهرة", "who", "s2"),
    ("لخص هذا النص", "other", "s2"),
    ("لماذا السماء زرقاء", "how", "s2"),
    ("ما هي عاصمة مصر", "how", "s3"),
    ("متى بدأت الحرب العالمية", "who", "s3"),
    ("ترجم الجملة التالية", "other", "s3"),
    ("كيف أحسب النسبة المئوية", "how", "s3"),
    ("من هي ماري كوري", "who", "s4"),
    ("أعطني مثالا على الفلترة", "other", "s4"),
    ("ما هو التعلم العميق", "how", "s4"),
    ("من هو مؤسس الشركة", "who", "s4"),
    ("أصلح هذا الخطأ في الكود", "other", "s5"),
    ("كيف أكتب اختبارا", "how", "s5"),
    ("من هو ابن سينا", "who", "s5"),
    ("أين أجد الملف", "who", "s5"),
]


def rule_classify(text: str) -> str:
    """The keyword baseline."""
    for label, words in RULES.items():
        if any(w in text for w in words):
            return label
    return "other"


def split_by_source(
    rows: list[tuple[str, str, str]], train_frac: float = 0.6
) -> tuple[list, list]:
    """Split by source so no source straddles the boundary (no group leakage)."""
    sources = sorted({src for _, _, src in rows})
    cut = max(1, int(train_frac * len(sources)))
    train_sources = set(sources[:cut])
    train = [r for r in rows if r[2] in train_sources]
    test = [r for r in rows if r[2] not in train_sources]
    return train, test


class NaiveBayes:
    """Multinomial Naive Bayes over word tokens (stdlib only)."""

    def __init__(self) -> None:
        self.log_prior: dict[str, float] = {}
        self.log_likelihood: dict[str, dict[str, float]] = {}
        self.vocab: set[str] = set()
        self._default: dict[str, float] = {}

    def fit(self, rows: list[tuple[str, str, str]]) -> "NaiveBayes":
        docs_by_label: dict[str, list[list[str]]] = defaultdict(list)
        for text, label, _ in rows:
            docs_by_label[label].append(text.split())
            self.vocab.update(text.split())

        n = len(rows)
        v = len(self.vocab) or 1
        for label in LABELS:
            docs = docs_by_label.get(label, [])
            self.log_prior[label] = math.log((len(docs) + 1) / (n + len(LABELS)))
            counts = Counter(tok for doc in docs for tok in doc)
            total = sum(counts.values())
            denom = total + v
            self.log_likelihood[label] = {
                tok: math.log((counts[tok] + 1) / denom) for tok in self.vocab
            }
            self._default[label] = math.log(1 / denom)
        return self

    def predict(self, text: str) -> str:
        scores = {label: self.log_prior[label] for label in LABELS}
        for tok in text.split():
            for label in LABELS:
                scores[label] += self.log_likelihood[label].get(
                    tok, self._default[label]
                )
        return max(scores, key=lambda label: scores[label])

    def predict_fn(self, text: str) -> str:
        return self.predict(text)


def prf(golds: list[str], preds: list[str], label: str) -> tuple[float, float, float]:
    """Per-class precision, recall, F1."""
    tp = sum(1 for g, p in zip(golds, preds) if g == label and p == label)
    fp = sum(1 for g, p in zip(golds, preds) if g != label and p == label)
    fn = sum(1 for g, p in zip(golds, preds) if g == label and p != label)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def macro_f1(golds: list[str], preds: list[str]) -> float:
    return sum(prf(golds, preds, label)[2] for label in LABELS) / len(LABELS)


def majority_baseline(golds: list[str]) -> list[str]:
    majority = Counter(golds).most_common(1)[0][0]
    return [majority] * len(golds)


def error_analysis(rows: list[tuple[str, str, str]], preds: list[str]) -> list[tuple]:
    """Return the misclassifications (text, gold, predicted, source)."""
    return [
        (text, gold, pred, src)
        for (text, gold, src), pred in zip(rows, preds)
        if pred != gold
    ]


def report(name: str, golds: list[str], preds: list[str]) -> float:
    print(f"\n{name}")
    for label in LABELS:
        p, r, f1 = prf(golds, preds, label)
        print(f"  {label:6} precision={p:.2f} recall={r:.2f} f1={f1:.2f}")
    mf1 = macro_f1(golds, preds)
    print(f"  macro-F1 = {mf1:.3f}")
    return mf1


def run(verbose: bool = True) -> dict:
    train, test = split_by_source(DATASET, train_frac=0.6)

    # Leakage check: no source straddles the split.
    train_sources = {s for _, _, s in train}
    test_sources = {s for _, _, s in test}
    assert not (train_sources & test_sources), "a source straddles the split"

    model = NaiveBayes().fit(train)
    golds = [label for _, label, _ in test]
    rule_preds = [rule_classify(text) for text, _, _ in test]
    model_preds = [model.predict_fn(text) for text, _, _ in test]
    maj_preds = majority_baseline(golds)

    if verbose:
        print(f"train={len(train)} test={len(test)} sources={sorted(train_sources)}")
        print(f"test sources={sorted(test_sources)} (no overlap)")
        report("rule baseline", golds, rule_preds)
        report("majority baseline", golds, maj_preds)
        model_f1 = report("naive bayes", golds, model_preds)
        print("\nerror analysis (model misclassifications):")
        for text, gold, pred, src in error_analysis(test, model_preds):
            print(f"  [{src}] '{text}' gold={gold} predicted={pred}")

    return {
        "rule": macro_f1(golds, rule_preds),
        "majority": macro_f1(golds, maj_preds),
        "model": macro_f1(golds, model_preds),
        "golds": golds,
        "model_preds": model_preds,
        "errors": error_analysis(test, model_preds),
    }


def _verify() -> bool:
    train, test = split_by_source(DATASET, train_frac=0.6)
    checks: list[tuple[str, bool]] = []

    train_sources = {s for _, _, s in train}
    test_sources = {s for _, _, s in test}
    checks.append(("no source straddles the split", not (train_sources & test_sources)))
    checks.append(("both splits non-empty", bool(train) and bool(test)))

    checks.append(("rule catches a how-question", rule_classify("كيف أتعلم") == "how"))
    checks.append(
        ("rule catches a who-question", rule_classify("من هو الخوارزمي") == "who")
    )
    checks.append(("rule defaults to other", rule_classify("لخص النص") == "other"))

    model = NaiveBayes().fit(train)
    checks.append(("model predicts a label", model.predict("كيف أتعلم") in LABELS))

    result = run(verbose=False)
    checks.append(
        ("model beats the majority baseline", result["model"] > result["majority"])
    )
    checks.append(
        ("rule and model both scored", result["rule"] >= 0.0 and result["model"] >= 0.0)
    )
    checks.append(("error analysis is a list", isinstance(result["errors"], list)))

    p, r, f1 = prf(
        ["how", "how", "other", "other"], ["how", "other", "how", "other"], "how"
    )
    checks.append(("precision computed", abs(p - 0.5) < 1e-9))
    checks.append(("recall computed", abs(r - 0.5) < 1e-9))
    checks.append(("f1 computed", abs(f1 - 0.5) < 1e-9))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Full report (python 05-baseline-intent-classifier.py --verify):")
    run()
