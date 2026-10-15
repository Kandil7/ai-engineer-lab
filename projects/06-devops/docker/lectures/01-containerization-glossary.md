# Glossary: Docker Containerization

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Image | Immutable layered filesystem snapshot plus metadata | Never mutated at runtime |
| Container | A running process with its own namespaces and cgroups | Ephemeral by default |
| Registry | Server that stores and serves images by tag | Docker Hub, ghcr.io, ECR |
| Tag | Mutable name pointing at an image | Pin by digest in production |
| Layer | One filesystem diff produced by a Dockerfile instruction | Cached by content hash |
| Build Context | Directory sent to the Docker daemon for a build | Keep it small with .dockerignore |
| Dockerfile | Text file of instructions that build an image | Each instruction adds a layer |
| Multi-Stage Build | Build in one stage, run from a smaller second stage | Discards the toolchain |
| CMD | Default arguments for the container's main process | Use the exec form |
| ENTRYPOINT | The executable a container runs | Pairs with CMD for args |
| Compose | Declarative multi-container app in one YAML file | Single-host tool, not a cluster |
| Volume | Persistent, Docker-managed storage for container data | Survives container removal |
| Network | Docker-managed bridge or overlay for service DNS | Service names become hostnames |
| Health Check | Command Docker runs in-container to test liveness | Non-zero exit means unhealthy |
| Resource Limit | CPU and memory ceiling for a container | Exceeding memory triggers OOM |
| Non-Root | Running the container process as an unprivileged user | Reduces escape blast radius |
| .dockerignore | Rules excluding files from the build context | Keeps secrets and weights out |

---

## Detailed Definitions

### Image

**Definition:** An immutable, read-only stack of filesystem layers plus configuration metadata such as the default command, exposed ports, and environment. Images are the artifact you build, scan, push, and deploy.

**Example:**
```bash
# List local images with size
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'

# Inspect an image's layers
docker history ghcr.io/org/devmate-api:v1.2.0 --no-trunc

# Pull a specific digest, immune to tag retargeting
docker pull python:3.12-slim@sha256:2c797b45f2d0...
```

**Related Terms:** Container, Layer, Registry, Tag

**Key Facts:**
- Images are never modified; changing anything creates a new image
- Each `RUN`, `COPY`, and `ADD` instruction appends a layer
- The same image can run as any number of containers simultaneously
- Image size is roughly the sum of its layers, minus shared layers

---

### Container

**Definition:** A running instance of an image, given its own process namespace, network namespace, and mount namespace, plus cgroup-enforced CPU and memory limits. The writable top layer is discarded when the container is removed unless a volume is attached.

**Example:**
```bash
# Run a container from an image, detached, with a name
docker run -d --name api -p 8000:8000 ghcr.io/org/devmate-api:v1.2.0

# List running containers with live resource usage
docker stats --no-stream

# Remove a container and its writable layer
docker rm -f api
```

**Related Terms:** Image, Volume, Namespace, Cgroup

**Key Facts:**
- A container is a process, not a lightweight virtual machine
- Removing a container destroys its writable layer and any files written to it
- State you care about belongs on a volume, not in the container filesystem
- One image can back many independent containers

---

### Layer

**Definition:** A single filesystem change produced by one Dockerfile instruction. Layers stack bottom to top; later layers may hide files from earlier ones but cannot change them.

**Example:**
```bash
# See every layer in an image, with its size and the command that made it
docker history python:3.12-slim

# Typical layer stack for an application image
#   ─────────────────────────────────────
#   CMD ["uvicorn", ...]         ← metadata, no layer
#   COPY src/ ./src/             ← layer 4
#   RUN pip install -r req.txt   ← layer 3  (large, changes rarely)
#   COPY requirements.txt .      ← layer 2
#   FROM python:3.12-slim        ← layer 1  (shared, cached globally)
```

**Related Terms:** Build Cache, Dockerfile, Multi-Stage Build

**Key Facts:**
- A layer is cached when the instruction text and every prior layer are unchanged
- Deleting a file in a later `RUN` does not remove it from earlier layers; it hides it
- Secrets written into a layer are recoverable from image history
- Fewer, larger layers generally beat many, small layers

---

### Build Cache

**Definition:** The daemon's store of previously computed layers, keyed by the hash of an instruction and its parent layer. A cache hit means the step is skipped entirely rather than re-executed.

**Example:**
```bash
# Build twice; the second run should print CACHED for unchanged steps
docker build -t demo .
docker build -t demo .

# Force a full rebuild, ignoring the cache
docker build --no-cache -t demo .
```

**Related Terms:** Layer, Dockerfile, BuildKit

**Key Facts:**
- Cache order follows Dockerfile order exactly; there is no dependency graph
- `COPY` is keyed on file content, so an unchanged file does not invalidate the layer
- A common mistake is `COPY . .` early, which invalidates every later step on any file change
- BuildKit additionally caches across machines via a shared cache backend when configured

---

### Build Context

**Definition:** The directory tree sent from the client to the Docker daemon before a build starts. Every `COPY` and `ADD` path resolves relative to this directory, and nothing outside it is reachable.

**Example:**
```bash
# Context is the current directory; .dockerignore applies inside it
docker build -t demo .

# Context is a parent directory, so Dockerfile paths must be adjusted
docker build -f projects/04-ai-engineering/devmate/docker/Dockerfile -t demo .

# Context from stdin, useful for tiny images with no local files
docker build -t demo - < Dockerfile
```

**Related Terms:** .dockerignore, Dockerfile, COPY

**Key Facts:**
- The context is tarred and shipped to the daemon before any instruction runs
- A large context slows every build, even steps that report `CACHED`
- `.dockerignore` shrinks the context and prevents accidental secret inclusion
- Paths in `COPY` cannot escape the context with `..`

---

### .dockerignore

**Definition:** A file in the context root whose glob patterns exclude files and directories from the build context, exactly like `.gitignore` semantics.

**Example:**
```
.git
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
*.bin
outputs/
evaluations/rag/reports/
infra/docker/
**/*.md
```

**Related Terms:** Build Context, COPY, Secrets

**Key Facts:**
- Excludes apply to the context, not to the image; they do not remove existing layers
- Excluding `.env` is the cheapest protection against baking a key into an image
- Excluding model weights keeps build context and image size under control
- Patterns use Go filepath.Match syntax plus `**` for recursive matches

---

### Dockerfile

**Definition:** The declarative text file that defines how to build an image: base image, file copies, command executions, metadata, and the runtime user and command.

**Example:**
```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

RUN useradd --system --uid 10001 appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0"]
```

**Related Terms:** Layer, Multi-Stage Build, CMD, ENTRYPOINT

**Key Facts:**
- Instructions run top to bottom; order determines cache behavior
- `RUN` executes during build; `CMD` and `ENTRYPOINT` execute at runtime
- The `# syntax=` directive enables BuildKit features such as cache mounts
- A Dockerfile must live inside or be reachable from the build context

---

### Multi-Stage Build

**Definition:** A Dockerfile pattern that uses multiple `FROM` instructions as separate stages. An earlier stage compiles or installs; a later stage copies only the artifacts it needs and becomes the final image.

**Example:**
```dockerfile
# Stage 1: fat builder with compilers and caches
FROM python:3.12 AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev
COPY src/ ./src/

# Stage 2: slim runtime, no compilers, no caches
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0"]
```

**Related Terms:** Stage, Layer, Image Size

**Key Facts:**
- Only the last stage becomes the final image unless you `--target` a specific one
- The builder stage's size is irrelevant to the shipped artifact
- Build dependencies such as compilers, headers, and git never reach production
- Typical result: an AI service image drops from roughly 2.5 GB to roughly 350 MB

---

### CMD

**Definition:** The default arguments Docker passes to the container's `ENTRYPOINT`, or the default executable when no entrypoint is set. Only one `CMD` takes effect; the last one in the Dockerfile wins.

**Example:**
```dockerfile
# Exec form: the process is PID 1 and receives signals directly
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Shell form: wrapped in /bin/sh -c, signals stop at the shell
CMD uvicorn app:app --host 0.0.0.0 --port 8000

# Override at run time
# docker run myimage uvicorn app:app --host 0.0.0.0 --port 9000
```

**Related Terms:** ENTRYPOINT, Exec Form, Signal

**Key Facts:**
- The exec form is required for `SIGTERM` to reach your application
- The shell form exists for cases that genuinely need a shell, such as variable expansion
- `docker run myimage args` replaces CMD entirely
- Using both CMD and ENTRYPOINT lets CMD supply default arguments that run-time arguments extend

---

### ENTRYPOINT

**Definition:** The executable a container runs. When set, CMD and run-time arguments become arguments to that executable rather than replacements for it.

**Example:**
```dockerfile
# The container always runs devmate; CMD supplies default args
ENTRYPOINT ["devmate"]
CMD ["--help"]

# docker run myimage              → runs `devmate --help`
# docker run myimage stats .      → runs `devmate stats .`
```

**Related Terms:** CMD, Exec Form, Arguments

**Key Facts:**
- ENTRYPOINT defines what runs; CMD defines default arguments to it
- The exec form is strongly preferred for the same signal-handling reasons as CMD
- `docker run --entrypoint /bin/sh myimage` overrides the entrypoint for debugging
- A shell-form ENTRYPOINT has the same PID 1 problem as a shell-form CMD

---

### Compose

**Definition:** A tool and file format for declaring a multi-container application as a set of services, networks, and volumes, then starting and stopping it as a unit with `docker compose up` and `down`.

**Example:**
```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.8.0
    ports: ["6333:6333"]
    volumes: ["qdrant-data:/qdrant/storage"]
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:6333/healthz || exit 1"]
      interval: 15s
      retries: 5

  api:
    build: ../..
    env_file: [../../.env]
    depends_on:
      qdrant:
        condition: service_healthy

volumes:
  qdrant-data:
```

**Related Terms:** Service, Volume, Network, depends_on

**Key Facts:**
- Compose runs on one host; it does not replicate or fail over
- Service names resolve as hostnames on the Compose network
- `docker compose down` preserves named volumes; `down -v` destroys them
- The top-level `version` key is obsolete and should be omitted

---

### Volume

**Definition:** Docker-managed persistent storage that lives outside a container's writable layer, survives container removal, and can be shared between containers.

**Example:**
```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.8.0
    volumes:
      - qdrant-data:/qdrant/storage

volumes:
  qdrant-data:
```

```bash
# List volumes
docker volume ls

# Inspect where a volume is mounted on the host
docker volume inspect devmate_qdrant-data

# Remove all unused volumes
docker volume prune
```

**Related Terms:** Bind Mount, tmpfs, State

**Key Facts:**
- Named volumes outlive `docker compose down`; bind mounts reference a host path
- Anything a database writes belongs on a volume or it disappears with the container
- `docker compose down -v` deletes named volumes and their data
- tmpfs mounts are memory-backed and vanish on restart; use them for scratch space

---

### Network

**Definition:** A Docker-managed virtual network that gives containers their own IP and, on user-defined networks, DNS resolution by service name.

**Example:**
```bash
# Inside a Compose stack, this resolves to the qdrant container
curl http://qdrant:6333/healthz

# On the host, use the published port instead
curl http://localhost:6333/healthz

# List networks
docker network ls
```

**Related Terms:** Service DNS, Bridge, Port Mapping

**Key Facts:**
- Compose creates a default user-defined network per project
- On user-defined networks, service names are DNS names; `localhost` is the container itself
- `ports:` publishes a container port to the host; `expose:` documents but does not publish
- Only publish ports the host genuinely needs; everything published is attack surface

---

### Health Check

**Definition:** A command Docker runs inside the container on a fixed interval. A zero exit marks the container healthy; a non-zero exit, after the configured number of consecutive failures, marks it unhealthy.

**Example:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -fsS http://127.0.0.1:8000/health || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 30s
```

```bash
# Read the last health result
docker inspect --format '{{json .State.Health}}' devmate-api | jq
```

**Related Terms:** livenessProbe, readinessProbe, depends_on

**Key Facts:**
- `curl` without `-f` returns exit 0 on HTTP 500, falsely reporting healthy
- `start_period` gives a slow-starting service time before failures count
- `depends_on: service_healthy` requires this block to exist and pass
- A health check that only checks the process is running tells you almost nothing

---

### Resource Limit

**Definition:** A cgroup-enforced ceiling on a container's CPU and memory. Exceeding the memory limit triggers the OOM killer; exceeding the CPU limit throttles the process rather than killing it.

**Example:**
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

```bash
# Observe actual usage before choosing limits
docker stats --no-stream
```

**Related Terms:** Cgroup, OOM Killer, Reservation

**Key Facts:**
- `limits.memory` is a hard ceiling; the OOM killer terminates the container
- `limits.cpus` is a quota expressed as a fraction of one core
- On Compose, `reservations` are advisory; on Swarm they reserve capacity
- Retrieval workloads spike memory on large queries, so measure under load

---

### Non-Root

**Definition:** Running the container's main process as an unprivileged user instead of root, so a container escape grants the attacker far fewer privileges on the host.

**Example:**
```dockerfile
# Create a system user with a fixed UID, then switch to it
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser
USER appuser
```

```bash
# Verify who the process runs as
docker exec devmate-api id
```

**Related Terms:** Least Privilege, Image Security, USER

**Key Facts:**
- The `USER` instruction only affects subsequent instructions and runtime
- A fixed UID makes host bind-mount ownership predictable
- Most compliance scanners and many registries reject root-running images
- Non-root does not replace a read-only filesystem or an image scan; it is one control among several

---

### Distroless Image

**Definition:** A base image stripped to the application and its runtime dependencies, with no shell, no package manager, and no common diagnostic tooling.

**Example:**
```dockerfile
# Traditional slim image: has a shell you can exec into
FROM python:3.12-slim

# Distroless: no shell, nothing to exec into, smallest attack surface
FROM gcr.io/distroless/python3-debian12
```

```bash
# This fails on a distroless image and is exactly the point
docker exec -it api /bin/sh
```

**Related Terms:** Minimal Base, Attack Surface, Image Security

**Key Facts:**
- No shell means no interactive debugging; diagnose from logs and health checks instead
- Dramatically fewer packages to patch when a CVE lands
- Pair with an external debug sidecar or a separate debug image when you need a shell
- Well suited to services that are pure application code with no system dependencies

---

### Image Scanning

**Definition:** Static analysis of an image's filesystem and package manifest against a vulnerability database, reporting known CVEs by severity.

**Example:**
```bash
# Docker Scout
docker scout cves ghcr.io/org/devmate-api:v1.2.0

# Trivy, commonly wired into CI
trivy image --severity HIGH,CRITICAL --exit-code 1 ghcr.io/org/devmate-api:v1.2.0
```

**Related Terms:** CVE, SBOM, Supply Chain

**Key Facts:**
- Scanning at build time catches issues before the image reaches a registry
- `--exit-code 1` on high and critical findings makes the scan a gate, not a report
- Scanning only the final stage misses vulnerabilities in a single-stage build's layers
- Base-image updates are the cheapest remediation for most findings

---

### GPU Container

**Definition:** A container given direct access to the host's NVIDIA GPU through the NVIDIA Container Toolkit, which mounts the device and injects the CUDA user-space libraries the image needs.

**Example:**
```bash
# Verify the host driver is visible inside a container
docker run --gpus all --rm nvidia/cuda:12.6.3-base-ubuntu24.04 nvidia-smi
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

**Related Terms:** NVIDIA Container Toolkit, CUDA, Driver, WSL2

**Key Facts:**
- The image supplies CUDA user-space libraries; the host supplies the driver; they must be compatible
- `could not select device driver "" with capabilities: [[gpu]]` means the toolkit is missing or the daemon was not restarted after installing it
- On Windows with WSL2, the GPU backend requires Docker Desktop's WSL2 integration enabled
- A CPU-only PyTorch wheel inside a GPU container reports `torch.cuda.is_available() == False`; reinstall the CUDA build

---

### BuildKit

**Definition:** Docker's modern build engine, enabled by default in recent versions, providing parallel layer execution, cache mounts, secrets mounting, and a more informative build output.

**Example:**
```dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12-slim
# Cache survives across builds; not part of any image layer
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

# Mount a secret for one instruction without it entering a layer
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

```bash
# Enable BuildKit explicitly on older installs
DOCKER_BUILDKIT=1 docker build -t demo .
```

**Related Terms:** Cache Mount, Secret Mount, Layer

**Key Facts:**
- The `# syntax=` directive pins the Dockerfile frontend version
- Cache mounts persist between builds but are not part of the image, so they neither inflate it nor leak data
- Secret mounts keep credentials out of layers entirely
- BuildKit builds independent stages in parallel, cutting multi-stage build time substantially

---

## Summary

These terms cover the vocabulary you need to build, run, and operate containerized AI services:

1. **Immutable images, ephemeral containers.** State you care about lives on a volume.
2. **Layers and the build cache** are the performance backbone; instruction order is a deliberate decision.
3. **Multi-stage builds** are the largest available lever on image size.
4. **Compose** models a single-host application; its service names are hostnames and its health gates turn "started" into "ready."
5. **Limits, non-root users, minimal bases, and image scans** together move a container from demo to production.
6. **GPU containers** need the toolkit, a compatible driver, and a CUDA-enabled build of your framework; the three fail in diagnosable ways.

**Next:** Lecture 02 covers CI/CD with GitHub Actions, where images built here get tested, scanned, and promoted.
