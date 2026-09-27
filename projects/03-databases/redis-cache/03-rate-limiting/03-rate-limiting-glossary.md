# Redis 03: Rate Limiting — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Sliding window | Counts requests in the last N seconds | recent rate |
| Sorted set | The timestamp store | zadd, zcard |
| Atomic | The count is race-free | pipeline |
| Limit | The max requests per window | 10/min |
| Endpoint limit | Per-endpoint limits | auth strict |
| Window expiry | The counter's TTL | window + margin |
| Rejection | The 429 with a retry hint | over-limit response |

---

## Alphabetical Glossary

### Atomic

**Definition:** The count operations are race-free, executed in a pipeline.
Two concurrent requests cannot both pass the limit.

**Example:**
```python
pipe.zremrangebyscore(...)
pipe.zadd(...)
pipe.zcard(...)
```

**Related concepts:** Sorted set

---

### Endpoint limit

**Definition:** The per-endpoint limit, part of the key: `rate:{ip}:{endpoint}`.
Auth is strict; general API is loose.

**Example:**
```python
# auth 10/min, chat 60/min, general 120/min
```

**Related concepts:** Limit

---

### Limit

**Definition:** The maximum requests allowed in the window. The threshold
the counter is compared against.

**Example:**
```python
# 10 requests per 60 seconds
```

**Related concepts:** Endpoint limit

---

### Rejection

**Definition:** The response to an over-limit request: a 429 with a
retry-after hint. The contract telling the client when to retry.

**Example:**
```python
# HTTP 429, Retry-After: 30
```

**Related concepts:** Limit

---

### Sliding window

**Definition:** Counting requests in the last N seconds. Each request adds
a timestamp; older timestamps are removed. The window slides with time.

**Example:**
```python
# count requests in the last 60 seconds
```

**Related concepts:** Sorted set

---

### Sorted set

**Definition:** The Redis structure storing request timestamps. Each
request adds its timestamp; the count is the set's size.

**Example:**
```python
# zadd key timestamp; zcard key
```

**Related concepts:** Atomic, Sliding window

---

### Window expiry

**Definition:** The counter's TTL, set to the window plus a margin. Clears
idle clients' counters.

**Example:**
```python
# EXPIRE key 120 for a 60-second window
```

**Related concepts:** Sliding window

---

## Related Concepts

- **Key patterns**: rate keys are namespaced (topic 02)
- **Cache strategies**: counters are write-through (topic 01)
- **Security**: rate limiting blocks abuse (security section)

## Key Takeaways

1. The sliding window counts the recent rate.
2. A sorted set stores the timestamps atomically.
3. Limits are set per endpoint.
4. The TTL clears idle counters.
5. Over-limit requests are rejected with a retry hint.