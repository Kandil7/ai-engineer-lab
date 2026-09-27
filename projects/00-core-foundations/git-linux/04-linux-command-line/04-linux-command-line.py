"""
Git-Linux — 04: Linux Command Line
==================================
Topics: the shell, pipes, and safe commands.

Why this matters:
    The command line is where the work happens. This exercise models
    pipes and the destructive-command discipline.

Run:      python 04-linux-command-line.py
Verify:   python 04-linux-command-line.py --verify
"""

from __future__ import annotations

import sys


def pipe(commands: list[str], data: list[str]) -> list[str]:
    """Chain commands: each command's output feeds the next."""
    out = list(data)
    for cmd in commands:
        if cmd == "grep-error":
            out = [line for line in out if "error" in line]
        elif cmd == "sort":
            out = sorted(out)
        elif cmd == "uniq":
            out = list(dict.fromkeys(out))
        elif cmd == "head-2":
            out = out[:2]
        else:
            raise ValueError(f"unknown command: {cmd}")
    return out


def is_destructive(cmd: str) -> bool:
    """Destructive commands delete or overwrite without recovery."""
    return cmd.startswith("rm -rf") or cmd.startswith("rm -r")


def main() -> None:
    log = [
        "info: started",
        "error: timeout",
        "info: done",
        "error: retry",
        "error: timeout",
    ]

    # A pipe chains small tools into a one-liner.
    result = pipe(["grep-error", "sort", "uniq"], log)
    assert result == ["error: retry", "error: timeout"], "filtered, sorted, deduped"

    # head slices the stream.
    assert pipe(["grep-error", "head-2"], log) == ["error: timeout", "error: retry"]

    # Destructive commands are flagged before running.
    assert is_destructive("rm -rf /tmp/x"), "rm -rf is destructive"
    assert not is_destructive("ls -la"), "read-only commands are safe"

    print("pipes chain small tools: grep -> sort -> uniq")
    print("head slices the stream")
    print("destructive commands flagged before running")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
