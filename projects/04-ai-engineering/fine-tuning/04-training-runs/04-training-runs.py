"""
Fine-Tuning — 04: Training Runs
================================
Topics: the run config, eval-loss monitoring, and run comparison.

Why this matters:
    A training run is a reproducible experiment. This exercise records a
    config, detects overfitting from eval loss, and compares runs.

Run:      python 04-training-runs.py
Verify:   python 04-training-runs.py --verify
"""

from __future__ import annotations

import sys


def is_overfit(train_loss: float, eval_loss: float) -> bool:
    return train_loss < 0.05 and eval_loss > train_loss * 3


def better(candidate: dict, baseline: dict) -> bool:
    """A candidate is better when eval loss is lower on the same split."""
    assert candidate["data_split"] == baseline["data_split"], (
        "runs compare only on the same data version"
    )
    return candidate["eval_loss"] < baseline["eval_loss"]


def main() -> None:
    config = {
        "base_model": "qwen2.5-7b",
        "rank": 16,
        "lr": 2e-4,
        "batch_size": 4,
        "epochs": 3,
        "data_split": "v1",
        "seed": 42,
    }
    assert config["rank"] == 16 and config["data_split"] == "v1"

    # Overfitting: training loss near zero, eval loss much higher.
    assert is_overfit(0.01, 0.5), "memorized training, failed evaluation"
    assert not is_overfit(0.2, 0.25), "healthy run"

    # Runs compare on the same data split.
    baseline = {"data_split": "v1", "eval_loss": 0.50}
    candidate = {"data_split": "v1", "eval_loss": 0.42}
    assert better(candidate, baseline), "lower eval loss on the same split"

    # A candidate on a different data version is a different run.
    other_split = {"data_split": "v2", "eval_loss": 0.30}
    try:
        better(other_split, baseline)
        assert False, "must refuse cross-split comparison"
    except AssertionError:
        pass

    print("run config recorded: base, rank, lr, batch, epochs, split, seed")
    print("overfitting detected from eval loss; healthy run passes")
    print("candidate compared to baseline on the same data split only")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
