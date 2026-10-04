<#
.SYNOPSIS
    Generate a new Architecture Decision Record (ADR) with numbered filename.

.DESCRIPTION
    Creates a new ADR file from the ADR template with the next sequential number.
    The ADR is placed in docs/decisions/ with format: NNNN-slug.md.

.EXAMPLE
    ./infra/scripts/new-adr.ps1 "Adopt keyset pagination"
    ./infra/scripts/new-adr.ps1 "Use Redis for session cache"
    ./infra/scripts/new-adr.ps1 "Switch to Qdrant for vector DB" -Status accepted
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Title,
    [ValidateSet("proposed", "accepted", "deprecated", "superseded")]
    [string]$Status = "proposed"
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$DecisionsDir = "$RootDir/docs/decisions"
$TemplateFile = "$RootDir/templates/adr.template.md"

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

function ConvertTo-Slug {
    param([string]$Text)
    $Text.ToLower() -replace '[^a-z0-9\s-]', '' -replace '\s+', '-' -replace '-+', '-' -replace '^-|-$', ''
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   AI Engineer Lab — New ADR   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Find Next Number ─────────────────────

Write-Step "Finding next ADR number..."

if (-not (Test-Path $DecisionsDir)) {
    New-Item -ItemType Directory -Path $DecisionsDir -Force | Out-Null
}

$existingAdrs = Get-ChildItem "$DecisionsDir/*.md" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '^\d{4}-' } |
    Sort-Object Name

if ($existingAdrs.Count -gt 0) {
    $lastAdr = $existingAdrs[-1].Name
    $lastNumber = [int]($lastAdr -replace '^(\d+)-.*$', '$1')
    $nextNumber = $lastNumber + 1
} else {
    $nextNumber = 1
}

$numberStr = $nextNumber.ToString("0000")
Write-Ok "Next ADR number: $numberStr"

# ─── Step 2: Generate Filename ────────────────────

Write-Step "Generating filename..."

$slug = ConvertTo-Slug $Title
$filename = "$numberStr-$slug.md"
$filepath = "$DecisionsDir/$filename"
$statusLabel = $Status.Substring(0, 1).ToUpper() + $Status.Substring(1)

Write-Ok "Filename: $filename"

# ─── Step 3: Check for Existing ADR ───────────────

if (Test-Path $filepath) {
    Write-Fail "ADR already exists: $filepath"
    exit 1
}

# ─── Step 4: Create ADR from Template ─────────────

Write-Step "Creating ADR from template..."

if (-not (Test-Path $TemplateFile)) {
    Write-Fail "ADR template not found: $TemplateFile"
    exit 1
}

$template = Get-Content $TemplateFile -Raw

# Replace the template's fill-in markers (literal replace — titles may
# contain regex-special characters, so -replace is not safe here)
$date = Get-Date -Format "yyyy-MM-dd"
$content = $template.Replace("NNNN", $numberStr).Replace(
    "<short decision title>", $Title
).Replace("YYYY-MM-DD", $date)
$content = [regex]::Replace(
    $content, '(?m)^- \*\*Status:\*\*.*$', "- **Status:** $statusLabel"
)

# Set content (UTF-8 without BOM, matching the existing ADRs)
[System.IO.File]::WriteAllText($filepath, $content, [System.Text.UTF8Encoding]::new($false))

Write-Ok "Created: $filepath"

# ─── Step 5: Update Decision Log ──────────────────

Write-Step "Updating decision log..."

$decisionLog = "$RootDir/registries/decision-log.yaml"

$logEntry = @"
  - id: "$numberStr"
    title: "$Title"
    status: $statusLabel
    date: $date
    path: docs/decisions/$filename
    supersedes: null
    superseded_by: null
"@

if (Test-Path $decisionLog) {
    Add-Content -Path $decisionLog -Value $logEntry -Encoding UTF8
    Write-Ok "Decision log updated"
} else {
    $logContent = @"
# Decision Log — Architecture Decision Records
version: 1
decisions:
$logEntry
"@
    [System.IO.File]::WriteAllText($decisionLog, $logContent, [System.Text.UTF8Encoding]::new($false))
    Write-Ok "Decision log created"
}

# ─── Step 6: Update Decisions README Index ──────

Write-Step "Updating decisions index..."

$indexFile = "$DecisionsDir/README.md"
$indexRow = "| [$numberStr]($filename) | $Title | $statusLabel | $date |"
$indexText = [System.IO.File]::ReadAllText($indexFile, [System.Text.Encoding]::UTF8)
if ($indexText -notmatch [regex]::Escape("[$numberStr]")) {
    $nl = if ($indexText -match "`r`n") { "`r`n" } else { "`n" }
    $rows = [regex]::Matches($indexText, '(?m)^\| \[\d{4}\].*$')
    if ($rows.Count -gt 0) {
        $last = $rows[$rows.Count - 1]
        $indexText = $indexText.Insert($last.Index + $last.Length, $nl + $indexRow)
    } else {
        $anchor = $nl + "## Lifecycle"
        $indexText = $indexText -replace [regex]::Escape($anchor), ($nl + $indexRow + $anchor)
    }
    [System.IO.File]::WriteAllText($indexFile, $indexText, [System.Text.UTF8Encoding]::new($false))
    Write-Ok "Decisions index updated"
} else {
    Write-Ok "Already indexed — skipped duplicate row"
}

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║           ADR Created!                   ║
  ╠══════════════════════════════════════════╣
  ║  File  : $filename
  ║  Title : $Title
  ║  Status: $Status
  ║  Date  : $date
  ╚══════════════════════════════════════════╝

  Edit the ADR to fill in Context, Decision, and Consequences.

"@ -ForegroundColor Green
