# Docker — Containerization

Multi-stage Docker builds, Docker Compose orchestration, and production best practices
for all services in the AI Engineer Lab.

---

## Multi-Stage Builds

### Go Backend (auth-service)

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /auth-service .

# Runtime stage
FROM alpine:3.19
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=builder /auth-service .
EXPOSE 8080
CMD ["./auth-service"]
```

**Benefits:**
- Final image: ~15MB (vs ~800MB with full Go image)
- No build tools in production
- Reduced attack surface

### Flutter Web

```dockerfile
# Build stage
FROM ghcr.io/cirruslabs/flutter:stable AS builder
WORKDIR /app
COPY pubspec.* ./
RUN flutter pub get
COPY . .
RUN flutter build web --release --dart-define=FLUTTER_WEB_AUTO_DETECT=false

# Runtime stage
FROM nginx:alpine
COPY --from=builder /app/build/web /usr/share/nginx/html
EXPOSE 80
```

### Python AI Services

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Docker Compose Orchestration

### Service Architecture

```
┌─────────────────────────────────────────────────┐
│                  Docker Network                  │
│                  (fslab-net)                     │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ PostgreSQL│  │  Redis   │  │  Qdrant  │      │
│  │  :5432   │  │  :6379   │  │  :6333   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Go API   │  │ FastAPI  │  │  Nginx   │      │
│  │  :8080   │  │  :8000   │  │  :80     │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Core Services

| Service      | Image               | Port  | Purpose                  |
| ------------ | ------------------- | ----- | ------------------------ |
| postgres     | postgres:16-alpine  | 5432  | Primary database         |
| redis        | redis:7-alpine      | 6379  | Cache, sessions          |
| qdrant       | qdrant/qdrant:v1.12 | 6333  | Vector database          |

### Dev Tools (profile: dev-tools)

| Service         | Image                    | Port | Purpose              |
| --------------- | ------------------------ | ---- | -------------------- |
| pgadmin         | dpage/pgadmin4           | 5050 | Database GUI         |
| redis-commander | rediscommander/redis-commander | 8081 | Redis GUI       |

---

## Health Checks

Every service includes health checks:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U fslab -d fslab"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

### Health Check Strategy

| Service   | Check Method                    | Interval | Timeout |
| --------- | ------------------------------- | -------- | ------- |
| PostgreSQL| `pg_isready`                    | 10s      | 5s      |
| Redis     | `redis-cli ping`                | 10s      | 5s      |
| Qdrant    | `wget /healthz`                 | 15s      | 5s      |
| Go API    | `curl /health`                  | 10s      | 5s      |

---

## Resource Limits

Prevent any single service from consuming all host resources:

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: "1.0"
    reservations:
      memory: 256M
      cpus: "0.5"
```

| Service   | Memory Limit | CPU Limit |
| --------- | ------------ | --------- |
| PostgreSQL| 512M         | 1.0       |
| Redis     | 300M         | 0.5       |
| Qdrant    | 1G           | 1.0       |
| Go API    | 256M         | 0.5       |

---

## Production Best Practices

### Security

1. **Non-root containers** — run as non-root user
2. **Read-only filesystem** — mount volumes as read-only where possible
3. **No secrets in images** — use Docker secrets or environment variables
4. **Scan images** — run `docker scan` before deploying
5. **Minimal base images** — use `alpine` or `distroless`

### Logging

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

Rotated logs prevent disk exhaustion.

### Networking

- Services communicate on internal bridge network (`fslab-net`)
- Only necessary ports exposed to host
- Inter-service communication uses container names (DNS)

---

## Getting Started

```bash
# Start core services
docker compose -f infra/docker/docker-compose.yml up -d

# Start with dev tools
docker compose -f infra/docker/docker-compose.yml --profile dev-tools up -d

# View running containers
docker compose -f infra/docker/docker-compose.yml ps

# View logs
docker compose -f infra/docker/docker-compose.yml logs -f postgres

# Stop everything
docker compose -f infra/docker/docker-compose.yml down

# Full reset (delete data)
docker compose -f infra/docker/docker-compose.yml down -v
```
