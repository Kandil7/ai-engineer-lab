"""
Redis — 03: Rate Limiting
=========================
Topics: the sliding window, the counter, and the rejection.

Why this matters:
    Rate limiting protects the service from abuse. This exercise models
    the sliding-window counter and the rejection.

Run:      python 03-rate-limiting.py
Verify:   python 03-rate-limiting.py --verify
"""

from __future__ import annotations

import sys


class SlidingWindow:
    def __init__(self, limit: int, window: int) -> None:
        self.limit = limit
        self.window = window
        self.timestamps: list[int] = []

    def allow(self, now: int) -> bool:
        """Add the request; reject if the recent count exceeds the limit."""
        self.timestamps = [t for t in self.timestamps if t > now - self.window]
        if len(self.timestamps) >= self.limit:
            return False
        self.timestamps.append(now)
        return True


def main() -> None:
    limiter = SlidingWindow(limit=3, window=60)

    # Three requests within the window pass.
    assert limiter.allow(0)
    assert limiter.allow(10)
    assert limiter.allow(20)

    # The fourth is rejected.
    assert not limiter.allow(30), "over the limit -> rejected"

    # The window slides: after 60 seconds the counter clears.
    assert limiter.allow(70), "expired timestamps removed, request passes"

    # A per-endpoint limit: auth is stricter than general.
    auth = SlidingWindow(limit=10, window=60)
    general = SlidingWindow(limit=120, window=60)
    assert auth.limit < general.limit, "limits are set per endpoint"

    print("three requests within the window pass; the fourth is rejected")
    print("the window slides: expired timestamps clear the counter")
    print("limits are set per endpoint")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
