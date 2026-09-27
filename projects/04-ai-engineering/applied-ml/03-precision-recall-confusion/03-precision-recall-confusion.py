"""
Applied ML — 03: Precision/Recall and the Confusion Matrix
===========================================================
Topics: the four cells, precision, recall, F1, and reading the matrix for
        error patterns.

Why this matters:
    Accuracy lies on imbalanced data. This exercise computes precision,
    recall, and F1 from a confusion matrix and reads the failure pattern.

Run:      python 03-precision-recall-confusion.py
Verify:   python 03-precision-recall-confusion.py --verify
"""

from __future__ import annotations

import sys


def precision(tp: int, fp: int) -> float:
    return tp / (tp + fp)


def recall(tp: int, fn: int) -> float:
    return tp / (tp + fn)


def f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r)


def accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    return (tp + tn) / (tp + tn + fp + fn)


def main() -> None:
    # A rare-class classifier: 100 yeses, 9900 noes.
    # It catches 80 yeses, misses 20, and flags 100 false alarms.
    tp, fn, fp, tn = 80, 20, 100, 9800

    p = precision(tp, fp)
    r = recall(tp, fn)
    acc = accuracy(tp, tn, fp, fn)

    # Accuracy is high but recall is modest: the imbalance trap.
    assert acc > 0.98, "accuracy is high on imbalanced data"
    assert abs(p - 80 / 180) < 1e-9
    assert abs(r - 0.8) < 1e-9
    assert abs(f1(p, r) - 2 * p * r / (p + r)) < 1e-9

    # The matrix reveals the failure pattern: 100 false alarms.
    # A "predict majority always" baseline would have recall 0.
    baseline_recall = recall(0, 100)
    assert baseline_recall == 0.0

    print(f"accuracy={acc:.3f} precision={p:.3f} recall={r:.3f} f1={f1(p, r):.3f}")
    print("accuracy hides the misses: 20 yeses lost, 100 false alarms")
    print("majority-baseline recall = 0.0: accuracy alone is a lie")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
