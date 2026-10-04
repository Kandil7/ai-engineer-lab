# Redis Caching Layer

Redis implementation for caching, session storage, rate limiting, and real-time features
in the AI Engineer Lab.

---

## Cache Strategies

### Cache-Aside (Lazy Loading)

The primary pattern used for read-heavy data:

1. Application checks Redis for key
2. **Cache hit** → return cached value
3. **Cache miss** → query PostgreSQL, store in Redis, return

```
App → Redis GET user:123
  HIT  → return cached user
  MISS → SELECT * FROM users WHERE id=123 → Redis SET user:123 → return
```

**Use for:** User profiles, course metadata, frequently-accessed content.

### Write-Through

Write to cache and database simultaneously:

1. Application writes to PostgreSQL
2. Application writes same data to Redis
3. Both are always in sync

**Use for:** Session data, real-time counters, data that must be immediately consistent.

### Write-Behind (Write-Back)

Write to Redis immediately, async flush to PostgreSQL:

1. Application writes to Redis
2. Background worker flushes to PostgreSQL periodically
3. Risk: data loss on crash; use for non-critical data

**Use for:** Analytics counters, view counts, non-critical metrics.

---

## Key Patterns

| Key Pattern           | TTL    | Strategy     | Purpose                  |
| --------------------- | ------ | ------------ | ------------------------ |
| `user:{id}`           | 30 min | Cache-aside  | User profile cache       |
| `session:{id}`        | 24 hr  | Write-through| Active session data      |
| `chat:{session_id}`   | 1 hr   | Write-through| Recent chat messages     |
| `rate:{ip}:{endpoint}`| 1 min  | Write-through| Rate limiting counter    |
| `course:{id}`         | 1 hr   | Cache-aside  | Course metadata          |
| `embedding:{hash}`    | 24 hr  | Cache-aside  | Cached embedding vectors |

---

## Session Storage

Sessions are stored in Redis with hash structures:

```
HSET session:{session_id}
  user_id    "123"
  expires_at "2026-06-27T12:00:00Z"
  role       "student"
  preferences "{...}"
```

**Advantages over DB sessions:**
- Sub-millisecond reads
- Automatic TTL expiration
- Atomic operations
- No DB connection overhead

---

## Rate Limiting

Implement a sliding window rate limiter using Redis sorted sets:

```python
# Pseudocode for rate limiting
def is_rate_limited(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"rate:{user_id}"
    now = time.time()
    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)  # Remove expired
    pipe.zadd(key, {str(now): now})  # Add current request
    pipe.zcard(key)  # Count requests
    pipe.expire(key, window)  # Set TTL
    _, _, count, _ = pipe.execute()
    return count > limit
```

**Configuration:**

| Endpoint         | Limit        | Window |
| ---------------- | ------------ | ------ |
| Auth endpoints   | 10 req/min   | 60s    |
| Chat API         | 60 req/min   | 60s    |
| Embedding API    | 20 req/min   | 60s    |
| General API      | 120 req/min  | 60s    |

---

## Pub/Sub for Real-Time Features

Redis Pub/Sub enables real-time chat message delivery:

- **Publisher:** Go backend publishes new messages to `chat:{session_id}` channel
- **Subscribers:** WebSocket handlers subscribe and push to connected clients

```
Go Backend → PUBLISH chat:abc123 {message}
WebSocket Handler → SUBSCRIBE chat:abc123 → push to client
```

**Limitation:** Pub/Sub is fire-and-forget. For guaranteed delivery, use Redis Streams.

---

## Getting Started

```bash
# Start Redis
docker compose -f infra/docker/docker-compose.yml up -d redis

# Connect with CLI
docker exec -it fslab-redis redis-cli

# Test basic operations
redis-cli SET test "hello"
redis-cli GET test
redis-cli DEL test
```
