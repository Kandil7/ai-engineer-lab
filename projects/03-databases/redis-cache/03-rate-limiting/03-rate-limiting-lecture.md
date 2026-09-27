# Redis 03: Rate Limiting

## 🎯 Topic Overview

Rate limiting protects the service from abuse and overload. Redis is the
natural home for the counters: fast, atomic, and TTL-bounded. This lecture
covers the sliding window, the counter, and the limits per endpoint.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the sliding window
2. Count requests with a Redis sorted set
3. Set limits per endpoint
4. Handle the window expiry
5. Return a clear rejection

---

## 1. The Sliding Window

A sliding window counts requests in the last N seconds. Each request adds
a timestamp to the window; requests older than the window are removed. The
window slides with time, so the count is always the recent rate. The
roadmap's exit test: "rate limiting uses a sliding window."

## 2. The Counter

A Redis sorted set stores the request timestamps. Each request adds its
timestamp; expired timestamps are removed; the count is the set's size.
The operations are atomic in a pipeline. The roadmap's exit test: "the
counter is atomic."

```python
pipe.zremrangebyscore(key, 0, now - window)  # remove expired
pipe.zadd(key, {str(now): now})  # add current
pipe.zcard(key)  # count
```

## 3. Limits per Endpoint

Each endpoint has its own limit: auth is strict, general API is loose. The
limit is part of the key — `rate:{ip}:{endpoint}`. The roadmap's exit
test: "limits are set per endpoint."

| Endpoint | Limit | Window |
|----------|-------|--------|
| Auth | 10/min | 60s |
| Chat | 60/min | 60s |
| General | 120/min | 60s |

## 4. Window Expiry

The key carries a TTL so an idle client's counter disappears. Without the
TTL, counters accumulate forever. The TTL is the window plus a margin.

## 5. The Rejection

A request over the limit is rejected with a clear response: a 429 and a
retry-after hint. The rejection is the contract — the client knows when to
retry. The roadmap's exit test: "over-limit requests are rejected."

## Common Mistakes

- No TTL on the counter (accumulates forever).
- One limit for all endpoints.
- Non-atomic counting (race conditions).
- No retry-after in the rejection.
- Counting without removing expired timestamps.

## Key Takeaways

1. The sliding window counts the recent rate.
2. A sorted set stores the timestamps atomically.
3. Limits are set per endpoint.
4. The TTL clears idle counters.
5. Over-limit requests are rejected with a retry hint.