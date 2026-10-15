# Lecture 01: Docker Containerization for AI Services

## Topic Overview

Docker packages an application and everything it needs to run into a portable image, so the same artifact behaves identically on a laptop, a CI runner, and a production host. For AI services the stakes are higher than for a typical web app: an image must carry the right CUDA runtime, pin its vector-database version to the client library, and ship without leaking API keys or model weights. This lecture teaches containerization as an engineering discipline, from image anatomy through multi-stage builds, Compose orchestration, GPU passthrough, and the security and resource controls that keep a container fleet from taking down its host.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Linux command line, HTTP fundamentals, basic Python, a working Docker install

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** the image, container, and registry model and how they differ
2. **Write** a Dockerfile whose layer order exploits the build cache instead of fighting it
3. **Apply** multi-stage builds to cut an AI service image from gigabytes to megabytes
4. **Compose** a multi-service stack with health checks, volumes, and internal DNS
5. **Constrain** CPU and memory so one service cannot starve the host
6. **Harden** containers with non-root users, read-only filesystems, and minimal base images
7. **Expose** a GPU to a container for CUDA workloads and diagnose the common failures
8. **Diagnose** why a container will not start, will not stay up, or cannot reach a dependency

---

## Key Concepts

### 1. Image, Container, Registry

Three nouns carry almost all of Docker's meaning:

| Concept | What it is | Analogy |
|---|---|---|
| **Image** | Immutable, layered filesystem snapshot plus metadata | A compiled binary |
| **Container** | A running process with its own namespace, cgroups, and mount | A running process |
| **Registry** | A server that stores and serves images by tag | An artifact repository |

An image is a stack of read-only layers. When you run it, Docker adds a writable top layer, so every container from the same image starts identical and diverges only at runtime.

```
Registry (ghcr.io / Docker Hub)
        │  pull by tag
        ▼
Image  ┌──────────────┐  ← read-only layers
       │  app code    │
       │  deps        │
       │  base OS     │
       └──────────────┘
              │  docker run
              ▼
Container ┌──────────────┐
          │ + writable   │  ← the only mutable layer
          │   tmp layer  │
          └──────────────┘
```

**Tag discipline matters.** `latest` is not a version; it is whatever the registry decided to serve when you asked. Pin images by digest in production:

```dockerfile
# Mutable: what was "python:3.12-slim" last week?
FROM python:3.12-slim

# Immutable: this exact build, forever
FROM python:3.12-slim@sha256:2c797b45f2d0...
```

### 2. Dockerfile Anatomy

Every instruction produces a layer. Order decides both correctness and build speed.

```dockerfile
# 1. Base image. Pin it.
FROM python:3.12-slim

# 2. Set the working directory. Everything below resolves from here.
WORKDIR /app

# 3. Copy dependency manifests FIRST, alone.
#    This layer stays cached until the manifests actually change.
COPY pyproject.toml uv.lock ./

# 4. Install dependencies. Only this step re-runs when deps change.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 5. Copy the application source LAST.
#    Editing a .py file no longer invalidates the dependency layer.
COPY src/ ./src/

# 6. Metadata. Non-functional but expected by tooling.
EXPOSE 8000

# 7. Runtime user. Never root.
RUN useradd --create-home --uid 10001 appuser
USER appuser

# 8. Exec form. This is the PID 1 process.
CMD ["uv", "run", "uvicorn", "devmate.api.main:app", "--host", "0.0.0.0"]
```

**CMD vs ENTRYPOINT.** `CMD` supplies default arguments; `ENTRYPOINT` defines the executable. The usual split for a CLI tool is `ENTRYPOINT ["devmate"]` plus `CMD ["--help"]`, so `docker run myimage stats .` runs `devmate stats .`.

**CMD exec form vs shell form.** `CMD ["a", "b"]` runs `a b` directly as PID 1 and forwards signals. `CMD a b` wraps in `/bin/sh -c`, which makes your app a grandchild of a shell that swallows `SIGTERM`. Use the exec form for anything that must shut down cleanly.

### 3. Layer Caching and Build Order

Docker reuses a layer when the instruction and all prior layers are unchanged. The practical rule: **copy the least-changing files first, the most-changing files last.**

```dockerfile
# ❌ BAD: every source edit re-installs every dependency
COPY . .
RUN pip install -r requirements.txt

# ✅ GOOD: source edits skip the install layer entirely
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
```

Measure it yourself. Build twice and read the timings:

```bash
docker build -t demo .
docker build -t demo .   # second run should print CACHED for most steps
```

A layer invalidated by an accidental `.env` copy or a stray `COPY . .` is the single most common cause of slow AI-service builds, because dependency installation for torch or transformers can take many minutes.

### 4. .dockerignore

`.dockerignore` decides what never enters the build context. Without it, `COPY . .` drags in `.git`, virtualenvs, caches, model weights, and secrets, inflating build time and often the image itself.

```
.git
.gitignore
.venv
venv
__pycache__
*.pyc
.mypy_cache
.pytest_cache
.ruff_cache
.env
.env.*
*.gguf
*.safetensors
outputs/
evaluations/rag/reports/
infra/docker/
```

Two categories matter for AI repos specifically:

- **Secrets.** `.env` files must never enter the context. A `COPY . .` that lands a `.env` in an image layer is a leak that survives even if you delete the file in a later `RUN`, because earlier layers remain in the image history.
- **Weights.** Multi-gigabyte checkpoints do not belong in images. Mount them as volumes or pull them at startup from a model registry.

### 5. Multi-Stage Builds

A multi-stage build uses one stage to compile and a second to run. The build toolchain stays behind in a discarded stage; only the artifacts cross over.

```dockerfile
# ---------- Stage 1: builder ----------
FROM python:3.12 AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"
USER 10001
EXPOSE 8000
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0"]
```

The measured effect on a typical Python AI service:

| Image | Approximate size | Contains |
|---|---|---|
| `python:3.12` | ~1.0 GB | Interpreter, headers, build tools |
| Single-stage app | ~2.5 GB | Plus all deps plus source |
| Multi-stage runtime | ~350 MB | Interpreter plus runtime deps only |

The builder stage is free to be fat. The runtime stage is the one you push, scan, and pay to serve.

### 6. Docker Compose

Compose declares a multi-container application in one YAML file and starts it with one command. It is the right tool for local development and single-host staging; it is not a cluster orchestrator.

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.8.0
    ports:
      - "6333:6333"
    volumes:
      - qdrant-data:/qdrant/storage
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:6333/healthz || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 30s

  devmate-api:
    build:
      context: ../..
      dockerfile: projects/04-ai-engineering/devmate/docker/Dockerfile
    env_file:
      - ../../.env
    depends_on:
      qdrant:
        condition: service_healthy
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

volumes:
  qdrant-data:
```

Three details decide whether this works:

- **`depends_on` with `condition: service_healthy`** waits for the dependency's health check, not merely its process start. A plain `depends_on: [qdrant]` returns as soon as the container is running, which is usually before the service inside it is accepting connections.
- **Service names are hostnames.** Inside the Compose network, `http://qdrant:6333` resolves to the qdrant container. Never use `localhost` for a sibling service; that refers to the container itself.
- **Named volumes outlive containers.** `qdrant-data:` binds to a Docker-managed volume that survives `docker compose down`. Use `down -v` only when you intend to destroy state.

### 7. Health Checks

A health check is a command Docker runs inside the container on a schedule. Without one, `depends_on: service_healthy` does nothing, and an orchestrator cannot tell a live service from a wedged one.

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -fsS http://localhost:8000/health || exit 1"]
  interval: 10s     # how often to run
  timeout: 5s       # how long one run may take
  retries: 3        # consecutive failures before unhealthy
  start_period: 30s # grace period before failures count
```

The test command must exit non-zero when unhealthy. `curl` without `-f` returns exit code 0 on a 500 response, silently reporting a broken service as healthy. Use `curl -fsS` or `wget -qO-`.

### 8. Resource Limits

Without limits, a single container can consume every CPU and all memory on the host. On a shared workstation this is not hypothetical; a runaway embedding job can freeze every other container and the host itself.

```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: "1.0"
    reservations:
      memory: 256M
      cpus: "0.5"
```

| Field | Effect |
|---|---|
| `limits.memory` | Hard ceiling. Exceeding it triggers the OOM killer and the container exits. |
| `reservations.memory` | Scheduler hint. On Compose it is advisory; on Swarm it reserves capacity. |
| `limits.cpus` | CPU quota as a fraction of one core. `"2.0"` means two full cores. |

Tune limits against measurement, not intuition. Watch actual usage before setting a ceiling:

```bash
docker stats --no-stream
```

An AI service with a poorly chosen memory limit dies at the worst moment, because retrieval workloads spike memory on large queries rather than steadily.

### 9. GPU Containers

Running a CUDA workload in a container requires the NVIDIA Container Toolkit and, on Docker Desktop, the WSL2 GPU backend. The container does not get a virtual GPU; it gets direct access to the host driver through a mounted device.

```dockerfile
FROM nvidia/cuda:12.6.3-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3.12 python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/

CMD ["python3", "src/serve.py"]
```

```yaml
services:
  inference:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Or from the CLI:

```bash
docker run --gpus all --rm nvidia/cuda:12.6.3-base-ubuntu24.04 nvidia-smi
```

**The three failures you will hit, in order:**

1. `could not select device driver "" with capabilities: [[gpu]]` means the NVIDIA Container Toolkit is missing or the Docker daemon was not restarted after installing it.
2. On Windows, a CUDA error inside WSL2 usually means the Windows driver is too old for the CUDA runtime in the image. The container ships the runtime; the driver comes from the host, and they must be compatible.
3. `torch.cuda.is_available()` returning `False` inside a container that looks correctly configured usually means the image installed a CPU-only build of PyTorch. Check with `pip show torch` and reinstall the CUDA variant.

An AI engineer should be able to state the split in one sentence: **the image provides CUDA user-space libraries; the host provides the driver; the toolkit stitches them together.**

### 10. Image Security

```dockerfile
# ❌ BAD: running as root, shipping a shell, shipping a key
FROM python:3.12
COPY . .
ENV OPENAI_API_KEY=sk-live-abc123
CMD ["python", "app.py"]

# ✅ GOOD: minimal base, non-root, secret from a runtime source
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
RUN useradd --system --uid 10001 appuser
USER appuser
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

The hardening checklist, in the order that pays off:

1. **Never bake secrets into layers.** A `RUN` that writes a key is recoverable from image history even if a later layer deletes it. Inject secrets at runtime through environment variables, a mounted file, or a secrets manager.
2. **Run as non-root.** `USER appuser` limits the blast radius of a container escape and satisfies most compliance scanners.
3. **Use a slim or distroless base.** A smaller surface means fewer packages to patch. Distroleess images have no shell at all, which breaks interactive debugging but removes an entire class of tooling an attacker could use.
4. **Make the filesystem read-only where possible.** `--read-only` plus an explicit `tmpfs` for scratch directories stops an attacker from writing a payload to disk.
5. **Scan images.** Run `docker scout cves <image>` or Trivy in CI and fail on critical findings, not just report them.

### 11. Logging

Containers should log to stdout and let the runtime collect. Writing log files inside the container means the logs die with the container and fill its writable layer.

```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

Without rotation, the Docker json-file driver grows without bound. On a long-running AI service that logs every retrieval, this silently fills the host disk and takes down every container on the machine.

---

## Code Examples

### Example 1: Production Dockerfile for a FastAPI AI Service

```dockerfile
# syntax=docker/dockerfile:1.7

# ---------- Stage 1: resolve and install ----------
FROM python:3.12-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_CACHE_DIR=/root/.cache/uv

WORKDIR /app

# Dependency manifests only. This layer is cached across source edits.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Application source.
COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------- Stage 2: runtime ----------
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Only the virtualenv and source cross the stage boundary.
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# Non-root runtime user with a fixed UID.
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

# Exec form. uvicorn is PID 1 and receives SIGTERM directly.
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Example 2: Compose Stack with Health-Gated Dependencies

```yaml
name: devmate

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: devmate
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set POSTGRES_PASSWORD in .env}
      POSTGRES_DB: devmate
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devmate -d devmate"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

  qdrant:
    image: qdrant/qdrant:v1.8.0
    ports:
      - "6333:6333"
    volumes:
      - qdrant-data:/qdrant/storage
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:6333/healthz || exit 1"]
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

  devmate-api:
    build:
      context: ../..
      dockerfile: projects/04-ai-engineering/devmate/docker/Dockerfile
    env_file:
      - ../../.env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  postgres-data:
  qdrant-data:
```

Note the `${POSTGRES_PASSWORD:?...}` form. The `:?` syntax makes Compose fail fast with a clear message when the variable is unset, instead of starting Postgres with an empty password.

### Example 3: Diagnosing a Container That Will Not Stay Up

```bash
# 1. Is it exiting, or running-but-broken?
docker compose ps -a

# 2. Why did it exit? The last lines of the log usually say.
docker compose logs --tail=50 devmate-api

# 3. Run the same image interactively, overriding CMD.
docker compose run --rm --entrypoint sh devmate-api

# 4. Check health status and the probe that produced it.
docker inspect --format '{{json .State.Health}}' devmate-qdrant | jq

# 5. Confirm the container can resolve and reach a dependency.
docker compose exec devmate-api python -c \
    "import socket; print(socket.getaddrinfo('qdrant', 6333))"

# 6. Check resource pressure. An OOM kill looks like a crash.
docker stats --no-stream
```

The distinction between step 2 and step 3 matters. Reading logs tells you what the process reported. Running interactively tells you whether the image itself is correct, separate from the orchestrator's environment.

---

## Common Mistakes to Avoid

### 1. Copying the Whole Repo Before Installing Dependencies

```dockerfile
# ❌ BAD: any .py edit invalidates the install layer
COPY . .
RUN pip install -r requirements.txt

# ✅ GOOD: dependency layer survives source edits
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
```

### 2. Baking Secrets into Image Layers

```dockerfile
# ❌ BAD: this key is recoverable from the image history forever
RUN echo "OPENAI_API_KEY=sk-live-..." > /app/.env

# ✅ GOOD: inject at runtime
# docker run --env-file .env  or  Compose env_file, or a secrets manager
```

### 3. Using Shell Form for CMD

```dockerfile
# ❌ BAD: your app is a grandchild of sh; SIGTERM never reaches it
CMD uvicorn app:app --host 0.0.0.0

# ✅ GOOD: your app is PID 1 and shuts down on SIGTERM
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

### 4. Depending on a Service Without a Health Gate

```yaml
# ❌ BAD: returns as soon as the process starts, not when it is ready
depends_on:
  - qdrant

# ✅ GOOD: waits until the health check passes
depends_on:
  qdrant:
    condition: service_healthy
```

### 5. Using `localhost` to Reach a Sibling Service

```python
# ❌ BAD: localhost is the container itself, not the qdrant service
url = "http://localhost:6333"

# ✅ GOOD: Compose service names are hostnames on the internal network
url = "http://qdrant:6333"
```

### 6. Forgetting to Pin the Vector Database Version

The client library and the server must agree on a major version. A Compose file that runs `qdrant/qdrant:latest` while the application pins `qdrant-client>=1.8.0,<1.9` will work until the registry ships v1.9, then fail with a confusing protocol error. Pin both sides and change them together.

---

## Best Practices

1. **Pin every base image**, preferably by digest in production
2. **Order Dockerfile instructions** so cheap layers change often and expensive layers change rarely
3. **Use multi-stage builds** so build toolchains never reach production
4. **Write a `.dockerignore`** that excludes secrets, weights, caches, and VCS data
5. **Run as a non-root user** with a fixed UID so file ownership is predictable
6. **Use the exec form of CMD and ENTRYPOINT** so signals reach your process
7. **Add health checks** and gate `depends_on` on `service_healthy`
8. **Set memory and CPU limits** after measuring real usage with `docker stats`
9. **Log to stdout** and configure rotation so the host disk survives a chatty service
10. **Scan images in CI** and fail on critical CVEs rather than merely reporting them
11. **Mount model weights as volumes**; never bake multi-gigabyte checkpoints into layers
12. **Separate build from run**: the image that builds your code should not be the image that serves traffic

---

## Practice Exercises

### Exercise 1: Cut an Image in Half
Take a single-stage Dockerfile for any Python service and convert it to a multi-stage build. Record the image size before and after with `docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'`. Explain which layer disappeared and why.

### Exercise 2: Prove the Cache Works
Build an image twice with no changes and confirm most steps report `CACHED`. Then edit one source file, rebuild, and confirm that only the `COPY src/` layer and everything after it re-run.

### Exercise 3: Gate a Dependency Properly
Add a health check to a service in `infra/docker/docker-compose.yml`, then convert a plain `depends_on` to `condition: service_healthy`. Start the stack from cold and confirm the dependent service waits.

### Exercise 4: Contain the Blast Radius
Add memory and CPU limits to every service in a Compose file. Then start a deliberately memory-hungry process in one container and confirm the others stay responsive.

### Exercise 5: Diagnose a GPU Failure
On a machine with the NVIDIA Container Toolkit, run `docker run --gpus all --rm nvidia/cuda:12.6.3-base-ubuntu24.04 nvidia-smi`. If it fails, read the error and determine whether the cause is a missing toolkit, a stale Docker daemon, or a driver/runtime mismatch.

---

## Summary

Containerization for AI services is the same discipline as for any other service, plus three extra constraints: CUDA must be exposed correctly, vector-database versions must be pinned to the client library, and model weights must stay out of image layers. The durable takeaways:

1. **Images are layered and immutable; containers are running processes.** Most Docker confusion dissolves once this is firm.
2. **Build order is a performance decision.** Dependencies before source, always.
3. **Multi-stage builds** are the single largest image-size lever available.
4. **Health checks and `depends_on: service_healthy`** turn "it started" into "it is ready."
5. **Limits, non-root users, and image scans** are what separate a demo container from a production one.
6. **Compose is for single hosts.** When you need replication and failover, that is Kubernetes, and it is a different lecture.

**Next lecture:** CI/CD with GitHub Actions, where every image built here gets tested, scanned, and promoted through environments.
