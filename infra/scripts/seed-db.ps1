<#
.SYNOPSIS
    Seed the database with test data for development.

.DESCRIPTION
    Connects to PostgreSQL and inserts test data including users,
    sessions, and sample records for the auth-service.

.EXAMPLE
    ./infra/scripts/seed-db.ps1
    ./infra/scripts/seed-db.ps1 -Reset
    ./infra/scripts/seed-db.ps1 -DryRun
#>

param(
    [switch]$Reset,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# ─── Configuration ─────────────────────────────────

$DbHost = "localhost"
$DbPort = "5432"
$DbName = "fslab"
$DbUser = "fslab"
$DbPassword = "fslab_dev_2026"

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

function Write-SQL {
    param([string]$SQL)
    Write-Host "  $SQL" -ForegroundColor Gray
}

function Invoke-Sql {
    param([string]$SQL)
    if ($DryRun) {
        Write-SQL $SQL
        return
    }
    $env:PGPASSWORD = $DbPassword
    $result = psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -c $SQL 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Error: $result" -ForegroundColor Red
    }
    $result
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Full-Stack AI Engineer Lab — Seed DB   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

if ($DryRun) {
    Write-Warn "DRY RUN — SQL will be printed but not executed"
}

# ─── Step 1: Check Connection ─────────────────────

Write-Step "Checking database connection..."

$testConnection = Invoke-Sql "SELECT 1 AS connected;"
if ($testConnection -match "connected") {
    Write-Ok "Database connection successful"
} else {
    Write-Host "  Cannot connect to database. Is it running?" -ForegroundColor Red
    Write-Host "  Run: ./infra/scripts/setup.ps1" -ForegroundColor Yellow
    exit 1
}

# ─── Step 2: Reset (Optional) ─────────────────────

if ($Reset) {
    Write-Step "Resetting database..."

    Invoke-Sql "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    Write-Ok "Schema reset"

    # Re-run migrations if available
    $migrationsDir = "$PSScriptRoot/../../projects/01-backend-go/01-auth-service/migrations"
    if (Test-Path $migrationsDir) {
        Get-ChildItem "$migrationsDir/*.up.sql" | Sort-Object Name | ForEach-Object {
            Write-Host "  Running $($_.Name)..." -ForegroundColor Gray
            $env:PGPASSWORD = $DbPassword
            psql -h $DbHost -p $DbPort -U $DbUser -d $DbName -f $_.FullName 2>$null | Out-Null
        }
        Write-Ok "Migrations applied"
    } else {
        Write-Warn "No migrations found — tables may not exist"
    }
}

# ─── Step 3: Seed Users ───────────────────────────

Write-Step "Seeding test users..."

$users = @(
    @{ id = "00000000-0000-0000-0000-000000000001"; email = "admin@fslab.local"; name = "Admin User"; role = "admin" },
    @{ id = "00000000-0000-0000-0000-000000000002"; email = "dev@fslab.local"; name = "Dev User"; role = "user" },
    @{ id = "00000000-0000-0000-0000-000000000003"; email = "test@fslab.local"; name = "Test User"; role = "user" }
)

foreach ($user in $users) {
    $sql = @"
INSERT INTO users (id, email, name, role, created_at, updated_at)
VALUES ('$($user.id)', '$($user.email)', '$($user.name)', '$($user.role)', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;
"@
    Invoke-Sql $sql | Out-Null
    Write-Ok "User: $($user.email)"
}

# ─── Step 4: Seed API Keys ────────────────────────

Write-Step "Seeding test API keys..."

$apiKeys = @(
    @{ id = "key-dev-001"; user_id = "00000000-0000-0000-0000-000000000002"; name = "Dev Key"; prefix = "fslab_dev_" }
)

foreach ($key in $apiKeys) {
    $sql = @"
INSERT INTO api_keys (id, user_id, name, key_prefix, created_at, expires_at)
VALUES ('$($key.id)', '$($key.user_id)', '$($key.name)', '$($key.prefix)', NOW(), NOW() + INTERVAL '90 days')
ON CONFLICT (id) DO NOTHING;
"@
    Invoke-Sql $sql | Out-Null
    Write-Ok "API Key: $($key.name)"
}

# ─── Step 5: Seed Audit Log ───────────────────────

Write-Step "Seeding audit log entries..."

$auditEntries = @(
    @{ action = "user.created"; user_id = "00000000-0000-0000-0000-000000000001"; details = "Initial admin user" },
    @{ action = "user.created"; user_id = "00000000-0000-0000-0000-000000000002"; details = "Dev user for testing" },
    @{ action = "user.created"; user_id = "00000000-0000-0000-0000-000000000003"; details = "Test user for QA" }
)

foreach ($entry in $auditEntries) {
    $sql = @"
INSERT INTO audit_log (user_id, action, details, created_at)
VALUES ('$($entry.user_id)', '$($entry.action)', '$($entry.details)', NOW())
ON CONFLICT DO NOTHING;
"@
    Invoke-Sql $sql | Out-Null
    Write-Ok "Audit: $($entry.action)"
}

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║           Seed Complete!                 ║
  ╠══════════════════════════════════════════╣
  ║  Users     : 3                           ║
  ║  API Keys  : 1                           ║
  ║  Audit Log : 3 entries                   ║
  ╚══════════════════════════════════════════╝

  Test accounts:
    admin@fslab.local  (admin)
    dev@fslab.local    (user)
    test@fslab.local   (user)

"@ -ForegroundColor Green
