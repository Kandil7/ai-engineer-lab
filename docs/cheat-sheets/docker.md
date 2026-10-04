# Docker Cheat Sheet

## Dockerfile Best Practices

### Structure
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
CMD ["python", "main.py"]
```

### Layer Optimization
```dockerfile
# Bad
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Multi-Stage Builds
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD ["python", "main.py"]
```

---

## Docker Compose

### Basic Structure
```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Common Commands
```bash
docker compose up -d              # Start in detached mode
docker compose down               # Stop and remove containers
docker compose ps                 # List running services
docker compose logs -f web        # Follow logs for service
docker compose exec web bash      # Shell into running container
docker compose build              # Build/rebuild images
docker compose pull               # Pull latest images
docker compose config             # Validate and view config
```

---

## Health Checks

### Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

### Common Patterns
```bash
# HTTP check
curl -f http://localhost:8000/health || exit 1

# TCP check
nc -z localhost 5432 || exit 1

# PostgreSQL check
pg_isready -U user || exit 1

# Redis check
redis-cli ping || exit 1
```

---

## Volumes

### Types
```bash
# Named volumes
docker volume create mydata
docker volume ls

# Bind mounts
docker run -v /host/path:/container/path image

# tmpfs mounts
docker run --tmpfs /app/temp image
```

### Common Patterns
```bash
# Database persistence
docker run -v pgdata:/var/lib/postgresql/data postgres

# Development with live reload
docker run -v $(pwd):/app -w /app node:18 npm start
```

### Backup & Restore
```bash
# Backup
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

---

## Networking

### Network Types
```bash
# Bridge (default)
docker network create mybridge
docker run --network mybridge image

# Host (no isolation)
docker run --network host image

# None (no networking)
docker run --network none image
```

### Container Communication
```bash
# Containers on same network use service names
docker run --network mybridge --name api image
docker run --network mybridge --name db image
# api connects to db at "db:5432"

# Expose ports
docker run -p 8000:8000 image    # Host:Container
docker run -p 127.0.0.1:8000:8000 image  # Localhost only
```

---

## Image Management

### Building
```bash
docker build -t myimage:latest .           # Build image
docker build --no-cache -t myimage .       # Build without cache
docker build --pull -t myimage .           # Pull base image first
```

### Cleanup
```bash
docker image prune -a              # Remove all unused images
docker container prune             # Remove stopped containers
docker volume prune                # Remove unused volumes
docker system prune -a             # Remove everything unused
docker system df                   # Show disk usage
```

---

## Security Best Practices

### Non-Root User
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

### Resource Limits
```bash
docker run --memory=512m --cpus=1.5 image
docker run --memory-swap=512m image  # No swap
```

### Secrets Management
```bash
# Use environment files
docker run --env-file .env image

# Never hardcode secrets in Dockerfile
```

---

## Debugging

### Container Inspection
```bash
docker inspect <container>         # Full container details
docker logs <container>            # View logs
docker logs -f <container>         # Follow logs
docker logs --tail 100 <container> # Last 100 lines
docker top <container>             # Running processes
docker stats <container>           # Resource usage
```

### Exec & Debug
```bash
docker exec -it <container> bash   # Shell into container
docker exec -it <container> sh     # Shell (Alpine)
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `docker build -t name .` | Build image |
| `docker run -d -p 80:80 name` | Run container |
| `docker ps` | List running containers |
| `docker logs container` | View logs |
| `docker exec -it container bash` | Shell into container |
| `docker compose up -d` | Start services |
| `docker compose down` | Stop services |
| `docker system prune -a` | Clean up everything |

---

*Last updated: 2026-08-06*
