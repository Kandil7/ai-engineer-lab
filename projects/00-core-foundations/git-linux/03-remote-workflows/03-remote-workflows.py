"""
Git-Linux — 03: Remote Workflows
================================
Topics: push, pull, divergence, and the review gate.

Why this matters:
    A remote is where collaboration happens. This exercise models the
    push/pull loop and the rejected-push rule.

Run:      python 03-remote-workflows.py
Verify:   python 03-remote-workflows.py --verify
"""

from __future__ import annotations

import sys


class Remote:
    def __init__(self) -> None:
        self.commits: list[str] = []

    def push(self, local: list[str], last_pushed: int) -> tuple[bool, int]:
        """Push local commits. Rejected if the remote has commits the
        local lacks."""
        if not all(c in local for c in self.commits):
            return False, last_pushed
        self.commits = list(local)
        return True, len(local)

    def pull(self, local: list[str]) -> list[str]:
        """Merge remote commits into local (append, no conflicts here)."""
        merged = list(local)
        for c in self.commits:
            if c not in merged:
                merged.append(c)
        return merged


def main() -> None:
    remote = Remote()
    local = ["c1", "c2"]
    last_pushed = 0

    # Push sends local commits up.
    ok, last_pushed = remote.push(local, last_pushed)
    assert ok and remote.commits == ["c1", "c2"]

    # A rejected push: the remote has commits the local lacks.
    remote.commits.append("c3")  # someone else pushed
    ok, _ = remote.push(local, last_pushed)
    assert not ok, "push rejected when the remote is ahead"

    # Pull merges the remote's commits, then push succeeds.
    local = remote.pull(local)
    assert "c3" in local
    ok, last_pushed = remote.push(local, last_pushed)
    assert ok, "after pull, the push succeeds"

    print("push sends local commits to the remote")
    print("push rejected when the remote has commits the local lacks")
    print("pull merges the remote's commits; the push then succeeds")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
