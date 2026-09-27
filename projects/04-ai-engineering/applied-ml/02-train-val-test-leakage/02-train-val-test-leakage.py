"""
Applied ML — 02: Train/Validation/Test and Leakage
===================================================
Topics: the three-way split, group leakage, and why test must stay
        untouched.

Why this matters:
    A model's job is to generalize, not memorize. This exercise builds a
    group split (by book) and proves a random split leaks group identity.

Run:      python 02-train-val-test-leakage.py
Verify:   python 02-train-val-test-leakage.py --verify
"""

from __future__ import annotations

import sys


def group_split(passages: list[dict], train_frac: float = 0.7) -> tuple[list, list]:
    """Split by book_id so no book appears in both train and test."""
    books = sorted({p["book_id"] for p in passages})
    train_books = set(books[: int(train_frac * len(books))])
    train = [p for p in passages if p["book_id"] in train_books]
    test = [p for p in passages if p["book_id"] not in train_books]
    return train, test


def random_split(passages: list[dict], train_frac: float = 0.7) -> tuple[list, list]:
    """Split by row (the leaky way for grouped data)."""
    n = int(train_frac * len(passages))
    return passages[:n], passages[n:]


def main() -> None:
    passages = [
        {"book_id": "b1", "page": 1},
        {"book_id": "b1", "page": 2},
        {"book_id": "b2", "page": 1},
        {"book_id": "b2", "page": 2},
        {"book_id": "b3", "page": 1},
    ]

    # Group split: no book straddles the boundary.
    train, test = group_split(passages)
    train_books = {p["book_id"] for p in train}
    test_books = {p["book_id"] for p in test}
    assert not (train_books & test_books), "no book in both train and test"
    assert len(train) + len(test) == len(passages)

    # Random split: book b2 straddles -> group leakage.
    r_train, r_test = random_split(passages)
    r_train_books = {p["book_id"] for p in r_train}
    r_test_books = {p["book_id"] for p in r_test}
    assert r_train_books & r_test_books, "random split leaks group identity"

    print(
        f"group split: train books={sorted(train_books)} test books={sorted(test_books)}"
    )
    print("no book straddles the group split")
    print(f"random split leaks: shared books={sorted(r_train_books & r_test_books)}")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
