<#
.SYNOPSIS
    Create today's daily log from the template.

.DESCRIPTION
    Creates docs/learning/daily-logs/YYYY-MM-DD.md from
    templates/daily-log.template.md. Opens the existing file instead of
    failing if today's log has already been started.

.EXAMPLE
    ./infra/scripts/new-daily-log.ps1
    ./infra/scripts/new-daily-log.ps1 -Date 2026-08-01
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Date
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$TemplateFile = "$RootDir/templates/daily-log.template.md"
$LogDir = "$RootDir/docs/learning/daily-logs"

# ─── Helpers ───────────────────────────────────────

function Write-Step { param([string]$Message); Write-Host "`n> $Message" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Message); Write-Host "  [ok] $Message" -ForegroundColor Green }
function Write-Fail { param([string]$Message); Write-Host "  [!!] $Message" -ForegroundColor Red }

# ─── Resolve date ──────────────────────────────────

if ([string]::IsNullOrWhiteSpace($Date)) {
    $Date = Get-Date -Format "yyyy-MM-dd"
} elseif ($Date -notmatch '^\d{4}-\d{2}-\d{2}$') {
    Write-Fail "Date must be in YYYY-MM-DD format. Got: $Date"
    exit 1
}

# ─── Validate template ─────────────────────────────

Write-Step "Checking template..."

if (-not (Test-Path $TemplateFile)) {
    Write-Fail "Daily log template not found: $TemplateFile"
    exit 1
}

Write-Ok "Template found"

# ─── Create log ────────────────────────────────────

Write-Step "Creating daily log for $Date..."

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    Write-Ok "Created $LogDir"
}

$logPath = Join-Path $LogDir "$Date.md"

if (Test-Path $logPath) {
    Write-Ok "Log already exists: $logPath"
    Write-Host "`n  Continue in the existing file.`n" -ForegroundColor Yellow
    exit 0
}

$template = Get-Content $TemplateFile -Raw
# The template uses a literal YYYY-MM-DD in its heading and a {{DATE}} placeholder
# elsewhere; substitute both.
$content = $template -replace 'YYYY-MM-DD', $Date -replace '\{\{DATE\}\}', $Date

Set-Content -Path $logPath -Value $content -Encoding UTF8

Write-Ok "Created: $logPath"

# ─── Reminders ─────────────────────────────────────

$focusFile = "$RootDir/docs/tracking/current-focus.md"
$staleDays = $null

if (Test-Path $focusFile) {
    $stamp = (Select-String -Path $focusFile -Pattern '\d{4}-\d{2}-\d{2}' |
              Select-Object -First 1).Matches.Value
    if ($stamp) {
        $staleDays = (New-TimeSpan -Start ([datetime]$stamp) -End (Get-Date)).Days
    }
}

Write-Host ""
Write-Host "  Daily log ready — $Date" -ForegroundColor Green
Write-Host ""
Write-Host "  Loop: Build 3h -> Learn 1h -> Review 1h -> Recall 30m" -ForegroundColor Gray
Write-Host "  Focus: docs/tracking/current-focus.md" -ForegroundColor Gray

if ($null -ne $staleDays -and $staleDays -gt 8) {
    Write-Host ""
    Write-Host "  [!!] current-focus.md is $staleDays days old — update it." -ForegroundColor Red
}

Write-Host ""
