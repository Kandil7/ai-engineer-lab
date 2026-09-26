<#
.SYNOPSIS
    Setup the Full-Stack AI Engineer Lab development environment.

.DESCRIPTION
    Checks prerequisites (Go, Docker, Flutter), pulls Docker images,
    starts services, and creates the database.

.EXAMPLE
    ./infra/scripts/setup.ps1
    ./infra/scripts/setup.ps1 -SkipFlutter
    ./infra/scripts/setup.ps1 -WithDevTools
#>

param(
    [switch]$SkipFlutter,
    [switch]$WithDevTools,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ComposeFile = "$PSScriptRoot/../docker/docker-compose.yml"

# ─── Helpers ───────────────────────────────────────

function Write-Step {
    param([string]$Message)
    Write-Host "`n► $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "  ⚠ $Message" -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Message)
    Write-Host "  ✗ $Message" -ForegroundColor Red
}

function Test-CommandExists {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Full-Stack AI Engineer Lab — Setup     ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Check Prerequisites ──────────────────

Write-Step "Checking prerequisites..."

$prereqFailed = $false

# Go
if (Test-CommandExists "go") {
    $goVersion = (go version) -replace '.*go(\d+\.\d+\.\d+).*', '$1'
    Write-Ok "Go $goVersion"
} else {
    Write-Fail "Go not found — install from https://go.dev/dl/"
    $prereqFailed = $true
}

# Docker
if (Test-CommandExists "docker") {
    $dockerVersion = (docker --version) -replace '.*Docker version (\d+\.\d+\.\d+).*', '$1'
    Write-Ok "Docker $dockerVersion"
} else {
    Write-Fail "Docker not found — install Docker Desktop"
    $prereqFailed = $true
}

# Docker Compose
if (Test-CommandExists "docker" -and (docker compose version 2>$null)) {
    Write-Ok "Docker Compose"
} else {
    Write-Fail "Docker Compose not found"
    $prereqFailed = $true
}

# Flutter (optional)
if (-not $SkipFlutter) {
    if (Test-CommandExists "flutter") {
        $flutterVersion = (flutter --version 2>$null | Select-Object -First 1) -replace 'Flutter\s+(\S+).*', '$1'
        Write-Ok "Flutter $flutterVersion"
    } else {
        Write-Warn "Flutter not found — skipping (use -SkipFlutter to suppress)"
    }
}

if ($prereqFailed -and -not $Force) {
    Write-Host "`n  Fix the issues above and re-run setup." -ForegroundColor Red
    exit 1
}

# ─── Step 2: Create Docker Networks ────────────────

Write-Step "Ensuring Docker network exists..."

$networkExists = docker network ls --format '{{.Name}}' 2>$null | Select-String "fslab-net"
if (-not $networkExists) {
    docker network create fslab-net 2>$null | Out-Null
    Write-Ok "Created fslab-net network"
} else {
    Write-Ok "fslab-net network already exists"
}

# ─── Step 3: Pull Docker Images ───────────────────

Write-Step "Pulling Docker images..."

$images = @(
    "postgres:16-alpine",
    "redis:7-alpine",
    "qdrant/qdrant:v1.12.1"
)

if ($WithDevTools) {
    $images += @(
        "dpage/pgadmin4:latest",
        "rediscommander/redis-commander:latest"
    )
}

foreach ($img in $images) {
    Write-Host "  Pulling $img..." -ForegroundColor Gray
    docker pull $img 2>$null | Out-Null
    Write-Ok $img
}

# ─── Step 4: Start Services ───────────────────────

Write-Step "Starting services..."

$composeArgs = @("-f", $ComposeFile, "up", "-d")

if ($WithDevTools) {
    $composeArgs += @("--profile", "dev-tools")
}

& docker compose @composeArgs

if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to start services"
    exit 1
}

Write-Ok "Services started"

# ─── Step 5: Wait for Health Checks ───────────────

Write-Step "Waiting for services to become healthy..."

$maxWait = 60
$elapsed = 0

while ($elapsed -lt $maxWait) {
    $postgresHealthy = docker inspect --format='{{.State.Health.Status}}' fslab-postgres 2>$null -eq "healthy"
    $redisHealthy = docker inspect --format='{{.State.Health.Status}}' fslab-redis 2>$null -eq "healthy"

    if ($postgresHealthy -and $redisHealthy) {
        Write-Ok "PostgreSQL is healthy"
        Write-Ok "Redis is healthy"
        break
    }

    Start-Sleep -Seconds 2
    $elapsed += 2
    Write-Host "  Waiting... ($elapsed s)" -ForegroundColor Gray
}

if ($elapsed -ge $maxWait) {
    Write-Warn "Some services may not be fully healthy yet"
}

# ─── Step 6: Create Database ──────────────────────

Write-Step "Verifying database..."

$dbExists = docker exec fslab-postgres psql -U fslab -d fslab -c "SELECT 1;" 2>$null
if ($dbExists) {
    Write-Ok "Database 'fslab' exists and is accessible"
} else {
    Write-Warn "Database may need initialization — check postgres/init/ scripts"
}

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║           Setup Complete!                ║
  ╠══════════════════════════════════════════╣
  ║  PostgreSQL : localhost:5432             ║
  ║  Redis      : localhost:6379             ║
  ║  Qdrant     : localhost:6333             ║
  ╠══════════════════════════════════════════╣
  ║  DB Name    : fslab                      ║
  ║  DB User    : fslab                      ║
  ║  DB Pass    : fslab_dev_2026             ║
  ╚══════════════════════════════════════════╝

  Next: ./infra/scripts/seed-db.ps1

"@ -ForegroundColor Green
