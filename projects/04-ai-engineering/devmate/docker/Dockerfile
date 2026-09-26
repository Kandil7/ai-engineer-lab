# Multi-stage Dockerfile for DevMate
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the project definition and source. pyproject.toml declares a PEP 621
# setuptools build (there is no [tool.poetry] section), so plain pip installs
# it. README.md ships because pyproject.toml references it as the readme.
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install DevMate AND its dependencies to /install. The package itself must
# be installed — copying src/ alone leaves `import devmate` unresolvable,
# because /app is on sys.path but the code lives one level deeper in src/.
RUN pip install --no-cache-dir --prefix=/install .


# Runtime stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages (dependencies + devmate itself) from builder.
# No src/ copy: devmate resolves from site-packages, and every file the code
# reads (repos, uploads) arrives via explicit request/CLI paths.
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose ports
EXPOSE 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0", "--port", "8000"]