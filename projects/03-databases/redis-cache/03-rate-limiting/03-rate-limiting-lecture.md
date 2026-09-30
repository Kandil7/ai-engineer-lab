# Redis 03: Rate Limiting

## Topic Overview

Rate limiting protects a service from abuse and overload by capping how many requests a client can make
in a window. Redis is the natural home for the counters: it is fast, its operations are atomic, and its
keys are TTL-bounded. The sliding window is the standard algorithm, and it is what turns "we should
rate-limit" into a concrete, enforcible rule.

This lecture covers the sliding window, the Redis sorted set that implements it, the limits per
endpoint, the TTL that clears idle counters, and the clear rejection that tells a client when to retry.

The core discipline is atomicity: the count and the update must be atomic, or two concurrent requests
can both slip through the limit. Redis's atomic operations are what make the counter correct under
concurrency.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the sliding window.
2. Implement the counter with a Redis sorted set.
3. Set limits per endpoint.
4. Handle the window expiry with a TTL.
5. Return a clear rejection with a retry hint.
6. Explain why the counter must be atomic.

## Prerequisites

- Redis 02 (key patterns and TTL) for the key design.

---

## 1. The Sliding Window

### The idea

A sliding window counts requests in the last N seconds. Each request adds a timestamp; requests older
than the window are removed, so the count is always the recent rate:

```python
def allow(self, now: int) -> bool:
    """Add the request; reject if the recent count exceeds the limit."""
    self.timestamps = [t for t in self.timestamps if t > now - self.window]
    if len(self.timestamps) >= self.limit:
        return False
    self.timestamps.append(now)
    return True
```

### Why sliding

A fixed window (reset every minute) allows a burst at the window boundary: a client can send the limit
at the end of one window and the limit at the start of the next. The sliding window has no boundary,
so the rate is smooth.

### The exit test

The roadmap's exit test is that rate limiting uses a sliding window, which is what prevents the
boundary burst.

## 2. The Counter

### Redis sorted set

A Redis sorted set stores the request timestamps, scored by time. Each request:

1. Removes timestamps older than the window.
2. Adds the current timestamp.
3. Counts the remaining members.

```text
ZREMRANGEBYSCORE key 0 (now - window)    # remove expired
ZADD key now now                          # add current
ZCARD key                                 # count
```

### Atomicity

The three operations run in a pipeline or a Lua script so they are atomic. Without atomicity, two
concurrent requests can both read a count below the limit and both add, exceeding it.

### The exit test

The roadmap's exit test is that the counter is atomic, which is what makes the limit correct under
concurrency.

## 3. Limits per Endpoint

### The pattern

Each endpoint has its own limit, and the key includes the endpoint:

```text
rate:{ip}:{endpoint}
```

| Endpoint | Limit | Window |
| --- | --- | --- |
| Auth | 10/min | 60 s |
| Chat | 60/min | 60 s |
| General | 120/min | 60 s |

### Why per endpoint

Authentication is expensive and sensitive, so its limit is strict; general reads are cheap, so their
limit is loose. One global limit either blocks legitimate traffic or fails to protect the sensitive
endpoint.

### The exit test

The roadmap's exit test is that limits are set per endpoint, which is what matches the limit to the
endpoint's cost and risk.

## 4. Window Expiry

### The TTL

The key carries a TTL so an idle client's counter disappears:

```text
EXPIRE rate:{ip}:{endpoint} {window + margin}
```

### Why

Without the TTL, counters accumulate forever and consume memory for clients that are long gone. The
TTL is the window plus a small margin, so the counter survives until its oldest request expires.

### The exit test

The roadmap's exit test is that the window expires, which is what keeps the memory bounded.

## 5. The Rejection

### The response

A request over the limit is rejected with a clear response: an HTTP 429 and a `Retry-After` header:

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

### Why the hint

The rejection is a contract: it tells the client when to retry, so a well-behaved client backs off and
a misbehaving one is throttled. A rejection without the hint leaves the client guessing.

### The exit test

The roadmap's exit test is that over-limit requests are rejected, and the rejection is informative
rather than silent.

## 6. The Exercise

### What it models

The exercise models a sliding-window limiter with a limit and a window, and shows the rejection, the
window sliding, and per-endpoint limits.

### The assertions

```python
assert limiter.allow(0) and limiter.allow(10) and limiter.allow(20)
assert not limiter.allow(30), "over the limit -> rejected"
assert limiter.allow(70), "expired timestamps removed, request passes"
assert auth.limit < general.limit, "limits are set per endpoint"
```

The window-slides assertion is the key behavior: after the window passes, the counter clears.

## Real-World Application

- Limiting login attempts per IP so credential stuffing is throttled.
- Limiting a chat endpoint per session so one client cannot flood it.
- Returning a 429 with `Retry-After` so a well-behaved client backs off.
- A TTL on the counter so idle clients do not consume memory.

## Common Mistakes

1. **No TTL on the counter.** Counters accumulate forever.
2. **One limit for all endpoints.** Sensitive endpoints under-protected.
3. **Non-atomic counting.** Race conditions let requests exceed the limit.
4. **No retry hint in the rejection.** The client cannot back off correctly.
5. **A fixed window.** The boundary burst defeats the limit.
6. **Not removing expired timestamps.** The count never drops.

## Key Takeaways

1. The sliding window counts the recent rate without a boundary burst.
2. A Redis sorted set stores the timestamps, and the operations must be atomic.
3. Limits are set per endpoint to match cost and risk.
4. The TTL clears idle counters and bounds memory.
5. Over-limit requests are rejected with a retry hint.

## Self-Check Questions

1. Why does a sliding window beat a fixed window?
2. Why must the counter operations be atomic?
3. Why set the limit per endpoint rather than globally?
4. What does the counter's TTL accomplish?
5. Why does the rejection include a `Retry-After` hint?

## Further Reading / Connections

- Redis 02 (key patterns and TTL) — the key and TTL this builds on.
- Redis 04 (pub/sub and streams) — the other Redis patterns.
- RAG System 02 (hard filters) — the same boundary-enforcement discipline.
- `docs/cheat-sheets/qdrant.md` — related infrastructure reference.
