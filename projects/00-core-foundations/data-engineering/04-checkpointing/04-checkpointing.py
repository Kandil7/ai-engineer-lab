"""
Data Engineering — 04: Checkpointing
=====================================
Topics: durable checkpoints, atomic writes, resume, checkpoint + idempotency.

Why this matters:
    Long pipelines fail. Checkpointing records progress so a failed run
    resumes where it stopped instead of restarting from zero.

Run:      python 04-checkpointing.py
Verify:   python 04-checkpointing.py --verify
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path


class Checkpoint:
    """Durable, atomic checkpoint: write tmp, then rename."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, state: dict) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state), encoding="utf-8")
        os.replace(tmp, self.path)  # atomic on most filesystems

    def load(self) -> dict | None:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))


def process_pages(pages: list[int], checkpoint: Checkpoint) -> list[int]:
    """Process pages, checkpointing after each. Simulates a crash at page 3."""
    state = checkpoint.load() or {"last_committed": 0}
    done = list(range(1, state["last_committed"] + 1))
    for page in pages:
        if page <= state["last_committed"]:
            continue  # already committed: resume skips it
        if page == 3:
            raise RuntimeError("simulated crash at page 3")
        done.append(page)
        checkpoint.save({"last_committed": page})
    return done


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        cp = Checkpoint(Path(tmp) / "checkpoint.json")
        pages = [1, 2, 3, 4, 5]

        # First run crashes at page 3.
        try:
            process_pages(pages, cp)
            raise AssertionError("expected crash")
        except RuntimeError:
            pass

        # Resume: continues from page 3, does not redo 1-2.
        done = process_pages(pages, cp)
        assert done == [1, 2, 4, 5], f"resume skipped committed work: {done}"
        final_state = cp.load()
        assert final_state is not None
        assert final_state["last_committed"] == 5

        # Atomicity: no leftover tmp file after a clean save.
        assert not (cp.path.with_suffix(".tmp")).exists()

        print(f"after crash: checkpoint at page {final_state['last_committed']}")
        print(f"resume processed: {done} (pages 1-2 not redone)")
        print("atomic write: no torn or leftover tmp records")
        print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
