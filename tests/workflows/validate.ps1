<#
.SYNOPSIS
    Validate all workflow files exist and have required structure.

.DESCRIPTION
    Checks that every workflow listed in workflow-registry.yaml exists,
    each has entry/artifacts/exit criteria, and the registry matches
    actual files on disk.

.EXAMPLE
    ./tests/workflows/validate.ps1
    ./tests/workflows/validate.ps1 -Verbose
#>

param(
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$RootDir = (Resolve-Path "$PSScriptRoot/../..").Path
$RegistryFile = "$RootDir/registries/workflow-registry.yaml"

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

# ─── Banner ────────────────────────────────────────

Write-Host @"

  ╔══════════════════════════════════════════╗
  ║   Workflow Validation                   ║
  ╚══════════════════════════════════════════╝

"@ -ForegroundColor Magenta

# ─── 1. Check Registry ────────────────────────────

Write-Host "`n── Registry Check ──" -ForegroundColor White

if (-not (Test-Path $RegistryFile)) {
    Write-Fail "Workflow registry not found: $RegistryFile"
    exit 1
}

Write-Pass "Workflow registry found"

# ─── 2. Parse Registry ────────────────────────────

Write-Host "`n── Registry Parsing ──" -ForegroundColor White

$registryContent = Get-Content $RegistryFile -Raw

# Extract workflow entries
$workflowEntries = @()
$lines = $registryContent -split "`n"
$currentWorkflow = $null
$currentCategory = ""

foreach ($line in $lines) {
    # Category headers (feature:, debugging:, learning:, architecture:, evaluation:)
    if ($line -match '^\s{2}(\w+):') {
        $currentCategory = $matches[1]
    }

    if ($line -match '^\s*- id:\s*(.+)') {
        if ($currentWorkflow) {
            $workflowEntries += $currentWorkflow
        }
        $currentWorkflow = @{
            id = $matches[1].Trim()
            path = ""
            entry_point = $false
            prompts_used = @()
            template_used = ""
            produces = @()
            exit_criteria = ""
            category = $currentCategory
        }
    }
    elseif ($line -match '^\s*path:\s*(.+)') {
        if ($currentWorkflow) {
            $currentWorkflow.path = $matches[1].Trim()
        }
    }
    elseif ($line -match '^\s*entry_point:\s*(.+)') {
        if ($currentWorkflow) {
            $currentWorkflow.entry_point = $matches[1].Trim() -eq "true"
        }
    }
    elseif ($line -match '^\s*exit_criteria:\s*"?(.+)"?\s*$') {
        if ($currentWorkflow) {
            $currentWorkflow.exit_criteria = $matches[1].Trim('"')
        }
    }
}

if ($currentWorkflow) {
    $workflowEntries += $currentWorkflow
}

Write-Pass "Parsed $($workflowEntries.Count) workflows from registry"

# ─── 3. Validate Each Workflow ────────────────────

Write-Host "`n── Workflow Validation ──" -ForegroundColor White

foreach ($wf in $workflowEntries) {
    $fullPath = Join-Path $RootDir $wf.path

    # Check file exists
    if (-not (Test-Path $fullPath -PathType Leaf)) {
        Write-Fail "Workflow file missing: $($wf.id) ($($wf.path))"
        continue
    }

    Write-Pass "File exists: $($wf.id)"

    # Check workflow has content
    $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
    if ($content.Length -lt 50) {
        Write-Warn "Workflow '$($wf.id)' seems too short ($($content.Length) chars)"
    }

    # Check for exit criteria in file
    if ($wf.exit_criteria -and $content) {
        # Look for common section headers
        $hasExitSection = $content -match '(?i)(exit|criteria|done|complete|success)'
        if (-not $hasExitSection) {
            Write-Warn "Workflow '$($wf.id)' may be missing exit criteria section"
        }
    }

    # Check for entry point marker: entry-point workflows must declare an
    # ## Inputs section. (Frontmatter carries entry_point too, so a loose
    # keyword search would false-positive on its own metadata.)
    if ($wf.entry_point -and $content) {
        $hasInputs = $content -match '(?m)^## Inputs'
        if (-not $hasInputs) {
            Write-Warn "Workflow '$($wf.id)' is entry point but lacks an ## Inputs section"
        }
    }
}

# ─── 4. Check Category Directories ────────────────

Write-Host "`n── Category Directory Check ──" -ForegroundColor White

$categories = @("feature", "debugging", "learning", "architecture", "evaluation")

foreach ($cat in $categories) {
    $catDir = "$RootDir/.ai/workflows/$cat"
    if (Test-Path $catDir -PathType Container) {
        $catWorkflows = $workflowEntries | Where-Object { $_.category -eq $cat }
        $catFiles = Get-ChildItem "$catDir/*.md" -ErrorAction SilentlyContinue

        Write-Pass "Category '$cat': $($catWorkflows.Count) registered, $($catFiles.Count) files"

        # Check for unregistered files
        foreach ($file in $catFiles) {
            $relativePath = $file.FullName.Replace("$RootDir\", "").Replace("\", "/")
            $isRegistered = $catWorkflows | Where-Object { $_.path -eq $relativePath }
            if (-not $isRegistered) {
                Write-Warn "Unregistered workflow file: $relativePath"
            }
        }
    } else {
        Write-Warn "Category directory missing: $cat"
    }
}

# ─── Summary ───────────────────────────────────────

Write-Host "`n── Summary ──" -ForegroundColor White
Write-Host "  Passed: $passCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Warnings: $warnCount" -ForegroundColor $(if ($warnCount -gt 0) { "Yellow" } else { "Green" })

if ($failCount -gt 0 -or $warnCount -gt 0) {
    Write-Host "`n  [FAIL] Validation FAILED" -ForegroundColor Red
    exit 1
} else {
    Write-Host "`n  [PASS] All workflows valid" -ForegroundColor Green
    exit 0
}
