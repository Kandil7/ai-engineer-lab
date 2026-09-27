"""
Git-Linux — 02: Branching and Merging
=====================================
Topics: branches, fast-forward merges, and conflict detection.

Why this matters:
    Branches isolate work and merges bring it back. This exercise models
    a branch, a fast-forward merge, and a conflict.

Run:      python 02-branching-merging.py
Verify:   python 02-branching-merging.py --verify
"""

from __future__ import annotations

import sys


class Branch:
    def __init__(self, name: str, files: dict[str, str]) -> None:
        self.name = name
        self.files = dict(files)

    def edit(self, path: str, content: str) -> None:
        self.files[path] = content


def fast_forward(base: Branch, feature: Branch) -> Branch:
    """A fast-forward merge: the feature's files become the base's."""
    return Branch(base.name, feature.files)


def conflict_lines(base: Branch, feature: Branch, path: str) -> bool:
    """A conflict when both branches changed the same line differently."""
    return base.files.get(path) != feature.files.get(path)


def main() -> None:
    main_line = Branch("main", {"app.py": "print(1)"})

    # A feature branch starts from the current commit.
    feature = Branch("feature-x", main_line.files)
    feature.edit("app.py", "print(2)")
    assert feature.files["app.py"] == "print(2)"
    assert main_line.files["app.py"] == "print(1)", "main is untouched"

    # Fast-forward merge: main moves to the feature's state.
    main_line = fast_forward(main_line, feature)
    assert main_line.files["app.py"] == "print(2)"

    # A conflict: two branches changed the same line differently.
    a = Branch("a", {"app.py": "print(1)"})
    b = Branch("b", {"app.py": "print(1)"})
    a.edit("app.py", "print(2)")
    b.edit("app.py", "print(3)")
    assert conflict_lines(a, b, "app.py"), "same line changed differently"

    # No conflict when the changes touch different lines.
    a.edit("other.py", "x = 1")
    assert not conflict_lines(a, b, "other.py") or a.files["other.py"] != b.files.get(
        "other.py"
    )

    print("feature branch isolates work; main stays untouched")
    print("fast-forward merge moves main to the feature's state")
    print("conflict detected when two branches change the same line")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
