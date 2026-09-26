<#
.SYNOPSIS
    Start the development environment and run the auth-service.

.DESCRIPTION
    Ensures Docker services are running, then starts the auth-service
    in development mode with live reload.

.EXAMPLE
    ./infra/scripts/dev-run.ps1
    ./infra/scripts/dev-run.ps1 -Service auth-service
    ./infra/scripts/dev-run.ps1 -WithDevTools
#>

param(
    [string]$Service = "auth-service",
    [switch]$WithDevTools
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
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
  ║   Full-Stack AI Engineer Lab — Dev Run   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Ensure Docker Services Running ───────

Write-Step "Checking Docker services..."

$composeArgs = @("-f", $ComposeFile, "ps", "--format", "json")
$runningServices = & docker compose @composeArgs 2>$null | ConvertFrom-Json

$neededServices = @("fslab-postgres", "fslab-redis", "fslab-qdrant")
foreach ($svc in $neededServices) {
    $found = $runningServices | Where-Object { $_.Name -eq $svc -and $_.State -eq "running" }
    if ($found) {
        Write-Ok "$svc is running"
    } else {
        Write-Host "  Starting $svc..." -ForegroundColor Gray
        $upArgs = @("-f", $ComposeFile, "up", "-d", $svc.Replace("fslab-", ""))
        if ($WithDevTools) { $upArgs += @("--profile", "dev-tools") }
        & docker compose @upArgs
    }
}

# ─── Step 2: Wait for Health ──────────────────────

Write-Step "Waiting for services to be healthy..."

$maxWait = 30
$elapsed = 0

while ($elapsed -lt $maxWait) {
    $pg = docker inspect --format='{{.State.Health.Status}}' fslab-postgres 2>$null
    $rd = docker inspect --format='{{.State.Health.Status}}' fslab-redis 2>$null

    if ($pg -eq "healthy" -and $rd -eq "healthy") {
        Write-Ok "All services healthy"
        break
    }

    Start-Sleep -Seconds 2
    $elapsed += 2
}

# ─── Step 3: Run the Service ──────────────────────

Write-Step "Starting $Service..."

$servicePath = "$RootDir/projects/01-backend-go/01-auth-service"

if (-not (Test-Path $servicePath)) {
    Write-Fail "Service path not found: $servicePath"
    Write-Host "  Available projects:" -ForegroundColor Yellow
    Get-ChildItem "$RootDir/projects" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "    - $($_.Name)" -ForegroundColor Gray
    }
    exit 1
}

Push-Location $servicePath

try {
    # Check if Go module exists
    if (-not (Test-Path "go.mod")) {
        Write-Fail "go.mod not found in $servicePath"
        exit 1
    }

    Write-Host "`n  Running: go run .`n" -ForegroundColor Gray

    # Set environment variables for development
    $env:DB_HOST = "localhost"
    $env:DB_PORT = "5432"
    $env:DB_NAME = "fslab"
    $env:DB_USER = "fslab"
    $env:DB_PASSWORD = "fslab_dev_2026"
    $env:REDIS_URL = "redis://localhost:6379"
    $env:QDRANT_URL = "http://localhost:6333"
    $env:JWT_SECRET = "dev-secret-do-not-use-in-production"

    # Run the service
    go run .

} finally {
    Pop-Location
}
