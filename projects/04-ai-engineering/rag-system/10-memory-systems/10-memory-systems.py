"""
RAG System — 10: Memory Systems
================================
Topics: the three memory types, write/read paths, and coherence.

Why this matters:
    Memory is what the system remembers. This exercise models the three
    types and tests coherence.

Run:      python 10-memory-systems.py
Verify:   python 10-memory-systems.py --verify
"""

from __future__ import annotations

import sys


class Memory:
    def __init__(self) -> None:
        self.conversation: list[str] = []
        self.semantic: dict[str, str] = {}
        self.episodic: list[dict] = []

    def write(self, turn: str, facts: dict[str, str], episode: dict) -> None:
        """Write to all three stores after each interaction."""
        self.conversation.append(turn)
        self.semantic.update(facts)
        self.episodic.append(episode)

    def read(self) -> dict:
        return {
            "recent": self.conversation[-5:],
            "facts": self.semantic,
            "episodes": self.episodic[-3:],
        }


def is_coherent(memory: Memory, claim: str) -> bool:
    """Coherence: the system does not contradict its own memory."""
    return all(v != f"not-{claim}" for v in memory.semantic.values())


def main() -> None:
    m = Memory()
    m.write(
        turn="What is the capital of France?",
        facts={"capital_france": "Paris"},
        episode={"q": "capital of France", "a": "Paris"},
    )
    m.write(
        turn="What is 2+2?",
        facts={"math_2plus2": "4"},
        episode={"q": "2+2", "a": "4"},
    )

    # The three types are distinct.
    assert len(m.conversation) == 2
    assert len(m.semantic) == 2
    assert len(m.episodic) == 2

    # The read path assembles all three.
    ctx = m.read()
    assert len(ctx["recent"]) == 2
    assert "capital_france" in ctx["facts"]

    # Coherence: no contradiction in the memory.
    assert is_coherent(m, "Paris")
    m.semantic["capital_france"] = "not-Paris"
    assert not is_coherent(m, "Paris"), "contradiction detected"

    print("three memory types: conversation, semantic, episodic")
    print("the read path assembles all three")
    print("coherence: contradiction detected in semantic memory")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
