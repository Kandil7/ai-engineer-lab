"""
Fine-Tuning — 01: Supervised Fine-Tuning (SFT)
===============================================
Topics: the chat template, answer-token loss, and overfitting detection.

Why this matters:
    SFT adapts a model's behavior, not its knowledge. This exercise builds
    the masked labels and detects overfitting on a held-out set.

Run:      python 01-supervised-fine-tuning.py
Verify:   python 01-supervised-fine-tuning.py --verify
"""

from __future__ import annotations

import sys


def build_labels(prompt_tokens: list[int], answer_tokens: list[int]) -> list[int]:
    """Mask the prompt with -100; the answer tokens carry the loss."""
    return [-100] * len(prompt_tokens) + list(answer_tokens)


def loss_on_answer(labels: list[int], logits: list[float]) -> float:
    """Cross-entropy on the answer tokens only (masked tokens ignored)."""
    total = 0.0
    count = 0
    for label, logit in zip(labels, logits):
        if label == -100:
            continue
        total += -logit  # stub: -log p for the correct token
        count += 1
    return total / count


def is_overfit(train_loss: float, eval_loss: float) -> bool:
    """Overfit when training loss is near zero and eval loss is higher."""
    return train_loss < 0.05 and eval_loss > train_loss * 3


def main() -> None:
    prompt = [1, 2, 3, 4]
    answer = [5, 6, 7]

    # The prompt is masked; only the answer carries the loss.
    labels = build_labels(prompt, answer)
    assert labels[:4] == [-100] * 4, "prompt masked"
    assert labels[4:] == [5, 6, 7], "answer tokens carry the loss"

    # Loss is computed over the answer span only.
    loss = loss_on_answer(labels, [0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3])
    assert abs(loss - (-0.2)) < 1e-9, "mean of the three answer logits"

    # Overfitting: train loss near zero, eval loss much higher.
    assert is_overfit(0.01, 0.5), "memorized training, failed evaluation"
    assert not is_overfit(0.2, 0.25), "healthy: eval tracks train"

    print("prompt tokens masked with -100; answer tokens carry the loss")
    print("loss computed over the answer span only")
    print("overfitting detected: train near zero, eval much higher")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
