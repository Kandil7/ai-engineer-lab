<#
.SYNOPSIS
    Validate the repository structure for the Full-Stack AI Engineer Lab.

.DESCRIPTION
    Checks that all required directories exist, required files are present,
    and no orphaned files exist in critical directories.

.EXAMPLE
    ./tests/repo-structure/validate.ps1
    ./tests/repo-structure/validate.ps1 -Verbose
#>

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path

# ─── Counters ──────────────────────────────────────

$passCount = 0
$failCount = 0
$warnCount = 0

# ─── Helpers ───────────────────────────────────────

function Write-Check {
    param([string]$Message)
    Write-Host "  [CHECK] $Message" -ForegroundColor Cyan
}

function Write-Pass {
    param([string]$Message)
    Write-Host "  [PASS]  $Message" -ForegroundColor Green
    $script:passCount++
}

function Write-Fail {
    param([string]$Message)
    Write-Host "  [FAIL]  $Message" -ForegroundColor Red
    $script:failCount++
}

function Write-Warn {
    param([string]$Message)
    Write-Host "  [WARN]  $Message" -ForegroundColor Yellow
    $script:warnCount++
}

function Test-DirectoryExists {
    param([string]$Path, [string]$Description)
    if (Test-Path $Path -PathType Container) {
        Write-Pass "Directory exists: $Description"
    } else {
        Write-Fail "Directory missing: $Description ($Path)"
    }
}

function Test-FileExists {
    param([string]$Path, [string]$Description)
    if (Test-Path $Path -PathType Leaf) {
        Write-Pass "File exists: $Description"
    } else {
        Write-Fail "File missing: $Description ($Path)"
    }
}

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Repo Structure Validation             ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── 1. Required Top-Level Directories ────────────

Write-Host "`n── Required Directories ──" -ForegroundColor White

$requiredDirs = @(
    @{ path = ".ai"; desc = "AI prompt and workflow system" },
    @{ path = ".ai/prompts"; desc = "Prompts directory" },
    @{ path = ".ai/prompts/system"; desc = "System prompts" },
    @{ path = ".ai/prompts/roles"; desc = "Role prompts" },
    @{ path = ".ai/prompts/tasks"; desc = "Task prompts" },
    @{ path = ".ai/prompts/critics"; desc = "Critic prompts" },
    @{ path = ".ai/prompts/repair"; desc = "Repair prompts" },
    @{ path = ".ai/workflows"; desc = "Workflows directory" },
    @{ path = "templates"; desc = "Templates directory" },
    @{ path = "registries"; desc = "Registries directory" },
    @{ path = "docs"; desc = "Documentation directory" },
    @{ path = "docs/architecture"; desc = "Architecture docs" },
    @{ path = "docs/decisions"; desc = "ADRs directory" },
    @{ path = "docs/learning"; desc = "Learning docs" },
    @{ path = "docs/product"; desc = "Product docs" },
    @{ path = "learning-sources"; desc = "Learning sources" },
    @{ path = "evaluations"; desc = "Evaluations directory" },
    @{ path = "infra"; desc = "Infrastructure directory" },
    @{ path = "infra/docker"; desc = "Docker configs" },
    @{ path = "infra/scripts"; desc = "Scripts directory" },
    @{ path = "tests"; desc = "Tests directory" }
)

foreach ($dir in $requiredDirs) {
    $fullPath = Join-Path $RootDir $dir.path
    Test-DirectoryExists -Path $fullPath -Description $dir.desc
}

# ─── 2. Required Top-Level Files ──────────────────

Write-Host "`n── Required Files ──" -ForegroundColor White

$requiredFiles = @(
    @{ path = "README.md"; desc = "Main README" },
    @{ path = "ROADMAP.md"; desc = "Project roadmap" },
    @{ path = "MAKEFILE.md"; desc = "Makefile documentation" },
    @{ path = ".gitignore"; desc = "Git ignore rules" },
    @{ path = ".gitattributes"; desc = "Git attributes" },
    @{ path = ".editorconfig"; desc = "Editor config" },
    @{ path = "registries/prompt-registry.yaml"; desc = "Prompt registry" },
    @{ path = "registries/workflow-registry.yaml"; desc = "Workflow registry" },
    @{ path = "registries/template-registry.yaml"; desc = "Template registry" },
    @{ path = "registries/decision-log.yaml"; desc = "Decision log" },
    @{ path = "registries/skills-registry.yaml"; desc = "Skills registry" },
    @{ path = "registries/review-log.yaml"; desc = "Review log" }
)

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $RootDir $file.path
    Test-FileExists -Path $fullPath -Description $file.desc
}

# ─── 3. Required Templates ────────────────────────

Write-Host "`n── Required Templates ──" -ForegroundColor White

$requiredTemplates = @(
    "adr.template.md",
    "architecture-review.template.md",
    "bug-report.template.md",
    "code-review.template.md",
    "daily-log.template.md",
    "debugging-session.template.md",
    "evaluation-report.template.md",
    "feature-spec.template.md",
    "monthly-review.template.md",
    "project-plan.template.md",
    "source-book.template.md",
    "source-doc.template.md",
    "source-notebook.template.md",
    "source-repo.template.md",
    "weekly-review.template.md"
)

foreach ($tpl in $requiredTemplates) {
    $fullPath = Join-Path $RootDir "templates/$tpl"
    Test-FileExists -Path $fullPath -Description "Template: $tpl"
}

# ─── 4. Required Eval Directories ─────────────────

Write-Host "`n── Required Eval Directories ──" -ForegroundColor White

$requiredEvalDirs = @(
    "evaluations/prompts/golden-cases",
    "evaluations/prompts/regressions",
    "evaluations/rag/datasets",
    "evaluations/rag/reports",
    "evaluations/rag/baselines",
    "evaluations/projects/auth-service",
    "evaluations/projects/rag-system",
    "evaluations/projects/capstone"
)

foreach ($dir in $requiredEvalDirs) {
    $fullPath = Join-Path $RootDir $dir
    Test-DirectoryExists -Path $fullPath -Description $dir
}

# ─── 5. Required Infra Files ──────────────────────

Write-Host "`n── Required Infra Files ──" -ForegroundColor White

$requiredInfraFiles = @(
    "infra/docker/docker-compose.yml",
    "infra/scripts/setup.ps1",
    "infra/scripts/dev-run.ps1",
    "infra/scripts/seed-db.ps1",
    "infra/scripts/new-adr.ps1",
    "infra/scripts/new-review.ps1",
    "infra/scripts/new-source-note.ps1"
)

foreach ($file in $requiredInfraFiles) {
    $fullPath = Join-Path $RootDir $file
    Test-FileExists -Path $fullPath -Description $file
}

# ─── 6. Required Test Files ───────────────────────

Write-Host "`n── Required Test Files ──" -ForegroundColor White

$requiredTestFiles = @(
    "tests/repo-structure/validate.ps1",
    "tests/templates/validate.ps1",
    "tests/workflows/validate.ps1",
    "tests/prompts/validate.ps1",
    "tests/registries/validate.ps1"
)

foreach ($file in $requiredTestFiles) {
    $fullPath = Join-Path $RootDir $file
    Test-FileExists -Path $fullPath -Description $file
}

# ─── 7. Check for Orphaned Files ──────────────────

Write-Host "`n── Orphan Checks ──" -ForegroundColor White

# Check for .md files directly in root that shouldn't be there
$rootMdFiles = Get-ChildItem "$RootDir/*.md" -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -notin @("README.md", "ROADMAP.md", "MAKEFILE.md", "AGENTS.md") }

if ($rootMdFiles.Count -gt 0) {
    foreach ($f in $rootMdFiles) {
        Write-Warn "Unexpected .md file in root: $($f.Name)"
    }
} else {
    Write-Pass "No orphaned .md files in root"
}

# Check for stray .py files in root
$rootPyFiles = Get-ChildItem "$RootDir/*.py" -ErrorAction SilentlyContinue
if ($rootPyFiles.Count -gt 0) {
    foreach ($f in $rootPyFiles) {
        Write-Warn "Unexpected .py file in root: $($f.Name)"
    }
} else {
    Write-Pass "No orphaned .py files in root"
}

# ─── Summary ───────────────────────────────────────

Write-Host "`n── Summary ──" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Warnings: $warnCount" -ForegroundColor $(if ($warnCount -gt 0) { "Yellow" } else { "Green" })

if ($failCount -gt 0 -or $warnCount -gt 0) {
    Write-Host "`n  ✗ Validation FAILED — fix the issues above" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n  ✓ All checks passed" -ForegroundColor Green
    exit 0
}
