"""
Redis — 04: Pub/Sub and Streams
===============================
Topics: the channel, fire-and-forget, and the stream's persistence.

Why this matters:
    Pub/Sub broadcasts in real time; Streams guarantee delivery. This
    exercise models both and the delivery-guarantee choice.

Run:      python 04-pubsub-streams.py
Verify:   python 04-pubsub-streams.py --verify
"""

from __future__ import annotations

import sys


class PubSub:
    def __init__(self) -> None:
        self.subscribers: dict[str, list[str]] = {}

    def subscribe(self, channel: str, client: str) -> None:
        self.subscribers.setdefault(channel, []).append(client)

    def publish(self, channel: str, message: str) -> list[str]:
        """Fire-and-forget: only current subscribers receive it."""
        return [c for c in self.subscribers.get(channel, [])]


class Stream:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def add(self, message: str) -> None:
        self.messages.append(message)

    def read(self) -> list[str]:
        """Persistence: the full history is available."""
        return list(self.messages)


def main() -> None:
    ps = PubSub()
    ps.subscribe("chat:abc123", "client-1")

    # A subscriber receives the published message.
    assert ps.publish("chat:abc123", "hello") == ["client-1"]

    # Fire-and-forget: a message published with no subscriber is lost.
    assert ps.publish("chat:empty", "lost") == [], "no subscriber -> lost"

    # A stream persists: messages are readable later.
    stream = Stream()
    stream.add("job-1")
    stream.add("job-2")
    assert stream.read() == ["job-1", "job-2"], "history is available"

    print("a subscriber receives the published message")
    print("fire-and-forget: no subscriber means the message is lost")
    print("a stream persists: the full history is readable")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
