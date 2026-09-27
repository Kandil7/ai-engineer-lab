"""
Git-Linux — 01: Git Basics
==========================
Topics: the three areas, staging, and the commit.

Why this matters:
    Git is the version control system every project runs on. This exercise
    models the three areas and the staging discipline.

Run:      python 01-git-basics.py
Verify:   python 01-git-basics.py --verify
"""

from __future__ import annotations

import sys


class Repo:
    """A minimal model of the three areas: working tree, index, HEAD."""

    def __init__(self) -> None:
        self.working: dict[str, str] = {}
        self.index: dict[str, str] = {}
        self.head: dict[str, str] = {}
        self.history: list[str] = []

    def add(self, path: str) -> None:
        assert path in self.working, "cannot stage an untracked file"
        self.index[path] = self.working[path]

    def commit(self, message: str) -> None:
        assert self.index, "nothing staged to commit"
        self.head = dict(self.index)
        self.history.append(message)
        self.index = {}

    def status(self) -> list[str]:
        staged = sorted(set(self.index) - set(self.head))
        modified = sorted(
            p
            for p in self.working
            if p in self.head and self.working[p] != self.head[p]
        )
        untracked = sorted(set(self.working) - set(self.head) - set(self.index))
        return staged + modified + untracked


def main() -> None:
    repo = Repo()
    repo.working = {"app.py": "print(1)", "secret.env": "KEY=value"}

    # Staging is deliberate: only the intended file is staged.
    repo.add("app.py")
    assert "app.py" in repo.index, "app.py staged"
    assert "secret.env" not in repo.index, "secret not staged"

    # A commit moves the index to HEAD and records the message.
    repo.commit("feat: add app entry point")
    assert repo.head == {"app.py": "print(1)"}
    assert repo.history == ["feat: add app entry point"]

    # The secret is never staged or committed.
    assert "secret.env" not in repo.head, "secrets never enter the history"

    # A change to a tracked file shows as modified, not committed.
    repo.working["app.py"] = "print(2)"
    assert "app.py" in repo.status()

    print("staging is deliberate: only the intended file is staged")
    print("commit moves the index to HEAD and records the message")
    print("the secret never enters the history")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
