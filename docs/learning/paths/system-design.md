# Learning Path: System Design

**Last updated:** 2026-08-06

**Goal:** develop the ability to design scalable, reliable distributed systems — covering
architecture patterns, infrastructure components, and real-world case studies.

**Primary project:** `projects/05-system-design`

---

## Milestones

### 1. Designing for Scale (Week 1)
- Vertical vs horizontal scaling — when each makes sense
- Stateful vs stateless services — why stateless scales easier
- The CAP theorem: consistency, availability, partition tolerance tradeoffs
- PACELC: extending CAP with latency considerations
- SLAs, SLOs, SLIs: defining reliability mathematically
- Capacity estimation: back-of-envelope calculations for QPS, storage, bandwidth

### 2. Load Balancing (Week 1–2)
- **L4 load balancing:** TCP-level, fast, limited routing logic
  - HAProxy, AWS NLB, LVS
- **L7 load balancing:** HTTP-level, content-aware routing
  - NGINX, AWS ALB, Envoy
- Algorithms: round-robin, weighted, least-connections, consistent hashing, IP hash
- Health checks: active vs passive, critical for zero-downtime deploys
- Global load balancing: DNS-based, GeoDNS, Anycast
- Sticky sessions: why they exist, why to avoid them

### 3. Caching (Week 2)
- **Client-side caching:** browser cache headers, ETags, Cache-Control
- **CDN caching:** CloudFront, Cloudflare — edge caching for static + dynamic
- **Application caching:** in-process (LRU), Redis, Memcached
- Cache patterns:
  - **Cache-aside:** app checks cache → miss → DB → populate cache
  - **Read-through:** cache fetches from DB on miss
  - **Write-through:** writes go to cache and DB simultaneously
  - **Write-behind:** writes go to cache, async flush to DB
- Cache invalidation: TTL-based, event-based, versioned keys
- Cache stampede: thundering herd problem, lock-and-rebuild, probabilistic early expiry
- Redis data structures: strings, hashes, lists, sets, sorted sets, streams

### 4. Message Queues (Week 2–3)
- **Why queues:** decouple producers/consumers, handle traffic spikes, async processing
- **RabbitMQ:** traditional broker, exchanges, routing keys, ack/nack
- **Apache Kafka:** distributed log, partitions, consumer groups, offset management
- **Redis Streams:** lightweight alternative, consumer groups, trimming
- Delivery semantics: at-most-once, at-least-once, exactly-once
- Dead letter queues: handling poison messages
- Schema evolution: Avro, Protobuf, schema registry
- Ordering guarantees: per-partition vs global

### 5. Event-Driven Architecture (Week 3)
- Events vs commands vs queries — different message types
- **Event sourcing:** store events, derive state, full audit trail
- **CQRS:** separate read and write models
  - When to use: read-heavy systems, complex domain logic
  - Tradeoffs: eventual consistency, operational complexity
- **Saga pattern:** distributed transactions without 2PC
  - Choreography: services emit and listen to events
  - Orchestration: central coordinator manages the flow
- Idempotency: making operations safe to retry
- Eventual consistency: embracing it vs fighting it

### 6. Microservices Patterns (Week 3–4)
- **Service decomposition:** bounded contexts, domain-driven design
- **API Gateway:** single entry point, routing, rate limiting, auth
  - Kong, AWS API Gateway, Envoy
- **Service mesh:** Istio, Linkerd — sidecar proxy for inter-service communication
- **Circuit breaker:** Hystrix pattern — fail fast, prevent cascade failures
- **Bulkhead:** isolate failures to one service, not the entire system
- **Strangler fig:** gradual migration from monolith to microservices
- Observability: distributed tracing (Jaeger, Zipkin), structured logging, metrics (Prometheus)

### 7. Database Design for Scale (Week 4)
- **Replication:** primary-replica, read replicas, multi-primary
- **Sharding:** horizontal partitioning — hash-based, range-based, directory-based
  - Challenges: cross-shard queries, rebalancing, hotspots
- **Partitioning:** PostgreSQL table partitioning by range/list/hash
- **Polyglot persistence:** right tool for right job
  - PostgreSQL for transactional data
  - Qdrant for vector search
  - Redis for caching/sessions
  - S3 for object storage
- Indexing strategies: B-tree, hash, GIN, GiST, partial indexes
- Connection pooling: PgBouncer, HikariCP

### 8. Case Studies (Week 5–6)

#### ChatGPT / LLM Inference Service
- Request flow: API → load balancer → inference scheduler → GPU pool
- KV-cache management for long conversations
- Streaming responses: SSE, chunked transfer encoding
- Rate limiting: per-user, per-organization, tiered
- Cost optimization: model routing (cheap model for simple queries)
- Caching: prompt caching, semantic deduplication

#### WhatsApp / Real-time Messaging
- Connection management: WebSocket farms, connection persistence
- Message ordering: Lamport clocks, vector clocks
- End-to-end encryption: key exchange, forward secrecy
- Group messaging: fan-out on write vs fan-out on read
- Media handling: upload to CDN, thumbnail generation, lazy loading
- Online status: heartbeat, presence service, tradeoffs of accuracy vs cost

#### Coursera / Learning Platform
- Video delivery: transcoding pipeline, adaptive bitrate streaming (HLS/DASH)
- Progress tracking: event sourcing, idempotent checkpoints
- Recommendation engine: collaborative filtering + content-based
- Assessment system: quiz engine, plagiarism detection, auto-grading
- Certificate generation: event-driven pipeline, PDF generation at scale

### 9. Infrastructure & Deployment (Week 6–7)
- **Docker:** containers, Dockerfile best practices, multi-stage builds
- **Kubernetes:** pods, deployments, services, ingress, configmaps
- **CI/CD:** GitHub Actions, deployment pipelines, blue-green vs canary
- **Observability stack:** Prometheus (metrics) + Grafana (dashboards) + Loki (logs)
- **Alerting:** PagerDuty, OpsGenie, alert fatigue avoidance
- **Disaster recovery:** RPO, RTO, backup strategies, chaos engineering

---

## The 20% That Unlocks 80%

| Concept | Why It Matters |
|---|---|
| Back-of-envelope estimation | Grounds design in reality, not hand-waving |
| Statelessness | Enables horizontal scaling without session complexity |
| Cache-aside pattern | Covers 90% of caching use cases |
| At-least-once + idempotency | Practical message delivery without exactly-once complexity |
| Circuit breaker | Prevents cascade failures in distributed systems |

---

## Design Framework (for interview or practice)

1. **Requirements:** functional + non-functional (latency, throughput, availability)
2. **Estimation:** QPS, storage, bandwidth — order of magnitude
3. **High-level design:** boxes and arrows, major components
4. **Deep dive:** pick 2-3 components, detail the internals
5. **Bottlenecks:** identify failure modes, single points of failure
6. **Tradeoffs:** explicitly state what you chose and why

---

## Daily Pattern

1h reading (paper, blog, case study) → 2h design exercise (whiteboard/diagram) → 1h implement
one component → 1h discuss/review with peer or AI.

---

## Key Resources

| Topic | Resource |
|---|---|
| System Design Interview | Alex Xu — *System Design Interview* Vol 1 & 2 |
| Designing Data-Intensive Apps | Martin Kleppmann — *DDIA* |
| High Scalability | [highscalability.com](http://highscalability.com) |
| System Design Primer | [github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) |
| ByteByteGo | [bytebytego.com](https://blog.bytebytego.com) |
| AWS Architecture Center | [aws.amazon.com/architecture](https://aws.amazon.com/architecture/) |

---

## Practice Tasks

1. Design a URL shortener: estimate capacity, choose storage, handle redirects
2. Design a chat system: WebSocket management, message ordering, group chat
3. Design a news feed: fan-out strategies, caching, real-time updates
4. Implement a Redis-based cache-aside layer for an existing service
5. Set up Kafka producer/consumer for async event processing
6. Design a rate limiter: token bucket vs sliding window
7. Write a capacity estimation doc for the ai-engineer-lab system
8. Diagram the full architecture: client → API gateway → FastAPI → Qdrant

---

## Architecture Patterns Reference

### Caching Layers

```
Client Browser (Cache-Control, ETags)
    ↓
CDN (CloudFront / Cloudflare)
    ↓
API Gateway (rate limit, auth)
    ↓
Application Cache (Redis)
    ↓
Database (PostgreSQL with read replicas)
    ↓
Object Storage (S3 for blobs)
```

### Message Queue Patterns

```
Producer → Queue → Consumer (point-to-point)
Producer → Exchange → Queue(s) → Consumer(s) (pub/sub with routing)
Producer → Topic Partition → Consumer Group (Kafka)
```

### Microservice Communication

```
Synchronous:  Service A → HTTP/gRPC → Service B (blocks until response)
Asynchronous: Service A → Queue → Service B (fire and forget)
Event-driven:  Service A → Event Bus → Service B, C, D (pub/sub)
```

### Load Balancing Algorithms

| Algorithm | How It Works | Best For |
|---|---|---|
| Round Robin | Cycle through servers | Equal-capacity servers |
| Weighted RR | More requests to powerful servers | Heterogeneous hardware |
| Least Connections | Route to least busy server | Variable request durations |
| Consistent Hash | Hash key maps to server | Session affinity, caching |
| IP Hash | Hash client IP | Sticky sessions (avoid if possible) |

### Case Study: ChatGPT Architecture

```
User Request
    ↓
API Gateway (rate limit, auth, routing)
    ↓
Load Balancer
    ↓
Inference Router
├─ Simple query → Smaller model (GPT-4o-mini)
├─ Complex query → Larger model (GPT-4o)
└─ Code query → Specialized model
    ↓
GPU Pool (A100/H100)
├─ KV-Cache management (reuse across turns)
├─ Speculative decoding (parallel draft + verify)
└─ Continuous batching (maximize GPU utilization)
    ↓
Streaming Response (SSE)
    ↓
Response Cache (semantic deduplication)
```

### Capacity Estimation Formula

```
Daily Active Users (DAU):     1,000,000
Requests per user per day:    10
Total requests per day:       10,000,000
Peak QPS (10x average):      ~1,200 QPS
Average QPS:                  ~115 QPS

Storage per user:             1 KB metadata
Total metadata:               1 GB
Message history:              100 KB/user → 100 GB

Bandwidth:                    1,200 req/s × 10 KB avg = 12 MB/s
```

### Circuit Breaker States

```
Closed (normal)
├─ Request passes through
├─ Track failure count
└─ If failures > threshold → Open

Open (failing)
├─ Requests fail immediately (no call to downstream)
├─ Start timer
└─ After timeout → Half-Open

Half-Open (testing)
├─ Allow one probe request
├─ If success → Closed
└─ If failure → Open
```

### Database Scaling Decision Tree

```
Read-heavy or write-heavy?
├─ Read-heavy → Read replicas + caching
├─ Write-heavy → Sharding or partitioning
└─ Both → Consider CQRS

Single database handling load?
├─ < 10K QPS → Optimized single DB + cache
├─ 10K-100K QPS → Read replicas + connection pooling
├─ 100K+ QPS → Sharding + dedicated cache layer
└─ Global → Multi-region with conflict resolution
```

### Kubernetes Deployment Pattern

```yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: devmate-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: api
        image: devmate-api:v1.2.0
        resources:
          requests: { cpu: "250m", memory: "256Mi" }
          limits:   { cpu: "500m", memory: "512Mi" }
        readinessProbe:
          httpGet: { path: /health, port: 8080 }
          initialDelaySeconds: 5
        livenessProbe:
          httpGet: { path: /health, port: 8080 }
          initialDelaySeconds: 10
---
# Service
apiVersion: v1
kind: Service
metadata:
  name: devmate-api
spec:
  selector: { app: devmate-api }
  ports: [{ port: 80, targetPort: 8080 }]
---
# HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: devmate-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target: { type: Utilization, averageUtilization: 70 }
```

### Observability Stack

```
Metrics:    Prometheus → Grafana (dashboards)
Logs:       Fluent Bit → Loki → Grafana (log search)
Traces:     OpenTelemetry → Jaeger (distributed tracing)
Alerts:     Alertmanager → PagerDuty (incident response)
```

---

## Self-Check

Can you explain:
- When to choose Kafka over RabbitMQ and vice versa?
- How consistent hashing helps with cache distribution?
- The tradeoffs between fan-out-on-write vs fan-out-on-read?
- How a circuit breaker prevents cascade failures?
- How to estimate QPS for a system with 1M daily active users?
- The difference between L4 and L7 load balancing?
- When to use CQRS and the tradeoffs involved?

---

## ملخص عربي (Arabic Summary)

مسار تصميم الأنظمة القابلة للتوسع: من التوسع الأفقي إلى موازنات التحميل والتخزين
المؤقت وقنوات الرسائل والبنية التفاعلية القائمة على الأحداث. يشمل أنماط الخدمات
المصغرة ودراسات حالة واقعية (ChatGPT، WhatsApp، Coursera) والبنية التحتية
للكوبرنيتيس والمراقبة. يتضمن مخططات معمارية تفصيلية ونماذج حساب القدرة
وأabr-states patterns وأabr Kubernetes deployments.
