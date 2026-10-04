<#
.SYNOPSIS
    Generate a new source learning note from the appropriate template.

.DESCRIPTION
    Creates a source learning note in docs/learning/source-summaries/ using
    the matching template (source-book, source-repo, source-notebook, or source-doc).

.EXAMPLE
    ./infra/scripts/new-source-note.ps1 "go-chi/chi" repo
    ./infra/scripts/new-source-note.ps1 "Concurrency in Go" book
    ./infra/scripts/new-source-note.ps1 "PostgreSQL 16 Docs" doc
    ./infra/scripts/new-source-note.ps1 "RAG Chunking notebook" notebook
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourceName,

    [Parameter(Mandatory=$true)]
    [ValidateSet("book", "repo", "notebook", "doc")]
    [string]$Type
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$TemplateMap = @{
    "book"     = "$RootDir/templates/source-book.template.md"
    "repo"     = "$RootDir/templates/source-repo.template.md"
    "notebook" = "$RootDir/templates/source-notebook.template.md"
    "doc"      = "$RootDir/templates/source-doc.template.md"
}
$SummariesDir = "$RootDir/docs/learning/source-summaries"

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
  ║   AI Engineer Lab — Source    ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── Step 1: Validate Template ────────────────────

Write-Step "Checking template for type: $Type..."

$templateFile = $TemplateMap[$Type]
if (-not (Test-Path $templateFile)) {
    Write-Fail "Template not found: $templateFile"
    exit 1
}

Write-Ok "Template: $(Split-Path $templateFile -Leaf)"

# ─── Step 2: Generate Slug ────────────────────────

Write-Step "Generating slug..."

$slug = ConvertTo-Slug $SourceName
$filename = "$slug.md"
$filepath = "$SummariesDir/$filename"

Write-Ok "Slug: $slug"

# ─── Step 3: Check for Existing Note ──────────────

if (-not (Test-Path $SummariesDir)) {
    New-Item -ItemType Directory -Path $SummariesDir -Force | Out-Null
}

if (Test-Path $filepath) {
    Write-Fail "Source note already exists: $filepath"
    exit 1
}

# ─── Step 4: Create Note from Template ────────────

Write-Step "Creating source note..."

$template = Get-Content $templateFile -Raw

$date = Get-Date -Format "yyyy-MM-dd"
$content = $template -replace '\{\{SOURCE_NAME\}\}', $SourceName
$content = $content -replace '\{\{TYPE\}\}', $Type
$content = $content -replace '\{\{DATE\}\}', $date
$content = $content -replace '\{\{SLUG\}\}', $slug

# Add header
$header = @"
# Source Learning: $SourceName

- **Type**: $Type
- **Date Started**: $date
- **Status**: In Progress
- **Template**: source-$Type.template.md

---

"@

$fullContent = $header + $content

Set-Content -Path $filepath -Value $fullContent -Encoding UTF8

Write-Ok "Created: $filepath"

# ─── Step 5: Update Source Index ──────────────────

Write-Step "Note: Update learning-sources/source-index.md manually..."

Write-Host "  1. Find the entry for '$SourceName' in source-index.md" -ForegroundColor Gray
Write-Host "  2. Change status from 'planned' to 'in-progress'" -ForegroundColor Gray
Write-Host "  3. When done, change to 'completed'" -ForegroundColor Gray

# ─── Summary ───────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║       Source Note Created!               ║
  ╠══════════════════════════════════════════╣
  ║  File   : $filename
  ║  Source : $SourceName
  ║  Type   : $Type
  ║  Date   : $date
  ╚══════════════════════════════════════════╝

  Next steps:
  1. Read the source material
  2. Fill in the template sections
  3. Link to a project task
  4. Add Arabic summary (ملخص عربي)

"@ -ForegroundColor Green
