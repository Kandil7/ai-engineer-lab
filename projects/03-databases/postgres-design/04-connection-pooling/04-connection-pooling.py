"""
PostgreSQL — 04: Connection Pooling
===================================
Topics: the pool, borrow/return, and leaks.

Why this matters:
    Opening a connection is expensive; a pool reuses them. This exercise
    models the pool and detects a leak.

Run:      python 04-connection-pooling.py
Verify:   python 04-connection-pooling.py --verify
"""

from __future__ import annotations

import sys


class Pool:
    def __init__(self, size: int) -> None:
        self.available = size
        self.checked_out = 0

    def acquire(self) -> bool:
        if self.available <= 0:
            return False
        self.available -= 1
        self.checked_out += 1
        return True

    def release(self) -> None:
        assert self.checked_out > 0, "cannot release a connection not borrowed"
        self.checked_out -= 1
        self.available += 1

    def exhausted(self) -> bool:
        return self.available == 0 and self.checked_out > 0


def main() -> None:
    pool = Pool(size=2)

    # Borrow and return keeps the pool healthy.
    assert pool.acquire()
    assert pool.acquire()
    assert not pool.acquire(), "pool exhausted at max size"
    pool.release()
    assert pool.acquire(), "returned connection is available again"

    # A leak exhausts the pool: borrowed and never returned.
    pool2 = Pool(size=1)
    assert pool2.acquire()
    assert pool2.exhausted(), "borrowed without return -> exhausted"
    assert not pool2.acquire()

    # Releasing restores capacity.
    pool2.release()
    assert pool2.acquire(), "after release the pool serves again"

    print("borrow and return keeps the pool healthy")
    print("a connection never returned leaks the pool")
    print("releasing restores capacity")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
