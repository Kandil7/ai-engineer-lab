"""
Redis — 02: Key Patterns and TTL
================================
Topics: namespaces, key patterns, and TTL per data type.

Why this matters:
    A key is the cache's address. This exercise models namespaced keys
    and the TTL bound.

Run:      python 02-key-patterns-ttl.py
Verify:   python 02-key-patterns-ttl.py --verify
"""

from __future__ import annotations

import sys


def key(namespace: str, id_: str) -> str:
    """A namespaced key: namespace:id."""
    return f"{namespace}:{id_}"


def ttl_for(namespace: str) -> int:
    """TTL per data type: profiles 30 min, sessions 24 hr, rate 1 min."""
    return {"user": 1800, "session": 86400, "rate": 60}[namespace]


def main() -> None:
    # Namespaces prevent collisions between data types.
    user_key = key("user", "123")
    session_key = key("session", "123")
    assert user_key != session_key, "namespaces prevent collisions"

    # The pattern encodes the identity.
    assert user_key == "user:123"
    assert key("rate", "1.2.3.4:login") == "rate:1.2.3.4:login"

    # TTL is set per data type.
    assert ttl_for("user") == 1800
    assert ttl_for("session") == 86400
    assert ttl_for("rate") == 60

    # A flat key space collides: two types share "123".
    flat_user = "123"
    flat_session = "123"
    assert flat_user == flat_session, "flat keys collide"

    print("namespaces prevent collisions between data types")
    print("the key pattern encodes the identity")
    print("TTL is set per data type")
    print("a flat key space collides")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
